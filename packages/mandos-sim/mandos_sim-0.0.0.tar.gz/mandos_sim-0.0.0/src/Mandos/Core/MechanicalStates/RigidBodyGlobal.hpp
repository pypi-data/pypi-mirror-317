#ifndef MANDOS_MECHANICALSTATE_RIGIDBODYGLOBALCLOUD_H
#define MANDOS_MECHANICALSTATE_RIGIDBODYGLOBALCLOUD_H

#include <Mandos/Core/MechanicalStates/RigidBodyCommon.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief Tag to represent a single Rigid Body in space
 *
 */
struct RigidBodyGlobalTag {
};

template <>
struct MANDOS_CORE_EXPORT MechanicalState<RigidBodyGlobalTag> : RigidBodyCommon {
    void updateState(const Eigen::Ref<const Vec> &dx,
                     const Eigen::Ref<const Vec> &x0,
                     const Eigen::Ref<const Vec> &v0,
                     Scalar h);
};

}  // namespace mandos::core

#endif  // MANDOS_MECHANICALSTATE_RIGIDBODYGLOBALCLOUD_H
