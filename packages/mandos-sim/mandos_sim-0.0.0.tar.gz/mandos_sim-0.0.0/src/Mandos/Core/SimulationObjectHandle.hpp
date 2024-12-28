#ifndef MANDOS_CORE_SIMULATIONOBJECTHANDLE_HPP
#define MANDOS_CORE_SIMULATIONOBJECTHANDLE_HPP

#include <cstddef>
#include <limits>
#include <vector>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

class Model;

template <typename Tag>
struct SimulationObject;

template <typename Tag>
struct SimulationObjectHandle {
    SimulationObjectHandle() = default;

    SimulationObjectHandle(std::size_t index, std::vector<SimulationObject<Tag>> &simulationObjects)
        : m_index(index)
        , m_simulationObjects(&simulationObjects)
    {
    }

    MANDOS_CORE_EXPORT SimulationObject<Tag> *operator->() const
    {
        return &(*m_simulationObjects)[m_index];
    }

    MANDOS_CORE_EXPORT SimulationObject<Tag> &simulationObject() const
    {
        return (*m_simulationObjects)[m_index];
    }

private:
    std::size_t m_index = std::numeric_limits<std::size_t>::max();
    std::vector<SimulationObject<Tag>> *m_simulationObjects{nullptr};
};

template <typename SimulationObjectT>
using SimulationObjectHandle_t = SimulationObjectHandle<typename SimulationObjectT::SimulationObjectTag>;

}  // namespace mandos::core

#endif  // MANDOS_CORE_SIMULATIONOBJECTHANDLE_HPP