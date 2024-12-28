#ifndef MANDOS_PY_BARYCENTRICMAPPING_HPP
#define MANDOS_PY_BARYCENTRICMAPPING_HPP

#include <pybind11/pybind11.h>

#include <Mandos/python/Deformable3D.hpp>

namespace py = pybind11;

namespace mandos::py
{
// struct BarycentricMapping {
//     RigidBodyPointMapping(RigidBodyCloud3D &rigidBodyCloud, mandos::core::Model &model);

//     void addParticle(core::Vec3 &localPos, int rigidBodyIndex);

//     core::RigidBodyPointMapping &mapping();

//     py::Deformable3D m_deformable;
//     py::RigidBodyCloud3D &m_rigidBodyCloud;
//     unsigned int m_mapping_index;
// };

void wrapBarycentricMapping(::py::module_ &m);
}  // namespace mandos::py

#endif  // MANDOS_PY_BARYCENTRICMAPPING_HPP