#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

#include <Mandos/Core/Energies/RigidBodyInertia.hpp>
#include <Mandos/Core/RotationUtilities.hpp>

namespace mandos::core
{

void MechanicalState<RigidBodyTag>::updateState(const Eigen::Ref<const Vec> &dx,
                                                const Eigen::Ref<const Vec> &x0,
                                                const Eigen::Ref<const Vec> & /*v0*/,
                                                Scalar h)
{
    for (auto i = 0UL; i < m_x.size(); ++i) {
        // The traslation part behaves like a normal 3D particle
        m_x[i].segment<3>(0) += dx.segment<3>(6 * static_cast<Eigen::Index>(i));
        m_v[i].segment<3>(0) = (m_x[i].segment<3>(0) - x0.segment<3>(6 * static_cast<Eigen::Index>(i))) / h;

        // The rotational part is a bit more tricky

        const Vec3 theta = m_x[i].segment<3>(3);
        const Vec3 theta0 = x0.segment<3>(6 * static_cast<Eigen::Index>(i) + 3);
        const Vec3 dtheta = dx.segment<3>(6 * static_cast<Eigen::Index>(i) + 3);

        const Vec3 newTheta = clampAxisAngle(composeAxisAngle(dtheta, theta));
        m_x[i].segment<3>(3) = newTheta;
        m_v[i].segment<3>(3) = computeRelativeAxisAngle(theta0, newTheta) / h;  // omega
    }
}

}  // namespace mandos::core
