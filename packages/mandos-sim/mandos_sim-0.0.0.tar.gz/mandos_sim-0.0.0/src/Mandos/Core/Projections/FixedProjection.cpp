#include <Mandos/Core/Projections/FixedProjection.hpp>

namespace mandos::core
{

void mandos::core::FixedProjection::applyP(Eigen::Ref<Vec> to) const
{
    for (auto index : m_indices) {
        to[index] = 0.0;
    }
}

void FixedProjection::applyPT(Eigen::Ref<Vec> to) const
{
    for (auto index : m_indices) {
        to[index] = 0.0;
    }
}

const std::vector<int> &FixedProjection::indices() const
{
    return m_indices;
}

std::vector<int> &FixedProjection::indices()
{
    return m_indices;
}

void FixedProjection::setIndices(std::vector<int> indices)
{
    m_indices = std::move(indices);
}

}  // namespace mandos::core
