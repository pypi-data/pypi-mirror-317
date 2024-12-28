#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <Mandos/python/RigidBodyPointMapping.hpp>

#include <Mandos/Core/Mappings/RigidBodyPointMapping.hpp>

namespace mandos::py
{

RigidBodyPointMapping::RigidBodyPointMapping(RigidBodyCloud3D &rigidBodyCloud, mandos::core::Model &model)
    : m_deformable(model.add<core::Particle3DTag>())
    , m_rigidBodyCloud(rigidBodyCloud)

{
    auto &mappings = m_rigidBodyCloud.simObject().mappings<core::RigidBodyPointMapping>();
    m_mapping_index = static_cast<unsigned int>(mappings.size());
    mappings.emplace_back(m_rigidBodyCloud.handle(), m_deformable.handle());
}

core::RigidBodyPointMapping &RigidBodyPointMapping::mapping()
{
    return m_rigidBodyCloud.simObject().mappings<core::RigidBodyPointMapping>()[m_mapping_index];
}

void RigidBodyPointMapping::addParticle(core::Vec3 &localPos, int rigidBodyIndex)
{
    if (rigidBodyIndex >= m_rigidBodyCloud.size()) {
        throw std::invalid_argument("rigidBodyIndex is out of bounds for the rigidBodyCloud");
    }
    auto &mappings = m_rigidBodyCloud.simObject().mappings<core::RigidBodyPointMapping>();
    mappings[m_mapping_index].addLocalPoint(localPos, rigidBodyIndex);
    m_deformable.resize(mapping().size());
    m_deformable.setX(Eigen::Matrix<core::Scalar, Eigen::Dynamic, 3>::Zero(mapping().size(), 3));

    mapping().apply(mapping().from()->mstate.m_x, mapping().to()->mstate.m_x);
}

void wrapRigidBodyPointMapping(::py::module_ &m)
{
    ::py::class_<RigidBodyPointMapping>(m, "RigidBodyPointMapping")
        .def("add_particle", &RigidBodyPointMapping::addParticle)
        .def_property_readonly("deformable", [](const RigidBodyPointMapping &self) { return self.m_deformable; });
}

}  // namespace mandos::py
