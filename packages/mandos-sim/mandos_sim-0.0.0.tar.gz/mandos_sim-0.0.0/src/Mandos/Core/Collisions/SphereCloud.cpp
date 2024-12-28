#include <Mandos/Core/Collisions/SphereCloud.hpp>

namespace mandos::core::collisions
{

SphereCloud::SphereCloud(Scalar radius)
    : m_radius({radius})
{
}

const std::vector<Scalar> &SphereCloud::radius() const
{
    return m_radius;
}

const std::vector<Vec3> &SphereCloud::centers() const
{
    return m_centers;
}

void SphereCloud::update(const MechanicalState<Particle3DTag> &mstate)
{
    if (!mstate.m_x.empty()) {
        // Copy the particle positions
        m_centers = mstate.m_x;
        const auto radius = m_radius[0];
        m_radius.resize(m_centers.size(), radius);
    }
}
}  // namespace mandos::core::collisions