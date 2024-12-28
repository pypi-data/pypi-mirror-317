#include <catch2/catch_all.hpp>

#include <Mandos/Core/Energies/StableNeoHookean.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/SimulationObject.hpp>

#include <TinyAD/Scalar.hh>
#include <TinyAD/ScalarFunction.hh>

#include "Mandos/Core/linear_algebra.hpp"

#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators.hpp>
#include <catch2/generators/catch_generators_adapters.hpp>
#include <catch2/generators/catch_generators_random.hpp>
#include <catch2/generators/catch_generators_range.hpp>
#include <catch2/internal/catch_source_line_info.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>

#include <spdlog/spdlog.h>

#include <fmt/ostream.h>

TEST_CASE("StableNeoHookean")
{
    mandos::core::MechanicalState<mandos::core::Particle3DTag> mstate;
    mstate.m_x.resize(5);
    mstate.m_grad.resize(5);
    mstate.m_hessian.resize(mstate.size(), mstate.size());

    mstate.clearGradient();
    mstate.clearHessian();

    mstate.m_x[0] = mandos::core::Vec3{0, 0, 0};
    mstate.m_x[1] = mandos::core::Vec3{1, 0, 0};
    mstate.m_x[2] = mandos::core::Vec3{0, 1, 0};
    mstate.m_x[3] = mandos::core::Vec3{0, 0, 1};
    mstate.m_x[4] = mandos::core::Vec3{2, 2, 2};

    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> x0s =
        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType(
            mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3);
    mandos::core::StableNeoHookean snh;

    auto lambda = mandos::core::Scalar{10};
    auto mu = mandos::core::Scalar{20};

    const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType x(
        mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3);

    const auto tet0 = std::array<int, 4>{0, 1, 2, 3};
    const auto tet1 = std::array<int, 4>{4, 2, 1, 3};
    const auto x00 = mandos::core::Mat43(x(tet0, Eigen::all).eval());
    const auto x01 = mandos::core::Mat43(x(tet1, Eigen::all).eval());
    snh.addElement(tet0, {x00, lambda, mu});
    snh.addElement(tet1, {x01, lambda, mu});

    const Eigen::Matrix<int, 2, 4> indices{{0, 1, 2, 3}, {4, 2, 1, 3}};

    SECTION("ParameterSet")
    {
        auto expectedRestPoseMatrix = Eigen::Matrix<mandos::core::Scalar, 3, 3>::Zero().eval();
        expectedRestPoseMatrix.col(0) = x00.row(tet0[1]) - x00.row(tet0[0]);
        expectedRestPoseMatrix.col(1) = x00.row(tet0[2]) - x00.row(tet0[0]);
        expectedRestPoseMatrix.col(2) = x00.row(tet0[3]) - x00.row(tet0[0]);

        const mandos::core::StableNeoHookean::ParameterSet p0(x00, 100.0, 100.0);
        REQUIRE(p0.lambda == 100.0);
        REQUIRE(p0.mu == 100.0);
        REQUIRE(((p0.restPoseMatrix - expectedRestPoseMatrix).eval().array() == 0).all());

        const mandos::core::StableNeoHookean::ParameterSet p1(
            std::array<mandos::core::Vec3, 4>{x0s.row(tet0[0]), x0s.row(tet0[1]), x0s.row(tet0[2]), x0s.row(tet0[3])},
            100.0,
            100.0);
        REQUIRE(p1.lambda == 100.0);
        REQUIRE(p1.mu == 100.0);
        REQUIRE(((p1.restPoseMatrix - expectedRestPoseMatrix).eval().array() == 0).all());

        const mandos::core::StableNeoHookean::ParameterSet p2(expectedRestPoseMatrix, 100.0, 100.0);
        REQUIRE(p2.lambda == 100.0);
        REQUIRE(p2.mu == 100.0);
        REQUIRE(((p2.restPoseMatrix - expectedRestPoseMatrix).eval().array() == 0).all());
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
                                               return Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3>::Random(
                                                          static_cast<Eigen::Index>(size), 3)
                                                   .eval();
                                           },
                                           range(0, nTests))));
        });

        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
            mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3) += dx;

        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> vertices{
            Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
                mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3)};

        auto func = TinyAD::scalar_function<3>(TinyAD::range(vertices.rows()));
        func.add_elements<4>(TinyAD::range(indices.rows()), [&](auto &element) -> TINYAD_SCALAR_TYPE(element) {
            using T = TINYAD_SCALAR_TYPE(element);

            auto faceId = element.handle;
            const Eigen::Vector<T, 3> x0 = element.variables(indices(faceId, 0));
            const Eigen::Vector<T, 3> x1 = element.variables(indices(faceId, 1));
            const Eigen::Vector<T, 3> x2 = element.variables(indices(faceId, 2));
            const Eigen::Vector<T, 3> x3 = element.variables(indices(faceId, 3));

            auto i0 = indices(faceId, 0);
            auto i1 = indices(faceId, 1);
            auto i2 = indices(faceId, 2);
            auto i3 = indices(faceId, 3);

            auto dm = Eigen::Matrix<mandos::core::Scalar, 3, 3>::Zero().eval();
            dm.col(0) = x0s.row(i1) - x0s.row(i0);
            dm.col(1) = x0s.row(i2) - x0s.row(i0);
            dm.col(2) = x0s.row(i3) - x0s.row(i0);

            auto volume{mandos::core::Scalar{1.0} / mandos::core::Scalar{6.0} * dm.determinant()};
            auto invDm = dm.inverse().eval();

            auto ds{Eigen::Matrix<T, 3, 3>{}};
            ds.col(0) = x1 - x0;
            ds.col(1) = x2 - x0;
            ds.col(2) = x3 - x0;

            const auto &F{(ds * invDm).eval()};

            const auto I2{(F.transpose() * F).trace()};
            const auto I3{F.determinant()};

            return volume * (mu / mandos::core::Scalar{2.0} * (I2 - 3) - mu * (I3 - 1) +
                             lambda / mandos::core::Scalar{2.0} * (I3 - 1) * (I3 - 1));
        });

        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        snh.initialize(mstate);
        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = snh.computeEnergy(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        }

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = snh.computeEnergyAndGradient(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
            REQUIRE_THAT((mandos::core::Vec::ConstMapType(mstate.m_grad.data()->data(), mstate.size(), 1) - gradAD)
                             .cwiseAbs()
                             .squaredNorm(),
                         Catch::Matchers::WithinAbs(0, 1e-8));
        }

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = snh.computeEnergyGradientAndHessian(mstate);
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