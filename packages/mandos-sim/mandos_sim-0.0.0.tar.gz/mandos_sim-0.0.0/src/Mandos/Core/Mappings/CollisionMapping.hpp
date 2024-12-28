#ifndef MANDOS_MAPPINGS_COLLISIONMAPPING_H
#define MANDOS_MAPPINGS_COLLISIONMAPPING_H

#include <vector>

#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/Collisions/ContactEvent.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/Energies/RigidBodyInertia.hpp>

#include <Mandos/Core/Collisions/SphereCloud.hpp>
#include <Mandos/Core/Collisions/SDF.hpp>
#include "Mandos/Core/MechanicalState.hpp"
#include "Mandos/Core/SimulationObjectHandle.hpp"

#include <Eigen/src/Core/util/Constants.h>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{
template <typename MechanicalStateT>
struct SimulationObject;

namespace collisions
{

template <typename FromT, typename ColliderT>
struct MappingInfo {
};

template <>
struct MappingInfo<Particle3DTag, SphereCloud> {
    void apply(const std::vector<Vec3> &from, std::vector<Vec3> &to) const;

    void applyJ(const std::vector<Vec3> &from, std::vector<Vec3> &to) const;

    void applyJT(std::vector<Vec3> &from, const std::vector<Vec3> &to) const;

    std::size_t m_fromId;
    std::size_t m_toId;
};

template <>
struct MappingInfo<RigidBodyTag, SDF> {
    void apply(const std::vector<Vec6> &from, std::vector<Vec3> &to) const;

    void applyJ(const std::vector<Vec6> &from, std::vector<Vec3> &to) const;

    void applyJT(std::vector<Vec6> &from, const std::vector<Vec3> &to) const;

    Vec3 m_r;
    const MechanicalState<RigidBodyTag> &mstate;
    std::size_t m_toId;
};

template <>
struct MappingInfo<RigidBodyGlobalTag, SDF> {
    void apply(const std::vector<Vec6> & /*from*/, std::vector<Vec3> & /*to*/) const
    {
    }

    void applyJ(const std::vector<Vec6> & /*from*/, std::vector<Vec3> & /*to*/) const
    {
    }

    void applyJT(std::vector<Vec6> & /*from*/, const std::vector<Vec3> & /*to*/) const
    {
    }
};

template <typename FromT, typename ColliderT>
class CollisionMapping
{
public:
    using From = SimulationObject<FromT>;
    using To = SimulationObject<Particle3DTag>;

    CollisionMapping(SimulationObjectHandle<FromT> &from, SimulationObjectHandle<Particle3DTag> &to)
        : m_from(from)
        , m_to(to)
    {
    }

    template <typename FromTP>
    void apply(const std::vector<FromTP> &from, std::vector<Vec3> &to) const
    {
        for (auto collisionId{0UL}; collisionId < m_mappingInfo.size(); ++collisionId) {
            m_mappingInfo[collisionId].apply(from, to);
        }
    }

    template <typename FromTV>
    void applyJ(const std::vector<FromTV> &from, std::vector<Vec3> &to) const
    {
        for (auto collisionId{0UL}; collisionId < m_mappingInfo.size(); ++collisionId) {
            m_mappingInfo[collisionId].applyJ(from, to);
        }
    }

    template <typename FromTG>
    void applyJT(std::vector<FromTG> &from, const std::vector<Vec3> &to) const
    {
        for (auto collisionId{0UL}; collisionId < m_mappingInfo.size(); ++collisionId) {
            m_mappingInfo[collisionId].applyJT(from, to);
        }
    }

    SimulationObjectHandle<FromT> from() const
    {
        return m_from;
    }

    SimulationObjectHandle<Particle3DTag> to() const
    {
        return m_to;
    }

    void addMappingInfo(const MappingInfo<FromT, ColliderT> &mappingInfo)
    {
        m_mappingInfo.push_back(mappingInfo);
    }

    void resize(int n)
    {
        m_mappingInfo.clear();
        m_mappingInfo.reserve(static_cast<std::size_t>(n));
    }

private:
    std::vector<MappingInfo<FromT, ColliderT>> m_mappingInfo;

    SimulationObjectHandle<FromT> m_from;
    SimulationObjectHandle<Particle3DTag> m_to;
};

void updateMapping(const collisions::ContactEventSide<SphereCloud> &contact,
                   CollisionMapping<Particle3DTag, SphereCloud> &mapping,
                   int CollisionParticle);

void updateMapping(const collisions::ContactEventSide<SDF> &contact,
                   CollisionMapping<RigidBodyTag, SDF> &mapping,
                   int collisionParticle);

void updateMapping(const collisions::ContactEventSide<SDF> &contact,
                   CollisionMapping<RigidBodyGlobalTag, SDF> &mapping,
                   int collisionParticle);

}  // namespace collisions
}  // namespace mandos::core

#endif  // MANDOS_MAPPINGS_IDENTITYMAPPING_H