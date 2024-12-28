#ifndef MANDOS_PY_DIFFERENTIABLE_HPP
#define MANDOS_PY_DIFFERENTIABLE_HPP

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace mandos::py
{
void wrapDifferentiable(::py::module_ &m);
}  // namespace mandos::py

#endif  // MANDOS_PY_DIFFERENTIABLE_HPP
