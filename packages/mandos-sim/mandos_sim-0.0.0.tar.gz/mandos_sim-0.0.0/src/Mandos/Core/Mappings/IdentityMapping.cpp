#include <Mandos/Core/Mappings/IdentityMapping.hpp>
#include <Mandos/Core/SimulationObject.hpp>

namespace mandos::core
{

IdentityMapping::IdentityMapping(SimulationObjectHandle<Particle3DTag> from, SimulationObjectHandle<Particle3DTag> to)
    : m_from(from)
    , m_to(to)
{
}

void IdentityMapping::applyJT(std::vector<Vec3> &from, const std::vector<Vec3> &to) const
{
    Vec::MapType(from.data()->data(), static_cast<Eigen::Index>(from.size() * 3)) =
        m_J * Vec::ConstMapType(to.data()->data(), static_cast<Eigen::Index>(3 * to.size()));
}

void IdentityMapping::applyJ(const std::vector<Vec3> &from, std::vector<Vec3> &to) const
{
    Vec::MapType(to.data()->data(), static_cast<Eigen::Index>(to.size() * 3)) =
        m_J * Vec::ConstMapType(from.data()->data(), static_cast<Eigen::Index>(3 * from.size()));
}

void IdentityMapping::apply(const std::vector<Vec3> &from, std::vector<Vec3> &to) const
{
    Vec::MapType(to.data()->data(), static_cast<Eigen::Index>(to.size() * 3)) =
        m_J * Vec::ConstMapType(from.data()->data(), static_cast<Eigen::Index>(3 * from.size()));
}

SimulationObjectHandle<Particle3DTag> IdentityMapping::to() const
{
    return m_to;
}

SimulationObjectHandle<Particle3DTag> IdentityMapping::from() const
{
    return m_from;
}

const SparseMat &IdentityMapping::J() const
{
    return m_J;
}
void IdentityMapping::setJ(const SparseMat &j)
{
    m_J = j;
}
}  // namespace mandos::core