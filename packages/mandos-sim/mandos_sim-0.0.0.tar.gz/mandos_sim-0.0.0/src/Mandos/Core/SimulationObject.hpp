#ifndef EA5CC9BC_9B26_421C_B4CB_4E265608D7F2
#define EA5CC9BC_9B26_421C_B4CB_4E265608D7F2

#include <Mandos/Core/Energies.hpp>
#include <Mandos/Core/Mappings.hpp>
#include <Mandos/Core/MechanicalState.hpp>
#include <Mandos/Core/Projections.hpp>
#include <Mandos/Core/Colliders.hpp>

#include <type_traits>

namespace mandos::core
{
/**
 * @brief The SimulationObject represents a mechanical object that can be simulated using Mandos.
 * It is composed of its configuration space, represented by the mechanical state, its energies, its mappings and its
 * projections
 *
 * @tparam Tag
 * Specifies the type of this SimulationObject and therefore, the type of mechanical state, energies, mappings and
 * projections it has.
 */
template <typename Tag>
struct SimulationObject : Inertias<Tag>, Potentials<Tag>, Projections<Tag>, Mappings<Tag>, Colliders<Tag> {
    using SimulationObjectTag = Tag;

    static constexpr bool hasInertias = !std::is_empty_v<Inertias<Tag>>;
    static constexpr bool hasPotentials = !std::is_empty_v<Potentials<Tag>>;
    static constexpr bool hasProjections = !std::is_empty_v<Projections<Tag>>;
    static constexpr bool hasMappings = !std::is_empty_v<Mappings<Tag>>;
    static constexpr bool hasColliders = !std::is_empty_v<Colliders<Tag>>;

    template <typename EnergyT>
    [[nodiscard]] EnergyT &potential()
    {
        static_assert(hasPotentials,
                      "Trying to get a potential energy from a SimulationObject without potential energies");
        return std::get<EnergyT>(this->m_potentials);
    }

    template <typename EnergyT>
    [[nodiscard]] const EnergyT &potential() const
    {
        static_assert(hasPotentials,
                      "Trying to get a potential energy from a SimulationObject without potential energies");
        return std::get<EnergyT>(this->m_potentials);
    }

    template <typename EnergyT>
    [[nodiscard]] EnergyT &inertia()
    {
        static_assert(hasInertias,
                      "Trying to get an inertial energy from a SimulationObject without inertial energies");
        return std::get<EnergyT>(this->inertias());
    }

    template <typename EnergyT>
    [[nodiscard]] const EnergyT &inertia() const
    {
        static_assert(hasInertias,
                      "Trying to get an inertial energy from a SimulationObject without inertial energies");
        return std::get<EnergyT>(this->inertias());
    }

    template <typename MappingT>
    int addMapping(typename MappingT::To &to)
    {
        static_assert(hasMappings, "Trying to add a Mapping to a SimulationObject without mappings");
        std::get<std::vector<MappingT>>(this->m_mappings).emplace_back(*this, to);
        return static_cast<int>(std::get<std::vector<MappingT>>(this->m_mappings).size()) - 1;
    }

    template <typename MappingT>
    std::vector<MappingT> &mappings()
    {
        static_assert(hasMappings, "Trying to get a Mapping from a SimulationObject without mappings");
        return std::get<std::vector<MappingT>>(this->m_mappings);
    }

    template <typename MappingT>
    const std::vector<MappingT> &mappings() const
    {
        static_assert(hasMappings, "Trying to get a Mapping from a SimulationObject without mappings");
        return std::get<std::vector<MappingT>>(this->m_mappings);
    }

    auto &potentials()
    {
        static_assert(hasPotentials,
                      "Trying to get potential energies from a SimulationObject without potential energies");
        return this->m_potentials;
    }

    const auto &potentials() const
    {
        static_assert(hasPotentials,
                      "Trying to get potential energies from a SimulationObject without potential energies");
        return this->m_potentials;
    }

    auto &inertias()
    {
        static_assert(hasInertias, "Trying to get inertial energies from a SimulationObject without inertial energies");
        return this->m_inertias;
    }

    const auto &inertias() const
    {
        static_assert(hasInertias, "Trying to get inertial energies from a SimulationObject without inertial energies");
        return this->m_inertias;
    }

    auto &colliders()
    {
        static_assert(hasColliders, "Trying to get colliders from a SimulationObject without colliders");
        return this->m_colliders;
    }

    const auto &colliders() const
    {
        static_assert(hasColliders, "Trying to get colliders from a SimulationObject without colliders");
        return this->m_colliders;
    }

    /**
     * @brief The current mechanical state of the SimulationObject
     *
     */
    MechanicalState<Tag> mstate;
};

}  // namespace mandos::core

#endif /* EA5CC9BC_9B26_421C_B4CB_4E265608D7F2 */
