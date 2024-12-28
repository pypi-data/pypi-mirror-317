#ifndef MANDOS_CORE_COLLIDERS_H
#define MANDOS_CORE_COLLIDERS_H

#include <Mandos/Core/utility_functions.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>

#include <Mandos/Core/Collisions/SDF.hpp>
#include <Mandos/Core/Collisions/SphereCloud.hpp>

namespace mandos::core
{

// List of the possible colliders each SimulationObject<> can handle
template <typename Tag>
struct Colliders {
};

template <>
struct Colliders<mandos::core::Particle3DTag> {
    using types = utilities::typelist<mandos::core::collisions::SphereCloud>;
    types::template map<std::vector>::template as<std::tuple> m_colliders;
};

template <>
struct Colliders<mandos::core::RigidBodyTag> {
    using types = utilities::typelist<mandos::core::collisions::SDF>;
    types::template map<std::vector>::template as<std::tuple> m_colliders;
};

template <>
struct Colliders<mandos::core::RigidBodyGlobalTag> {
    using types = utilities::typelist<mandos::core::collisions::SDF>;
    types::template map<std::vector>::template as<std::tuple> m_colliders;
};

}  // namespace mandos::core

#endif  // MANDOS_CORE_COLLIDERS_H