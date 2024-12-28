#include <catch2/catch_all.hpp>

#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/utility_functions.hpp>

TEST_CASE("static_for_each")
{
    SECTION("tuple")
    {
        std::tuple t{1, 1.2, 3.4F, 5};
        auto acc = 0.0;
        mandos::core::utilities::static_for_each([&acc](auto &v) { acc += static_cast<decltype(acc)>(v); }, t);

        REQUIRE_THAT(acc, Catch::Matchers::WithinAbsMatcher(10.6, 1e-6));
    }

    SECTION("tuple with custom types")
    {
        struct A {
            int v = 7;
        };

        struct B {
            int v = 8;
        };

        std::tuple t{A{}, B{}};
        auto acc = 0;
        mandos::core::utilities::static_for_each([&acc](auto &v) { acc += v.v; }, t);

        REQUIRE(acc == 15);
    }
}

TEST_CASE("skew")
{
    const mandos::core::Vec3 v0 = mandos::core::Vec3::Random();
    const mandos::core::Vec3 v1 = mandos::core::Vec3::Random();

    REQUIRE(((v0.cross(v1) - mandos::core::skew(v0) * v1).array() == 0).all());
}

TEST_CASE("Project SPD")
{
    SECTION("Identity should stay the same")
    {
        Eigen::Matrix<mandos::core::Scalar, 9, 9> hess;
        hess.setIdentity();
        auto hessSPD = hess.eval();
        mandos::core::projectSPD(hessSPD, 1e-8, [](const auto /*v*/) { return 0; });

        REQUIRE(hessSPD == hess);
    }

    SECTION("SPD should stay the same")
    {
        Eigen::Matrix<mandos::core::Scalar, 9, 9> hess;
        hess.setIdentity();
        hess(0, 1) = 0.5;
        hess(1, 0) = 0.5;
        auto hessSPD = hess.eval();
        mandos::core::projectSPD(hessSPD, 1e-8, [](const auto /*v*/) { return 0; });

        REQUIRE(hessSPD == hess);
    }

    SECTION("non SPD should project to 0")
    {
        Eigen::Matrix<mandos::core::Scalar, 9, 9> hess;
        hess.setIdentity();
        hess(1, 1) = -1;
        auto hessSPD = hess.eval();
        mandos::core::projectSPD(hessSPD, 1e-8, [](const auto /*v*/) { return 0; });

        SECTION("Should have projected value to 0")
        {
            REQUIRE(hessSPD(1, 1) == 0);
        }

        SECTION("Should have maintain the rest of values")
        {
            hessSPD(1, 1) = -1;
            REQUIRE(hessSPD == hess);
        }
    }

    SECTION("non SPD should reflect")
    {
        Eigen::Matrix<mandos::core::Scalar, 9, 9> hess;
        hess.setIdentity();
        hess(1, 1) = -1;
        auto hessSPD = hess.eval();
        mandos::core::projectSPD(hessSPD, 1e-8, [](const auto v) { return -v; });

        SECTION("Should have reflected value")
        {
            REQUIRE(hessSPD(1, 1) == 1);
        }

        SECTION("Should have maintain the rest of values")
        {
            hessSPD(1, 1) = -1;
            REQUIRE(hessSPD == hess);
        }
    }
}
