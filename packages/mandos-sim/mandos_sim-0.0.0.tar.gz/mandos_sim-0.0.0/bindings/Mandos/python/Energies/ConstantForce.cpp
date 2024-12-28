#include <Mandos/python/Energies/ConstantForce.hpp>

void mandos::py::energies::wrapConstantForce(::py::module_ &m)
{
    ::py::class_<mandos::core::ConstantForce>(m, "energies.ConstantForce")  //
        .def("add_element", &mandos::core::ConstantForce::addElement)
        .def("set_force_vector", &mandos::core::ConstantForce::setForceVector)
        .def("get_force_vector", &mandos::core::ConstantForce::getForceVector);
}
