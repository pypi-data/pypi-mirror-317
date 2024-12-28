#ifndef MANDOS_CORE_KINEMATICGRAPH_HPP
#define MANDOS_CORE_KINEMATICGRAPH_HPP

#include <boost/graph/adjacency_list.hpp>

#include <Mandos/Core/SimulationObject.hpp>
#include <Mandos/Core/SimulationObjectHandle.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>

#include <Mandos/Core/utility_functions.hpp>

namespace mandos::core
{
using SimulationObjects = utilities::typelist<SimulationObject<Particle3DTag>,  //
                                              SimulationObject<RigidBodyTag>,
                                              SimulationObject<RigidBodyGlobalTag>>;

using KinematicGraph = boost::adjacency_list<boost::vecS,
                                             boost::vecS,
                                             boost::bidirectionalS,
                                             SimulationObjects::map<SimulationObjectHandle_t>::as<std::variant>>;
}  // namespace mandos::core

#endif  // MANDOS_CORE_KINEMATICGRAPH_HPP