#ifndef MANDOS_PY_ENERGIES_MASSSPRING_HPP
#define MANDOS_PY_ENERGIES_MASSSPRING_HPP

#include <pybind11/pybind11.h>

#include <Mandos/Core/Energies/MassSpring.hpp>

namespace py = pybind11;

namespace mandos::py::energies
{
void wrapMassSpring(::py::module_ &m);
}

#endif  //  MANDOS_PY_ENERGIES_MASSSPRING_HPP