#include <Mandos/Core/Differentiable.hpp>
#include <Mandos/python/Differentiable.hpp>

#include <pybind11/eigen.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace mandos::py
{
void wrapDifferentiable(::py::module_ &m)
{
    ::py::class_<core::Trajectory>(m, "Trajectory")
        .def(::py::init())
        .def_readwrite("positions", &core::Trajectory::positions)
        .def_readwrite("velocities", &core::Trajectory::velocities)
        .def("get_n_dof", &core::Trajectory::getNDof)
        .def("get_n_states", &core::Trajectory::getNStates)
        .def("get_n_steps", &core::Trajectory::getNSteps)
        .def("append_state", [](core::Trajectory &trajectory, core::Model &model) {
            // Get state
            core::Vec x(model.nDof());
            core::Vec v(model.nDof());
            model.state(x, v);
            // Append state
            trajectory.positions.push_back(std::move(x));
            trajectory.velocities.push_back(std::move(v));
        });

    ::py::class_<core::LossFunctionAndGradients>(m, "LossFunctionAndGradients")
        .def(::py::init())
        .def_readwrite("loss", &core::LossFunctionAndGradients::loss)
        .def_readwrite("loss_position_partial_derivative",
                       &core::LossFunctionAndGradients::lossPositionPartialDerivative)
        .def_readwrite("loss_velocity_partial_derivative",
                       &core::LossFunctionAndGradients::lossVelocityPartialDerivative)
        .def_readwrite("loss_parameter_partial_derivative",
                       &core::LossFunctionAndGradients::lossParameterPartialDerivative)
        .def("get_n_parameters", &core::LossFunctionAndGradients::getNParameters);

    m.def("compute_loss_function_gradient_backpropagation", &core::computeLossFunctionGradientBackpropagation);
}
}  // namespace mandos::py
