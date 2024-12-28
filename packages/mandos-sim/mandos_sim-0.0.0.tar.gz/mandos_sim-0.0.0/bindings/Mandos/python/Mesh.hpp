#ifndef MANDOS_PY_MESH_HPP
#define MANDOS_PY_MESH_HPP

#include <pybind11/pybind11.h>

#include <Mandos/Core/Energies/GravityEnergy.hpp>
#include <Mandos/Core/Energies/LumpedMassInertia.hpp>
#include <Mandos/Core/Energies/MassSpring.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/SimulationObject.hpp>

namespace py = pybind11;

namespace mandos::py
{
void wrapSurfaceMesh(::py::module_ &m);
}  // namespace mandos::py

#endif  // MANDOS_PY_MESH_HPP