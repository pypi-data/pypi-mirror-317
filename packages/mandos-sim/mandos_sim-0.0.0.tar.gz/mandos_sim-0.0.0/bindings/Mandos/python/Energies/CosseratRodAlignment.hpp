#ifndef MANDOS_PY_ENERGIES_COSSERATRODALIGMENT_HPP
#define MANDOS_PY_ENERGIES_COSSERATRODALIGMENT_HPP

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace mandos::py::energies
{
void wrapCosseratRodAlignment(::py::module_ &m);
}

#endif  // MANDOS_PY_ENERGIES_COSSERATRODALIGMENT_HPP