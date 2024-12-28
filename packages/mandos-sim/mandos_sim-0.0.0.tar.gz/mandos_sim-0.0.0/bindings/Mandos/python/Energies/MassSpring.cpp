#include <Mandos/python/Energies/MassSpring.hpp>

#include <Mandos/Core/Energies/MassSpring.hpp>

#include <Eigen/Eigen>

#include <pybind11/cast.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <span>

void mandos::py::energies::wrapMassSpring(::py::module_ &m)
{
    auto springs = ::py::class_<mandos::core::MassSpring>(m, "MassSpring");
    ::py::class_<mandos::core::MassSpring::ParameterSet>(springs, "ParameterSet")
        .def(::py::init<std::array<mandos::core::Vec3, 2>, mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("stiffness"),
             ::py::arg("damping") = mandos::core::Scalar{0})
        .def(::py::init<mandos::core::Mat23, mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("stiffness"),
             ::py::arg("damping") = mandos::core::Scalar{0})
        .def(::py::init<mandos::core::Scalar, mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("rest_length"),
             ::py::arg("stiffness"),
             ::py::arg("damping") = mandos::core::Scalar{0})
        .def_readwrite("stiffness", &mandos::core::MassSpring::ParameterSet::stiffness)
        .def_readwrite("rest_length", &mandos::core::MassSpring::ParameterSet::restLength);

    springs
        .def("add_element",
             [](mandos::core::MassSpring &spring,
                const std::array<int, 2> &indices,
                const mandos::core::MassSpring::ParameterSet &parameterSet) {
                 spring.addElement(indices, parameterSet);
             })
        .def("get_parameter_set",
             [](const mandos::core::MassSpring &massSpring, int elementId) {
                 return massSpring.getParameterSet(elementId);
             })
        .def("set_parameter_set",
             [](mandos::core::MassSpring &massSpring,
                int elementId,
                mandos::core::MassSpring::ParameterSet parameterSet) {
                 massSpring.setParameterSet(elementId, parameterSet);
             });
}
