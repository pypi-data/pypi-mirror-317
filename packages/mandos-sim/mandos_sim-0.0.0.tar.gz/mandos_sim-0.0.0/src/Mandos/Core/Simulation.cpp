#include <Mandos/Core/Simulation.hpp>

#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/SystemMatrix.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <tracy/Tracy.hpp>

namespace mandos::core
{

// TODO move this into its own class, so we can provide a configuration scheme (iterations, line search, cache...)
SimulationStepResult step(Model &model, const StepParameters &stepParameters)
{
    FrameMark;
    // Get the size of the DoF of the model
    auto nDof = model.nDof();

    // Get the current generalized state of the simulation
    Vec x0{Vec::Zero(nDof)};
    Vec v0{Vec::Zero(nDof)};
    model.state(x0, v0);

    model.updateColliders();
    model.detectCollisions();

    // We perform the advection
    model.computeAdvection(stepParameters.h);

    Vec grad{Vec::Zero(nDof)};
    SystemMatrix hessian(nDof, nDof);

    // TODO Make these variables
    const int maxNewtonIterations = stepParameters.newtonIterations;

    Vec linX{Vec::Zero(nDof)};
    Vec linV{Vec::Zero(nDof)};
    auto currentNewtonIteration{0};
    while (currentNewtonIteration < maxNewtonIterations) {
        ZoneScopedN("Simulation.step.NewtonIteration");
        // Get state on current linearization point
        model.state(linX, linV);

        // Compute energy and derivatives
        // -----------------------------------------------------------------------------------------
        grad.setZero();
        // There is no need to clear the SystemMatrix; it only contains references to the actual SimulationObject
        // hessians, which are going to be clear

        const Scalar linEnergy{model.computeEnergyGradientAndHessian(stepParameters.h, grad, hessian)};
        TracyPlot("Energy", linEnergy);
        TracyPlot("dEdx.norm()", grad.norm());
        TracyPlot("Newton iteration", static_cast<int64_t>(currentNewtonIteration));

        // If the grad is small, consider the step a success
        const auto gradNorm = grad.norm();
        TracyPlot("Gradient norm", gradNorm);
        if (gradNorm < stepParameters.gradNorm) {
            return SimulationStepResult::Success;
        }

        // // Integration step
        // // ----------------------------------------------------------------------------------------
        const auto dx = [&stepParameters, &hessian, &grad]() {
            if (stepParameters.cgIterations != 0) {
                Eigen::ConjugateGradient<SystemMatrix, Eigen::Upper | Eigen::Lower, Eigen::IdentityPreconditioner> cg;
                cg.setTolerance(stepParameters.cgError);
                cg.setMaxIterations(stepParameters.cgIterations);
                cg.compute(hessian);
                return [&cg, &grad]() {
                    ZoneScopedN("Simulation.step.cgSolve");
                    return cg.solve(-grad).eval();
                }();
            }
            return (-grad).eval();
        }();

        // // Update state
        // // -----------------------------------------------------------------------------------------
        model.updateState(dx, x0, v0, stepParameters.h);

        // Line search
        // -----------------------------------------------------------------------------------------
        Scalar lineSearchEnergy{model.computeEnergy(stepParameters.h)};
        Scalar alpha{1.0};
        const int maxLSIterations = stepParameters.lineSearchIterations;
        int lsIterations{0};
        if (maxLSIterations != 0) {
            while (lineSearchEnergy > linEnergy) {
                ZoneScopedN("Simulation.step.lineSearch");
                if (lsIterations >= maxLSIterations) {
                    // If we dont converge, set the original state and return
                    if (!stepParameters.acceptFailedSolution) {
                        model.setState(x0, v0);
                    }
                    return SimulationStepResult::LineSearchFailed;
                }

                alpha *= 0.5;
                model.setState(linX, linV);
                model.updateState(alpha * dx, x0, v0, stepParameters.h);
                lineSearchEnergy = model.computeEnergy(stepParameters.h);
                lsIterations++;
            }
        }

        currentNewtonIteration++;
    }

    // If we dont converge, set the original state and return
    if (!stepParameters.acceptFailedSolution) {
        model.setState(x0, v0);
    }
    return SimulationStepResult::NewtonFailed;
}

}  // namespace mandos::core
