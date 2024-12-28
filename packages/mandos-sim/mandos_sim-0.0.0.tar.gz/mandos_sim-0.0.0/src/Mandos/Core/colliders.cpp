#include <Mandos/Core/colliders.hpp>

#include <Mandos/Core/utility_functions.hpp>

#include <spdlog/spdlog.h>

#include <openvdb/Grid.h>
#include <openvdb/io/Stream.h>
#include <openvdb/tools/Interpolation.h>
#include <openvdb/tools/MeshToVolume.h>

namespace mandos::core
{

void SphereCollider::compute_contact_geometry(const Vec3 &point, ContactEvent &out) const
{
    const Vec3 delta = point - center;
    const Scalar distance = delta.norm();
    out.normal = delta / distance;
    out.s_distance = distance - radius;
}

void PlaneCollider::compute_contact_geometry(const Vec3 &point, ContactEvent &out) const
{
    out.s_distance = normal.dot(point - center);
    out.normal = normal;
}

SDFCollider::SDF::SDF(const SurfaceMesh &mesh, Scalar contactOffset, int nbVoxelsOnMaxSide)
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

    const Scalar voxelSize{extend.maxCoeff() / nbVoxelsOnMaxSide};

    const auto nbVoxelsInteriorBand{std::max(contactOffset / voxelSize, Scalar{3.0})};
    const auto nbVoxelsExteriorBand{std::max(contactOffset / voxelSize, Scalar{3.0})};

    spdlog::info("SDF with {} voxels in interior band", nbVoxelsInteriorBand);
    spdlog::info("SDF with {} voxels in exterior band", nbVoxelsExteriorBand);

    const auto indexTransform{openvdb::math::Transform::createLinearTransform(voxelSize)};

    // Create the OpenVDB points
    std::vector<openvdb::Vec3d> ovdbPoints;
    ovdbPoints.reserve(mesh.vertices.size());
    for (const auto &p : mesh.vertices) {
        ovdbPoints.emplace_back(indexTransform->worldToIndex(openvdb::Vec3d{p.x(), p.y(), p.z()}));
    }

    // And finally, the Grid structure
    PolygonIndexGrid polygonGrid;
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
                                                &polygonGrid);

    spdlog::info("SDF created with {} voxels", m_grid->activeVoxelCount());
    spdlog::info("Background value is {}", m_grid->background());
}

bool SDFCollider::SDF::isInside(const mandos::core::Vec3 &query) const
{
    const openvdb::tools::GridSampler<Grid, openvdb::tools::BoxSampler> sampler(*m_grid);
    auto value = sampler.wsSample(openvdb::Vec3d{query.x(), query.y(), query.z()});
    return value < 0;
}

SDFCollider::SDF::Grid::ValueType SDFCollider::SDF::distance(const mandos::core::Vec3 &query) const
{
    const openvdb::tools::GridSampler<Grid, openvdb::tools::BoxSampler> sampler(*m_grid);
    return sampler.wsSample(openvdb::Vec3d{query.x(), query.y(), query.z()});
}

const SDFCollider::SDF &SDFCollider::sdf() const
{
    return m_sdf;
}

SDFCollider::SDFCollider(const SurfaceMesh &mesh, Scalar contactOffset, int nbVoxels)
    : m_sdf(mesh, contactOffset, nbVoxels)
{
}

// void SDFCollider::compute_contact_geometry(const Vec3& point, ContactEvent& out) const
// {

//     tmd::Result result = sdf->signed_distance(point);
//     // Compute normal from triangle
//     const int triangle_idx = result.triangle_id;
//     const Vec3 A = Vec3(mesh.vertices[3 * mesh.indices[3 * triangle_idx + 0] + 0],
//                         mesh.vertices[3 * mesh.indices[3 * triangle_idx + 0] + 1],
//                         mesh.vertices[3 * mesh.indices[3 * triangle_idx + 0] + 2]);

//     const Vec3 B = Vec3(mesh.vertices[3 * mesh.indices[3 * triangle_idx + 1] + 0],
//                         mesh.vertices[3 * mesh.indices[3 * triangle_idx + 1] + 1],
//                         mesh.vertices[3 * mesh.indices[3 * triangle_idx + 1] + 2]);

//     const Vec3 C = Vec3(mesh.vertices[3 * mesh.indices[3 * triangle_idx + 2] + 0],
//                         mesh.vertices[3 * mesh.indices[3 * triangle_idx + 2] + 1],
//                         mesh.vertices[3 * mesh.indices[3 * triangle_idx + 2] + 2]);
//     const Vec3 normal = cross(B - A, C - A).normalized();

//     // const Scalar dx = 1e-3;
//     // const Scalar sx = sdf->signed_distance(point + Vec3(dx, 0.0, 0.0)).distance;
//     // const Scalar sy = sdf->signed_distance(point + Vec3(0.0, dx, 0.0)).distance;
//     // const Scalar sz = sdf->signed_distance(point + Vec3(0.0, 0.0, dx)).distance;
//     // const Vec3 normal = Vec3(sx - result.distance, sy - result.distance, sz - result.distance).normalized();
//     // DEBUG_LOG(normal.transpose());
//     out.s_distance = result.distance;
//     out.normal = normal;
// }

// struct ComputePointParticleEventVisitor {
//     ComputePointParticleEventVisitor(const Vec3& point,
//                                      unsigned int index,
//                                      Scalar particle_radius,
//                                      std::vector<ContactEvent>& events)
//         : point(point)
//         , index(index)
//         , particle_radius(particle_radius)
//         , events(events)
//     {
//     }
//     const Vec3& point;
//     const unsigned int index;
//     const Scalar particle_radius;
//     std::vector<ContactEvent>& events;

//     template <typename T>
//     void operator()(const std::vector<T>& colliders)
//     {
//         ContactEvent event;
//         for (unsigned int j = 0; j < colliders.size(); j++) {
//             colliders[j].compute_contact_geometry(point, event);
//             event.index = index;
//             if (event.s_distance < particle_radius) {
//                 event.s_distance -= particle_radius;
//                 events.push_back(event);
//             }
//         }
//     }
// };

// void find_point_particle_contact_events(const Colliders& colliders,
//                                         const Simulables& simulables,
//                                         const PhysicsState& state,
//                                         std::vector<ContactEvent>& events)
// {
//     const Scalar particle_radius = 0.4;

//     for (unsigned int i = 0; i < simulables.particles.size(); i++) {
//         const Vec3 point = simulables.particles[i].get_position(state);
//         const unsigned int index = simulables.particles[i].index;
//         colliders.for_each(ComputePointParticleEventVisitor(point, index, particle_radius, events));
//     }

// #pragma omp parallel for
//     for (unsigned int i = 0; i < simulables.rigid_bodies.size(); i++) {
//         const Vec3 point = simulables.rigid_bodies[i].get_COM_position(state.x);
//         const unsigned int index = simulables.rigid_bodies[i].index;
//         colliders.for_each(ComputePointParticleEventVisitor(point, index, particle_radius, events));
//     }
// }

// void compute_contact_events_energy_and_derivatives(const Scalar TimeStep,
//                                                    const std::vector<ContactEvent>& events,
//                                                    const PhysicsState state,
//                                                    EnergyAndDerivatives& out)
// {
//     const Scalar contact_stiffness = 100000.0;
//     const Scalar friction_coefficient = 100.0;
//     const Scalar contact_damping_coefficient = 1000.0;
//     for (unsigned int i = 0; i < events.size(); i++) {
//         // Compute the energy and derivatives
//         const ContactEvent& event = events[i];
//         // Collision penalty force
//         const Scalar c_energy = contact_stiffness * event.s_distance * event.s_distance;
//         const Vec3 c_gradient = contact_stiffness * event.normal * event.s_distance;
//         const Mat3 c_hessian = contact_stiffness * event.normal * event.normal.transpose();

//         // Friction
//         const Vec3 velocity = state.v.segment<3>(event.index);
//         const Mat3 nnt = event.normal * event.normal.transpose();
//         const Mat3 proj_mat = (Mat3::Identity() - nnt);
//         const Vec3 tan_vel = proj_mat * velocity;
//         const Scalar f_energy = 0.5 * friction_coefficient * tan_vel.squaredNorm();
//         const Vec3 f_gradient = friction_coefficient * tan_vel;
//         const Mat3 f_hessian = 1.0 / TimeStep * friction_coefficient * proj_mat;

//         // Contact damping
//         const Vec3 normal_vel = nnt * velocity;
//         const Scalar d_energy = 0.5 * contact_damping_coefficient * normal_vel.squaredNorm();
//         const Vec3 d_gradient = contact_damping_coefficient * normal_vel;
//         const Mat3 d_hessian = 1.0 / TimeStep * contact_damping_coefficient * nnt;

//         // Fill the global structure
//         out.energy += c_energy + f_energy + d_energy;

//         out.gradient.segment<3>(event.index) += c_gradient + f_gradient + d_gradient;

//         for (unsigned int a = 0; a < 3; a++)
//             for (unsigned int b = 0; b < 3; b++)
//                 out.hessian_triplets.emplace_back(
//                     event.index + a, event.index + b, c_hessian(a, b) + f_hessian(a, b) + d_hessian(a, b));
//     }
// }

// SDFCollider::SDFCollider(const SDFCollider &other) {
//     this->mesh = other.mesh;
//     this->sdf = std::make_unique<tmd::TriangleMeshDistance>(mesh.vertices.data(), mesh.vertices.size() / 3,
//                                                             mesh.indices.data(), mesh.indices.size() / 3);
// }

// Define default constructor and destructor where the complete TriangleMeshDistance type is defined
// SDFCollider::SDFCollider() {}
// SDFCollider::~SDFCollider() {}
}  // namespace mandos::core
