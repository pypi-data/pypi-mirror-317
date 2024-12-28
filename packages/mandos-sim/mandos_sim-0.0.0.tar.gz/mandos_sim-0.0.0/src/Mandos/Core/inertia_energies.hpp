#ifndef MANDOS_INERTIA_ENERGIES_H_
#define MANDOS_INERTIA_ENERGIES_H_

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/particle.hpp>
#include <Mandos/Core/physics_state.hpp>
#include <Mandos/Core/rigid_body.hpp>

namespace mandos::core
{

// struct LinearInertia {
//     LinearInertia(Particle p)
//         : Mass(Mat3::Identity() * p.mass)
//         , p(p)
//     {
//     }

//     Mat3 Mass;
//     Particle p;

//     Scalar compute_energy(Scalar TimeStep, const PhysicsState& state, const PhysicsState& state0) const;
//     void compute_energy_gradient(Scalar TimeStep,
//                                  const PhysicsState& state,
//                                  const PhysicsState& state0,
//                                  Vec& grad) const;
//     void compute_energy_and_derivatives(Scalar TimeStep,
//                                         const PhysicsState& state,
//                                         const PhysicsState& state0,
//                                         EnergyAndDerivatives& f) const;
//     inline void update_state(const Scalar TimeStep,
//                              const Vec& dx,
//                              PhysicsState& state,
//                              const PhysicsState& state0) const
//     {
//         state.x.segment<3>(p.index) += dx.segment<3>(p.index);
//         state.v.segment<3>(p.index) = (state.x.segment<3>(p.index) - state0.x.segment<3>(p.index)) / TimeStep;
//     }
// };

// struct RotationalInertia {
//     RotationalInertia(RigidBody rb)
//         : rb(rb)
//     {
//     }
//     RigidBody rb;

//     Scalar compute_energy(Scalar TimeStep, const PhysicsState& state, const PhysicsState& state0) const;
//     void compute_energy_gradient(Scalar TimeStep,
//                                  const PhysicsState& state,
//                                  const PhysicsState& state0,
//                                  Vec& grad) const;
//     void compute_energy_and_derivatives(Scalar TimeStep,
//                                         const PhysicsState& state,
//                                         const PhysicsState& state0,
//                                         EnergyAndDerivatives& f) const;
//     void update_state(const Scalar TimeStep, const Vec& dx, PhysicsState& state, const PhysicsState& state0) const;
// };

// struct RotationalInertiaGlobal {
//     RotationalInertiaGlobal(RigidBody rb)
//         : rb(rb)
//     {
//     }
//     RigidBody rb;

//     Scalar compute_energy(Scalar TimeStep, const PhysicsState& state, const PhysicsState& state0) const;
//     void compute_energy_gradient(Scalar TimeStep,
//                                  const PhysicsState& state,
//                                  const PhysicsState& state0,
//                                  Vec& grad) const;
//     void compute_energy_and_derivatives(Scalar TimeStep,
//                                         const PhysicsState& state,
//                                         const PhysicsState& state0,
//                                         EnergyAndDerivatives& f) const;
//     void update_state(const Scalar TimeStep, const Vec& dx, PhysicsState& state, const PhysicsState& state0) const;
// };

// struct Simulation;
// void add_particle_to_simulation(Simulation& simulation, const Particle& p);
// void add_rigid_body_to_simulation(Simulation& simulation, const RigidBody& rb, const bool global = false);

}  // namespace mandos::core

#endif  // MANDOS_INERTIA_ENERGIES_H_
