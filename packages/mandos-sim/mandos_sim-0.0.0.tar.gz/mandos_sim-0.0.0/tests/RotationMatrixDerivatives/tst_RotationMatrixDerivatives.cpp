#include <functional>

#include <catch2/catch_all.hpp>

#include <Mandos/Core/DiffRigidBody.hpp>
#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/utility_functions.hpp>

#include <iostream>

namespace
{
/**
 * Compute the derivative of a rotation matrix with respect to local axis angle, evaluated at theta.
 */
inline Eigen::Matrix<mandos::core::Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeLocal(
    const mandos::core::Vec3 &theta)
{
    const mandos::core::Mat3 R = mandos::core::rotationExpMap(theta);
    return mandos::core::vectorizedLeviCivita() * mandos::core::blockMatrix(R);
}

/**
 * Compute the derivative of a rotation matrix with respect to the global axis angle theta.
 */
inline Eigen::Matrix<mandos::core::Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeGlobal(
    const mandos::core::Vec3 &theta)
{
    const mandos::core::Mat3 jac = mandos::core::computeLocalToGlobalAxisAngleJacobian(theta);
    return jac.transpose() * computeVectorizedRotationMatrixDerivativeLocal(theta);
}

inline Eigen::Matrix<mandos::core::Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeLocalFinite(
    const mandos::core::Vec3 &theta,
    mandos::core::Scalar dx)
{
    Eigen::Matrix<mandos::core::Scalar, 3, 9> dRdtheta;
    const mandos::core::Mat3 R = mandos::core::rotationExpMap(theta);
    const mandos::core::Vec9 vecR = mandos::core::vectorizeMatrix<3>(R);
    for (int i = 0; i < 3; ++i) {
        mandos::core::Vec3 dvx = mandos::core::Vec3::Zero();
        dvx[i] = dx;
        const mandos::core::Mat3 Rnew = mandos::core::rotationExpMap(dvx) * R;
        const mandos::core::Vec9 vecRnew = mandos::core::vectorizeMatrix<3>(Rnew);
        dRdtheta.row(i) = (vecRnew - vecR) / dx;
    }
    return dRdtheta;
}

inline Eigen::Matrix<mandos::core::Scalar, 3, 9> computeVectorizedRotationMatrixDerivativeGlobalFinite(
    const mandos::core::Vec3 &theta,
    mandos::core::Scalar dx)
{
    Eigen::Matrix<mandos::core::Scalar, 3, 9> dRdtheta;
    const mandos::core::Vec9 vecR = mandos::core::vectorizeMatrix<3>(mandos::core::rotationExpMap(theta));
    for (int i = 0; i < 3; ++i) {
        mandos::core::Vec3 dvx = mandos::core::Vec3::Zero();
        dvx[i] = dx;
        const mandos::core::Vec9 vecRnew = mandos::core::vectorizeMatrix<3>(mandos::core::rotationExpMap(theta + dvx));
        dRdtheta.row(i) = (vecRnew - vecR) / dx;
    }
    return dRdtheta;
}
}  // namespace

TEST_CASE("ComputeRotationMatrixDerivatives")
{
    using mandos::core::Mat3;
    using mandos::core::Scalar;
    using mandos::core::Vec3;
    using mandos::core::Vec9;

    constexpr Scalar dx = 1e-8;
    constexpr Scalar tol = 1e-6;
    SECTION("GLOBAL DERIVATIVE")
    {
        const Vec3 theta = Vec3::Random();
        auto dRdtheta = computeVectorizedRotationMatrixDerivativeGlobal(theta);
        auto dRdthetaFinite = computeVectorizedRotationMatrixDerivativeGlobalFinite(theta, dx);
        std::cout << dRdtheta << "\n";
        std::cout << "\n";
        std::cout << dRdthetaFinite << "\n";
        std::cout << "\n";
        REQUIRE(dRdtheta.isApprox(dRdthetaFinite, tol));
    }

    SECTION("LOCAL DERIVATIVE")
    {
        const Vec3 theta = Vec3::Random();
        auto dRdtheta = computeVectorizedRotationMatrixDerivativeLocal(theta);
        auto dRdthetaFinite = computeVectorizedRotationMatrixDerivativeLocalFinite(theta, dx);
        std::cout << dRdtheta << "\n";
        std::cout << "\n";
        std::cout << dRdthetaFinite << "\n";
        std::cout << "\n";
        REQUIRE(dRdtheta.isApprox(dRdthetaFinite, tol));
    }

    SECTION("BLOCK AND VECTORIZED MATRIX MULTIPLICATION")
    {
        const Mat3 a = Mat3::Random();
        const Mat3 b = Mat3::Random();
        const Vec9 result1 = mandos::core::vectorizeMatrix<3>(a * b);
        const Vec9 result2 = mandos::core::blockDiagonalMatrix<3>(a) * mandos::core::vectorizeMatrix<3>(b);
        const Vec9 result3 = mandos::core::vectorizeMatrix<3>(a).transpose() * mandos::core::blockMatrix<3>(b);
        std::cout << "result1\t" << result1.transpose() << "\n";
        std::cout << "result2\t" << result2.transpose() << "\n";
        std::cout << "result3\t" << result3.transpose() << "\n";
        std::cout << "\n";
        REQUIRE(result1.isApprox(result2, tol));
        REQUIRE(result1.isApprox(result3, tol));
    }

    SECTION("LAGGED DERIVATIVES")
    {
        const Vec3 theta = Vec3::Random();
        const Vec3 theta0 = Vec3::Random();
        const Vec3 omega0 = Vec3::Random();
        const Mat3 M = Vec3::Random().asDiagonal();
        const Scalar h = 0.1;

        using RbFuncT = Mat3(const Vec3 &, const Vec3 &, const Vec3 &);
        const std::function<RbFuncT> computeRguess = [h](const Vec3 &, const Vec3 &x0, const Vec3 &v0) {
            const Mat3 Rold = mandos::core::rotationExpMap(x0);
            const Mat3 deltaR = mandos::core::rotationExpMap(h * v0);
            const Mat3 Rguess = Rold + (Rold - deltaR.transpose() * Rold);
            return Rguess;
        };

        const std::function<RbFuncT> computeRMRguess = [M, h](const Vec3 &x, const Vec3 &x0, const Vec3 &v0) {
            const Mat3 R = mandos::core::rotationExpMap(x);
            const Mat3 Rold = mandos::core::rotationExpMap(x0);
            const Mat3 deltaR = mandos::core::rotationExpMap(h * v0);
            const Mat3 Rguess = Rold + (Rold - deltaR.transpose() * Rold);
            const Mat3 RMRguess = R * M * Rguess.transpose();
            return RMRguess;
        };

        const Mat3 R = mandos::core::rotationExpMap(theta);
        const Mat3 Rold = mandos::core::rotationExpMap(theta0);
        const Mat3 deltaR = mandos::core::rotationExpMap(h * omega0);

        const Mat3 Rguess = computeRguess(theta, theta0, omega0);
        const Mat3 Rguess_x0 = computeRguess(theta, theta0 + Vec3(dx, 0, 0), omega0);

        // TEST Rguess derivative wrt theta0
        const Eigen::Matrix<Scalar, 9, 3> dRguess_dx0 =
            mandos::core::blockDiagonalMatrix<3>(2 * Mat3::Identity() - deltaR.transpose()) *
            computeVectorizedRotationMatrixDerivativeGlobal(theta0).transpose();
        const Vec9 dRguess_dx0_finite =
            (mandos::core::vectorizeMatrix(Rguess_x0) - mandos::core::vectorizeMatrix(Rguess)) / dx;
        REQUIRE(dRguess_dx0_finite.isApprox(dRguess_dx0.col(0), tol));
        std::cout << "Rguess finite\t" << dRguess_dx0_finite.transpose() << "\n";
        std::cout << "Rguess normal\t" << dRguess_dx0.col(0).transpose() << "\n";
        std::cout << "\n";

        // TEST RMRguess derivative
        const Mat3 RMRguess = computeRMRguess(theta, theta0, omega0);
        const Vec9 vecRMRguess = mandos::core::vectorizeMatrix(RMRguess);
        const Mat3 RMRguess_x0 = computeRMRguess(theta, theta0 + Vec3(dx, 0, 0), omega0);
        const Vec9 vecRMRguess_x0 = mandos::core::vectorizeMatrix<3>(RMRguess_x0);
        const Vec9 dvecRMRguess_dx0 = (vecRMRguess_x0 - vecRMRguess) / dx;
        const Eigen::Matrix<Scalar, 9, 3> dRMRguess_dx0 =
            mandos::core::blockDiagonalMatrix<3>(R * M) *
            mandos::core::transposeVectorizedMatrixRows<9, 3>(dRguess_dx0);
        REQUIRE(dvecRMRguess_dx0.isApprox(dRMRguess_dx0.col(0), tol));
        std::cout << "RMRguess finite\t" << dvecRMRguess_dx0.transpose() << "\n";
        std::cout << "RMRguess normal\t" << dRMRguess_dx0.col(0).transpose() << "\n";
        std::cout << "\n";

        {
            // TEST transpose & matrix products
            const Mat3 R0old = deltaR.transpose() * Rold;
            const Mat3 R0oldT = Rold.transpose() * deltaR;
            const Vec9 vR0old = mandos::core::transposeVectorizedVector<9>(
                mandos::core::blockDiagonalMatrix<3>(Rold.transpose()) * mandos::core::vectorizeMatrix(deltaR));
            const Vec9 vR0oldT =
                mandos::core::blockDiagonalMatrix<3>(Rold.transpose()) * mandos::core::vectorizeMatrix(deltaR);
            std::cout << "vR0old 1" << mandos::core::vectorizeMatrix(R0old).transpose() << "\n";
            std::cout << "vR0old 2" << vR0old.transpose() << "\n";
            std::cout << "vR0old 1T" << mandos::core::vectorizeMatrix(R0oldT).transpose() << "\n";
            std::cout << "vR0old 2T" << vR0oldT.transpose() << "\n";
            std::cout << "\n";
            REQUIRE(vR0old.reshaped().isApprox(vR0old, tol));
            REQUIRE(vR0oldT.reshaped().isApprox(vR0oldT, tol));
        }

        // TEST derivative Rguess wrt omega0
        const Mat3 Rguess_v0 = computeRguess(theta, theta0, omega0 + Vec3(dx, 0, 0));
        const Vec9 dvecRguess_dv0_finite =
            (mandos::core::vectorizeMatrix(Rguess_v0) - mandos::core::vectorizeMatrix(Rguess)) / dx;
        const Eigen::Matrix<Scalar, 9, 3> dvecRguess_dv0 =
            -h * mandos::core::transposeVectorizedMatrixRows<9, 3>(
                     mandos::core::blockDiagonalMatrix<3>(Rold.transpose()) *
                     computeVectorizedRotationMatrixDerivativeGlobal(h * omega0).transpose());
        std::cout << "Rguess omega finite\t" << dvecRguess_dv0_finite.transpose() << "\n";
        std::cout << "Rguess omega normal\t" << dvecRguess_dv0.col(0).transpose() << "\n";
        std::cout << "\n";
        REQUIRE(dvecRguess_dv0_finite.isApprox(dvecRguess_dv0.col(0), tol));
    }
}

TEST_CASE("TANGENTIAL TRANSFORMATION")
{
    using mandos::core::computeLocalToGlobalAxisAngleJacobian;
    using mandos::core::computeTangentialTransform;
    using mandos::core::Mat3;
    using mandos::core::Vec3;
    const Vec3 phi = Vec3::Random();
    SECTION("Local To Global equivalence")
    {
        const Mat3 LocalToGlobal = computeLocalToGlobalAxisAngleJacobian(phi);
        const Mat3 T = computeTangentialTransform(phi);
        std::cout << "Local To Global Jacobian \n" << LocalToGlobal << "\n";
        std::cout << "\n";
        std::cout << "Tangent transformation jacobian\n" << T << "\n";
        std::cout << "\n";
        REQUIRE(LocalToGlobal.isApprox(T, 1e-8));
    }
}
