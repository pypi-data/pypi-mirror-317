#include <catch2/catch_all.hpp>

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/utility_functions.hpp>

#include <Mandos/Core/Energies/CosseratBendingRod.hpp>

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/RotationUtilities.hpp>

#include <TinyAD/Scalar.hh>
#include <TinyAD/ScalarFunction.hh>

#include <spdlog/spdlog.h>

#include <fmt/ostream.h>

namespace
{
/*
** Second order aproximation of the exponential map (accurate enough for up to second derivatives)
*/
template <typename T>
inline Eigen::Matrix3<T> rotationExpMap0(const Eigen::Vector3<T> &w)
{
    using mandos::core::skew;
    return Eigen::Matrix3<mandos::core::Scalar>::Identity() + skew(w) + 0.5 * skew(w) * skew(w);
}
}  // namespace

TEST_CASE("CosseratBendingRod")
{
    mandos::core::MechanicalState<mandos::core::RigidBodyTag> mstate;
    mstate.m_x.resize(5);
    mstate.m_grad.resize(5);
    mstate.m_hessian.resize(mstate.size(), mstate.size());

    mstate.clearGradient();
    mstate.clearHessian();

    mstate.m_x[0] = mandos::core::Vec6{0, 0, 0, 0, 0, 0};
    mstate.m_x[1] = mandos::core::Vec6{1, 0, 0, 0, 1, 0};
    mstate.m_x[2] = mandos::core::Vec6{0, 1, 0, 0, 0, 1};
    mstate.m_x[3] = mandos::core::Vec6{0, 0, 1, 0, 1, 1};
    mstate.m_x[4] = mandos::core::Vec6{2, 2, 2, 1, 0, 1};

    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> x0s =
        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::ConstMapType(
            mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 6);
    mandos::core::CosseratBendingRod bending;

    auto stiffness = mandos::core::Vec3{10, 11, 12};

    const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::ConstMapType x(
        mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 6);

    const auto bending0 = std::array<int, 2>{0, 1};
    const auto bending1 = std::array<int, 2>{4, 2};
    const auto x00 = mandos::core::Mat26(x(bending0, Eigen::all).eval());
    const auto x01 = mandos::core::Mat26(x(bending1, Eigen::all).eval());
    bending.addElement(bending0, {x00, stiffness});
    bending.addElement(bending1, {x01, stiffness});

    const Eigen::Matrix<int, 2, 2> indices{{0, 1}, {4, 2}};

    SECTION("ParameterSet")
    {
        const auto expectedRestLength = (x0s.row(bending0[0]) - x0s.row(bending0[1])).segment<3>(0).norm();
        const auto expectedDarbous =
            mandos::core::computeDarbouxVector(expectedRestLength,
                                               mandos::core::rotationExpMap(x0s.row(bending0[0]).segment<3>(3)),
                                               mandos::core::rotationExpMap(x0s.row(bending0[1]).segment<3>(3)));

        const mandos::core::CosseratBendingRod::ParameterSet p0(x00, mandos::core::Vec3{100.0, 110.0, 120.0});
        REQUIRE(p0.stiffnessTensor == mandos::core::Vec3{100.0, 110.0, 120.0});
        REQUIRE(p0.restLength == expectedRestLength);
        REQUIRE(p0.intrinsicDarboux == expectedDarbous);

        const mandos::core::CosseratBendingRod::ParameterSet p1(
            std::array<mandos::core::Vec6, 2>{x0s.row(bending0[0]), x0s.row(bending0[1])},
            mandos::core::Vec3{100.0, 110.0, 120.0});
        REQUIRE(p1.stiffnessTensor == mandos::core::Vec3{100.0, 110.0, 120.0});
        REQUIRE(p1.restLength == expectedRestLength);
        REQUIRE(p1.intrinsicDarboux == expectedDarbous);

        const mandos::core::CosseratBendingRod::ParameterSet p2(
            expectedRestLength, expectedDarbous, mandos::core::Vec3{100.0, 110.0, 120.0});
        REQUIRE(p2.stiffnessTensor == mandos::core::Vec3{100.0, 110.0, 120.0});
        REQUIRE(p2.restLength == expectedRestLength);
        REQUIRE(p2.intrinsicDarboux == expectedDarbous);
    }

    SECTION("energy")
    {
        constexpr auto nTests = 1024;
        const auto size = mstate.m_x.size();

        auto dx = Catch::Generators::generate("displacement generator", CATCH_INTERNAL_LINEINFO, [size, nTests] {
            // NOLINTNEXTLINE
            using namespace Catch::Generators;
            return makeGenerators(take(nTests,
                                       map(
                                           [size](const auto &) {
                                               return Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6>::Random(
                                                          static_cast<Eigen::Index>(size), 6)
                                                   .eval();
                                           },
                                           range(0, nTests))));
        });

        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::MapType(
            mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 6) += dx;

        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> vertices{
            Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::MapType(
                mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 6)};

        auto func = TinyAD::scalar_function<6>(TinyAD::range(vertices.rows()));
        func.add_elements<2>(TinyAD::range(indices.rows()), [&](auto &element) -> TINYAD_SCALAR_TYPE(element) {
            using T = TINYAD_SCALAR_TYPE(element);

            auto faceId = element.handle;
            Eigen::Vector<T, 3> theta0 = element.variables(indices(faceId, 0)).template segment<3>(3);
            Eigen::Vector<T, 3> theta1 = element.variables(indices(faceId, 1)).template segment<3>(3);

            const mandos::core::Vec3 thetaAvalue = TinyAD::to_passive(theta0);
            const mandos::core::Vec3 thetaBvalue = TinyAD::to_passive(theta1);

            // Zero recentering
            // TODO What is this?
            theta0 = theta0 - thetaAvalue;
            theta1 = theta1 - thetaBvalue;

            const Eigen::Matrix3<T> RA = rotationExpMap0(theta0) * mandos::core::rotationExpMap(thetaAvalue);
            const Eigen::Matrix3<T> RB = rotationExpMap0(theta1) * mandos::core::rotationExpMap(thetaBvalue);

            const auto &stiffnessTensor = bending.getParameterSet(static_cast<int>(faceId)).stiffnessTensor;
            const auto &restLength = bending.getParameterSet(static_cast<int>(faceId)).restLength;

            const mandos::core::Mat3 J =
                0.5 * mandos::core::Vec3(-stiffnessTensor(0) + stiffnessTensor(1) + stiffnessTensor(2),
                                         stiffnessTensor(0) - stiffnessTensor(1) + stiffnessTensor(2),
                                         stiffnessTensor(0) + stiffnessTensor(1) - stiffnessTensor(2))
                          .asDiagonal();

            const mandos::core::Vec3 &darboux = bending.getParameterSet(static_cast<int>(faceId)).intrinsicDarboux;
            const mandos::core::Mat3 Ak = 0.5 * (mandos::core::skew(darboux) * J + J * mandos::core::skew(darboux));
            const mandos::core::Mat3 JAk = J * mandos::core::Scalar{1.0} / restLength + Ak;
            return -(RB.transpose() * RA * JAk).trace();  // Bending energy
        });

        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = bending.computeEnergy(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        }

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = bending.computeEnergyAndGradient(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
            REQUIRE_THAT((mandos::core::Vec::ConstMapType(mstate.m_grad.data()->data(), mstate.size(), 1) - gradAD)
                             .cwiseAbs()
                             .squaredNorm(),
                         Catch::Matchers::WithinAbs(0, 1e-8));
        }

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = bending.computeEnergyGradientAndHessian(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
            REQUIRE_THAT((mandos::core::Vec::ConstMapType(mstate.m_grad.data()->data(), mstate.size(), 1) - gradAD)
                             .cwiseAbs()
                             .squaredNorm(),
                         Catch::Matchers::WithinAbs(0, 1e-8));
            REQUIRE_THAT((mstate.m_hessian - mandos::core::SparseMat(hessAD)).cwiseAbs().squaredNorm(),
                         Catch::Matchers::WithinAbs(0, 1e-8));
        }
    }
}