#ifndef MANDOS_ROTATION_UTILITIES_H_
#define MANDOS_ROTATION_UTILITIES_H_

#include <Mandos/Core/linear_algebra.hpp>

// TODO Review this. So at least I understand it
namespace mandos::core
{

/**
 * Compute the skew-symetric matrix of the given 3D vector.
 */

template <typename Derived>
inline Eigen::Matrix3<typename Derived::Scalar> skew(const Eigen::MatrixBase<Derived> &w)
{
    static_assert((Derived::RowsAtCompileTime * Derived::ColsAtCompileTime) == 3, "Input must be a 3D vector.");

    using T = typename Derived::Scalar;
    return Eigen::Matrix3<T>{{0, -w.z(), w.y()},  //
                             {w.z(), 0, -w.x()},
                             {-w.y(), w.x(), 0}};
}

template <typename Derived>
inline Eigen::Vector3<typename Derived::Scalar> unskew(const Eigen::MatrixBase<Derived> &m)
{
    static_assert(Derived::RowsAtCompileTime == 3 && Derived::ColsAtCompileTime == 3, "Input must be a 3x3 matrix.");
    using T = typename Derived::Scalar;
    return Eigen::Vector3<T>{m(2, 1), m(0, 2), m(1, 0)};
}

Scalar sinc(Scalar x);

Vec3 grad_sinc(const Vec3 &theta);

Mat3 hess_sinc(const Vec3 &theta);

Mat3 computeGlobalToLocalAxisAngleJacobian(const Vec3 &phi);

MANDOS_CORE_EXPORT Mat3 computeLocalToGlobalAxisAngleJacobian(const Vec3 &phi);

MANDOS_CORE_EXPORT Mat3 computeTangentialTransform(const Vec3 &phi);

/**
 * Compute the derivative of a rotation matrix with respect to local axis angle, evaluated at theta.
 */
Eigen::Matrix<Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeLocal(const Vec3 &theta);

/**
 * Compute the derivative of a rotation matrix with respect to the global axis angle theta.
 */
Eigen::Matrix<Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeGlobal(const Vec3 &theta);

Scalar clampAngle(Scalar angle);

Vec3 clampAxisAngle(const Vec3 &v);

/*
** The Baker-Campbell-Hausdorff Formula closed form for so3
** https://en.wikipedia.org/wiki/Baker%E2%80%93Campbell%E2%80%93Hausdorff_formula
*/
MANDOS_CORE_EXPORT Vec3 composeAxisAngle(const Vec3 &a, const Vec3 &b);

MANDOS_CORE_EXPORT Mat3 rotationExpMap(const mandos::core::Vec3 &theta);

MANDOS_CORE_EXPORT Vec3 rotationLogMap(const Mat3 &R);

Vec3 computeRelativeAxisAngle(const Vec3 &a, const Vec3 &b);
}  // namespace mandos::core

#endif  // MANDOS_ROTATION_UTILITIES_H_
