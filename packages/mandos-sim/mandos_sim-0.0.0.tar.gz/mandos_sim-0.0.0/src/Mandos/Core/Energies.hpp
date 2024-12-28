#ifndef MANDOS_ENERGIES_H_
#define MANDOS_ENERGIES_H_

#include <Mandos/Core/MechanicalState.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

#include <Mandos/Core/Energies/LumpedMassInertia.hpp>
#include <Mandos/Core/Energies/StableNeoHookean.hpp>
#include <Mandos/Core/Energies/GravityEnergy.hpp>
#include <Mandos/Core/Energies/ConstantForce.hpp>
#include <Mandos/Core/Energies/RigidBodyInertia.hpp>
#include <Mandos/Core/Energies/MassSpring.hpp>
#include <Mandos/Core/Energies/CosseratBendingRod.hpp>
#include <Mandos/Core/Energies/CosseratRodAlignment.hpp>

#include <Mandos/Core/utility_functions.hpp>
#include <Mandos/Core/Energies/CollisionSpring.hpp>

namespace mandos::core
{

/**
 * @brief The energies supported by a SimulationObject<Tag>

 * Some energies have sense only for a particular type of SimulationObject. For example, an object made of 3D particles
 * may have an elastic energy, like StVK. This same energy, doesn't make sense for a rigid body simulation object.
 *
 * Energies<> is specialized for each SimulationObject<> based on its Tag
 *
 * @tparam Tag Tag of the SimulationObject supporting this set of energies
 */
template <typename Tag>
struct Inertias {
};

template <typename Tag>
struct Potentials {
};

/**
 * @brief Specialization of the energies for Particle3DTag
 *
 * @tparam  Particle3DTag
 */
template <>
struct Inertias<Particle3DTag> {
    std::tuple<mandos::core::LumpedMassInertia> m_inertias;
};

template <>
struct Potentials<Particle3DTag> {
    std::tuple<mandos::core::GravityEnergy,
               mandos::core::ConstantForce,
               mandos::core::MassSpring,
               mandos::core::StableNeoHookean,
               mandos::core::CollisionSpring>
        m_potentials;
};

template <>
struct Inertias<RigidBodyTag> {
    std::tuple<mandos::core::RigidBodyInertia> m_inertias;
};

template <>
struct Potentials<RigidBodyTag> {
    std::tuple<mandos::core::GravityEnergy,
               mandos::core::MassSpring,
               mandos::core::CosseratBendingRod,
               mandos::core::CosseratRodAlignment>
        m_potentials;
};

template <>
struct Inertias<RigidBodyGlobalTag> {
    std::tuple<mandos::core::RigidBodyInertia> m_inertias;
};

template <>
struct Potentials<RigidBodyGlobalTag> {
    std::tuple<mandos::core::GravityEnergy> m_potentials;
};

}  // namespace mandos::core

#endif  //  MANDOS_ENERGIES_H_
