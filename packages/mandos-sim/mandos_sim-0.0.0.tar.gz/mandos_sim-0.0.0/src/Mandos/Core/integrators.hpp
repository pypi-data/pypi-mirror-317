#ifndef MANDOS_INTEGRATORS_H_
#define MANDOS_INTEGRATORS_H_

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/simulation.hpp>

namespace mandos::core
{

void handle_frozen_dof(const std::vector<unsigned int> &frozen_dof, Vec *eq_vec, SparseMat *eq_mat);

void integrate_implicit_euler(const Simulation &simulation,
                              const PhysicsState &state,
                              const EnergyAndDerivatives &f,
                              Vec &dx);

}  // namespace mandos::core

#endif  // MANDOS_INTEGRATORS_H_
