#include "Mandos/Core/Model.hpp"

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

#include <Mandos/python/Deformable3D.hpp>
#include <Mandos/python/Model.hpp>
#include <Mandos/python/RigidBody.hpp>
#include <Mandos/python/RigidBodyPointMapping.hpp>

#include <Mandos/Core/Collisions/CollisionPair.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include <Mandos/Core/SimulationObject.hpp>
#include <Mandos/Core/SimulationObjectHandle.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <pybind11/stl.h>
#include <pyerrors.h>
#include <warnings.h>

#include <fmt/format.h>

#include <stdexcept>
#include <unordered_map>

void mandos::py::wrapModel(::py::module_ &m)
{
    const ::py::class_<core::Model> model_(m, "Model_");
    ::py::class_<Model, core::Model>(m, "Model")
        .def(::py::init())
        .def("n_dof", &mandos::core::Model::nDof)

        ///////////////// Simulation objects //////////////////////

        .def(
            "add_deformable_3d",
            [](Model &model, std::optional<std::string> name = {}) {
                if (name) {
                    if (model.m_particle3DObjects.contains(name.value())) {
                        throw std::invalid_argument(
                            fmt::format("Model already contains a Deformable3D object named {}", name.value()).c_str());
                    }
                }

                auto vd{model.add<core::Particle3DTag>()};
                if (name) {
                    model.m_particle3DObjects[name.value()] = vd;
                }
                return Deformable3D{vd};
            },
            ::py::arg("name") = std::optional<std::string>{})
        .def(
            "add_rigidbody",
            [](Model &model, std::optional<std::string> name = {}) {
                if (name) {
                    if (model.m_rigidBodyObjects.contains(name.value())) {
                        throw std::invalid_argument(
                            fmt::format("Model already contains a RigidBody object named {}", name.value()).c_str());
                    }
                }

                auto vd{model.add<core::RigidBodyTag>()};
                if (name) {
                    model.m_rigidBodyObjects[name.value()] = vd;
                }
                return RigidBody3D<core::RigidBodyTag>{vd};
            },
            ::py::arg("name") = std::optional<std::string>{})
        .def(
            "add_rigidbody_global",
            [](Model &model, std::optional<std::string> name = {}) {
                if (name) {
                    if (model.m_rigidBodyGlobalObjects.contains(name.value())) {
                        throw std::invalid_argument(
                            fmt::format("Model already contains a RigidBodyGlobal object named {}", name.value())
                                .c_str());
                    }
                }

                auto vd{model.add<core::RigidBodyGlobalTag>()};
                if (name) {
                    model.m_rigidBodyGlobalObjects[name.value()] = vd;
                }
                return RigidBody3D<core::RigidBodyGlobalTag>{vd};
            },
            ::py::arg("name") = std::optional<std::string>{})
        .def(
            "add_rigidbody_cloud",
            [](Model &model, std::optional<std::string> name = {}) {
                if (name) {
                    if (model.m_rigidBodyCloudObjects.contains(name.value())) {
                        throw std::invalid_argument(
                            fmt::format("Model already contains a RigidBodyCloud object named {}", name.value())
                                .c_str());
                    }
                }

                auto vd{model.add<core::RigidBodyTag>()};
                if (name) {
                    model.m_rigidBodyCloudObjects[name.value()] = vd;
                }
                return RigidBodyCloud3D{vd};
            },
            ::py::arg("name") = std::optional<std::string>{})
        .def("get_deformable3d",
             [](Model &model, const std::string &name) -> std::optional<Deformable3D> {
                 if (auto it = model.m_particle3DObjects.find(name); it != std::end(model.m_particle3DObjects)) {
                     return Deformable3D{it->second};
                 }
                 return {};
             })
        .def("get_rigidbody",
             [](Model &model, const std::string &name) -> std::optional<RigidBody3D<core::RigidBodyTag>> {
                 if (auto it = model.m_rigidBodyObjects.find(name); it != std::end(model.m_rigidBodyObjects)) {
                     return RigidBody3D<core::RigidBodyTag>{it->second};
                 }
                 return {};
             })
        .def("get_rigidbody_cloud",
             [](Model &model, const std::string &name) -> std::optional<RigidBodyCloud3D> {
                 if (auto it = model.m_rigidBodyCloudObjects.find(name);
                     it != std::end(model.m_rigidBodyCloudObjects)) {
                     return RigidBodyCloud3D{it->second};
                 }
                 return {};
             })
        .def("get_rigidbody_global",
             [](Model &model, const std::string &name) -> std::optional<RigidBody3D<core::RigidBodyGlobalTag>> {
                 if (auto it = model.m_rigidBodyGlobalObjects.find(name);
                     it != std::end(model.m_rigidBodyGlobalObjects)) {
                     return RigidBody3D<core::RigidBodyGlobalTag>{it->second};
                 }
                 return {};
             })
        .def("get_collisions_state",
             [](Model &model, const std::string &name) -> std::optional<Deformable3D> {
                 if (auto it = model.m_collisionStateObjects.find(name);
                     it != std::end(model.m_collisionStateObjects)) {
                     return Deformable3D{it->second};
                 }
                 return {};
             })

        ///////////////// Mappings //////////////////////

        .def(
            "add_rigidbody_point_mapping",
            [](Model &model, mandos::py::RigidBodyCloud3D &rigidBodyCloud, std::optional<std::string> to_name) {
                if (to_name) {
                    if (model.m_particle3DObjects.contains(to_name.value())) {
                        throw std::invalid_argument(
                            fmt::format("Model already contains a Deformable3D named {}", to_name.value()).c_str());
                    }
                }

                auto mapping = RigidBodyPointMapping(rigidBodyCloud, model);
                if (to_name) {
                    auto deformable = mapping.m_deformable;
                    model.m_particle3DObjects[to_name.value()] = deformable.handle();
                }
                return mapping;
            },
            ::py::arg(),
            ::py::arg("to_name") = std::optional<std::string>{})

        ///////////////// Collision pairs //////////////////////

        .def(
            "add_collision_pair",
            [](Model &model,
               mandos::core::collisions::SimulationCollider<core::RigidBodyTag, core::collisions::SDF> c0,
               mandos::core::collisions::SimulationCollider<core::Particle3DTag, core::collisions::SphereCloud> c1,
               std::optional<std::string> name = {},
               mandos::core::Scalar stiffness = {},
               mandos::core::Scalar threshold = {}) {
                if (name) {
                    if (model.m_collisionStateObjects.contains(name.value())) {
                        throw std::invalid_argument(
                            fmt::format("Model already contains a Collision pair named {}", name.value()).c_str());
                    }
                }

                auto vd{model.addCollisionPair(c0, c1, stiffness, threshold)};
                if (name) {
                    model.m_collisionStateObjects[name.value()] = vd;
                }
                return Deformable3D{vd};
            },
            ::py::arg(),
            ::py::arg(),
            ::py::arg("name") = std::optional<std::string>{},
            ::py::arg("stiffness") = mandos::core::Scalar(0),
            ::py::arg("threshold") = mandos::core::Scalar(0))

        ///////////////// Visitors //////////////////////

        .def_property_readonly(
            "energy",
            [](const mandos::core::Model &model, const mandos::core::Scalar h) { return model.computeEnergy(h); })
        .def_property("state",
                      &mandos::core::Model::setState,
                      [](mandos::core::Model &model) {
                          mandos::core::Vec x(model.nDof());
                          mandos::core::Vec v(model.nDof());
                          model.state(x, v);
                          return std::pair<mandos::core::Vec, mandos::core::Vec>(x, v);
                      })
        .def("apply",
             [](Model &model) {
                 auto nDof = model.nDof();
                 mandos::core::Vec x = mandos::core::Vec::Zero(nDof);
                 mandos::core::Vec v = mandos::core::Vec::Zero(nDof);
                 model.state(x, v);
                 model.setState(x, v);
             })
        .def("compute_forces",
             [](Model &model, const mandos::core::Scalar h) {
                 auto nDof = model.nDof();
                 mandos::core::Vec g(nDof);
                 g.setZero();

                 // We need to compute advection to ensure inertial forces are correct
                 model.computeAdvection(h);

                 model.computeEnergyAndGradient(h, g);
             })
        .def("detect_collisions",
             [](Model &model) {
                 // Ensure all the graph is updated
                 auto nDof = model.nDof();
                 mandos::core::Vec x = mandos::core::Vec::Zero(nDof);
                 mandos::core::Vec v = mandos::core::Vec::Zero(nDof);
                 model.state(x, v);
                 model.setState(x, v);

                 model.updateColliders();
                 model.detectCollisions();
             })
        .def("compute_dag",
             [](Model &model) {
                 PyErr_WarnEx(
                     PyExc_DeprecationWarning, "Model.compute_dag() is deprecated. Use Model.commit() instead", 1);
                 model.commit();
             })
        .def("commit", [](Model &model) { model.commit(); });
}
