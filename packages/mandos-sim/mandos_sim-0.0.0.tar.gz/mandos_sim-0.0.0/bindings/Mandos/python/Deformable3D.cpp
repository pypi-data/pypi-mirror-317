#include "Mandos/Core/Collisions/CollisionPair.hpp"
#include "Mandos/Core/Collisions/SDF.hpp"
#include "Mandos/Core/Collisions/SimulationCollider.hpp"
#include "Mandos/Core/Collisions/SphereCloud.hpp"
#include "Mandos/Core/Energies/StableNeoHookean.hpp"
#include "Mandos/Core/MechanicalState.hpp"
#include "Mandos/Core/MechanicalStates/Particle3D.hpp"
#include "Mandos/Core/SimulationObjectHandle.hpp"
#include "Mandos/Core/linear_algebra.hpp"
#include <Mandos/python/Deformable3D.hpp>
#include <stdexcept>

#include <fmt/format.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <Mandos/Core/core_export.h>

void mandos::py::wrapDeformable3D(::py::module_ &m)
{
    // NOLINTNEXTLINE (bugprone-unused-raii)
    ::py::class_<mandos::core::collisions::SimulationCollider<core::Particle3DTag, core::collisions::SphereCloud>>(
        m, "SimulationCollider<Deformable3D, SphereCloud>");

    ::py::class_<Deformable3D>(m, "Deformable3D")
        .def_property("size", &Deformable3D::size, &Deformable3D::resize)
        .def_property("x", &Deformable3D::x, &Deformable3D::setX)
        .def_property("v", &Deformable3D::v, &Deformable3D::setV)
        .def_property_readonly("f", &Deformable3D::f)
        .def_property_readonly("snh", &Deformable3D::snh)
        .def_property_readonly("mass_spring", &Deformable3D::massSpring)
        .def_property_readonly("constant_force", &Deformable3D::constantForce)
        .def_property("particle_mass", &Deformable3D::vertexMass, &Deformable3D::setVertexMass)
        .def(
            "add_sphere_cloud",
            [](Deformable3D &def3d, mandos::core::Scalar radius) {
                auto &scs = std::get<std::vector<core::collisions::SphereCloud>>(def3d.simObject().colliders());
                auto &sc = scs.emplace_back(radius);
                sc.update(def3d.simObject().mstate);
                return mandos::core::collisions::SimulationCollider<core::Particle3DTag, core::collisions::SphereCloud>{
                    def3d.handle(), static_cast<int>(scs.size() - 1)};
            })
        .def("fix_particle",
             &Deformable3D::fixParticle,
             ::py::arg("index"),
             ::py::arg("x") = true,
             ::py::arg("y") = true,
             ::py::arg("z") = true)
        .def("fixed_dof_vector", &Deformable3D::getFixedDofVector);
}

mandos::core::SimulationObject<mandos::core::Particle3DTag> &mandos::py::Deformable3D::simObject()
{
    return m_handle.simulationObject();
}

const mandos::core::SimulationObject<mandos::core::Particle3DTag> &mandos::py::Deformable3D::simObject() const
{
    return m_handle.simulationObject();
}

mandos::core::StableNeoHookean &mandos::py::Deformable3D::snh()
{
    return simObject().potential<mandos::core::StableNeoHookean>();
}

mandos::core::MassSpring &mandos::py::Deformable3D::massSpring()
{
    return simObject().potential<mandos::core::MassSpring>();
}

mandos::core::ConstantForce &mandos::py::Deformable3D::constantForce()
{
    return simObject().potential<mandos::core::ConstantForce>();
}

const std::vector<mandos::core::Scalar> &mandos::py::Deformable3D::vertexMass() const
{
    return simObject().potential<mandos::core::GravityEnergy>().vertexMass();
}

void mandos::py::Deformable3D::setVertexMass(std::vector<mandos::core::Scalar> vertexMass)
{
    simObject().potential<mandos::core::GravityEnergy>().vertexMass() = vertexMass;
    simObject().inertia<mandos::core::LumpedMassInertia>().vertexMass() = std::move(vertexMass);
}

void mandos::py::Deformable3D::setV(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> &v)
{
    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
        simObject().mstate.m_v.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_v.size()), 3) = v;
}

Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>> mandos::py::Deformable3D::v()
    const
{
    return {simObject().mstate.m_v.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_v.size()), 3};
}

Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> mandos::py::Deformable3D::f() const
{
    return -1 * Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType(
                    simObject().mstate.m_grad.data()->data(),
                    static_cast<Eigen::Index>(simObject().mstate.m_grad.size()),
                    3);
}

void mandos::py::Deformable3D::setX(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> &x)
{
    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
        simObject().mstate.m_x.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_x.size()), 3) = x;
}

void mandos::py::Deformable3D::resize(int nParticles)
{
    simObject().mstate.m_x.resize(static_cast<std::size_t>(nParticles));
    simObject().mstate.m_v.resize(static_cast<std::size_t>(nParticles));
    simObject().mstate.m_grad.resize(static_cast<std::size_t>(nParticles));
    simObject().mstate.m_hessian.resize(3 * static_cast<Eigen::Index>(nParticles),
                                        3 * static_cast<Eigen::Index>(nParticles));
}

int mandos::py::Deformable3D::size() const
{
    return static_cast<int>(simObject().mstate.m_x.size());
}

void mandos::py::Deformable3D::fixParticle(int index, bool x, bool y, bool z)
{
    if (x) {
        getFixedDofVector().push_back(3 * index);
    }
    if (y) {
        getFixedDofVector().push_back(3 * index + 1);
    }
    if (z) {
        getFixedDofVector().push_back(3 * index + 2);
    }
}

std::vector<int> &mandos::py::Deformable3D::getFixedDofVector()
{
    return std::get<mandos::core::FixedProjection>(simObject().projections).indices();
}

Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>> mandos::py::Deformable3D::x()
    const
{
    return {simObject().mstate.m_x.data()->data(), static_cast<Eigen::Index>(simObject().mstate.m_x.size()), 3};
}

mandos::py::Deformable3D::Deformable3D(mandos::core::SimulationObjectHandle<mandos::core::Particle3DTag> handle)
    : m_handle(handle)
{
}

mandos::core::SimulationObjectHandle<mandos::core::Particle3DTag> mandos::py::Deformable3D::handle()
{
    return m_handle;
}
