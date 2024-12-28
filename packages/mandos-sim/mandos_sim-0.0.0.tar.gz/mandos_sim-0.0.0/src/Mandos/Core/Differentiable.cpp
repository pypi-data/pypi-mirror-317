#include <Mandos/Core/DiffRigidBody.hpp>
#include <Mandos/Core/Differentiable.hpp>
#include <Mandos/Core/SystemMatrix.hpp>

namespace
{

mandos::core::Vec approximateHzFiniteDiff(mandos::core::Model &model,
                                          const mandos::core::Vec &grad,
                                          const mandos::core::Vec &x0,
                                          const mandos::core::Vec &v0,
                                          const mandos::core::Vec &z,
                                          mandos::core::Scalar h,
                                          mandos::core::Scalar dx)
{
    mandos::core::Vec gradient = mandos::core::Vec::Zero(model.nDof());
    mandos::core::Vec x_current = mandos::core::Vec::Zero(model.nDof());
    mandos::core::Vec v_current = mandos::core::Vec::Zero(model.nDof());

    // Finite diff
    model.state(x_current, v_current);
    model.updateState(z * dx, x0, v0, h);
    model.computeEnergyAndGradient(h, gradient);

    model.setState(x_current, v_current);  // Recover state

    return (gradient - grad) / dx;
}

}  // namespace

namespace mandos::core
{

Vec computeLossFunctionGradientBackpropagation(Scalar h,
                                               Model &model,
                                               const Trajectory &trajectory,
                                               const LossFunctionAndGradients &loss,
                                               const Mat &dx0_dp,
                                               const Mat &dv0_dp,
                                               unsigned int maxIterations)
{
    const int nParameters = loss.getNParameters();
    const int nDof = trajectory.getNDof();
    const int nSteps = trajectory.getNSteps();

    // Initialize the loss function gradients dg_dp, dg_dx and dg_dv
    // -------------------------------------------------------------------------
    Vec lossGradient = loss.lossParameterPartialDerivative;
    Vec lossPositionGradient = loss.lossPositionPartialDerivative[static_cast<std::size_t>(nSteps)];
    Vec lossVelocityGradient = loss.lossVelocityPartialDerivative[static_cast<std::size_t>(nSteps)];
    // Backward loop
    // -------------------------------------------------------------------------
    const Scalar one_over_h = 1.0 / h;
    for (int i = nSteps - 1; i >= 0; --i) {
        // Set the correc state
        const Vec &x = trajectory.positions[static_cast<std::size_t>(i) + 1];
        const Vec &v = trajectory.velocities[static_cast<std::size_t>(i) + 1];
        const Vec &x0 = trajectory.positions[static_cast<std::size_t>(i)];
        const Vec &v0 = trajectory.velocities[static_cast<std::size_t>(i)];

        model.setState(x0, v0);
        model.computeAdvection(h);
        model.setState(x, v);

        // Compute 2nd order derivatives
        SystemMatrix hessian(static_cast<int>(nDof), static_cast<int>(nDof));
        // At the moment they ignore mappings
        SparseMat dgradE_dx0(static_cast<int>(nDof), static_cast<int>(nDof));
        SparseMat dgradE_dv0(static_cast<int>(nDof), static_cast<int>(nDof));

        Vec grad = Vec::Zero(nDof);
        model.computeEnergyGradientAndHessian(h, grad, hessian);
        Vec grad_test = Vec::Zero(nDof);
        model.computeEnergyAndGradient(h, grad_test);

        // TODO Handle gradients with respect to paramters!
        const Mat dgradE_dp = Mat::Zero(nDof, nParameters);

        const Vec equation_vector = -(lossPositionGradient + one_over_h * lossVelocityGradient);

        Eigen::ConjugateGradient<SystemMatrix, Eigen::Upper | Eigen::Lower, Eigen::IdentityPreconditioner> solver;
        solver.compute(hessian);
        Vec z = solver.solve(equation_vector);  // Adjoint

        // Multiple backward iterations
        Vec h_grad = -equation_vector;
        Vec dz = Vec::Zero(nDof);
        constexpr Scalar dx = 1e-8;
        for (unsigned int j = 0; j < maxIterations; ++j) {
            const Vec Hz = approximateHzFiniteDiff(model, grad, x0, v0, z, h, dx);
            if (Hz.hasNaN()) {
                throw std::runtime_error(
                    "Back Propagation failed to converge with the current number of backward iterations.");
            }
            h_grad = Hz - equation_vector;
            dz = solver.solve(-h_grad);

            z += dz;
        }

        // Update the loss function gradients
        // -------------------------------------------------------------------------
        applyComposeAxisAngleJacobian(h, model, lossVelocityGradient);

        model.computeEnergyRetardedPositionHessian(h, dgradE_dx0);
        lossPositionGradient = loss.lossPositionPartialDerivative[static_cast<std::size_t>(i)].transpose() -
                               one_over_h * lossVelocityGradient.transpose() + z.transpose() * dgradE_dx0;

        model.computeEnergyRetardedVelocityHessian(h, dgradE_dv0);
        lossVelocityGradient =
            loss.lossVelocityPartialDerivative[static_cast<std::size_t>(i)].transpose() + z.transpose() * dgradE_dv0;

        lossGradient += z.transpose() * dgradE_dp;
    }
    // Add the initial conditions term
    // -------------------------------------------------------------------------
    applyLocalToGlobal(model, lossPositionGradient);
    lossGradient += lossPositionGradient.transpose() * dx0_dp + lossVelocityGradient.transpose() * dv0_dp;

    return lossGradient;
}

}  // namespace mandos::core
