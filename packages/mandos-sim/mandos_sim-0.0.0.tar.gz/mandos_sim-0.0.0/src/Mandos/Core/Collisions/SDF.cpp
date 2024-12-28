#include <Mandos/Core/Collisions/SDF.hpp>

#include <openvdb/Grid.h>
#include <openvdb/io/Stream.h>
#include <openvdb/tools/Interpolation.h>
#include <openvdb/tools/MeshToVolume.h>
#include <openvdb/tools/ValueTransformer.h>

#include <Mandos/Core/RotationUtilities.hpp>

namespace mandos::core::collisions
{

SDF::VDB::VDB(const SurfaceMesh &mesh, Scalar contactOffset, int nbVoxelsOnMaxSide, bool flip)
{
    // Compute AABBox of this mesh
    Eigen::Matrix<Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType points{
        mesh.vertices.data()->data(),  //
        static_cast<Eigen::Index>(mesh.vertices.size()),
        3};

    // Compute size of voxels and number of voxels in interior and exterior bands
    const auto min{points.colwise().minCoeff().eval()};
    const auto max{points.colwise().maxCoeff().eval()};
    const auto extend{(max - min).eval()};

    m_voxelSize = extend.maxCoeff() / nbVoxelsOnMaxSide;

    const auto nbVoxelsInteriorBand{std::max(contactOffset / m_voxelSize, Scalar{3.0})};
    const auto nbVoxelsExteriorBand{std::max(contactOffset / m_voxelSize, Scalar{3.0})};

    const auto indexTransform{openvdb::math::Transform::createLinearTransform(m_voxelSize)};

    // Create the OpenVDB points
    std::vector<openvdb::Vec3d> ovdbPoints;
    ovdbPoints.reserve(mesh.vertices.size());
    for (const auto &p : mesh.vertices) {
        ovdbPoints.emplace_back(indexTransform->worldToIndex(openvdb::Vec3d{p.x(), p.y(), p.z()}));
    }

    // And finally, the Grid structure
    auto adapter{openvdb::tools::QuadAndTriangleDataAdapter<openvdb::Vec3d, openvdb::Vec3I>(
        ovdbPoints.data(),
        ovdbPoints.size(),
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        reinterpret_cast<const openvdb::Vec3I *>(mesh.indices.data()),
        mesh.indices.size())};
    m_grid = openvdb::tools::meshToVolume<Grid>(adapter,
                                                *indexTransform,
                                                static_cast<float>(nbVoxelsExteriorBand),
                                                static_cast<float>(nbVoxelsInteriorBand),
                                                0,
                                                &m_polygonGrid);

    if (flip) {
        openvdb::tools::foreach (m_grid->beginValueAll(), [](const auto &iter) { iter.setValue(-(*iter)); });
    }

    m_transform.setIdentity();
    m_invTransform.setIdentity();
}

bool SDF::VDB::isInside(const mandos::core::Vec3 &query) const
{
    const auto value = distance(query);
    return value < 0;
}

SDF::VDB::Grid::ValueType SDF::VDB::distance(const mandos::core::Vec3 &query) const
{
    const auto localQuery = (m_invTransform * query).eval();
    const openvdb::tools::GridSampler<Grid, openvdb::tools::BoxSampler> sampler(*m_grid);
    return sampler.wsSample(openvdb::Vec3d{localQuery.x(), localQuery.y(), localQuery.z()});
}

SDF::VDB::PolygonIndexGrid::ValueType SDF::VDB::closestPolygon(const mandos::core::Vec3 &query) const
{
    const auto localQuery = (m_invTransform * query).eval();
    const openvdb::tools::GridSampler<PolygonIndexGrid, openvdb::tools::PointSampler> sampler(m_polygonGrid);
    return sampler.wsSample(openvdb::Vec3d{localQuery.x(), localQuery.y(), localQuery.z()});
}

const SDF::VDB &SDF::vdb() const
{
    return m_vdb;
}

SDF::SDF(const SurfaceMesh &mesh, Scalar contactOffset, int nbVoxels, bool flip)
    : m_vdb(mesh, contactOffset, nbVoxels, flip)
    , m_surfaceMesh(mesh)
{
}

void SDF::update(const MechanicalState<RigidBodyGlobalTag> &mstate)
{
    m_vdb.update(mstate);
}

void SDF::update(const MechanicalState<RigidBodyTag> &mstate)
{
    m_vdb.update(mstate);
}

const SurfaceMesh &SDF::mesh() const
{
    return m_surfaceMesh;
}
void SDF::VDB::update(const MechanicalState<RigidBodyGlobalTag> &mstate)
{
    mandos::core::Mat4 transform = mandos::core::Mat4::Zero();
    transform.block<3, 3>(0, 0) = mandos::core::rotationExpMap(mstate.m_x[0].segment<3>(3));  // Rotation
    transform.block<3, 1>(0, 3) = mstate.m_x[0].segment<3>(0);                                // Position
    transform(3, 3) = 1.0;
    m_transform = transform;
    m_invTransform = m_transform.inverse();
}

void SDF::VDB::update(const MechanicalState<RigidBodyTag> &mstate)
{
    mandos::core::Mat4 transform = mandos::core::Mat4::Zero();
    transform.block<3, 3>(0, 0) = mandos::core::rotationExpMap(mstate.m_x[0].segment<3>(3));  // Rotation
    transform.block<3, 1>(0, 3) = mstate.m_x[0].segment<3>(0);                                // Position
    transform(3, 3) = 1.0;
    m_transform = transform;
    m_invTransform = m_transform.inverse();
}
const Eigen::Transform<Scalar, 3, Eigen::Isometry> &SDF::VDB::transform() const
{
    return m_transform;
}
const Eigen::Transform<Scalar, 3, Eigen::Isometry> &SDF::transform() const
{
    return m_vdb.transform();
}
SDF::VDB::Scalar SDF::VDB::voxelSize() const
{
    return m_voxelSize;
}
}  // namespace mandos::core::collisions
