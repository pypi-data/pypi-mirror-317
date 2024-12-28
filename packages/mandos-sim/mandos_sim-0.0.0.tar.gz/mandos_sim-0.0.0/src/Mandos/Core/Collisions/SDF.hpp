#ifndef MANDOS_CORE_COLLISIONS_SDF_H
#define MANDOS_CORE_COLLISIONS_SDF_H

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/Mesh.hpp>

#include <Eigen/src/Core/util/Constants.h>
#include <openvdb/openvdb.h>

#include <Mandos/Core/core_export.h>

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include "Mandos/Core/Collisions/ContactEvent.hpp"
#include "Mandos/Core/MechanicalState.hpp"
#include "Mandos/Core/MechanicalStates/Particle3D.hpp"

namespace mandos::core::collisions
{

/**
 * @brief The SDFCollider provides ways to check collision detection using an signed distance field
 *
 */
class MANDOS_CORE_EXPORT SDF
{
    // An SDFCollider must hold an SDF structure. We use OpenVDB for this
    // TODO Consider taking the structure out if is needed somewhere else
    class MANDOS_CORE_EXPORT VDB
    {
        using Scalar = mandos::core::Scalar;
        using ScalarTree = typename openvdb::tree::Tree4<Scalar>::Type;
        using Grid = openvdb::Grid<ScalarTree>;
        using PolygonIndexGrid = openvdb::Int32Grid;

    public:
        VDB(const SurfaceMesh &mesh, Scalar contactOffset, int nbVoxelsOnMaxSide, bool flip);

        bool isInside(const mandos::core::Vec3 &query) const;
        Scalar distance(const mandos::core::Vec3 &query) const;
        PolygonIndexGrid::ValueType closestPolygon(const mandos::core::Vec3 &query) const;

        void update(const MechanicalState<RigidBodyTag> &mstate);
        void update(const MechanicalState<RigidBodyGlobalTag> &mstate);
        const Eigen::Transform<Scalar, 3, Eigen::Isometry> &transform() const;

        Scalar voxelSize() const;

    private:
        Grid::Ptr m_grid;
        PolygonIndexGrid m_polygonGrid;
        Eigen::Transform<mandos::core::Scalar, 3, Eigen::Isometry> m_transform;
        Eigen::Transform<mandos::core::Scalar, 3, Eigen::Isometry> m_invTransform;

        Scalar m_voxelSize;
    };

public:
    /**
     * @brief Construct a new SDFCollider object
     *
     * @param mesh The mesh to compute the SDF for
     * @param contactOffset The narrow band size for the SDF structure. Querying points outside the narrow band will
     * always return the contact offset distance. Use a value bigger than the actual contact offset you plan to use with
     * this collider
     * @param nbVoxels Number of voxels used in the longest side of the mesh. Increasing this value will increase
     * accuracy of the underlying SDF, but will dramatically incrase memory consumption and build time. By default 256.
     */
    SDF(const SurfaceMesh &mesh, Scalar contactOffset, int nbVoxels = 256, bool flip = false);

    const VDB &vdb() const;
    const SurfaceMesh &mesh() const;

    void update(const MechanicalState<RigidBodyGlobalTag> &mstate);
    void update(const MechanicalState<RigidBodyTag> &mstate);

    const Eigen::Transform<Scalar, 3, Eigen::Isometry> &transform() const;

    // /**
    //  * @brief Given a point, computes the contact information between the point and the SDF
    //  *
    //  * @param point
    //  * @param out
    //  */
    // void compute_contact_geometry(const Vec3 &point, ContactEvent &out) const;

private:
    VDB m_vdb;
    SurfaceMesh m_surfaceMesh;
};

template <>
struct ContactEventSide<SDF> {
    int primitiveId;
    Vec3 contactPoint;
};

}  // namespace mandos::core::collisions

#endif  // MANDOS_CORE_COLLISIONS_SDF_H