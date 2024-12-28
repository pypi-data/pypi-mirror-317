#include <Mandos/python/Energies/CosseratBendingRod.hpp>

#include <Mandos/Core/Energies/CosseratBendingRod.hpp>

#include <Eigen/Eigen>

#include <pybind11/cast.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

void mandos::py::energies::wrapCosseratBendingRod(::py::module_ &m)
{
    auto cosseratBendingRod = ::py::class_<mandos::core::CosseratBendingRod>(m, "CosseratBendingRod");
    ::py::class_<mandos::core::CosseratBendingRod::ParameterSet>(cosseratBendingRod, "ParameterSet")
        .def(::py::init<std::array<mandos::core::Vec6, 2>, mandos::core::Vec3>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("stiffness_tensor"))
        .def(::py::init<mandos::core::Mat26, mandos::core::Vec3>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("stiffness_tensor"))
        .def(::py::init<mandos::core::Scalar, mandos::core::Vec3, mandos::core::Vec3>(),  //
             ::py::kw_only(),
             ::py::arg("rest_length"),
             ::py::arg("intrinsic_darboux"),
             ::py::arg("stiffness_tensor"))
        .def_readwrite("stiffness_tensor", &mandos::core::CosseratBendingRod::ParameterSet::stiffnessTensor)
        .def_readwrite("intrinsic_darboux", &mandos::core::CosseratBendingRod::ParameterSet::intrinsicDarboux)
        .def_readwrite("rest_length", &mandos::core::CosseratBendingRod::ParameterSet::restLength);

    cosseratBendingRod
        .def("add_element",
             [](mandos::core::CosseratBendingRod &spring,
                const std::array<int, 2> &indices,
                const mandos::core::CosseratBendingRod::ParameterSet &parameterSet) {
                 spring.addElement(indices, parameterSet);
             })
        .def("get_parameter_set",
             [](const mandos::core::CosseratBendingRod &massSpring, int elementId) {
                 return massSpring.getParameterSet(elementId);
             })
        .def("set_parameter_set",
             [](mandos::core::CosseratBendingRod &massSpring,
                int elementId,
                const mandos::core::CosseratBendingRod::ParameterSet &parameterSet) {
                 massSpring.setParameterSet(elementId, parameterSet);
             });
}
