#ifndef MANDOS_MAPPINGS_H_
#define MANDOS_MAPPINGS_H_

// #include <Mandos/Core/fem_element.hpp>
// #include <Mandos/Core/gravity.hpp>
// #include <Mandos/Core/inertia_energies.hpp>
// #include <Mandos/Core/spring.hpp>
// #include <Mandos/Core/rod_segment.hpp>

#include <Mandos/Core/MechanicalState.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>

#include <Mandos/Core/Mappings/BarycentricMapping.hpp>
#include <Mandos/Core/Mappings/IdentityMapping.hpp>
#include <Mandos/Core/Mappings/RigidBodyPointMapping.hpp>

#include <Mandos/Core/utility_functions.hpp>
#include <Mandos/Core/Collisions/SphereCloud.hpp>
#include <Mandos/Core/Collisions/SDF.hpp>
#include <Mandos/Core/Mappings/CollisionMapping.hpp>

namespace mandos::core
{

/**
 * @brief The mappings supported by a SimulationObject<MechanicalState>
 *
 * Mappings<> is specialized for each SimulationObject<> based on its MechanicalStateTag
 *
 */
template <typename MechanicalStateTag>
struct Mappings {
};

/**
 * @brief Specialization of the mappings for Particle3DTag
 *
 * @tparam  Particle3DTag
 */
template <>
struct Mappings<Particle3DTag> {
    static constexpr bool HasMappings = true;
    using types =
        utilities::typelist<mandos::core::IdentityMapping,
                            mandos::core::BarycentricMapping,
                            mandos::core::collisions::CollisionMapping<Particle3DTag, collisions::SphereCloud>>;
    types::template map<std::vector>::template as<std::tuple> m_mappings;
};

template <>
struct Mappings<RigidBodyTag> {
    static constexpr bool HasMappings = true;
    using types =
        utilities::typelist<mandos::core::RigidBodyPointMapping,
                            mandos::core::collisions::CollisionMapping<RigidBodyTag, mandos::core::collisions::SDF>>;
    types::template map<std::vector>::template as<std::tuple> m_mappings;
};

template <>
struct Mappings<RigidBodyGlobalTag> {
    static constexpr bool HasMappings = false;
};

}  // namespace mandos::core

#endif  // MANDOS_MAPPINGS_H
