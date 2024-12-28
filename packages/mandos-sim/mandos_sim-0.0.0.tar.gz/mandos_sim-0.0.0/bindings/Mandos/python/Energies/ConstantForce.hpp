#ifndef MANDOS_PY_ENERGIES_CONSTANTFORCE_HPP
#define MANDOS_PY_ENERGIES_CONSTANTFORCE_HPP

#include <pybind11/pybind11.h>

#include <Mandos/Core/Energies/ConstantForce.hpp>

namespace py = pybind11;

namespace mandos::py::energies
{
void wrapConstantForce(::py::module_ &m);
}

#endif  // MANDOS_PY_ENERGIES_CONSTANTFORCE_HPP