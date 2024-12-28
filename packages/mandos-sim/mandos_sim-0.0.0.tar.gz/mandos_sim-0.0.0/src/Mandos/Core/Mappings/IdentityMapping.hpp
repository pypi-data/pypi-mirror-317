#ifndef MANDOS_MAPPINGS_IDENTITYMAPPING_H
#define MANDOS_MAPPINGS_IDENTITYMAPPING_H

#include <vector>

#include <Mandos/Core/SimulationObjectHandle.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

class MANDOS_CORE_EXPORT IdentityMapping
{
public:
    using From = SimulationObjectHandle<Particle3DTag>;
    using To = SimulationObjectHandle<Particle3DTag>;

    IdentityMapping(SimulationObjectHandle<Particle3DTag> from, SimulationObjectHandle<Particle3DTag> to);

    void apply(const std::vector<Vec3> &from, std::vector<Vec3> &to) const;
    void applyJ(const std::vector<Vec3> &from, std::vector<Vec3> &to) const;
    void applyJT(std::vector<Vec3> &from, const std::vector<Vec3> &to) const;

    SimulationObjectHandle<Particle3DTag> from() const;
    SimulationObjectHandle<Particle3DTag> to() const;

    void setJ(const SparseMat &j);

    const SparseMat &J() const;

private:
    SparseMat m_J;

    SimulationObjectHandle<Particle3DTag> m_from;
    SimulationObjectHandle<Particle3DTag> m_to;
};
}  // namespace mandos::core

#endif  // MANDOS_MAPPINGS_IDENTITYMAPPING_H