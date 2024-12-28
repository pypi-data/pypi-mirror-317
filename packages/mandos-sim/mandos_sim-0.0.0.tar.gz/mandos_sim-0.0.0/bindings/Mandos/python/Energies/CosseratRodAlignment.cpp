#include <Mandos/python/Energies/CosseratRodAlignment.hpp>

#include <Mandos/Core/Energies/CosseratRodAlignment.hpp>

#include <Eigen/Eigen>

#include <pybind11/cast.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

void mandos::py::energies::wrapCosseratRodAlignment(::py::module_ &m)
{
    auto cosseratRodAlignment = ::py::class_<mandos::core::CosseratRodAlignment>(m, "CosseratRodAlignment");
    ::py::class_<mandos::core::CosseratRodAlignment::ParameterSet>(cosseratRodAlignment, "ParameterSet")
        .def(::py::init<std::array<mandos::core::Vec6, 2>, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("cosserat_stiffness"))
        .def(::py::init<mandos::core::Mat26, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("cosserat_stiffness"))
        .def(::py::init<mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("rest_length"),
             ::py::arg("cosserat_stiffness"))
        .def_readwrite("cosserat_stiffness", &mandos::core::CosseratRodAlignment::ParameterSet::cosseratStiffness)
        .def_readwrite("rest_length", &mandos::core::CosseratRodAlignment::ParameterSet::restLength);

    cosseratRodAlignment
        .def("add_element",
             [](mandos::core::CosseratRodAlignment &spring,
                const std::array<int, 2> &indices,
                const mandos::core::CosseratRodAlignment::ParameterSet &parameterSet) {
                 spring.addElement(indices, parameterSet);
             })
        .def("get_parameter_set",
             [](const mandos::core::CosseratRodAlignment &massSpring, int elementId) {
                 return massSpring.getParameterSet(elementId);
             })
        .def("set_parameter_set",
             [](mandos::core::CosseratRodAlignment &massSpring,
                int elementId,
                const mandos::core::CosseratRodAlignment::ParameterSet &parameterSet) {
                 massSpring.setParameterSet(elementId, parameterSet);
             });
}
