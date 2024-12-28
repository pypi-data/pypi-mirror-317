#include <Mandos/python/Energies/StableNeoHookean.hpp>

#include <Mandos/Core/Energies/StableNeoHookean.hpp>

#include <Eigen/Eigen>

#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <span>

void mandos::py::energies::wrapStableNeoHookean(::py::module_ &m)
{
    auto snhWrap = ::py::class_<mandos::core::StableNeoHookean>(m, "StableNeoHookean");

    ::py::class_<core::StableNeoHookean::ParameterSet>(snhWrap, "ParameterSet")
        .def(::py::init<std::array<mandos::core::Vec3, 4>, mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("l"),
             ::py::arg("mu"))
        .def(::py::init<mandos::core::Mat43, mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("x0"),
             ::py::arg("l"),
             ::py::arg("mu"))
        .def(::py::init<mandos::core::Mat3, mandos::core::Scalar, mandos::core::Scalar>(),  //
             ::py::kw_only(),
             ::py::arg("rest_pose"),
             ::py::arg("l"),
             ::py::arg("mu"))
        .def_readwrite("rest_pose", &core::StableNeoHookean::ParameterSet::restPoseMatrix)
        .def_readwrite("l", &core::StableNeoHookean::ParameterSet::lambda)
        .def_readwrite("mu", &core::StableNeoHookean::ParameterSet::mu);

    snhWrap.def_property_readonly("size", &mandos::core::StableNeoHookean::size)
        .def("add_element",
             [](mandos::core::StableNeoHookean &snh,
                const std::array<int, 4> &indices,
                const mandos::core::StableNeoHookean::ParameterSet &parameterSet) {
                 snh.addElement(indices, parameterSet);
             })
        .def("get_parameter_set",
             [](const core::StableNeoHookean &snh, int elementId) { return snh.getParameterSet(elementId); })
        .def("set_parameter_set",
             [](core::StableNeoHookean &snh, int elementId, const core::StableNeoHookean::ParameterSet &parameterSet) {
                 snh.setParameterSet(elementId, parameterSet);
             })
        .def_property(
            "project_spd",
            [](const mandos::core::StableNeoHookean &snh) { return snh.projectSPD(); },
            [](mandos::core::StableNeoHookean &snh, bool project) { snh.projectSPD() = project; });
}
