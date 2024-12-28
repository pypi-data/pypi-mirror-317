#include <catch2/catch_all.hpp>

#include <Mandos/Core/Projections/FixedProjection.hpp>
#include <Mandos/Core/linear_algebra.hpp>

TEST_CASE("FixedProjection")
{
    mandos::core::FixedProjection projection;

    SECTION("Empty indices")
    {
        SECTION("Vec")
        {
            mandos::core::Vec v;
            v.resize(33);
            v.setRandom();

            auto projectedV = v;
            projection.applyP(projectedV);

            REQUIRE(projectedV.cwiseEqual(v).all());
        }
    }

    SECTION("2 constraint indices")
    {
        projection.setIndices({3 * 4, 3 * 4 + 1, 3 * 4 + 2, 3 * 9, 3 * 9 + 1, 3 * 9 + 2});
        SECTION("Vec")
        {
            mandos::core::Vec v;
            v.resize(33);
            v.setRandom();

            auto projectedV = v;
            projection.applyP(projectedV);

            REQUIRE(projectedV[3 * 4 + 0] == 0);
            REQUIRE(projectedV[3 * 4 + 1] == 0);
            REQUIRE(projectedV[3 * 4 + 2] == 0);

            REQUIRE(projectedV[3 * 9 + 0] == 0);
            REQUIRE(projectedV[3 * 9 + 1] == 0);
            REQUIRE(projectedV[3 * 9 + 2] == 0);

            // Check the rest are equal
            projectedV[3 * 4 + 0] = v[3 * 4 + 0];
            projectedV[3 * 4 + 1] = v[3 * 4 + 1];
            projectedV[3 * 4 + 2] = v[3 * 4 + 2];

            projectedV[3 * 9 + 0] = v[3 * 9 + 0];
            projectedV[3 * 9 + 1] = v[3 * 9 + 1];
            projectedV[3 * 9 + 2] = v[3 * 9 + 2];
            REQUIRE(projectedV.cwiseEqual(v).all());
        }
    }
}
