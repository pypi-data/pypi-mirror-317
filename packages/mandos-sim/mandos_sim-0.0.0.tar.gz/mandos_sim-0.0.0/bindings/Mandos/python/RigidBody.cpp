#include <Mandos/python/RigidBody.hpp>

#include "Mandos/Core/Collisions/SDF.hpp"
#include "Mandos/Core/Collisions/SimulationCollider.hpp"
#include "Mandos/Core/Energies/CosseratRodAlignment.hpp"
#include "Mandos/Core/Energies/MassSpring.hpp"
#include "Mandos/Core/Mesh.hpp"
#include "Mandos/Core/linear_algebra.hpp"
#include <Mandos/Core/Energies/GravityEnergy.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include <Mandos/Core/RotationUtilities.hpp>

#include <Eigen/src/Core/util/Constants.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

namespace mandos::py
{
void wrapRigidBody(::py::module_ &m)
{
    // NOLINTNEXTLINE (bugprone-unused-raii)
    ::py::class_<mandos::core::collisions::SimulationCollider<core::RigidBodyTag, core::collisions::SDF>>(
        m, "SimulationCollider<RigidBody3D, SDF>")
        .def("distance",
             [](const mandos::core::collisions::SimulationCollider<core::RigidBodyTag, core::collisions::SDF> &collider,
                const mandos::core::Vec3 &v) { return collider.collider().vdb().distance(v); });

    ::py::class_<RigidBody3D<core::RigidBodyTag>>(m, "RigidBody3D")
        .def_property("x", &RigidBody3D<core::RigidBodyTag>::x, &RigidBody3D<core::RigidBodyTag>::setX)
        .def_property("v", &RigidBody3D<core::RigidBodyTag>::v, &RigidBody3D<core::RigidBodyTag>::setV)
        .def_property_readonly("grad", &RigidBody3D<core::RigidBodyTag>::grad)
        .def_property_readonly("hessian", &RigidBody3D<core::RigidBodyTag>::hessian)
        .def_property("mass", &RigidBody3D<core::RigidBodyTag>::mass, &RigidBody3D<core::RigidBodyTag>::setMass)
        .def_property("inertiaTensor",
                      &RigidBody3D<core::RigidBodyTag>::inertiaTensor,
                      &RigidBody3D<core::RigidBodyTag>::setInertiaTensor)
        .def(
            "add_sdf",
            [](RigidBody3D<core::RigidBodyTag> &rb,
               const core::SurfaceMesh &mesh,
               mandos::core::Scalar contactOffset,
               int nbVoxels,
               bool flip = false) {
                auto &sdfs = std::get<std::vector<core::collisions::SDF>>(rb.simObject().colliders());
                auto &sdf = sdfs.emplace_back(mesh, contactOffset, nbVoxels, flip);
                sdf.update(rb.simObject().mstate);
                return mandos::core::collisions::SimulationCollider<core::RigidBodyTag, core::collisions::SDF>(
                    rb.handle(), static_cast<int>(sdfs.size() - 1));
            },
            ::py::arg(),
            ::py::arg("contactOffset"),
            ::py::arg("nb_voxels") = 256,
            ::py::arg("flip") = false)
        .def("fix",
             [](RigidBody3D<core::RigidBodyTag> &self) {
                 std::get<mandos::core::FixedProjection>(self.simObject().projections).indices().emplace_back(0);
                 std::get<mandos::core::FixedProjection>(self.simObject().projections).indices().emplace_back(1);
                 std::get<mandos::core::FixedProjection>(self.simObject().projections).indices().emplace_back(2);
                 std::get<mandos::core::FixedProjection>(self.simObject().projections).indices().emplace_back(3);
                 std::get<mandos::core::FixedProjection>(self.simObject().projections).indices().emplace_back(4);
                 std::get<mandos::core::FixedProjection>(self.simObject().projections).indices().emplace_back(5);
             })
        .def("enable_gravity",
             [](RigidBody3D<core::RigidBodyTag> &self) { self.simObject().potential<core::GravityEnergy>().enable(); })
        .def("disable_gravity",
             [](RigidBody3D<core::RigidBodyTag> &self) { self.simObject().potential<core::GravityEnergy>().disable(); })
        .def("get_transform", [](const RigidBody3D<core::RigidBodyTag> &self) {
            mandos::core::Mat4 transform = mandos::core::Mat4::Zero();
            transform.block<3, 3>(0, 0) = mandos::core::rotationExpMap(self.x().segment<3>(3));  // Rotation
            transform.block<3, 1>(0, 3) = self.x().segment<3>(0);                                // Position
            transform(3, 3) = 1.0;
            return transform;
        });

    ::py::class_<RigidBody3D<core::RigidBodyGlobalTag>>(m, "RigidBodyGlobal3D")
        .def_property("x", &RigidBody3D<core::RigidBodyGlobalTag>::x, &RigidBody3D<core::RigidBodyGlobalTag>::setX)
        .def_property("v", &RigidBody3D<core::RigidBodyGlobalTag>::v, &RigidBody3D<core::RigidBodyGlobalTag>::setV)
        .def_property_readonly("grad", &RigidBody3D<core::RigidBodyGlobalTag>::grad)
        .def_property_readonly("hessian", &RigidBody3D<core::RigidBodyGlobalTag>::hessian)
        .def_property(
            "mass", &RigidBody3D<core::RigidBodyGlobalTag>::mass, &RigidBody3D<core::RigidBodyGlobalTag>::setMass)
        .def_property("inertiaTensor",
                      &RigidBody3D<core::RigidBodyGlobalTag>::inertiaTensor,
                      &RigidBody3D<core::RigidBodyGlobalTag>::setInertiaTensor)
        .def("enable_gravity",
             [](RigidBody3D<core::RigidBodyGlobalTag> &self) {
                 self.simObject().potential<core::GravityEnergy>().enable();
             })
        .def("disable_gravity",
             [](RigidBody3D<core::RigidBodyGlobalTag> &self) {
                 self.simObject().potential<core::GravityEnergy>().disable();
             })
        .def("get_transform", [](const RigidBody3D<core::RigidBodyGlobalTag> &self) {
            mandos::core::Mat4 transform = mandos::core::Mat4::Zero();
            transform.block<3, 3>(0, 0) = mandos::core::rotationExpMap(self.x().segment<3>(3));  // Rotation
            transform.block<3, 1>(0, 3) = self.x().segment<3>(0);                                // Position
            transform(3, 3) = 1.0;
            return transform;
        });

    ::py::class_<RigidBodyCloud3D>(m, "RigidBodyCloud3D")
        .def_property("size", &RigidBodyCloud3D::size, &RigidBodyCloud3D::resize)
        .def_property("x", &RigidBodyCloud3D::x, &RigidBodyCloud3D::setX)
        .def_property("v", &RigidBodyCloud3D::v, &RigidBodyCloud3D::setV)
        .def_property_readonly("grad", &RigidBodyCloud3D::grad)
        .def_property_readonly("hessian", &RigidBodyCloud3D::hessian)
        .def_property("mass", &RigidBodyCloud3D::mass, &RigidBodyCloud3D::setMass)
        .def_property("inertiaTensor", &RigidBodyCloud3D::inertiaTensor, &RigidBodyCloud3D::setInertiaTensor)
        .def("enable_gravity",
             [](RigidBodyCloud3D &self) { self.simObject().potential<core::GravityEnergy>().enable(); })
        .def("disable_gravity",
             [](RigidBodyCloud3D &self) { self.simObject().potential<core::GravityEnergy>().disable(); })
        .def_property_readonly("mass_spring", &RigidBodyCloud3D::massSpring)
        .def_property_readonly("cosserat_bending_rod", &RigidBodyCloud3D::cosseratBendingRod)
        .def_property_readonly("cosserat_rod_aligment", &RigidBodyCloud3D::cosseratRodAlignment)
        .def("get_transform",
             [](const RigidBodyCloud3D &self, std::size_t index) {
                 core::Mat4 transform = core::Mat4::Zero();
                 core::Vec6 x = self.simObject().mstate.m_x[index].segment<6>(0);
                 transform.block<3, 3>(0, 0) = core::rotationExpMap(x.segment<3>(3));  // Rotation
                 transform.block<3, 1>(0, 3) = x.segment<3>(0);                        // Position
                 transform(3, 3) = 1.0;
                 return transform;
             })
        .def("fix_translation",
             &RigidBodyCloud3D::fixRigidBodyTranslation,
             ::py::arg("index"),
             ::py::arg("x") = true,
             ::py::arg("y") = true,
             ::py::arg("z") = true)
        .def("fix_rotation", &RigidBodyCloud3D::fixRigidBodyRotation, ::py::arg("index"))
        .def("clear_fixing", &RigidBodyCloud3D::clearFixing)
        .def("fixed_dof_vector", &RigidBodyCloud3D::getFixedDofVector);
}

template <typename Tag>
RigidBody3D<Tag>::RigidBody3D(core::SimulationObjectHandle<Tag> handle)
    : m_handle(handle)
{
    simObject().mstate.m_x.resize(1);
    simObject().mstate.m_v.resize(1);
    simObject().mstate.m_grad.resize(1);
    simObject().mstate.m_hessian.resize(6, 6);

    simObject().template inertia<core::RigidBodyInertia>().mass().resize(1);
    simObject().template inertia<core::RigidBodyInertia>().inertiaTensor().resize(1);
    simObject().template potential<core::GravityEnergy>().vertexMass().resize(1);
}

template <typename Tag>
mandos::core::SimulationObject<Tag> &RigidBody3D<Tag>::simObject()
{
    return m_handle.simulationObject();
}
template <typename Tag>
const mandos::core::SimulationObject<Tag> &RigidBody3D<Tag>::simObject() const
{
    return m_handle.simulationObject();
}

template <typename Tag>
mandos::core::SimulationObjectHandle<Tag> RigidBody3D<Tag>::handle()
{
    return this->m_handle;
}

template <typename Tag>
mandos::core::Vec6 RigidBody3D<Tag>::x() const
{
    return simObject().mstate.m_x[0];
}
template <typename Tag>
void RigidBody3D<Tag>::setX(const mandos::core::Vec6 &x)
{
    simObject().mstate.m_x[0] = x;
}
template <typename Tag>
mandos::core::Vec6 RigidBody3D<Tag>::v() const
{
    return simObject().mstate.m_v[0];
}
template <typename Tag>
void RigidBody3D<Tag>::setV(const mandos::core::Vec6 &v)
{
    simObject().mstate.m_v[0] = v;
}
template <typename Tag>
mandos::core::Vec6 RigidBody3D<Tag>::grad() const
{
    return simObject().mstate.m_grad[0];
}
template <typename Tag>
mandos::core::Mat6 RigidBody3D<Tag>::hessian() const
{
    return simObject().mstate.m_hessian.toDense();
}
template <typename Tag>
void RigidBody3D<Tag>::setMass(core::Scalar mass)
{
    simObject().template inertia<core::RigidBodyInertia>().mass()[0] = mass;
    simObject().template potential<core::GravityEnergy>().vertexMass()[0] = mass;
}
template <typename Tag>
mandos::core::Scalar RigidBody3D<Tag>::mass()
{
    return simObject().template inertia<core::RigidBodyInertia>().mass()[0];
}
template <typename Tag>
void RigidBody3D<Tag>::setInertiaTensor(const core::Mat3 &inertiaTensor)
{
    simObject().template inertia<core::RigidBodyInertia>().inertiaTensor()[0] = inertiaTensor;
}
template <typename Tag>
const mandos::core::Mat3 &RigidBody3D<Tag>::inertiaTensor() const
{
    return simObject().template inertia<core::RigidBodyInertia>().inertiaTensor()[0];
}
RigidBodyCloud3D::RigidBodyCloud3D(core::SimulationObjectHandle<core::RigidBodyTag> handle)
    : m_handle(handle)
{
}
mandos::core::SimulationObject<core::RigidBodyTag> &RigidBodyCloud3D::simObject()
{
    return m_handle.simulationObject();
}
const mandos::core::SimulationObject<core::RigidBodyTag> &RigidBodyCloud3D::simObject() const
{
    return m_handle.simulationObject();
}
void RigidBodyCloud3D::resize(int n)
{
    simObject().mstate.m_x.resize(static_cast<std::size_t>(n));
    simObject().mstate.m_v.resize(static_cast<std::size_t>(n));
    simObject().mstate.m_grad.resize(static_cast<std::size_t>(n));
    simObject().mstate.m_hessian.resize(6 * static_cast<Eigen::Index>(n),  //
                                        6 * static_cast<Eigen::Index>(n));
}
int RigidBodyCloud3D::size() const
{
    return static_cast<int>(simObject().mstate.m_x.size());
}
Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>> RigidBodyCloud3D::x() const
{
    return {simObject().mstate.m_x.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_x.size()), 6};
}
void RigidBodyCloud3D::setX(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> &x)
{
    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::MapType(
        simObject().mstate.m_x.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_x.size()), 6) = x;
}
Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>> RigidBodyCloud3D::v() const
{
    return {simObject().mstate.m_v.data()->data(),  //
            static_cast<Eigen::Index>(simObject().mstate.m_v.size()),
            6};
}
void RigidBodyCloud3D::setV(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> &v)
{
    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::MapType(
        simObject().mstate.m_v.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_v.size()), 6) = v;
}
void RigidBodyCloud3D::setMass(std::vector<core::Scalar> mass)
{
    simObject().template inertia<core::RigidBodyInertia>().mass() = mass;
    simObject().template potential<core::GravityEnergy>().vertexMass() = std::move(mass);
}
const std::vector<mandos::core::Scalar> &RigidBodyCloud3D::mass()
{
    return simObject().template inertia<core::RigidBodyInertia>().mass();
}
void RigidBodyCloud3D::setInertiaTensor(std::vector<core::Mat3> inertiaTensor)
{
    simObject().template inertia<core::RigidBodyInertia>().inertiaTensor() = std::move(inertiaTensor);
}
const std::vector<mandos::core::Mat3> &RigidBodyCloud3D::inertiaTensor() const
{
    return simObject().template inertia<core::RigidBodyInertia>().inertiaTensor();
}
Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>> RigidBodyCloud3D::grad() const
{
    return {simObject().mstate.m_grad.data()->data(),  //
            static_cast<Eigen::Index>(simObject().mstate.m_grad.size()),
            6};
}
const mandos::core::SparseMat &RigidBodyCloud3D::hessian() const
{
    return simObject().mstate.m_hessian;
}

mandos::core::MassSpring &RigidBodyCloud3D::massSpring()
{
    return simObject().template potential<mandos::core::MassSpring>();
}

mandos::core::CosseratBendingRod &RigidBodyCloud3D::cosseratBendingRod()
{
    return simObject().template potential<mandos::core::CosseratBendingRod>();
}

mandos::core::CosseratRodAlignment &RigidBodyCloud3D::cosseratRodAlignment()
{
    return simObject().template potential<mandos::core::CosseratRodAlignment>();
}

void RigidBodyCloud3D::fixRigidBodyTranslation(int index, bool x, bool y, bool z)
{
    if (x) {
        getFixedDofVector().push_back(6 * index);
    }
    if (y) {
        getFixedDofVector().push_back(6 * index + 1);
    }
    if (z) {
        getFixedDofVector().push_back(6 * index + 2);
    }
}
void RigidBodyCloud3D::fixRigidBodyRotation(int index)
{
    getFixedDofVector().push_back(6 * index + 3);
    getFixedDofVector().push_back(6 * index + 4);
    getFixedDofVector().push_back(6 * index + 5);
}

void RigidBodyCloud3D::clearFixing()
{
    getFixedDofVector().clear();
}

std::vector<int> &RigidBodyCloud3D::getFixedDofVector()
{
    return std::get<mandos::core::FixedProjection>(simObject().projections).indices();
}

template struct mandos::py::RigidBody3D<core::RigidBodyTag>;
template struct mandos::py::RigidBody3D<core::RigidBodyGlobalTag>;
mandos::core::SimulationObjectHandle<mandos::core::RigidBodyTag> RigidBodyCloud3D::handle()
{
    return m_handle;
}
}  // namespace mandos::py
