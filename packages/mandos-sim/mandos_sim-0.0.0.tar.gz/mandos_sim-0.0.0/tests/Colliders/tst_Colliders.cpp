#include <catch2/catch_all.hpp>

#include <Mandos/Core/Colliders.hpp>
#include <Mandos/Core/Mesh.hpp>

#include <catch2/matchers/catch_matchers_floating_point.hpp>

TEST_CASE("SDF")
{
    // Create a cube
    mandos::core::SurfaceMesh cube;

    cube.vertices.emplace_back(1.000000, 1.000000, -1.000000);
    cube.vertices.emplace_back(1.000000, -1.000000, -1.000000);
    cube.vertices.emplace_back(1.000000, 1.000000, 1.000000);
    cube.vertices.emplace_back(1.000000, -1.000000, 1.000000);
    cube.vertices.emplace_back(-1.000000, 1.000000, -1.000000);
    cube.vertices.emplace_back(-1.000000, -1.000000, -1.000000);
    cube.vertices.emplace_back(-1.000000, 1.000000, 1.000000);
    cube.vertices.emplace_back(-1.000000, -1.000000, 1.000000);

    cube.indices.emplace_back(std::array{5 - 1, 3 - 1, 1 - 1});
    cube.indices.emplace_back(std::array{3 - 1, 8 - 1, 4 - 1});
    cube.indices.emplace_back(std::array{7 - 1, 6 - 1, 8 - 1});
    cube.indices.emplace_back(std::array{2 - 1, 8 - 1, 6 - 1});
    cube.indices.emplace_back(std::array{1 - 1, 4 - 1, 2 - 1});
    cube.indices.emplace_back(std::array{5 - 1, 2 - 1, 6 - 1});
    cube.indices.emplace_back(std::array{5 - 1, 7 - 1, 3 - 1});
    cube.indices.emplace_back(std::array{3 - 1, 7 - 1, 8 - 1});
    cube.indices.emplace_back(std::array{7 - 1, 5 - 1, 6 - 1});
    cube.indices.emplace_back(std::array{2 - 1, 4 - 1, 8 - 1});
    cube.indices.emplace_back(std::array{1 - 1, 3 - 1, 4 - 1});
    cube.indices.emplace_back(std::array{5 - 1, 1 - 1, 2 - 1});

    SECTION("SDF")
    {
        const mandos::core::collisions::SDF sdfCollider(cube, 0.2, 32);
        REQUIRE(sdfCollider.vdb().isInside({0.9, 1.0, -1.0}) == true);
        REQUIRE(sdfCollider.vdb().isInside({1.9, 1.0, -1.0}) == false);

        REQUIRE_THAT(sdfCollider.vdb().distance({0.9, 0.0, -0.0}), Catch::Matchers::WithinAbsMatcher(-0.1, 1e-6));
        REQUIRE_THAT(sdfCollider.vdb().distance({1.0, 1.0, -1.0}), Catch::Matchers::WithinAbsMatcher(0, 1e-6));
        REQUIRE_THAT(sdfCollider.vdb().distance({1.1, 1.0, -1.0}), Catch::Matchers::WithinAbsMatcher(0.1, 1e-6));
    }

    SECTION("Flipped SDF")
    {
        const mandos::core::collisions::SDF sdfCollider{cube, 0.2, 32, true};
        REQUIRE(sdfCollider.vdb().isInside({0.9, 1.0, -1.0}) == false);
        REQUIRE(sdfCollider.vdb().isInside({1.9, 1.0, -1.0}) == true);

        REQUIRE_THAT(sdfCollider.vdb().distance({0.9, 0.0, -0.0}), Catch::Matchers::WithinAbsMatcher(0.1, 1e-6));
        REQUIRE_THAT(sdfCollider.vdb().distance({1.0, 1.0, -1.0}), Catch::Matchers::WithinAbsMatcher(0, 1e-6));
        REQUIRE_THAT(sdfCollider.vdb().distance({1.1, 1.0, -1.0}), Catch::Matchers::WithinAbsMatcher(-0.1, 1e-6));
    }
}