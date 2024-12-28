#ifndef MANDOS_CORE_COLLISIONS_SIMULATIONCOLLIDER_H
#define MANDOS_CORE_COLLISIONS_SIMULATIONCOLLIDER_H

#include <Mandos/Core/KinematicGraph.hpp>

namespace mandos::core::collisions
{

template <typename Tag, typename ColliderT>
struct SimulationCollider {
    SimulationCollider() = default;
    SimulationCollider(SimulationObjectHandle<Tag> handle, int colliderIndex)
        : m_handle(handle)
        , m_colliderIndex(colliderIndex)
    {
    }

    SimulationObject<Tag> &simulationObject()
    {
        return m_handle.simulationObject();
    }

    const SimulationObject<Tag> &simulationObject() const
    {
        return m_handle.simulationObject();
    }

    SimulationObjectHandle<Tag> handle()
    {
        return m_handle;
    }

    ColliderT &collider()
    {
        auto &simObject = simulationObject();
        auto &colliders = std::get<std::vector<ColliderT>>(simObject.colliders());
        return colliders[static_cast<std::size_t>(m_colliderIndex)];
    }

    const ColliderT &collider() const
    {
        const auto &simObject = simulationObject();
        const auto &colliders = std::get<std::vector<ColliderT>>(simObject.colliders());
        return colliders[static_cast<std::size_t>(m_colliderIndex)];
    }

private:
    SimulationObjectHandle<Tag> m_handle;
    int m_colliderIndex{-1};
};

}  // namespace mandos::core::collisions

#endif  //  MANDOS_CORE_COLLISIONS_SIMULATIONCOLLIDER_H