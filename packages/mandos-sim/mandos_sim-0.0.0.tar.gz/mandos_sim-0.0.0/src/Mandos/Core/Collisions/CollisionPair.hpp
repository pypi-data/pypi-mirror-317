#ifndef MANDOS_CORE_COLLISIONS_COLLISIONPAIR_H
#define MANDOS_CORE_COLLISIONS_COLLISIONPAIR_H

#include <Mandos/Core/Collisions/SimulationCollider.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>

namespace mandos::core::collisions
{

/**
  List of pairs of SimulationColliders than can collide between each other and the Particle3D descriptor of the
  SimulationObject holding the collision particles
 */

template <typename SimulationColliderT0, typename SimulationColliderT1>
struct CollisionPair {
    SimulationObjectHandle<Particle3DTag> collisionParticlesHandle;
    SimulationColliderT0 c0SimulationCollider{};
    SimulationColliderT1 c1SimulationCollider{};

    int mappingIndex0{-1};
    int mappingIndex1{-1};
    Scalar stiffness{0};
    Scalar threshold{0};

    SimulationObject<Particle3DTag> &collisionState()
    {
        return collisionParticlesHandle.simulationObject();
    }
};

}  // namespace mandos::core::collisions

#endif  // MANDOS_CORE_COLLISIONS_COLLISIONPAIR_H
