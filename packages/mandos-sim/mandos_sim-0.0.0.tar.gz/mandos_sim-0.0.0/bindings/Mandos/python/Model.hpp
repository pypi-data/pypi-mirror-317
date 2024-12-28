#ifndef MANDOS_PY_MODEL_HPP
#define MANDOS_PY_MODEL_HPP

#include <pybind11/pybind11.h>

#include <Mandos/Core/SimulationObjectHandle.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include <Mandos/Core/Model.hpp>

namespace py = pybind11;

namespace mandos::py
{
struct Model : public mandos::core::Model {
    std::unordered_map<std::string, core::SimulationObjectHandle<core::Particle3DTag>> m_particle3DObjects;
    std::unordered_map<std::string, core::SimulationObjectHandle<core::RigidBodyTag>> m_rigidBodyObjects;
    std::unordered_map<std::string, core::SimulationObjectHandle<core::RigidBodyGlobalTag>> m_rigidBodyGlobalObjects;
    std::unordered_map<std::string, core::SimulationObjectHandle<core::RigidBodyTag>> m_rigidBodyCloudObjects;
    std::unordered_map<std::string, core::SimulationObjectHandle<core::Particle3DTag>> m_collisionStateObjects;
};

void wrapModel(::py::module_ &m);
}  // namespace mandos::py

#endif  // MANDOS_PY_MODEL_HPP