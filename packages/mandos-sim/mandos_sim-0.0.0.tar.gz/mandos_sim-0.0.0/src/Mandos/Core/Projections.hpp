#ifndef MANDOS_PROJECTIONS_H
#define MANDOS_PROJECTIONS_H

#include <Mandos/Core/MechanicalState.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>

#include <Mandos/Core/Projections/FixedProjection.hpp>
#include <Mandos/Core/utility_functions.hpp>

namespace mandos::core
{

/**
 * @brief The projections supported by a SimulationObject<PhysicalStateT>

 * Projections are used to impose constraint on the degrees of freedom of an object. It projects the gradients and
 * hessian during the simulation to ensure the constraints are met after the update.
 * They are only applied on degrees of freedom that are simulated. Projections added to SimulationObject which are
 * mapped will be ignored by the simulation
 *
 * The Projection doesn't projects positions or velocities, and the user must ensure the constrained degrees of freedom
 * meet the constraint. For example, if using a FixedProjection on a Particle3D SimulationObject to fix the second
 * particle to [0,0,0], the user must set the position manually. The Projection then ensures that the solver keeps that
 * particle on the specified location
 *
 * Projections<> is specialized for each SimulationObject<> based on its MechanicalStateTag
 *
 * @tparam MechanicalStateTag MechanicalState of the SimulationObject supporting this set of Projections
 */
template <typename Tag>
struct Projections {
};

/**
 * @brief Specialization of the Projections for Particle3DTag
 *
 * @tparam  Particle3DTag
 */
template <>
struct Projections<Particle3DTag> {
    static constexpr bool HasProjections = true;
    using types = utilities::typelist<mandos::core::FixedProjection>;
    types::template as<std::tuple> projections;
};

template <>
struct Projections<RigidBodyTag> {
    static constexpr bool HasProjections = true;
    using types = utilities::typelist<mandos::core::FixedProjection>;
    types::template as<std::tuple> projections;
};

template <>
struct Projections<RigidBodyGlobalTag> {
    static constexpr bool HasProjections = false;
};

}  // namespace mandos::core

#endif  //  MANDOS_PROJECTIONS_H
