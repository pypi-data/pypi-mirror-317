#ifndef MANDOS_PROJECTIONS_FIXEDPROJECTION_H
#define MANDOS_PROJECTIONS_FIXEDPROJECTION_H

#include <vector>

#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief FixedProjection projects the constrained indices to 0, allowing to implement fixed particles
 *
 */
class MANDOS_CORE_EXPORT FixedProjection
{
public:
    /**
     * @brief Applies the projection to a generalized state vector segment
     *
     * @param to The vector to project
     */
    void applyP(Eigen::Ref<Vec> to) const;

    /**
     * @brief Applies the projection transpose to a generalized state vector segment
     *
     * @param to The vector to project
     */
    void applyPT(Eigen::Ref<Vec> to) const;

    const std::vector<int> &indices() const;
    std::vector<int> &indices();
    void setIndices(std::vector<int> indices);

private:
    /**
     * @brief Indices of the fixed particles
     *
     */
    std::vector<int> m_indices;
};

}  // namespace mandos::core

#endif  // MANDOS_PROJECTIONS_FIXEDPROJECTION_H
