#include <Eigen/Dense>  // for inverse()
#include <cmath>

#include <spdlog/spdlog.h>
#include <fmt/ostream.h>

#include <Mandos/Core/inertia_energies.hpp>
#include <Mandos/Core/particle.hpp>
#include <Mandos/Core/rigid_body.hpp>
#include <Mandos/Core/simulation.hpp>
#include <Mandos/Core/utility_functions.hpp>
#include <Mandos/Core/sinc.hpp>

namespace mandos::core
{

Scalar LinearInertia::compute_energy(Scalar TimeStep, const PhysicsState &state, const PhysicsState &state0) const
{
    const Vec3 x = p.get_position(state);
    const Vec3 x0 = p.get_position(state0);
    const Vec3 v0 = p.get_velocity(state0);
    const Vec3 x_guess = x0 + TimeStep * v0;
    const Scalar h2 = TimeStep * TimeStep;

    const Scalar energy = 1.0 / (2.0 * h2) * (x - x_guess).transpose() * Mass * (x - x_guess);
    return energy;
}

void LinearInertia::compute_energy_gradient(Scalar TimeStep,
                                            const PhysicsState &state,
                                            const PhysicsState &state0,
                                            Vec &grad) const
{
    // Get the relevant sate
    // ---------------------------------------------------------------
    const Vec3 x = p.get_position(state);
    const Vec3 x0 = p.get_position(state0);
    const Vec3 v0 = p.get_velocity(state0);
    const Vec3 x_guess = x0 + TimeStep * v0;
    const Scalar one_over_h2 = 1 / (TimeStep * TimeStep);

    const Vec3 gradient = one_over_h2 * Mass * (x - x_guess);

    // Add the energy derivatives to the global structure
    // ---------------------------------------------------------------
    grad.segment<3>(p.index) += gradient;
}

void LinearInertia::compute_energy_and_derivatives(Scalar TimeStep,
                                                   const PhysicsState &state,
                                                   const PhysicsState &state0,
                                                   EnergyAndDerivatives &f) const
{
    // Get the relevant sate
    // ---------------------------------------------------------------
    const Vec3 x = p.get_position(state);
    const Vec3 x0 = p.get_position(state0);
    const Vec3 v0 = p.get_velocity(state0);
    const Vec3 x_guess = x0 + TimeStep * v0;
    const Scalar one_over_h2 = 1 / (TimeStep * TimeStep);

    // Compute the energy derivatives
    // ---------------------------------------------------------------
    const Scalar energy = 0.5 * one_over_h2 * (x - x_guess).transpose() * Mass * (x - x_guess);
    const Vec3 gradient = one_over_h2 * Mass * (x - x_guess);
    const Mat3 hessian = one_over_h2 * Mass;

    // Add the energy derivatives to the global structure
    // ---------------------------------------------------------------
    f.energy += energy;
    f.gradient.segment<3>(p.index) += gradient;
    for (unsigned int i = 0; i < 3; i++) {
        for (unsigned int j = 0; j < 3; j++) {
            f.hessian_triplets.emplace_back(p.index + i, p.index + j, hessian(i, j));
        }
    }
}

Scalar RotationalInertia::compute_energy(Scalar TimeStep, const PhysicsState &state, const PhysicsState &state0) const
{
    const Mat3 inertia_tensor = rb.J_inertia_tensor0;
    const Mat3 R = rb.compute_rotation_matrix(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 omega0 = rb.get_axis_angle(state0.v);
    const Mat3 R0 = compute_rotation_matrix_rodrigues(theta0);
    const Mat3 R0old = compute_rotation_matrix_rodrigues(theta0 - omega0 * TimeStep);
    const Mat3 R_guess = (R0 + (R0 - R0old));  // x0 + h* v0
    const Mat3 deltaR = R - R_guess;
    const Scalar h2 = TimeStep * TimeStep;

    // Compute the energy derivatives
    // ---------------------------------------------------------------
    const Scalar KE = (deltaR * rb.J_inertia_tensor0 * deltaR.transpose()).trace() / (2.0f * h2);
    return KE;
}

static const Scalar threshold2 = 1e-7;

inline void compute_axis_angle_jacobian_parts(const Vec3 &phi, Mat3 &A, Mat3 &B)
{
    const Mat3 phi_phiT = phi * phi.transpose();
    A = compute_rotation_matrix_rodrigues(phi) - Mat3::Identity() + phi_phiT;
    B = skew(phi) + phi_phiT;
}

inline Mat3 compute_global_to_local_axis_angle_jacobian(const Vec3 &phi)
{
    if (phi.norm() < threshold2)
        return Mat3::Identity();

    Mat3 A, B;
    compute_axis_angle_jacobian_parts(phi, A, B);
    return A.inverse() * B;
}

inline Mat3 compute_local_to_global_axis_angle_jacobian(const Vec3 &phi)
{
    if (phi.norm() < threshold2)
        return Mat3::Identity();

    Mat3 A, B;
    compute_axis_angle_jacobian_parts(phi, A, B);
    return B.inverse() * A;
}

inline Mat3 compute_global_axis_angle_jacobian(const Vec3 &phi)
{
    const Scalar angle = phi.norm();
    if (angle < threshold2)
        return Mat3::Identity();
    const Vec3 axis = phi / angle;
    const Scalar half_angle = 0.5 * angle;
    const Mat3 axisaxisT = axis * axis.transpose();
    return half_angle / tan(half_angle) * (Mat3::Identity() - axisaxisT) + axisaxisT - skew(0.5 * phi);
}

inline Scalar rotation_inertia_energy_global(const Scalar TimeStep,
                                             const Mat3 &inertia_tensor,
                                             const Vec3 &phi,
                                             const Vec3 &phi0,
                                             const Vec3 &omega0)
{
    const Mat3 R = compute_rotation_matrix_rodrigues(phi);
    const Mat3 R0 = compute_rotation_matrix_rodrigues(phi0);
    const Mat3 R0old = compute_rotation_matrix_rodrigues(phi0 - TimeStep * omega0);
    const Mat3 R_guess = (R0 + (R0 - R0old));  // x0 + h* v0
    const Mat3 deltaR = R - R_guess;
    const Scalar one_over_2h2 = 1.0 / (2.0 * TimeStep * TimeStep);

    return one_over_2h2 * (deltaR.transpose() * deltaR * inertia_tensor).trace();
}
inline Vec3 rotation_inertia_energy_finite_gradient_global(const Scalar dx,
                                                           const Scalar TimeStep,
                                                           const Mat3 &inertia_tensor,
                                                           const Vec3 &phi,
                                                           const Vec3 &phi0,
                                                           const Vec3 &omega0)
{
    const Scalar E0 = rotation_inertia_energy_global(TimeStep, inertia_tensor, phi, phi0, omega0);
    Vec3 grad = Vec3::Zero();
    for (unsigned int i = 0; i < 3; i++) {
        Vec3 dphi = phi;
        dphi[i] += dx;
        const Scalar dE = rotation_inertia_energy_global(TimeStep, inertia_tensor, dphi, phi0, omega0);
        grad[i] = (dE - E0) / dx;
    }
    return grad;
}

inline Mat3 rotation_inertia_energy_finite_hessian_global(const Scalar dx,
                                                          const Scalar TimeStep,
                                                          const Mat3 &inertia_tensor,
                                                          const Vec3 &phi,
                                                          const Vec3 &phi0,
                                                          const Vec3 &omega0)
{
    const Vec3 grad0 = rotation_inertia_energy_finite_gradient_global(dx, TimeStep, inertia_tensor, phi, phi0, omega0);
    Mat3 hess = Mat3::Zero();
    for (unsigned int i = 0; i < 3; i++) {
        Vec3 dphi = phi;
        dphi[i] += dx;
        const Vec3 dgrad =
            rotation_inertia_energy_finite_gradient_global(dx, TimeStep, inertia_tensor, dphi, phi0, omega0);
        hess.row(i) = (dgrad - grad0) / dx;
    }

    return hess;
}
void RotationalInertia::compute_energy_gradient(Scalar TimeStep,
                                                const PhysicsState &state,
                                                const PhysicsState &state0,
                                                Vec &grad) const
{
    // Get the relevant sate
    // ---------------------------------------------------------------
    const Mat3 inertia_tensor = rb.J_inertia_tensor0;
    const Mat3 R = rb.compute_rotation_matrix(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 omega0 = rb.get_axis_angle(state0.v);
    const Mat3 R0 = compute_rotation_matrix_rodrigues(theta0);
    const Mat3 R0old = compute_rotation_matrix_rodrigues(theta0 - omega0 * TimeStep);
    const Mat3 R_guess = (R0 + (R0 - R0old));  // x0 + h* v0

    const Mat3 rot_inertia = R * inertia_tensor * R_guess.transpose();
    const Mat3 A = (rot_inertia - rot_inertia.transpose()) / 2.0;
    const Scalar h2 = TimeStep * TimeStep;

    const Vec3 gradient = 2.0 * Vec3(-A(1, 2), A(0, 2), -A(0, 1)) / h2;  // v s.t. A = skew(v)

    grad.segment<3>(rb.index + 3) += gradient;
}

void RotationalInertia::compute_energy_and_derivatives(Scalar TimeStep,
                                                       const PhysicsState &state,
                                                       const PhysicsState &state0,
                                                       EnergyAndDerivatives &f) const
{
    // Get the relevant sate
    // ---------------------------------------------------------------
    const Mat3 inertia_tensor = rb.J_inertia_tensor0;
    const Mat3 R = rb.compute_rotation_matrix(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 omega0 = rb.get_axis_angle(state0.v);
    const Mat3 R0 = compute_rotation_matrix_rodrigues(theta0);
    const Mat3 R0old = compute_rotation_matrix_rodrigues(theta0 - omega0 * TimeStep);
    const Mat3 R_guess = (R0 + (R0 - R0old));  // x0 + h* v0

    const Mat3 deltaR = R - R_guess;
    const Mat3 rot_inertia = R * inertia_tensor * R_guess.transpose();
    const Mat3 S = (rot_inertia + rot_inertia.transpose()) / 2.0;  // Exact hessian
    // const Mat3 S = R * inertia_tensor * R.transpose(); // Linear approximation
    const Mat3 A = (rot_inertia - rot_inertia.transpose()) / 2.0;
    const Scalar h2 = TimeStep * TimeStep;

    // Compute the energy derivatives
    // ---------------------------------------------------------------
    const Scalar KE = (deltaR * inertia_tensor * deltaR.transpose()).trace() / (2.0 * h2);
    const Vec3 gradient = 2.0 * Vec3(-A(1, 2), A(0, 2), -A(0, 1)) / h2;  // v s.t. A = skew(v)
    const Mat3 hessian = 1.0 / h2 * (S.trace() * Mat3::Identity() - S);

    // Add the energy derivatives to the global structure
    // ---------------------------------------------------------------
    f.energy += KE;
    f.gradient.segment<3>(rb.index + 3) += gradient;
    for (unsigned int i = 0; i < 3; i++) {
        for (unsigned int j = 0; j < 3; j++) {
            f.hessian_triplets.emplace_back(rb.index + 3 + i, rb.index + 3 + j, hessian(i, j));
        }
    }
}

void RotationalInertia::update_state(const Scalar TimeStep,
                                     const Vec &dx,
                                     PhysicsState &state,
                                     const PhysicsState &state0) const
{
    const Vec3 theta = rb.get_axis_angle(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 dtheta = rb.get_axis_angle(dx);

    const Vec3 new_theta = compose_axis_angle(dtheta, theta);
    if (new_theta.hasNaN()) {
        spdlog::debug("{}", fmt::streamed(dtheta.transpose()));
        spdlog::debug("{}", fmt::streamed(theta.transpose()));
        spdlog::debug("{}", fmt::streamed(new_theta.transpose()));
    }
    state.x.segment<3>(rb.index + 3) = new_theta;  // x_new
    const Vec3 delta_theta = new_theta - theta0;
    state.v.segment<3>(rb.index + 3) = (delta_theta) / TimeStep;  // v_new
}

Scalar RotationalInertiaGlobal::compute_energy(Scalar TimeStep,
                                               const PhysicsState &state,
                                               const PhysicsState &state0) const
{
    const RotationalInertia i = RotationalInertia(rb);
    Scalar energy = i.compute_energy(TimeStep, state, state0);
    return energy;
}

void RotationalInertiaGlobal::compute_energy_gradient(Scalar TimeStep,
                                                      const PhysicsState &state,
                                                      const PhysicsState &state0,
                                                      Vec &grad) const
{
    // Get the relevant sate
    // ---------------------------------------------------------------
    const Mat3 inertia_tensor = rb.J_inertia_tensor0;
    const Vec3 phi = rb.get_axis_angle(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 omega0 = rb.get_axis_angle(state0.v);

    const Mat3 R0 = compute_rotation_matrix_rodrigues(theta0);
    const Mat3 R0old = compute_rotation_matrix_rodrigues(theta0 - omega0 * TimeStep);
    const Mat3 R_guess = (R0 + (R0 - R0old));  // x0 + h* v0

    const Mat3 rot_inertia = inertia_tensor * R_guess.transpose();
    const Mat3 A = rot_inertia.transpose() - rot_inertia;
    const Mat3 S = (rot_inertia + rot_inertia.transpose()) / 2.0;
    const Mat3 SS = (S.trace() * Mat3::Identity() - S);
    const Vec3 v = Vec3(A(1, 2), -A(0, 2), A(0, 1));
    const Scalar phi_norm = phi.norm();
    const Scalar sinc_phi_2 = sinc(phi_norm / 2);
    const Scalar one_over_2h2 = 1.0 / (2.0 * TimeStep * TimeStep);

    const Vec3 gradient =
        (2.0 * grad_sinc(phi) * v.dot(phi) + 2.0 * sinc(phi_norm) * v +
         sinc_phi_2 * grad_sinc(phi / 2) * phi.transpose() * SS * phi + 2.0 * sinc_phi_2 * sinc_phi_2 * SS * phi) *
        one_over_2h2;

    grad.segment<3>(rb.index + 3) += gradient;
}

void RotationalInertiaGlobal::compute_energy_and_derivatives(Scalar TimeStep,
                                                             const PhysicsState &state,
                                                             const PhysicsState &state0,
                                                             EnergyAndDerivatives &f) const
{
    // Get the relevant sate
    // ---------------------------------------------------------------
    const Mat3 inertia_tensor = rb.J_inertia_tensor0;
    const Vec3 phi = rb.get_axis_angle(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 omega0 = rb.get_axis_angle(state0.v);

    const Mat3 R = compute_rotation_matrix_rodrigues(phi);
    const Mat3 R0 = compute_rotation_matrix_rodrigues(theta0);
    const Mat3 R0old = compute_rotation_matrix_rodrigues(theta0 - omega0 * TimeStep);
    const Mat3 R_guess = (R0 + (R0 - R0old));  // x0 + h* v0
    const Mat3 deltaR = R - R_guess;

    const Mat3 rot_inertia = inertia_tensor * R_guess.transpose();
    const Mat3 A = rot_inertia.transpose() - rot_inertia;
    const Mat3 S = (rot_inertia + rot_inertia.transpose()) / 2.0;
    const Mat3 SS = (S.trace() * Mat3::Identity() - S);
    const Vec3 v = Vec3(A(1, 2), -A(0, 2), A(0, 1));
    const Scalar phi_norm = phi.norm();
    const Scalar sinc_phi_2 = sinc(phi_norm / 2);
    const Vec3 grad_sinc_phi_2 = 0.5 * grad_sinc(phi / 2.0);
    const Scalar phiSphi = phi.transpose() * SS * phi;
    const Scalar one_over_2h2 = 1.0 / (2.0 * TimeStep * TimeStep);

    // Compute the energy derivatives
    // ---------------------------------------------------------------
    const Scalar KE = (deltaR * rb.J_inertia_tensor0 * deltaR.transpose()).trace() * one_over_2h2;

    const Vec3 gradient =
        (2.0 * grad_sinc(phi) * v.dot(phi) + 2.0 * sinc(phi_norm) * v +
         sinc_phi_2 * grad_sinc(phi / 2) * phi.transpose() * SS * phi + 2.0 * sinc_phi_2 * sinc_phi_2 * SS * phi) *
        one_over_2h2;

    const Mat3 hessian =
        (2.0 * hess_sinc(phi) * v.dot(phi) + 2.0 * (v * grad_sinc(phi).transpose() + grad_sinc(phi) * v.transpose()) +
         2.0 * grad_sinc_phi_2 * grad_sinc_phi_2.transpose() * phiSphi +
         2.0 * sinc_phi_2 * 0.25 * hess_sinc(phi / 2.0) * phiSphi +
         4.0 * sinc_phi_2 * ((SS * phi) * grad_sinc_phi_2.transpose() + grad_sinc_phi_2 * (SS * phi).transpose()) +
         2.0 * sinc_phi_2 * sinc_phi_2 * SS) *
        one_over_2h2;

    // eigenvalues
    // Eigen::EigenSolver<Mat3> solver(hessian);
    // std ::cout << "Global eigenvalues" << " " << solver.eigenvalues().real().transpose() << std ::endl;

    // Add the energy derivatives to the global structure
    // ---------------------------------------------------------------
    f.energy += KE;
    f.gradient.segment<3>(rb.index + 3) += gradient;
    for (unsigned int i = 0; i < 3; i++) {
        for (unsigned int j = 0; j < 3; j++) {
            f.hessian_triplets.emplace_back(rb.index + 3 + i, rb.index + 3 + j, hessian(i, j));
        }
    }
}

void RotationalInertiaGlobal::update_state(const Scalar TimeStep,
                                           const Vec &dx,
                                           PhysicsState &state,
                                           const PhysicsState &state0) const
{
    const Vec3 theta = rb.get_axis_angle(state.x);
    const Vec3 theta0 = rb.get_axis_angle(state0.x);
    const Vec3 dtheta = rb.get_axis_angle(dx);

    const Vec3 new_theta = theta + dtheta;
    Scalar new_angle = new_theta.norm();
    const Vec3 axis = new_theta / new_angle;
    const Vec3 delta_theta = new_theta - theta0;  // Compute delta theta before clamping the angle between -pi and pi

    // Clamp the new angle betwenn -pi and pi
    new_angle = std::fmod(new_angle, 2.0 * M_PI);
    if (new_angle > M_PI) {
        new_angle -= 2 * M_PI;
    }

    // Update the simulation state
    state.x.segment<3>(rb.index + 3) = new_angle * axis;          // x_new
    state.v.segment<3>(rb.index + 3) = (delta_theta) / TimeStep;  // v_new
}

void add_particle_to_simulation(Simulation &simulation, const Particle &p)
{
    simulation.simulables.particles.push_back(p);
    simulation.energies.inertial_energies.linear_inertias.emplace_back(p);
}

void add_rigid_body_to_simulation(Simulation &simulation, const RigidBody &rb, const bool global)
{
    simulation.simulables.rigid_bodies.emplace_back(rb);
    simulation.energies.inertial_energies.linear_inertias.emplace_back(Particle(rb.mass, rb.index));
    if (global)
        simulation.energies.inertial_energies.rotational_global_inertias.emplace_back(rb);
    else
        simulation.energies.inertial_energies.rotational_inertias.emplace_back(rb);
}

}  // namespace mandos::core
