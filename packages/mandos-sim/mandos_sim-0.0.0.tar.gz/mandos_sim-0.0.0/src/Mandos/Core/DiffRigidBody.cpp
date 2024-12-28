#include <cmath>

#include <Mandos/Core/DiffRigidBody.hpp>
#include <Mandos/Core/RotationUtilities.hpp>

namespace mandos::core
{

void applyGlobalToLocal(const Model &model, Vec &x)
{
    auto offset = 0;
    for (auto node : model.freeSimulationObjects()) {
        const auto &simObjectV = model.graph()[node];
        if (const auto *handle = std::get_if<SimulationObjectHandle_t<SimulationObject<RigidBodyTag>>>(&simObjectV)) {
            const auto &simObj = handle->simulationObject();
            const auto size = simObj.mstate.size();
            for (auto i = 0; i < static_cast<int>(simObj.mstate.m_x.size()); ++i) {
                const Vec3 theta = handle->simulationObject().mstate.m_x[static_cast<std::size_t>(i)].segment(3, 3);
                const Mat3 &J = computeGlobalToLocalAxisAngleJacobian(theta);
                x.segment<3>(offset + 6 * i + 3) = x.segment<3>(offset + 6 * i + 3).transpose() * J;
            }
            offset += size;
        }
    }
}

void applyLocalToGlobal(const Model &model, Vec &x)
{
    auto offset = 0;
    for (auto node : model.freeSimulationObjects()) {
        const auto &simObjectV = model.graph()[node];
        if (const auto *handle = std::get_if<SimulationObjectHandle_t<SimulationObject<RigidBodyTag>>>(&simObjectV)) {
            const auto &simObj = handle->simulationObject();
            const auto size = simObj.mstate.size();
            for (auto i = 0; i < static_cast<int>(simObj.mstate.m_x.size()); ++i) {
                const Vec3 theta = handle->simulationObject().mstate.m_x[static_cast<std::size_t>(i)].segment(3, 3);
                const Mat3 &J = computeLocalToGlobalAxisAngleJacobian(theta);
                x.segment<3>(offset + 6 * i + 3) = x.segment<3>(offset + 6 * i + 3).transpose() * J;
            }
            offset += size;
        }
    }
}

void applyComposeAxisAngleJacobian(Scalar h, const Model &model, Vec &v)
{
    unsigned int offset = 0;
    for (auto node : model.freeSimulationObjects()) {
        const auto &simObjectV = model.graph()[node];
        std::visit(
            [&model, &offset, &v, h](const auto &handle) {
                const auto &simulationObject = model.simulationObject(handle);
                using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                const auto size = simulationObject.mstate.size();
                if constexpr (std::is_same<SimulationObjectT, SimulationObject<RigidBodyTag>>()) {
                    for (unsigned int i = 0; i < simulationObject.mstate.m_x.size(); ++i) {
                        const Vec3 theta = simulationObject.mstate.m_x[i].template segment<3>(3);
                        const Vec3 omega = simulationObject.mstate.m_v[i].template segment<3>(3);
                        const Mat3 J = rotationExpMap(h * omega);
                        v.segment(offset + 6 * i + 3, 3) = v.segment(offset + 6 * i + 3, 3).transpose() * J;
                    }
                }
                offset += static_cast<unsigned int>(size);
            },
            simObjectV);
    }
}

}  // namespace mandos::core
