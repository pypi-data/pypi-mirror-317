#ifndef MANDOS_CORE_COLLISIONS_COLLISIONDETECTION_H
#define MANDOS_CORE_COLLISIONS_COLLISIONDETECTION_H

#include <Mandos/Core/SimulationObject.hpp>

#include <Mandos/Core/Collisions/SDF.hpp>
#include <Mandos/Core/Collisions/SphereCloud.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include <Mandos/Core/KinematicGraph.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core::collisions
{

template <typename C0, typename C1>
void collisions(const C0 &, const C1 &)
{
    // Using std::is_same_v here as a trick to trigger the static_assert with a dependent type
    static_assert(
        std::is_same_v<C0, void>,
        "You need to specialize the collision routine for this type of objects. Maybe they are switched around?");
}

/**
 * @brief Computes ContactEvents between a SDF and a SphereCloud
 *
 * @param sdf  The SDF
 * @param sc  The SphereCloud
 * @return std::vector<ContactEvent>
 */
std::vector<ContactEvent<SDF, SphereCloud>> MANDOS_CORE_EXPORT collisions(const SDF &sdf, const SphereCloud &sc);

}  // namespace mandos::core::collisions

#endif  // MANDOS_CORE_COLLIDERS_COLLISIONS_H