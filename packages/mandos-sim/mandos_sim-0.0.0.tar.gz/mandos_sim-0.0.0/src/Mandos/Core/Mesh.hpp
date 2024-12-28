#ifndef MANDOS_MESH_H_
#define MANDOS_MESH_H_

#include <vector>

#include <Mandos/Core/linear_algebra.hpp>

namespace mandos::core
{

/**
 * Indexed triangle mesh
 *
 * The vertices are stored as a vector of mandos::core::Vec3.
 * The indices are stored as a vector of array<int, 3>
 */
struct SurfaceMesh {
    std::vector<mandos::core::Vec3> vertices;
    std::vector<std::array<int, 3>> indices;
};

/**
 * Indexed tetrahedron mesh
 *
 * The vertices are stored as a vector of mandos::core::Vec3.
 * The indices are stored as a vector of array<int, 4>
 */
struct VolumeMesh {
    std::vector<mandos::core::Vec3> vertices;
    std::vector<std::array<int, 4>> indices;
};

/**
 * Compute the volume of the mesh (units of the vertices).
 *
 * @param indices, vertices description of the mesh (no vertex repetition)
 */
Scalar compute_mesh_volume(const std::vector<unsigned int> &indices, const std::vector<Scalar> &vertices);

/**
 * Compute the surface area of the mesh (units of the vertices).
 *
 * @param indices, vertices description of the mesh (no vertex repetition)
 */
Scalar compute_mesh_surface_area(const std::vector<unsigned int> &indices, const std::vector<Scalar> &vertices);

/**
 * Computes the external and internal edges of the mesh to count the springs it should have.
 *
 * @param vertices, indices description of the indexed mesh (no vertex repetition)
 * @return The number of tension springs and the number of bending springs
 */
std::array<unsigned int, 2> count_springs(const std::vector<Scalar> &vertices,
                                          const std::vector<unsigned int> &indices);

/**
 * Centers the mesh to the specified position, modifying the values of the vertices.
 *
 * @param mesh the simulation mesh we want to center
 * @param com the center of mass of the given mesh
 */
void recenter_mesh(SurfaceMesh &mesh, const Vec3 &com);

/**
 * Computes unique triangle faces index from a tetrahedron mesh.
 *
 * @param tet_ind Indices of the tetrahedron mesh. Must be of a size multiple of 4.
 * @param out_ind Output vector of triangle indices.
 */
void compute_triangle_indices_from_tetrahedron_indices(const std::vector<unsigned int> &tet_ind,
                                                       std::vector<unsigned int> &out_ind);

std::vector<Scalar> LoadCurveTinyObj(std::string inputfile);

}  // namespace mandos::core

#endif  // MANDOS_MESH_H_
