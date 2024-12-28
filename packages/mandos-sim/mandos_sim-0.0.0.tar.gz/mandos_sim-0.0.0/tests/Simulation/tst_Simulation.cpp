#include <catch2/catch_all.hpp>

#include <Mandos/Core/Energies/StableNeoHookean.hpp>
#include <Mandos/Core/MechanicalState.hpp>
#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/Simulation.hpp>
#include <Mandos/Core/SimulationObject.hpp>

TEST_CASE("Particle3D")
{
    mandos::core::Model model;

    // Add a simulation object made of 3D particles to the model
    auto handle = model.add<mandos::core::Particle3DTag>();
    model.commit();
    auto &simObject{model.simulationObjects<mandos::core::Particle3DTag>()[0]};

    SECTION("handle should point to object")
    {
        REQUIRE(&handle.simulationObject() == &simObject);
    }

    SECTION("Should have a single simulation object")
    {
        REQUIRE(model.simulationObjects<mandos::core::Particle3DTag>().size() == 1);
    }

    SECTION("Should be unintialized")
    {
        REQUIRE(simObject.mstate.m_x.empty());
        REQUIRE(simObject.mstate.m_v.empty());

        REQUIRE(simObject.potential<mandos::core::StableNeoHookean>().size() == 0);
        REQUIRE(model.nDof() == 0);
    }

    // Lets adds some particles to the state
    // Note that modifying directly the mstate may make the object behave incorrectly, so its an unsupported practice
    simObject.mstate.m_x.emplace_back(0, 0, 0);
    simObject.mstate.m_x.emplace_back(1, 0, 0);
    simObject.mstate.m_x.emplace_back(0, 1, 0);
    simObject.mstate.m_x.emplace_back(0, 0, 1);

    simObject.mstate.m_v.resize(simObject.mstate.m_x.size());

    SECTION("Should have 4 positions")
    {
        REQUIRE(model.nDof() == 12);
    }

    SECTION("should have no energy elements")
    {
        auto &snh{simObject.potential<mandos::core::StableNeoHookean>()};
        REQUIRE(snh.size() == 0);
    }

    // SECTION("add snh element")
    // {
    //     // We add some SNH elements
    //     auto &snh{simObject.potential<mandos::core::StableNeoHookean>()};
    //     Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType x(
    //         simObject.mstate.m_x.data()->data(), static_cast<Eigen::Index>(simObject.mstate.m_x.size()), 3);
    //     snh.addElement({0, 1, 2, 3},
    //                    mandos::core::StableNeoHookean::ParameterSet(x({0, 1, 2, 3}, Eigen::all), 1.0, 2.0));

    //     model.commit();

    //     REQUIRE(snh.size() == 1);

    //     SECTION("computeEnergy")
    //     {
    //         SECTION("rest state")
    //         {
    //             auto energy{model.computeEnergy(0)};
    //             REQUIRE(energy == 0);
    //         }

    //         // When moving the vertex, we should have some energy

    //         SECTION("defomed stated")
    //         {
    //             simObject.mstate.m_x[1] = Eigen::Matrix<mandos::core::Scalar, 3, 1>{2, 0, 0};
    //             auto energy{model.computeEnergy(0)};
    //             REQUIRE(energy != 0);
    //         }
    //     }
    // }
}