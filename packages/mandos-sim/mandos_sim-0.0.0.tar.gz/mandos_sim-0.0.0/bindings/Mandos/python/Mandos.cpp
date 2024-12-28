#include <pybind11/pybind11.h>

#include <Mandos/Core/Simulation.hpp>

#include <Mandos/python/Deformable3D.hpp>
#include <Mandos/python/Differentiable.hpp>
#include <Mandos/python/Mesh.hpp>
#include <Mandos/python/Model.hpp>
#include <Mandos/python/RigidBody.hpp>
#include <Mandos/python/RigidBodyPointMapping.hpp>

#include <Mandos/python/Energies/ConstantForce.hpp>
#include <Mandos/python/Energies/CosseratBendingRod.hpp>
#include <Mandos/python/Energies/CosseratRodAlignment.hpp>
#include <Mandos/python/Energies/MassSpring.hpp>
#include <Mandos/python/Energies/StableNeoHookean.hpp>

PYBIND11_MODULE(mandos_cpp, m)
{
    mandos::py::wrapModel(m);
    mandos::py::wrapDeformable3D(m);
    mandos::py::wrapRigidBody(m);
    mandos::py::wrapRigidBodyPointMapping(m);
    mandos::py::wrapSurfaceMesh(m);
    mandos::py::wrapDifferentiable(m);

    auto energies = m.def_submodule("energies");
    mandos::py::energies::wrapMassSpring(energies);
    mandos::py::energies::wrapCosseratBendingRod(energies);
    mandos::py::energies::wrapCosseratRodAlignment(energies);
    mandos::py::energies::wrapStableNeoHookean(energies);
    mandos::py::energies::wrapConstantForce(energies);

    ::py::class_<mandos::core::StepParameters>(m, "StepParameters")
        .def(::py::init())
        .def_readwrite("h", &mandos::core::StepParameters::h)
        .def_readwrite("newton_iterations", &mandos::core::StepParameters::newtonIterations)
        .def_readwrite("cg_iterations", &mandos::core::StepParameters::cgIterations)
        .def_readwrite("cg_error", &mandos::core::StepParameters::cgError)
        .def_readwrite("line_search_iterations", &mandos::core::StepParameters::lineSearchIterations)
        .def_readwrite("grad_norm", &mandos::core::StepParameters::gradNorm)
        .def_readwrite("accept_failed_solution", &mandos::core::StepParameters::acceptFailedSolution);

    py::enum_<mandos::core::SimulationStepResult>(m, "SimulationStepResult")
        .value("Success", mandos::core::SimulationStepResult::Success)
        .value("LineSearchFailed", mandos::core::SimulationStepResult::LineSearchFailed)
        .value("NewtonFailed", mandos::core::SimulationStepResult::NewtonFailed)
        .export_values()
        .def("__bool__",
             [](mandos::core::SimulationStepResult s) { return s == mandos::core::SimulationStepResult::Success; });

    m.def("step", [](mandos::py::Model &model, mandos::core::StepParameters stepParameters) {
        return mandos::core::step(model, stepParameters);
    });
}
