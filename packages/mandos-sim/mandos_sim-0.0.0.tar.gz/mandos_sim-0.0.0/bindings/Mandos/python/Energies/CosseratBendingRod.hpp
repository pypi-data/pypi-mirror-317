#ifndef MANDOS_PY_ENERGIES_COSSERATBENDINGROD_HPP
#define MANDOS_PY_ENERGIES_COSSERATBENDINGROD_HPP

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace mandos::py::energies
{
void wrapCosseratBendingRod(::py::module_ &m);
}

#endif  // MANDOS_PY_ENERGIES_COSSERATBENDINGROD_HPP