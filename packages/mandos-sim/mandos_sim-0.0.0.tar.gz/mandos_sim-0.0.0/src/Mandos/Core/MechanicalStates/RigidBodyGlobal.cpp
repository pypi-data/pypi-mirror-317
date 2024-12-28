#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>

namespace mandos::core
{

void MechanicalState<RigidBodyGlobalTag>::updateState(const Eigen::Ref<const Vec> &dx,
                                                      const Eigen::Ref<const Vec> &x0,
                                                      const Eigen::Ref<const Vec> & /*v0*/,
                                                      Scalar h)
{
    for (unsigned int i = 0; i < m_x.size(); ++i) {
        // The traslation part behaves like a normal 3D particle
        m_x[i].segment<3>(0) += dx.segment<3>(6 * i);
        m_v[i].segment<3>(0) = (m_x[i].segment<3>(0) - x0.segment<3>(6 * i)) / h;

        // The rotational part is a bit more tricky

        const Vec3 theta = m_x[i].segment<3>(3);
        const Vec3 theta0 = x0.segment<3>(6 * i + 3);
        const Vec3 dtheta = dx.segment<3>(6 * i + 3);

        const Vec3 new_theta = theta + dtheta;
        Scalar new_angle = new_theta.norm();
        const Vec3 axis = new_theta / new_angle;
        const Vec3 delta_theta =
            new_theta - theta0;  // Compute delta theta before clamping the angle between -pi and pi

        // Clamp the new angle betwenn -pi and pi
        new_angle = std::fmod(new_angle, 2.0 * M_PI);
        if (new_angle > M_PI) {
            new_angle -= 2 * M_PI;
        }

        m_x[i].segment<3>(3) = new_angle * axis;  // x_new
        m_v[i].segment<3>(3) = delta_theta / h;   // v_new
    }
}

}  // namespace mandos::core
