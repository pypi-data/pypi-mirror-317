#ifndef MANDOS_MECHANICALSTATE_H_
#define MANDOS_MECHANICALSTATE_H_

#include <Mandos/Core/linear_algebra.hpp>

namespace mandos::core
{

/**
 * @brief The mechanical state represents the current state of a simulation object
 *
 * @tparam MechanicalStateTag Represents the type of the mechanical state. For example, a Particle3DTag represents
 * particles in 3D space, and therefore, positions, velocities and the gradient are represented as 3D vectors
 */
template <typename MechanicalStateTag>
struct MechanicalState {
};

}  // namespace mandos::core

#endif  // MANDOS_MECHANICALSTATE_H_
