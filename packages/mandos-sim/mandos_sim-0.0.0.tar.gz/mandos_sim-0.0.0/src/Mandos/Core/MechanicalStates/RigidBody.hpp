#ifndef MANDOS_MECHANICALSTATES_RIGIDBODY_H
#define MANDOS_MECHANICALSTATES_RIGIDBODY_H

#include <Mandos/Core/MechanicalStates/RigidBodyCommon.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief Tag to represent a cloud of Rigid Bodies in space
 *
 */
struct RigidBodyTag {
};

template <>
struct MANDOS_CORE_EXPORT MechanicalState<RigidBodyTag> : RigidBodyCommon {
    void updateState(const Eigen::Ref<const Vec> &dx,
                     const Eigen::Ref<const Vec> &x0,
                     const Eigen::Ref<const Vec> &v0,
                     Scalar h);
};

}  // namespace mandos::core

#endif  //  MANDOS_MECHANICALSTATES_RIGIDBODY_H
