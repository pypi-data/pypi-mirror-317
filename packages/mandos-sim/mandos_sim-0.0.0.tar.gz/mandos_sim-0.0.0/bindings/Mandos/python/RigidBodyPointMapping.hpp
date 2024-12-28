#ifndef MANDOS_PY_RIGIDBODYPOINTMAPPING_HPP
#define MANDOS_PY_RIGIDBODYPOINTMAPPING_HPP

#include <pybind11/pybind11.h>

#include <Mandos/python/Deformable3D.hpp>
#include <Mandos/python/RigidBody.hpp>

namespace py = pybind11;

namespace mandos::py
{
struct RigidBodyPointMapping {
    RigidBodyPointMapping(RigidBodyCloud3D &rigidBodyCloud, mandos::core::Model &model);

    void addParticle(core::Vec3 &localPos, int rigidBodyIndex);

    core::RigidBodyPointMapping &mapping();

    py::Deformable3D m_deformable;
    py::RigidBodyCloud3D &m_rigidBodyCloud;
    unsigned int m_mapping_index;
};

void wrapRigidBodyPointMapping(::py::module_ &m);
}  // namespace mandos::py
#endif  // MANDOS_PY_RIGIDBODYPOINTMAPPING_HPP
