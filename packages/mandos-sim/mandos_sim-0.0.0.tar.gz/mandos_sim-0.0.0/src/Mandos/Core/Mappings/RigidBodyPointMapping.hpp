#ifndef MANDOS_MAPPINGS_RIGIDBODYPOINT_MAPPING_H
#define MANDOS_MAPPINGS_RIGIDBODYPOINT_MAPPING_H

#include <vector>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/SimulationObjectHandle.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

class MANDOS_CORE_EXPORT RigidBodyPointMapping
{
public:
    using From = SimulationObjectHandle<RigidBodyTag>;
    using To = SimulationObjectHandle<Particle3DTag>;

    RigidBodyPointMapping(SimulationObjectHandle<RigidBodyTag> from, SimulationObjectHandle<Particle3DTag> to);

    void apply(const std::vector<Vec6> &from, std::vector<Vec3> &to) const;
    void applyJ(const std::vector<Vec6> &from, std::vector<Vec3> &to) const;
    void applyJT(std::vector<Vec6> &from, const std::vector<Vec3> &to) const;

    SimulationObjectHandle<RigidBodyTag> from() const;
    SimulationObjectHandle<Particle3DTag> to() const;

    void addLocalPoint(const Vec3 &localPoint, int rigidBodyIndex);

    int size() const;
    SparseMat J() const;

private:
    SimulationObjectHandle<RigidBodyTag> m_from;
    SimulationObjectHandle<Particle3DTag> m_to;

    std::vector<Vec3> m_localCoord;
    std::vector<int> m_rigidBodyIndex;
};
}  // namespace mandos::core
#endif  // RIGIDBODYPOINTMAPPING_H_
