#include "Mesh.hpp"

#include <Mandos/Core/Mesh.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <pybind11/eigen.h>

void mandos::py::wrapSurfaceMesh(::py::module_ &m)
{
    ::py::class_<mandos::core::SurfaceMesh>(m, "SurfaceMesh")
        .def(::py::init())
        .def_property(
            "x",
            [](core::SurfaceMesh &mesh) {
                return Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
                    mesh.vertices.data()->data(), static_cast<Eigen::Index>(mesh.vertices.size()), 3);
            },
            [](core::SurfaceMesh &mesh, const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> &x) {
                mesh.vertices.resize(static_cast<std::size_t>(x.rows()));

                Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
                    mesh.vertices.data()->data(), x.rows(), 3) = x;
            })
        .def_property(
            "indices",
            [](core::SurfaceMesh &mesh) {
                return Eigen::Matrix<int, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
                    mesh.indices.data()->data(), static_cast<Eigen::Index>(mesh.indices.size()), 3);
            },
            [](core::SurfaceMesh &mesh, const Eigen::Matrix<int, Eigen::Dynamic, 3> &indices) {
                mesh.indices.resize(static_cast<std::size_t>(indices.rows()));

                Eigen::Matrix<int, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
                    mesh.indices.data()->data(), indices.rows(), 3) = indices;
            });
}
