#include <Mandos/Core/Mappings/BarycentricMapping.hpp>

namespace mandos::core
{

BarycentricMapping::BarycentricMapping(SimulationObjectHandle<Particle3DTag> from,
                                       SimulationObjectHandle<Particle3DTag> to)
    : m_from(from)
    , m_to(to)
{
}

void BarycentricMapping::applyJT(std::vector<Vec3> &from, const std::vector<Vec3> &to) const
{
    Vec::MapType(from.data()->data(), static_cast<Eigen::Index>(from.size() * 3)) +=
        m_J.transpose() * Vec::ConstMapType(to.data()->data(), static_cast<Eigen::Index>(3 * to.size()));
}

void BarycentricMapping::applyJ(const std::vector<Vec3> &from, std::vector<Vec3> &to) const
{
    Vec::MapType(to.data()->data(), static_cast<Eigen::Index>(to.size() * 3)) +=
        m_J * Vec::ConstMapType(from.data()->data(), static_cast<Eigen::Index>(3 * from.size()));
}

void BarycentricMapping::apply(const std::vector<Vec3> &from, std::vector<Vec3> &to) const
{
    Vec::MapType(to.data()->data(), static_cast<Eigen::Index>(to.size() * 3)) +=
        m_J * Vec::ConstMapType(from.data()->data(), static_cast<Eigen::Index>(3 * from.size()));
}

SimulationObjectHandle<Particle3DTag> BarycentricMapping::to() const
{
    return m_to;
}

SimulationObjectHandle<Particle3DTag> BarycentricMapping::from() const
{
    return m_from;
}

const SparseMat &BarycentricMapping::J() const
{
    return m_J;
}
void BarycentricMapping::setJ(const SparseMat &j)
{
    m_J = j;
}
}  // namespace mandos::core