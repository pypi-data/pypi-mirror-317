#ifndef MANDOS_CORE_COLLISIONS_SPHERECLOUD_H
#define MANDOS_CORE_COLLISIONS_SPHERECLOUD_H

#include <vector>

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include "Mandos/Core/Collisions/ContactEvent.hpp"

#include <Mandos/Core/core_export.h>

namespace mandos::core::collisions
{

/**
 * @brief The SphereCloud provides ways to check collision detection using spheres
 *
 */
class MANDOS_CORE_EXPORT SphereCloud
{
public:
    /**
     * @brief Construct a new SDFCollider object
     *
     * @param radius The radius of the spheres
     */
    explicit SphereCloud(Scalar radius = 0.01);

    const std::vector<Vec3> &centers() const;
    const std::vector<Scalar> &radius() const;

    void update(const MechanicalState<Particle3DTag> &mstate);

private:
    std::vector<Vec3> m_centers;
    std::vector<Scalar> m_radius;
};

template <>
struct ContactEventSide<SphereCloud> {
    int sphereId;
};

}  // namespace mandos::core::collisions

#endif  //  MANDOS_CORE_COLLISIONS_SPHERECLOUD_H