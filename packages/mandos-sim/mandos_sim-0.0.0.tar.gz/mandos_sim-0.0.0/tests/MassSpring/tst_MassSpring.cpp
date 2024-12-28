#include <catch2/catch_all.hpp>

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/utility_functions.hpp>

#include <Mandos/Core/Energies/MassSpring.hpp>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

#include <TinyAD/Scalar.hh>
#include <TinyAD/ScalarFunction.hh>

TEST_CASE("MassSpring")
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
    mandos::core::MassSpring springs;

    auto stiffness = mandos::core::Scalar{10};

    const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType x(
        mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3);

    const auto spring0 = std::array<int, 2>{0, 1};
    const auto spring1 = std::array<int, 2>{4, 2};
    const auto x00 = mandos::core::Mat23(x(spring0, Eigen::all).eval());
    const auto x01 = mandos::core::Mat23(x(spring1, Eigen::all).eval());
    springs.addElement(spring0, {x00, stiffness});
    springs.addElement(spring1, {x01, stiffness});

    const Eigen::Matrix<int, 2, 2> indices{{0, 1}, {4, 2}};

    SECTION("ParameterSet")
    {
        auto expectedRestLength = (x0s.row(spring0[0]) - x0s.row(spring0[1])).norm();

        const mandos::core::MassSpring::ParameterSet p0(x00, 100.0);
        REQUIRE(p0.stiffness == 100.0);
        REQUIRE(p0.restLength == expectedRestLength);

        const mandos::core::MassSpring::ParameterSet p1(
            std::array<mandos::core::Vec3, 2>{x0s.row(spring0[0]), x0s.row(spring0[1])}, 100.0);
        REQUIRE(p1.stiffness == 100.0);
        REQUIRE(p1.restLength == expectedRestLength);

        const mandos::core::MassSpring::ParameterSet p2(expectedRestLength, 100.0);
        REQUIRE(p2.stiffness == 100.0);
        REQUIRE(p2.restLength == expectedRestLength);
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
        func.add_elements<2>(TinyAD::range(indices.rows()), [&](auto &element) -> TINYAD_SCALAR_TYPE(element) {
            using T = TINYAD_SCALAR_TYPE(element);

            auto faceId = element.handle;
            const Eigen::Vector<T, 3> x0 = element.variables(indices(faceId, 0));
            const Eigen::Vector<T, 3> x1 = element.variables(indices(faceId, 1));

            auto i0 = indices(faceId, 0);
            auto i1 = indices(faceId, 1);

            const auto restLength = (x0s.row(i0) - x0s.row(i1)).norm();

            if (restLength > std::numeric_limits<mandos::core::Scalar>::epsilon()) {
                stiffness = stiffness / restLength;
            }

            const auto L = (x0 - x1).norm();
            return 0.5 * stiffness * (L - restLength) * (L - restLength);
        });

        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = springs.computeEnergy(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        }

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = springs.computeEnergyAndGradient(mstate);
            REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
            REQUIRE_THAT((mandos::core::Vec::ConstMapType(mstate.m_grad.data()->data(), mstate.size(), 1) - gradAD)
                             .cwiseAbs()
                             .squaredNorm(),
                         Catch::Matchers::WithinAbs(0, 1e-8));
        }

        {
            mstate.clearGradient();
            mstate.clearHessian();
            auto energy = springs.computeEnergyGradientAndHessian(mstate);
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