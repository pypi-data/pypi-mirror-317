#include <Mandos/Core/Model.hpp>

#include <Mandos/Core/SystemMatrix.hpp>

#include <algorithm>
#include <iterator>
#include <memory>

#include <boost/graph/reverse_graph.hpp>
#include <boost/graph/topological_sort.hpp>
#include <boost/range/iterator_range_core.hpp>
#include <type_traits>

#include <tracy/Tracy.hpp>

#include "Mandos/Core/Collisions/CollisionDetection.hpp"
#include "Mandos/Core/Collisions/SphereCloud.hpp"
#include "Mandos/Core/Energies/CollisionSpring.hpp"
#include "Mandos/Core/KinematicGraph.hpp"
#include "Mandos/Core/Mappings/CollisionMapping.hpp"
#include "Mandos/Core/MechanicalState.hpp"
#include "Mandos/Core/MechanicalStates/Particle3D.hpp"
#include "Mandos/Core/MechanicalStates/RigidBody.hpp"
#include <Mandos/Core/utility_functions.hpp>

#include <spdlog/spdlog.h>

namespace
{

template <typename EnergyT, typename Tag>
void initialize(EnergyT & /*unused*/, const mandos::core::MechanicalState<Tag> & /*unused*/)
{
}

template <typename SimulationObjectT>
mandos::core::Scalar computeEnergy(SimulationObjectT &simulationObject, mandos::core::Scalar h)
{
    mandos::core::Scalar accumulatedEnergy{0};
    if constexpr (SimulationObjectT::hasPotentials) {
        mandos::core::utilities::static_for_each(
            [&accumulatedEnergy, &simulationObject](const auto &energy) {
                accumulatedEnergy += energy.computeEnergy(simulationObject.mstate);
            },
            simulationObject.potentials());
    }

    if (h != mandos::core::Scalar(0)) {
        if constexpr (SimulationObjectT::hasInertias) {
            mandos::core::utilities::static_for_each(
                [&accumulatedEnergy, &simulationObject, h](const auto &energy) {
                    accumulatedEnergy += energy.computeEnergy(simulationObject.mstate, h);
                },
                simulationObject.inertias());
        }
    }

    return accumulatedEnergy;
}

template <typename SimulationObjectT>
mandos::core::Scalar computeEnergyAndGradient(SimulationObjectT &simulationObject, mandos::core::Scalar h)
{
    mandos::core::Scalar accumulatedEnergy{0};
    if constexpr (SimulationObjectT::hasPotentials) {
        mandos::core::utilities::static_for_each(
            [&accumulatedEnergy, &simulationObject](const auto &energy) {
                accumulatedEnergy += energy.computeEnergyAndGradient(simulationObject.mstate);
            },
            simulationObject.potentials());
    }

    if (h != mandos::core::Scalar(0)) {
        if constexpr (SimulationObjectT::hasInertias) {
            mandos::core::utilities::static_for_each(
                [&accumulatedEnergy, &simulationObject, h](const auto &energy) {
                    accumulatedEnergy += energy.computeEnergyAndGradient(simulationObject.mstate, h);
                },
                simulationObject.inertias());
        }
    }

    return accumulatedEnergy;
}

template <typename SimulationObjectT>
mandos::core::Scalar computeEnergyGradientAndHessian(SimulationObjectT &simulationObject, mandos::core::Scalar h)
{
    mandos::core::Scalar accumulatedEnergy{0};
    if constexpr (SimulationObjectT::hasPotentials) {
        mandos::core::utilities::static_for_each(
            [&accumulatedEnergy, &simulationObject](const auto &energy) {
                accumulatedEnergy += energy.computeEnergyGradientAndHessian(simulationObject.mstate);
            },
            simulationObject.potentials());
    }

    if (h != mandos::core::Scalar(0)) {
        if constexpr (SimulationObjectT::hasInertias) {
            mandos::core::utilities::static_for_each(
                [&accumulatedEnergy, &simulationObject, h](const auto &energy) {
                    accumulatedEnergy += energy.computeEnergyGradientAndHessian(simulationObject.mstate, h);
                },
                simulationObject.inertias());
        }
    }

    return accumulatedEnergy;
}

}  // namespace

namespace mandos::core
{

void Model::computeAdvection(Scalar h)
{
    ZoneScopedN("Model.computeAdvection");
    utilities::static_for_each(
        [h](auto &simulationObjects) {
            for (auto &simulationObject : simulationObjects) {
                using SimulationObjectT = std::remove_cvref_t<decltype(simulationObject)>;
                if constexpr (SimulationObjectT::hasInertias) {
                    utilities::static_for_each(
                        [&simulationObject, h](auto &inertia) { inertia.advect(simulationObject.mstate, h); },
                        simulationObject.inertias());
                }
            }
        },
        m_simulationObjects);
}

Scalar Model::computeEnergy(Scalar h) const
{
    ZoneScopedN("Model.computeEnergy");
    // For computing the total energy of the system, we can just iterate on the simulation objects, there is no need
    // to take into consideration mappings
    auto accumulatedEnergy = Scalar{0};
    utilities::static_for_each(
        [&accumulatedEnergy, h](const auto &simulationObjects) {
            for (const auto &simulationObject : simulationObjects) {
                accumulatedEnergy += ::computeEnergy(simulationObject, h);
            }
        },
        m_simulationObjects);

    return accumulatedEnergy;
}

Scalar Model::computeEnergyAndGradient(Scalar h, Vec &gradient)
{
    ZoneScopedN("Model.computeEnergyAndGradient");
    // First we need to compute the gradient for each SimulationObject
    auto accumulatedEnergy = Scalar{0};
    utilities::static_for_each(
        [&accumulatedEnergy, h](auto &simulationObjects) {
            for (auto &simulationObject : simulationObjects) {
                using SimulationObjectT = std::remove_cvref_t<decltype(simulationObject)>;
                if constexpr (SimulationObjectT::hasPotentials || SimulationObjectT::hasInertias) {
                    simulationObject.mstate.clearGradient();
                }

                accumulatedEnergy += ::computeEnergyAndGradient(simulationObject, h);
            }
        },
        m_simulationObjects);

    // Propagate the forces back to the free simulation objects
    for (auto node : m_backwardSortedList) {
        auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this](const auto handle) {
                const auto &simulationObject = this->simulationObject(handle);
                using SimulationObjectT = std::remove_pointer_t<std::remove_cvref_t<decltype(simulationObject)>>;
                if constexpr (SimulationObjectT::hasMappings) {
                    utilities::static_for_each(
                        [this](const auto &mappings) {
                            for (const auto &mapping : mappings) {
                                auto fromHandle = mapping.from();
                                auto toHandle = mapping.to();

                                auto &from = this->simulationObject(fromHandle);
                                auto &to = this->simulationObject(toHandle);

                                mapping.applyJT(from.mstate.m_grad, to.mstate.m_grad);
                            }
                        },
                        simulationObject.m_mappings);
                }
            },
            simObjectV);
    }

    // And accumulate on the generalized gradient
    auto offset = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &gradient, &offset](auto handle) {
                auto &simulationObject = this->simulationObject(handle);
                const auto size = simulationObject.mstate.size();
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                if constexpr (SimulationObjectT::hasProjections) {
                    mandos::core::utilities::static_for_each(
                        [&simulationObject](const auto &projection) {
                            projection.applyPT(simulationObject.mstate.gradientView());
                        },
                        simulationObject.projections);
                }
                simulationObject.mstate.gradient(gradient.segment(offset, size));
                offset += size;
            },
            simObjectV);
    }

    return accumulatedEnergy;
}

Scalar Model::computeEnergyGradientAndHessian(Scalar h, Vec &gradient, SystemMatrix &hessian)
{
    ZoneScopedN("Model.computeEnergyGradientAndHessian");
    // // First we need to compute the gradient and hessian for each SimulationObject
    auto accumulatedEnergy{Scalar{0}};
    utilities::static_for_each(
        [&accumulatedEnergy, h](auto &simulationObjects) {
            for (auto &simulationObject : simulationObjects) {
                using SimulationObjectT = std::remove_cvref_t<decltype(simulationObject)>;
                if constexpr (SimulationObjectT::hasPotentials || SimulationObjectT::hasInertias) {
                    simulationObject.mstate.clearGradient();
                    simulationObject.mstate.clearHessian();
                }

                // This is a big hack because MSVC fails to compile if using a lambda here
                accumulatedEnergy += ::computeEnergyGradientAndHessian(simulationObject, h);
            }
        },
        m_simulationObjects);

    // Propagate the forces back to the free simulation objects
    for (auto node : m_backwardSortedList) {
        auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this](auto handle) {
                const auto &simulationObject = this->simulationObject(handle);
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                if constexpr (SimulationObjectT::hasMappings) {
                    utilities::static_for_each(
                        [this](const auto &mappings) {
                            for (const auto &mapping : mappings) {
                                const auto fromHandle = mapping.from();
                                const auto toHandle = mapping.to();

                                auto &from = this->simulationObject(fromHandle);
                                auto &to = this->simulationObject(toHandle);

                                mapping.applyJT(from.mstate.m_grad, to.mstate.m_grad);
                            }
                        },
                        simulationObject.m_mappings);
                }
            },
            simObjectV);
    }

    // And accumulate on the generalized gradient
    auto offset = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &gradient, &offset](auto handle) {
                auto &simulationObject = this->simulationObject(handle);
                const auto size = simulationObject.mstate.size();
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                if constexpr (SimulationObjectT::hasProjections) {
                    mandos::core::utilities::static_for_each(
                        [&simulationObject](const auto &projection) {
                            projection.applyPT(simulationObject.mstate.gradientView());
                        },
                        simulationObject.projections);
                }
                simulationObject.mstate.gradient(gradient.segment(offset, size));
                offset += size;
            },
            simObjectV);
    }

    hessian.setModel(*this);
    hessian.setBackwardSortedList(m_backwardSortedList);
    hessian.setForwardSortedList(m_forwardSortedList);
    hessian.setFreeSimulationObject(m_freeSimulationObjects);

    return accumulatedEnergy;
}

int Model::nDof() const
{
    ZoneScopedN("Model.nDof");
    // Only compute actual DoFs
    int nDof = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &nDof](const auto handle) {
                const auto &simulationObject = this->simulationObject(handle);
                nDof += simulationObject.mstate.size();
            },
            simObjectV);
    }

    return nDof;
}

void Model::state(Vec &x, Vec &v) const
{
    ZoneScopedN("Model.state");
    // Set the state of the free SimulationObjects
    int offset = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &offset, &x, &v](auto handle) {
                auto &simulationObject = this->simulationObject(handle);
                const auto size = simulationObject.mstate.size();
                simulationObject.mstate.state(x.segment(offset, size), v.segment(offset, size));
                offset += size;
            },
            simObjectV);
    }
}

void Model::setState(const Vec &x, const Vec &v)
{
    ZoneScopedN("Model.setState");

    {
        ZoneScopedN("Model.setState.setZero");
        // First, set the state to 0 of all the objects, so we can later accumulate through mappings
        utilities::static_for_each(
            [](auto &simulationObjects) {
                for (auto &simulationObject : simulationObjects) {
                    simulationObject.mstate.setZero();
                }
            },
            m_simulationObjects);
    }

    // Set the state of the free SimulationObjects
    {
        ZoneScopedN("Model.setState.setState");
        int offset = 0;
        for (auto node : m_freeSimulationObjects) {
            auto &simObjectV = m_simulationObjectsGraph[node];
            std::visit(
                [this, &offset, &x, &v](auto handle) {
                    auto &simulationObject = this->simulationObject(handle);
                    const auto size = simulationObject.mstate.size();
                    simulationObject.mstate.setState(x.segment(offset, size), v.segment(offset, size));
                    offset += size;
                },
                simObjectV);
        }
    }

    {
        ZoneScopedN("Model.setState.apply/J");
        for (auto node : m_forwardSortedList) {
            const auto &simObjectV = m_simulationObjectsGraph[node];
            std::visit(
                [this](auto handle) {
                    const auto simulationObject = this->simulationObject(handle);
                    using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                    if constexpr (SimulationObjectT::hasMappings) {
                        utilities::static_for_each(
                            [this, &simulationObject](const auto &mappings) {
                                for (const auto &mapping : mappings) {
                                    auto toHandle = mapping.to();
                                    auto &to = this->simulationObject(toHandle);

                                    mapping.apply(simulationObject.mstate.m_x, to.mstate.m_x);
                                    mapping.applyJ(simulationObject.mstate.m_v, to.mstate.m_v);
                                }
                            },
                            simulationObject.m_mappings);
                    }
                },
                simObjectV);
        }
    }
}

void Model::updateState(const Vec &dx, const Vec &x0, const Vec &v0, Scalar h)
{
    ZoneScopedN("Model.updateState");
    // First, reset the state of all the mapped objects, so we can later accumulate through mappings
    for (auto node : m_forwardSortedList) {
        if (std::find(std::begin(m_freeSimulationObjects), std::end(m_freeSimulationObjects), node) ==
            std::end(m_freeSimulationObjects)) {
            std::visit(
                [this](auto handle) {
                    auto &simulationObject = this->simulationObject(handle);
                    simulationObject.mstate.setZero();
                },
                m_simulationObjectsGraph[node]);
        }
    }

    // First, update the state of the free objects
    int offset = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &offset, &dx, &x0, &v0, h](auto handle) {
                auto &simulationObject = this->simulationObject(handle);
                const auto size = simulationObject.mstate.size();
                simulationObject.mstate.updateState(
                    dx.segment(offset, size), x0.segment(offset, size), v0.segment(offset, size), h);
                offset += size;
            },
            simObjectV);
    }

    // And propagate the state from the free Simulation Objects to the mapped ones
    for (auto node : m_forwardSortedList) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this](const auto &handle) {
                const auto &simulationObject = this->simulationObject(handle);
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                if constexpr (SimulationObjectT::hasMappings) {
                    utilities::static_for_each(
                        [this, &simulationObject](const auto &mappings) {
                            for (const auto &mapping : mappings) {
                                auto toHandle = mapping.to();
                                auto &to = this->simulationObject(toHandle);

                                mapping.apply(simulationObject.mstate.m_x, to.mstate.m_x);
                                mapping.applyJ(simulationObject.mstate.m_v, to.mstate.m_v);
                            }
                        },
                        simulationObject.m_mappings);
                }
            },
            simObjectV);
    }
}

const Model::KinematicGraph &Model::graph() const
{
    return m_simulationObjectsGraph;
}

Model::KinematicGraph &Model::graph()
{
    return m_simulationObjectsGraph;
}

void Model::updateColliders()
{
    utilities::static_for_each(
        [](auto &simulationObjects) {
            for (auto &simulationObject : simulationObjects) {
                using SimulationObjectT = std::remove_cvref_t<decltype(simulationObject)>;
                if constexpr (SimulationObjectT::hasColliders) {
                    utilities::static_for_each(
                        [&simulationObject](auto &colliders) {
                            for (auto &collider : colliders) {
                                collider.update(simulationObject.mstate);
                            }
                        },
                        simulationObject.colliders());
                }
            }
        },
        m_simulationObjects);
}

const std::vector<Model::KinematicGraph::vertex_descriptor> &Model::freeSimulationObjects() const
{
    return m_freeSimulationObjects;
}

void Model::detectCollisions()
{
    utilities::static_for_each(
        [](auto &collisionPairs) {
            for (auto &collisionPair : collisionPairs) {
                const auto &c0 = collisionPair.c0SimulationCollider;
                const auto &c1 = collisionPair.c1SimulationCollider;

                const auto &c0Collider = c0.collider();
                const auto &c1Collider = c1.collider();

                const auto &contactEvents = collisions::collisions(c0Collider, c1Collider);
                const auto nParticles = 2 * contactEvents.size();

                auto &collisionState = collisionPair.collisionState().mstate;
                collisionState.m_x.resize(static_cast<std::size_t>(nParticles));
                collisionState.m_v.resize(static_cast<std::size_t>(nParticles));
                collisionState.m_grad.resize(static_cast<std::size_t>(nParticles));
                collisionState.m_hessian.resize(3 * static_cast<Eigen::Index>(nParticles),
                                                3 * static_cast<Eigen::Index>(nParticles));

                using SimulationObject0Tag = std::remove_cvref_t<decltype(c0.simulationObject())>::SimulationObjectTag;
                using SimulationObject1Tag = std::remove_cvref_t<decltype(c1.simulationObject())>::SimulationObjectTag;

                using Collider0T = std::remove_cvref_t<decltype(c0Collider)>;
                using Collider1T = std::remove_cvref_t<decltype(c1Collider)>;

                auto &mapping0 =
                    collisionPair.c0SimulationCollider.simulationObject()
                        .template mappings<collisions::CollisionMapping<SimulationObject0Tag, Collider0T>>()
                            [static_cast<std::size_t>(collisionPair.mappingIndex0)];

                auto &simObject1 = collisionPair.c1SimulationCollider.simulationObject();
                auto &mapping1 =
                    simObject1.template mappings<collisions::CollisionMapping<SimulationObject1Tag, Collider1T>>()
                        [static_cast<std::size_t>(collisionPair.mappingIndex1)];

                mapping0.resize(static_cast<int>(contactEvents.size()));
                mapping1.resize(static_cast<int>(contactEvents.size()));
                auto &collisionSpringEnergy = collisionPair.collisionState().template potential<CollisionSpring>();
                collisionSpringEnergy.clear();
                for (auto cId = 0UL; cId < contactEvents.size(); ++cId) {
                    const auto &contact = contactEvents[cId];
                    collisions::updateMapping(contact.c0Contact, mapping0, static_cast<int>(cId));
                    collisions::updateMapping(
                        contact.c1Contact, mapping1, static_cast<int>(contactEvents.size() + cId));

                    collisionSpringEnergy.addElement(collisionPair.stiffness, collisionPair.threshold, contact.normal);
                }

                collisionState.setZero();
                mapping0.apply(c0.simulationObject().mstate.m_x, collisionState.m_x);
                mapping1.apply(c1.simulationObject().mstate.m_x, collisionState.m_x);
            }
        },
        m_collisionPairs);
}

void Model::commit()
{
    ZoneScopedN("Model.commit");

    // Clear edges
    for (const auto &node : boost::make_iterator_range(boost::vertices(m_simulationObjectsGraph))) {
        // The namemight be tricky, but this is removing all the edges of the node
        boost::clear_vertex(node, m_simulationObjectsGraph);
    }

    std::unordered_map<const void *, KinematicGraph::vertex_descriptor> vertexMap;

    // First create a map from the actual SimulationObject to the vertex_descriptor in the graph
    for (const auto &node : boost::make_iterator_range(boost::vertices(m_simulationObjectsGraph))) {
        std::visit(
            [node, &vertexMap](auto handle) {
                auto &simulationObject = handle.simulationObject();
                vertexMap.insert({&simulationObject, node});
            },
            m_simulationObjectsGraph[node]);
    }

    utilities::static_for_each(
        [this, &vertexMap](auto &simulationObjects) {
            for (auto &simulationObject : simulationObjects) {
                using SimulationObjectT = typename std::remove_cvref_t<decltype(simulationObject)>;
                if constexpr (SimulationObjectT::hasMappings) {
                    utilities::static_for_each(
                        [this, &vertexMap](const auto &mappings) {
                            for (const auto &mapping : mappings) {
                                auto fromHandle = mapping.from();
                                auto toHandle = mapping.to();

                                void *from = std::addressof(this->simulationObject(fromHandle));
                                void *to = std::addressof(this->simulationObject(toHandle));

                                boost::add_edge(vertexMap.at(from), vertexMap.at(to), m_simulationObjectsGraph);
                            }
                        },
                        simulationObject.m_mappings);
                }
            }
        },
        m_simulationObjects);

    // Get the SimulationObject nodes without an input edge
    m_freeSimulationObjects.clear();
    for (const auto &node : boost::make_iterator_range(boost::vertices(m_simulationObjectsGraph))) {
        if (boost::in_degree(node, m_simulationObjectsGraph) == 0) {
            m_freeSimulationObjects.push_back(node);
        }
    }

    m_forwardSortedList.clear();
    m_backwardSortedList.clear();

    m_forwardSortedList.reserve(boost::num_vertices(m_simulationObjectsGraph));
    m_backwardSortedList.reserve(boost::num_vertices(m_simulationObjectsGraph));

    auto reverseGraph = boost::make_reverse_graph(m_simulationObjectsGraph);

    // This might look strange.
    // According to BGL documentation, they output the data in reverse order, so we need to reverse
    std::vector<KinematicGraph::vertex_descriptor> sortedList;
    sortedList.reserve(boost::num_vertices(m_simulationObjectsGraph));

    boost::topological_sort(m_simulationObjectsGraph, std::back_inserter(sortedList));
    std::reverse_copy(std::begin(sortedList), std::end(sortedList), std::back_inserter(m_forwardSortedList));

    sortedList.clear();
    boost::topological_sort(reverseGraph, std::back_inserter(sortedList));
    std::reverse_copy(std::begin(sortedList), std::end(sortedList), std::back_inserter(m_backwardSortedList));

    // Initializing mappings this way might be a bit inneficient, but it avoid having to duplicate code, and its not a
    // hot path
    auto n = this->nDof();
    Vec x(n);
    Vec v(n);
    state(x, v);
    setState(x, v);

    // Initialize energies if needed
    utilities::static_for_each(
        [](auto &simulationObjects) {
            for (auto &simulationObject : simulationObjects) {
                using SimulationObjectT = typename std::remove_cvref_t<decltype(simulationObject)>;
                if constexpr (SimulationObjectT::hasPotentials) {
                    utilities::static_for_each(
                        [&simulationObject](auto &potential) {
                            using ::initialize;

                            // Called by ADL if initialize function is found for the particular potential type
                            // Otherwise, noop
                            initialize(potential, simulationObject.mstate);
                        },
                        simulationObject.m_potentials);
                }
            }
        },
        m_simulationObjects);
}

void Model::computeEnergyRetardedPositionHessian(Scalar h, SparseMat &hessian)
{
    ZoneScopedN("Model.computeEnergyRetardedPositionHessian");
    std::vector<Triplet> triplets;
    // // We compute the retarded position hessian for each simulation object with inertia
    // Only compute free objects
    unsigned int offset = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &offset, &triplets, h](auto &handle) {
                auto &simulationObject = this->simulationObject(handle);
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                const auto size = simulationObject.mstate.size();
                if constexpr (SimulationObjectT::hasInertias) {
                    utilities::static_for_each(
                        [&simulationObject, h, offset, &triplets](auto &inertia) {
                            inertia.computeEnergyRetardedPositionHessian(simulationObject.mstate, h, offset, triplets);
                        },
                        simulationObject.inertias());
                }
                offset += static_cast<unsigned int>(size);
            },
            simObjectV);
    }
    hessian.setFromTriplets(triplets.begin(), triplets.end());
}

void Model::computeEnergyRetardedVelocityHessian(Scalar h, SparseMat &hessian)
{
    ZoneScopedN("Model.computeEnergyRetardedVelocityHessian");
    // // We compute the retarded position hessian for each simulation object with inertia
    std::vector<Triplet> triplets;
    // Only compute free objects
    unsigned int offset = 0;
    for (auto node : m_freeSimulationObjects) {
        const auto &simObjectV = m_simulationObjectsGraph[node];
        std::visit(
            [this, &offset, &triplets, h](auto &handle) {
                auto &simulationObject = this->simulationObject(handle);
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                const auto size = simulationObject.mstate.size();
                if constexpr (SimulationObjectT::hasInertias) {
                    utilities::static_for_each(
                        [&simulationObject, h, offset, &triplets](auto &inertia) {
                            inertia.computeEnergyRetardedVelocityHessian(simulationObject.mstate, h, offset, triplets);
                        },
                        simulationObject.inertias());
                }
                offset += static_cast<unsigned int>(size);
            },
            simObjectV);
    }
    hessian.setFromTriplets(triplets.begin(), triplets.end());
}
}  // namespace mandos::core
