#include <catch2/catch_all.hpp>

#include <Mandos/Core/Energies/LumpedMassInertia.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/SimulationObject.hpp>

#include <TinyAD/Scalar.hh>
#include <TinyAD/ScalarFunction.hh>

#include <catch2/generators/catch_generators_adapters.hpp>
#include <catch2/generators/catch_generators_random.hpp>
#include <catch2/matchers/catch_matchers_floating_point.hpp>

TEST_CASE("LumpedMassInertia")
{
    SECTION("Particle3D")
    {
        mandos::core::MechanicalState<mandos::core::Particle3DTag> mstate;
        const auto nParticles{50};
        mstate.m_x.resize(nParticles);
        mstate.m_v.resize(nParticles);
        mstate.m_grad.resize(nParticles);
        mstate.m_hessian.resize(mstate.size(), mstate.size());

        mstate.clearGradient();
        mstate.clearHessian();

        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
            mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3)
            .setRandom();

        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::MapType(
            mstate.m_v.data()->data(), static_cast<Eigen::Index>(mstate.m_v.size()), 3)
            .setRandom();

        mandos::core::LumpedMassInertia inertia;
        inertia.vertexMass().resize(mstate.m_x.size());
        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 1>::MapType(inertia.vertexMass().data(),
                                                                        static_cast<Eigen::Index>(mstate.m_x.size()))
            .setRandom();

        Eigen::Matrix<int, Eigen::Dynamic, 1> indices(Eigen::Matrix<int, Eigen::Dynamic, 1>::LinSpaced(
            static_cast<Eigen::Index>(mstate.m_x.size()), 0, static_cast<int>(mstate.m_x.size() - 1)));

        SECTION("energy")
        {
            Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3> vertices{
                Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 3, Eigen::RowMajor>::ConstMapType(
                    mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 3)};

            const auto h = 0.1;
            inertia.advect(mstate, h);

            // NOLINTNEXTLINE(Wsign-conversion)
            auto func = TinyAD::scalar_function<3>(TinyAD::range(vertices.rows()));
            func.add_elements<1>(TinyAD::range(indices.rows()), [&](auto &element) -> TINYAD_SCALAR_TYPE(element) {
                using T = TINYAD_SCALAR_TYPE(element);

                auto faceId = element.handle;
                const Eigen::Vector<T, 3> x = element.variables(indices(faceId, 0));

                auto i0 = indices(faceId, 0);
                auto advect =
                    vertices.row(i0).transpose() + h * mstate.m_v[static_cast<std::size_t>(indices(faceId, 0))];

                return 1.0 / (2.0 * h * h) * (x - advect).transpose() *
                       inertia.vertexMass()[static_cast<std::size_t>(indices(faceId, 0))] * (x - advect);
            });

            auto [energyAD, gradAD, hessAD] =
                func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

            {
                mstate.clearGradient();
                mstate.clearHessian();
                auto energy = inertia.computeEnergy(mstate, h);
                REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
            }

            {
                mstate.clearGradient();
                mstate.clearHessian();
                auto energy = inertia.computeEnergyAndGradient(mstate, h);

                REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
                REQUIRE_THAT((mandos::core::Vec::ConstMapType(mstate.m_grad.data()->data(), mstate.size(), 1) - gradAD)
                                 .cwiseAbs()
                                 .squaredNorm(),
                             Catch::Matchers::WithinAbs(0, 1e-8));
            }

            {
                mstate.clearGradient();
                mstate.clearHessian();
                auto energy = inertia.computeEnergyGradientAndHessian(mstate, h);
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
}