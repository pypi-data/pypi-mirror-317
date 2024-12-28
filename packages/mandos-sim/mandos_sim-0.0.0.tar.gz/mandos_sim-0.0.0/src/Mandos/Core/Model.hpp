#ifndef MANDOS_MODEL_HPP
#define MANDOS_MODEL_HPP

#include <tuple>
#include <vector>

#include <Mandos/Core/KinematicGraph.hpp>
#include <Mandos/Core/SimulationObject.hpp>
#include <Mandos/Core/SimulationObjectHandle.hpp>

#include <Mandos/Core/utility_functions.hpp>

#include "Mandos/Core/Collisions/CollisionPair.hpp"
#include "Mandos/Core/Collisions/SimulationCollider.hpp"
#include "Mandos/Core/Mappings/BarycentricMapping.hpp"
#include "Mandos/Core/MechanicalStates/Particle3D.hpp"
#include "Mandos/Core/MechanicalStates/RigidBody.hpp"
#include <Mandos/Core/Mappings/CollisionMapping.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

struct SystemMatrix;

/**
 * @brief The Model represents the simulation model we want to simulate
 * It is made of all the SimulationObjects<> and all the Couplings<> between them
 *
 * A Model has several objects, with different mechanical states, but only some of those mechanical states are actually
 * degrees of freedom. The Model provides convenience functions to retrieve and set its generalized coordinates. This
 * functions traverse the mappings tree, getting or setting the state values as appropiate.
 *
 * [!WARNING] Fetching the MechanicalState directly from any SimulationObject is supported, but modifying it is
 * undefined behavior.
 *
 */
class MANDOS_CORE_EXPORT Model
{
public:
    /**
     * @brief A compile time list of supported SimulationObjects
     *
     */

    using SimulationObjects = mandos::core::SimulationObjects;

    using KinematicGraph = mandos::core::KinematicGraph;

    Model() = default;
    Model(const Model &other) = delete;
    Model(Model &&other) = default;
    Model &operator=(const Model &other) = delete;
    Model &operator=(Model &&other) = default;

    /**
     * @brief A compile time list of supported Projections
     *
     */
    using Projections = utilities::typelist<FixedProjection>;

    /**
     * @brief A compile time list of supported Mappings
     *
     */
    using Mappings = utilities::typelist<IdentityMapping, BarycentricMapping>;

    /**
     * @brief Accessor to the simulation objects of type SimulationObjectT.
     * Note that taking a reference to current simulation objects is not valid, as adding new object may reallocate and
     * invalid any current reference
     *
     * @tparam SimulationObjectT
     * @return const std::vector<SimulationObjectT>&
     */
    template <typename Tag>
    std::vector<SimulationObject<Tag>> &simulationObjects()
    {
        return std::get<std::vector<SimulationObject<Tag>>>(m_simulationObjects);
    }

    /**
     * @brief Accessor to the simulation objects of type SimulationObjectT.
     * Note that taking a reference to current simulation objects is not valid, as adding new object may reallocate and
     * invalid any current reference
     *
     * @tparam SimulationObjectT
     * @return const std::vector<SimulationObjectT>&
     */
    template <typename Tag>
    const std::vector<SimulationObject<Tag>> &simulationObjects() const
    {
        return std::get<std::vector<SimulationObject<Tag>>>(m_simulationObjects);
    }

    template <typename Tag>
    SimulationObject<Tag> &simulationObject(SimulationObjectHandle<Tag> handle)
    {
        return handle.simulationObject();
    }

    template <typename Tag>
    const SimulationObject<Tag> &simulationObject(SimulationObjectHandle<Tag> handle) const
    {
        return handle.simulationObject();
    }

    /**
     * @brief Add a simulation object of type SimulationObject<Tag> to the model
     *
     * @tparam Tag
     */
    template <typename Tag>
    SimulationObjectHandle<Tag> add()
    {
        // get the vector holding this types of SimulationObject<Tag>
        auto &v = std::get<std::vector<SimulationObject<Tag>>>(m_simulationObjects);

        // Emplace a new object
        v.emplace_back();

        // Create a handle for this object
        SimulationObjectHandle<Tag> handle(v.size() - 1, simulationObjects<Tag>());

        // Add the handle to the graph
        boost::add_vertex(handle, m_simulationObjectsGraph);

        // return the handle
        return handle;
    }

    template <typename MappingT, typename FromT, typename ToT>
    int addMapping(SimulationObjectHandle<FromT> fromHandle, SimulationObjectHandle<ToT> toHandle)
    {
        fromHandle.simulationObject().template mappings<MappingT>().emplace_back(fromHandle, toHandle);
        return static_cast<int>(fromHandle.simulationObject().template mappings<MappingT>().size()) - 1;
    }

    template <typename SimulationColliderT0, typename SimulationColliderT1>
    SimulationObjectHandle<Particle3DTag> addCollisionPair(SimulationColliderT0 c0,
                                                           SimulationColliderT1 c1,
                                                           Scalar stiffness,
                                                           Scalar threshold)
    {
        auto collisionParticlesHandle = this->add<Particle3DTag>();
        auto &collisionPair =
            std::get<std::vector<collisions::CollisionPair<SimulationColliderT0, SimulationColliderT1>>>(
                m_collisionPairs)
                .emplace_back(collisionParticlesHandle, c0, c1);

        const int indexMapping0 =
            this->addMapping<collisions::CollisionMapping<RigidBodyTag, collisions::SDF>, RigidBodyTag, Particle3DTag>(
                collisionPair.c0SimulationCollider.handle(), collisionPair.collisionParticlesHandle);

        const int indexMapping1 = this->addMapping<collisions::CollisionMapping<Particle3DTag, collisions::SphereCloud>,
                                                   Particle3DTag,
                                                   Particle3DTag>(collisionPair.c1SimulationCollider.handle(),
                                                                  collisionPair.collisionParticlesHandle);

        collisionPair.mappingIndex0 = indexMapping0;
        collisionPair.mappingIndex1 = indexMapping1;
        collisionPair.stiffness = stiffness;
        collisionPair.threshold = threshold;

        return collisionParticlesHandle;
    }

    /**
     * @brief Initializes the structures for simulating the current Model.

     * - Constructs a DAG using the SimulationObjects and the Mapping to ensure the correct iteration order
     * - Initializes the mappings by calling apply and applyJ with the current state of the free simulation object
     * - Initializes energies for proper parallelization if needed
     *
     * The function must be called if there is any modification to the simulation model that needs to reinitialize, like
     for example changing the mapping graph or adding new elements to parallel energies
     */
    void commit();

    void computeAdvection(Scalar h);

    /**
     * @brief Computes the amount of degrees of freedom the model  has
     *
     * [!NOTE] Some SimulationObjects may have some or all of their variables mapped, and they don't count as part of
     * the generalized degrees of freedom of the Model
     *
     * @return int
     */
    [[nodiscard]] int nDof() const;

    /**
     * @brief Computes the generalized coordinates of the simulation Model
     *
     * @param x Where to store the x generalized state.
     * [!WARNING] We dont perform bound checks, so ensure the size of x matches the nDof of the Model
     * @param v Where to store the v generalized state.
     * [!WARNING] We dont perform bound checks, so ensure the size of x matches the nDof of the Model
     */
    void state(Vec &x, Vec &v) const;

    /**
     * @brief Set the MechanicalState of the model. This triggers the update of all the mappings in the model, updating
     * the MechanicalState of each SimulationObject.
     *
     * @param x The x generalized state
     * @param v The v generalized state
     */
    void setState(const Vec &x, const Vec &v);

    /**
     * @brief Given a finite perturbation dx, update the MechanicalStates of the model. This triggers the update of all
     * the mappings in the model, updating the MechanicalState of each SimulationObject.
     *
     * @param dx The generalized perturbation vector
     * @param x0 The generalized x vector from where to apply the perturbation
     * @param v0 The generalized v vector from where to apply the perturbation
     */
    void updateState(const Vec &dx, const Vec &x0, const Vec &v0, Scalar h);

    /**
     * @brief Computes the energy of the simulation model on a given time span
     * The energy includes the kinetic energy and the potential energy
     *
     * @param model Simulation model
     * @param h Span of time to compute the energy model
     * @return Scalar The internal energy of the system
     */
    [[nodiscard]] Scalar computeEnergy(Scalar h) const;

    /**
     * @brief Computes the energy and its derivatives wrt x

     * [!NOTE] This function clears the current gradient from each SimulationObject and overrides with the result in the
     current configuration state
     *
     * @param model The simulation model
     * @param h Span of time to compute the energy model
     * @param gradient The derivatives of the energy wrt x
     * @return Scalar The internal energy of the system
     */
    Scalar computeEnergyAndGradient(Scalar h, Vec &gradient);

    /**
     * @brief Computes the energy, its derivatives and second order derivatives wrt x

     * [!NOTE] This function clears the current gradient and hessian from each SimulationObject and overrides with the
     result computed using the current configuration state
     *
     * @param model The simulation model
     * @param h Span of time to compute the energy model
     * @param gradient The derivatives of the energy wrt x
     * @param hessian The second derivatives of the energy wrt x
     * @return Scalar The internal energy of the system
     */
    Scalar computeEnergyGradientAndHessian(Scalar h, Vec &gradient, SystemMatrix &hessian);

    /**
     * @brief Computes the derivative of the energy gradient wrt the previous positions x0

     * [!NOTE] The only energies that depend on previous positions are the ones that depend on velocities. This includes
     inertia energies and dissipative or damping potentials.
     * [!NOTE] This function is needed exclusively for differentiability. It is necessary to compute how does the state
     after taking one simulation step changes if we change the previous positions x0.
     * [!NOTE] This function at the moment does not support mapped objects and will only work for free simulation
     objects

     * @param model The simulation model
     * @param h Span of time to compute the energy model
     * @param hessian The derivative of the energy gradient wrt x0
     */
    void computeEnergyRetardedPositionHessian(Scalar h, SparseMat &hessian);

    /**
     * @brief Computes the derivative of the energy gradient wrt the previous velocities v0

     * [!NOTE] The only energies that depend on previous velocities are the ones that depend on acceleration. This means
     that only affects inertial energies.
     * [!NOTE] This function is needed exclusively for differentiability. It is necessary to compute how does the state
     after taking one simulation step changes if we change the previous velocity v0.
     * [!NOTE] This function at the moment does not support mapped objects and will only work for free simulation
     objects

     * @param model The simulation model
     * @param h Span of time to compute the energy model
     * @param hessian The derivative of the energy gradient wrt v0
     */
    void computeEnergyRetardedVelocityHessian(Scalar h, SparseMat &hessian);

    void updateColliders();
    void detectCollisions();
    void updateCollisionMappings();

    KinematicGraph &graph();

    const std::vector<KinematicGraph::vertex_descriptor> &freeSimulationObjects() const;

    const KinematicGraph &graph() const;

private:
    /**
     * @brief The SimulationObjects that define the Model
     *
     * This is the direct accessor to the Simulation Objects in the model
     */
    SimulationObjects::map<std::vector>::as<std::tuple> m_simulationObjects;

    /**
     * @brief A graph containing references to the SimulationObject as nodes and edges representing the mappings
     *
     */
    KinematicGraph m_simulationObjectsGraph;

    std::vector<KinematicGraph::vertex_descriptor> m_freeSimulationObjects;

    /**
     * @brief A sorted list of the SimulationObject graph. It is used to propagate the state through the mappings in
     * order
     *
     */
    std::vector<KinematicGraph::vertex_descriptor> m_forwardSortedList;

    /**
     * @brief A sorted list of the reversed SimulationObjects graph. Is is used to propagate forces through the mappings
     * in order
     *
     */
    std::vector<KinematicGraph::vertex_descriptor> m_backwardSortedList;

    std::tuple<
        std::vector<collisions::CollisionPair<collisions::SimulationCollider<RigidBodyTag, collisions::SDF>,
                                              collisions::SimulationCollider<Particle3DTag, collisions::SphereCloud>>>>
        m_collisionPairs;
};

}  // namespace mandos::core

#endif  // MANDOS_MODEL_HPP
