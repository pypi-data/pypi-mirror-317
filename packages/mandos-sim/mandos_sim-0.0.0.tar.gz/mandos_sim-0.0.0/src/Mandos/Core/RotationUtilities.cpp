#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/utility_functions.hpp>

#include <cmath>

namespace
{
constexpr mandos::core::Scalar THRESHOLD = 1e-6;

inline void computeAxisAngleJacobianParts(const mandos::core::Vec3 &phi, mandos::core::Mat3 &A, mandos::core::Mat3 &B)
{
    const mandos::core::Mat3 phi_phiT = phi * phi.transpose();
    A = mandos::core::rotationExpMap(phi) - mandos::core::Mat3::Identity() + phi_phiT;
    B = mandos::core::skew(phi) + phi_phiT;
}
}  // namespace

namespace mandos::core
{

Scalar sinc(Scalar x)
{
    if (abs(x) < THRESHOLD) {
        const Scalar x2 = x * x;
        const Scalar x4 = x2 * x2;
        return 1.0 - x2 / 6.0 + x4 / 120.0;
    }
    return std::sin(x) / x;
}

inline Scalar sinc_g_function(Scalar x)
{
    if (abs(x) < THRESHOLD) {
        const Scalar x2 = x * x;
        const Scalar x4 = x2 * x2;
        return -1.0 / 3.0 + x2 / 30.0 + x4 / 840.0;
    }

    return (x * std::cos(x) - std::sin(x)) / (x * x * x);
}

inline Scalar sinc_h_function(Scalar x)
{
    const Scalar x2 = x * x;
    const Scalar x4 = x2 * x2;
    if (abs(x) < THRESHOLD) {
        return 1.0 / 15.0 + x2 / 210.0 + x4 / 7560.0;
    }

    return (-x2 * std::sin(x) - 3.0 * x * std::cos(x) + 3.0 * std::sin(x)) / (x4 * x);
}

Vec3 grad_sinc(const Vec3 &theta)
{
    const Scalar x = theta.norm();
    const Scalar g = sinc_g_function(x);
    return g * theta;
}

Mat3 hess_sinc(const Vec3 &theta)
{
    const Scalar x = theta.norm();
    const Scalar g = sinc_g_function(x);
    const Scalar h = sinc_h_function(x);
    return h * theta * theta.transpose() + g * Mat3::Identity();
}

Mat3 rotationExpMap(const Vec3 &theta)
{
    // https://ipc-sim.github.io/rigid-ipc/assets/rigid_ipc_paper_350ppi.pdf
    // NOTE: There is an error in the paper. The sinc² is multiplied by 2 instead of 1/2.
    const Scalar angle = fmod(theta.norm(), 2 * M_PI);
    const Scalar sinc_angle_2 = sinc(angle / 2.0);
    const Mat3 skew_theta = skew(theta);
    return Mat3::Identity() + sinc(angle) * skew_theta + 0.5 * sinc_angle_2 * sinc_angle_2 * skew_theta * skew_theta;
}

Mat3 computeGlobalToLocalAxisAngleJacobian(const Vec3 &phi)
{
    if (phi.squaredNorm() < THRESHOLD) {
        return mandos::core::Mat3::Identity();
    }
    Mat3 A;
    Mat3 B;
    computeAxisAngleJacobianParts(phi, A, B);
    return A.inverse() * B;
}

Mat3 computeLocalToGlobalAxisAngleJacobian(const Vec3 &phi)
{
    if (phi.squaredNorm() < THRESHOLD) {
        return mandos::core::Mat3::Identity();
    }

    Mat3 A;
    Mat3 B;
    computeAxisAngleJacobianParts(phi, A, B);
    return B.inverse() * A;
}

Mat3 computeTangentialTransform(const Vec3 &phi)
{
    // From eq. 8 in https://doi.org/10.1016/j.mechrescom.2010.07.022
    // NOTE there is an error in the publication.
    // (skew(phi) (INCORRECT) --> skew(axis) (CORRECT))

    if (phi.squaredNorm() < THRESHOLD) {
        return mandos::core::Mat3::Identity();
    }
    const Scalar angle = phi.norm();
    const Vec3 axis = phi / angle;
    return sin(angle) / angle * Mat3::Identity() + (1.0 - sin(angle) / angle) * axis * axis.transpose() +
           (1.0 - cos(angle)) / angle * skew(axis);
}

Eigen::Matrix<Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeLocal(const Vec3 &theta)
{
    const Mat3 R = rotationExpMap(theta);
    return vectorizedLeviCivita() * blockMatrix<3>(R);
}

Eigen::Matrix<Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeGlobal(const Vec3 &theta)
{
    const Mat3 jac = computeLocalToGlobalAxisAngleJacobian(theta);
    return jac.transpose() * computeVectorizedRotationMatrixDerivativeLocal(theta);
}

Scalar clampAngle(Scalar angle)
{
    angle = std::fmod(angle, 2.0 * M_PI);  // Normalize to -2π to 2π
    if (angle > M_PI) {
        angle -= 2.0 * M_PI;  // Shift to -π to π
    } else if (angle < -M_PI) {
        angle += 2.0 * M_PI;  // Shift to -π to π
    }
    return angle;
}

Vec3 clampAxisAngle(const Vec3 &v)
{
    const Scalar angle = v.norm();
    if (std::abs(angle) > std::numeric_limits<Scalar>::epsilon()) {
        return clampAngle(angle) / angle * v;
    }
    return v;
}

Vec3 composeAxisAngle(const Vec3 &a, const Vec3 &b)
{
    // TODO Review this function
    // SOURCE: https://math.stackexchange.com/questions/382760/composition-of-two-axis-angle-rotations
    constexpr Scalar tol = 1e-7;
    const Scalar b_angle = clampAngle(b.norm());
    const Scalar a_angle = clampAngle(a.norm());
    if (std::fabs(b_angle) < tol) {
        return b + a;
    }
    const Vec3 b_axis = b / b_angle;

    const Scalar sin_b_angle2 = std::sin(b_angle * 0.5);
    const Scalar cos_b_angle2 = std::cos(b_angle * 0.5);

    if (fabs(a_angle) < tol) {
        Scalar new_angle = b_angle + a.dot(b_axis);
        const Vec3 new_axis = 1.0 / std::sin(new_angle / 2.0) *
                              (0.5 * cos_b_angle2 * a + sin_b_angle2 * b_axis + 0.5 * sin_b_angle2 * (a.cross(b_axis)));

        new_angle = clampAngle(new_angle);
        return new_angle * new_axis;
    }

    const Scalar sin_a_angle2 = std::sin(a_angle / 2.0);
    const Scalar cos_a_angle2 = std::cos(a_angle / 2.0);

    const Vec3 a_axis = a / a_angle;

    Scalar new_angle = 2.0 * std::acos(cos_a_angle2 * cos_b_angle2 - sin_a_angle2 * sin_b_angle2 * b_axis.dot(a_axis));

    if (fabs(new_angle) < tol) {
        return Vec3::Zero();
    }

    const Vec3 new_axis = 1.0 / std::sin(new_angle / 2.0) *
                          (sin_a_angle2 * cos_b_angle2 * a_axis + cos_a_angle2 * sin_b_angle2 * b_axis +
                           sin_a_angle2 * sin_b_angle2 * (a_axis.cross(b_axis)));

    new_angle = clampAngle(new_angle);
    return new_angle * new_axis;
}

Vec3 rotationLogMap(const Mat3 &R)
{
    // Log map
    // https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation#Log_map_from_SO(3)_to_%F0%9D%94%B0%F0%9D%94%AC(3)
    const Scalar cosAngle = (R.trace() - 1.0) * 0.5;
    // Safely compute the arc cosine (avoid NaN)
    const Scalar angle = [&cosAngle]() {
        if (cosAngle > 1) {
            return 0.0;
        }
        if (cosAngle < -1) {
            return -M_PI;
        }
        return std::acos(cosAngle);
    }();
    const Vec3 axis = Vec3(R(2, 1) - R(1, 2), R(0, 2) - R(2, 0), R(1, 0) - R(0, 1));
    Scalar xOverSinx{0};
    if (abs(angle) < 1e-4) {
        xOverSinx = 1.0 + std::pow(angle, 2) / 6.0 + 7.0 * std::pow(angle, 4) / 360.0;  // Taylor x / sinx
    } else {
        xOverSinx = angle / std::sin(angle);
    }
    return 0.5 * xOverSinx * axis;
}

Vec3 computeRelativeAxisAngle(const Vec3 &a, const Vec3 &b)
{
    const Mat3 Ra = rotationExpMap(a);
    const Mat3 Rb = rotationExpMap(b);
    const Mat3 R = Rb * Ra.transpose();
    return rotationLogMap(R);
}

}  // namespace mandos::core
