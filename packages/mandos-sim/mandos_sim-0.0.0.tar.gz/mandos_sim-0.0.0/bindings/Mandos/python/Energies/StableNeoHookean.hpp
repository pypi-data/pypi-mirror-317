#ifndef MANDOS_PY_ENERGIES_STABLENEOHOOKEAN_HPP
#define MANDOS_PY_ENERGIES_STABLENEOHOOKEAN_HPP

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace mandos::py::energies
{
void wrapStableNeoHookean(::py::module_ &m);
}

#endif  //  MANDOS_PY_ENERGIES_STABLENEOHOOKEAN_HPP