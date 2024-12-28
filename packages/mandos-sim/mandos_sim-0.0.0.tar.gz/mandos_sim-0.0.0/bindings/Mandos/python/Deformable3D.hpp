#ifndef MANDOS_PY_DEFORMABLE3D_HPP
#define MANDOS_PY_DEFORMABLE3D_HPP

#include <pybind11/pybind11.h>

#include <Mandos/Core/Energies/GravityEnergy.hpp>
#include <Mandos/Core/Energies/ConstantForce.hpp>
#include <Mandos/Core/Energies/LumpedMassInertia.hpp>
#include <Mandos/Core/Energies/MassSpring.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/SimulationObject.hpp>

namespace py = pybind11;

namespace mandos::py
{

struct Deformable3D {
    explicit Deformable3D(core::SimulationObjectHandle<core::Particle3DTag> handle);
    core::SimulationObject<core::Particle3DTag> &simObject();
    const core::SimulationObject<core::Particle3DTag> &simObject() const;

    core::SimulationObjectHandle<core::Particle3DTag> handle();

    Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>> x() const;

    void resize(int nParticles);
    int size() const;

    void setX(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> &x);

    Eigen::Map<const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>> v() const;
    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> f() const;

    void setV(const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> &v);

    void setVertexMass(std::vector<mandos::core::Scalar> vertexMass);

    const std::vector<mandos::core::Scalar> &vertexMass() const;

    void fixParticle(int index, bool x = true, bool y = true, bool z = true);

    std::vector<int> &getFixedDofVector();

    mandos::core::StableNeoHookean &snh();

    mandos::core::MassSpring &massSpring();

    mandos::core::ConstantForce &constantForce();

private:
    core::SimulationObjectHandle<core::Particle3DTag> m_handle;
};

void wrapDeformable3D(::py::module_ &m);
}  // namespace mandos::py

#endif  // MANDOS_PY_DEFORMABLE3D_HPP
