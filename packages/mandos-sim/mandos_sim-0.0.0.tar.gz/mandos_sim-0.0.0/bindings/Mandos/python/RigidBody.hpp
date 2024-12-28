#ifndef MANDOS_PY_RIGIDBODY_HPP
#define MANDOS_PY_RIGIDBODY_HPP

#include <pybind11/pybind11.h>

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/SimulationObjectHandle.hpp>
#include <Mandos/Core/Energies/GravityEnergy.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include <Mandos/Core/Model.hpp>

#include <Mandos/python/Energies/MassSpring.hpp>
#include "Mandos/Core/Energies/MassSpring.hpp"

namespace py = pybind11;

namespace mandos::py
{

template <typename Tag>
struct RigidBody3D {
    explicit RigidBody3D(core::SimulationObjectHandle<Tag> handle);

    mandos::core::SimulationObject<Tag> &simObject();

    const mandos::core::SimulationObject<Tag> &simObject() const;
    mandos::core::SimulationObjectHandle<Tag> handle();

    mandos::core::Vec6 x() const;

    void setX(const mandos::core::Vec6 &x);

    mandos::core::Vec6 v() const;

    void setV(const mandos::core::Vec6 &v);

    mandos::core::Vec6 grad() const;

    mandos::core::Mat6 hessian() const;

    void setMass(core::Scalar mass);

    mandos::core::Scalar mass();

    void setInertiaTensor(const core::Mat3 &inertiaTensor);

    const mandos::core::Mat3 &inertiaTensor() const;

private:
    core::SimulationObjectHandle<Tag> m_handle;
};

extern template struct RigidBody3D<core::RigidBodyTag>;
extern template struct RigidBody3D<core::RigidBodyGlobalTag>;

struct RigidBodyCloud3D {
    explicit RigidBodyCloud3D(core::SimulationObjectHandle<core::RigidBodyTag> handle);

    mandos::core::SimulationObject<core::RigidBodyTag> &simObject();
    const mandos::core::SimulationObject<core::RigidBodyTag> &simObject() const;
    mandos::core::SimulationObjectHandle<mandos::core::RigidBodyTag> handle();

    void resize(int n);

    int size() const;

    Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>> x() const;

    void setX(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> &x);

    Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>> v() const;

    void setV(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> &v);

    void setMass(std::vector<core::Scalar> mass);

    const std::vector<mandos::core::Scalar> &mass();

    void setInertiaTensor(std::vector<core::Mat3> inertiaTensor);

    const std::vector<mandos::core::Mat3> &inertiaTensor() const;

    Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>> grad() const;

    const mandos::core::SparseMat &hessian() const;

    mandos::core::MassSpring &massSpring();
    mandos::core::CosseratBendingRod &cosseratBendingRod();
    mandos::core::CosseratRodAlignment &cosseratRodAlignment();

    void fixRigidBodyTranslation(int index, bool x = true, bool y = true, bool z = true);

    void fixRigidBodyRotation(int index);
    void clearFixing();

    std::vector<int> &getFixedDofVector();

private:
    core::SimulationObjectHandle<core::RigidBodyTag> m_handle;
};

void wrapRigidBody(::py::module_ &m);
}  // namespace mandos::py

#endif  // MANDOS_PY_DEFORMABLE3D_HPP
