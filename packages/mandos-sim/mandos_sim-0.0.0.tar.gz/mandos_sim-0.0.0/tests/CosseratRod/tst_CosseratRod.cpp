#include <catch2/catch_all.hpp>

#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/utility_functions.hpp>

#include <Mandos/Core/Energies/CosseratBendingRod.hpp>
#include <Mandos/Core/Energies/CosseratRodAlignment.hpp>
#include <Mandos/Core/Energies/MassSpring.hpp>

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

#include <TinyAD/Scalar.hh>
#include <TinyAD/ScalarFunction.hh>

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

TEST_CASE("COSSERAT ROD ENERGY DERIVATIVES")
{
    mandos::core::MechanicalState<mandos::core::RigidBodyTag> mstate;
    mstate.m_x.resize(3);
    mstate.m_v.resize(3, mandos::core::Vec6::Zero());
    mstate.m_grad.resize(3);
    mstate.m_hessian.resize(mstate.size(), mstate.size());

    mstate.clearGradient();
    mstate.clearHessian();

    mstate.m_x[0] = mandos::core::Vec6(0.0, 0.0, 2.0, 0.0, 0.0, 0.0);
    mstate.m_x[1] = mandos::core::Vec6(0.0, 0.0, 1.0, 0.0, 0.0, 0.0);
    mstate.m_x[2] = mandos::core::Vec6(0.0, 0.0, 0.0, 0.0, 0.0, 0.0);

    const Eigen::Matrix<int, 2, 2> indices{{0, 1}, {1, 2}};

    const mandos::core::Scalar L0 = 2.0;
    const mandos::core::Scalar Ks = 100.0;
    const mandos::core::Scalar cosseratStiffness = 100.0;
    const mandos::core::Vec3 stiffnessTensor = 1.0 * mandos::core::Vec3::Ones();

    mandos::core::MassSpring massSpringEnergy;
    massSpringEnergy.addElement({0, 1}, {L0, Ks});
    massSpringEnergy.addElement({1, 2}, {L0, Ks});

    mandos::core::CosseratBendingRod cosseratBendingRodEnergy;
    cosseratBendingRodEnergy.addElement(
        {0, 1},
        mandos::core::CosseratBendingRod::ParameterSet{
            L0,
            mandos::core::computeDarbouxVector(L0,
                                               mandos::core::rotationExpMap(mstate.m_x[0].segment<3>(0).eval()),
                                               mandos::core::rotationExpMap(mstate.m_x[1].segment<3>(0).eval())),
            stiffnessTensor});

    mandos::core::CosseratRodAlignment cosseratRodAlignmentEnergy;
    cosseratRodAlignmentEnergy.addElement({0, 1}, {L0, cosseratStiffness});
    cosseratRodAlignmentEnergy.addElement({1, 2}, {L0, cosseratStiffness});

    // Damping = 0
    constexpr auto nTests = 1024;
    const auto size = mstate.m_x.size();

    auto deformation = Catch::Generators::generate("displacement generator", CATCH_INTERNAL_LINEINFO, [size, nTests] {
        // NOLINTNEXTLINE
        using namespace Catch::Generators;
        return makeGenerators(take(nTests,
                                   map(
                                       [size](const auto &) {
                                           return (0.01 *
                                                   Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6>::Random(
                                                       static_cast<Eigen::Index>(size), 6))
                                               .eval();
                                       },
                                       range(0, nTests))));
    });

    Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::MapType(
        mstate.m_x.data()->data(), static_cast<Eigen::Index>(size), 6) += deformation;

    const Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6> vertices{
        Eigen::Matrix<mandos::core::Scalar, Eigen::Dynamic, 6, Eigen::RowMajor>::MapType(
            mstate.m_x.data()->data(), static_cast<Eigen::Index>(mstate.m_x.size()), 6)};

    auto func = TinyAD::scalar_function<6>(TinyAD::range(vertices.rows()));
    func.add_elements<2>(TinyAD::range(indices.rows()), [&](auto &element) -> TINYAD_SCALAR_TYPE(element) {
        using T = TINYAD_SCALAR_TYPE(element);
        auto segmentId = element.handle;

        // Energy parameters
        const auto massSpringParameterSet = massSpringEnergy.getParameterSet(static_cast<int>(segmentId));
        const auto cosseratRodAlignmentParameterSet =
            cosseratRodAlignmentEnergy.getParameterSet(static_cast<int>(segmentId));
        const mandos::core::Scalar elementL0 = massSpringParameterSet.restLength;
        const mandos::core::Scalar elementKs = massSpringParameterSet.stiffness;
        const mandos::core::Scalar elementCosseratStiffness = cosseratRodAlignmentParameterSet.cosseratStiffness;

        // Degrees of freedom
        const Eigen::Vector<T, 6> x0 = element.variables(indices(segmentId, 0));
        const Eigen::Vector<T, 6> x1 = element.variables(indices(segmentId, 1));

        const Eigen::Vector<T, 3> xA = x0.template segment<3>(0);
        const Eigen::Vector<T, 3> xB = x1.template segment<3>(0);

        Eigen::Vector<T, 3> thetaA = x0.template segment<3>(3);
        Eigen::Vector<T, 3> thetaB = x1.template segment<3>(3);

        const mandos::core::Vec3 thetaAvalue = TinyAD::to_passive(thetaA);
        const mandos::core::Vec3 thetaBvalue = TinyAD::to_passive(thetaB);

        // Zero recentering
        thetaA = thetaA - thetaAvalue;
        thetaB = thetaB - thetaBvalue;

        const Eigen::Matrix3<T> RA = rotationExpMap0(thetaA) * mandos::core::rotationExpMap(thetaAvalue);
        const Eigen::Matrix3<T> RB = rotationExpMap0(thetaB) * mandos::core::rotationExpMap(thetaBvalue);

        // Stretch Energy
        const T L = (xA - xB).norm();
        const T Vs = 0.5 * elementKs / elementL0 * (L - elementL0) * (L - elementL0);

        // Bending Energy
        T Vb = 0;
        // We have a bending rod element less than segments, so ensure we are not out of bounds
        if (segmentId < cosseratBendingRodEnergy.size()) {
            const auto cosseratBendingRodParameterSet =
                cosseratBendingRodEnergy.getParameterSet(static_cast<int>(segmentId));
            const mandos::core::Vec3 elementStiffnessTensor = cosseratBendingRodParameterSet.stiffnessTensor;
            const mandos::core::Vec3 elementIntrinsicDarboux = cosseratBendingRodParameterSet.intrinsicDarboux;

            // Bending Energy
            const mandos::core::Mat3 J =
                0.5 *
                mandos::core::Vec3(-elementStiffnessTensor(0) + elementStiffnessTensor(1) + elementStiffnessTensor(2),
                                   elementStiffnessTensor(0) - elementStiffnessTensor(1) + elementStiffnessTensor(2),
                                   elementStiffnessTensor(0) + elementStiffnessTensor(1) - elementStiffnessTensor(2))
                    .asDiagonal();

            const mandos::core::Mat3 Ak = 0.5 * (mandos::core::skew(elementIntrinsicDarboux) * J +
                                                 J * mandos::core::skew(elementIntrinsicDarboux));
            const mandos::core::Mat3 JAk = J / elementL0 + Ak;
            Vb = -(RB.transpose() * RA * JAk).trace();
        }

        // Cosserat Constraint Energy
        const Eigen::Vector3<T> u = ((xA - xB) / (xA - xB).norm()).eval();
        const T Vc = -elementL0 * elementCosseratStiffness * RA.col(2).dot(u);

        return Vs + Vb + Vc;
    });

    const auto originalParameterSetMassSpring0 = massSpringEnergy.getParameterSet(0);
    const auto originalParameterSetMassSpring1 = massSpringEnergy.getParameterSet(1);
    const auto originalParameterSetBending0 = cosseratBendingRodEnergy.getParameterSet(0);
    const auto originalParameterSetCosserat0 = cosseratRodAlignmentEnergy.getParameterSet(0);
    const auto originalParameterSetCosserat1 = cosseratRodAlignmentEnergy.getParameterSet(1);

    SECTION("STRETCH ENERGY")
    {
        // Disable other energies
        {
            auto parameterSet = originalParameterSetBending0;
            parameterSet.stiffnessTensor.setZero();
            cosseratBendingRodEnergy.setParameterSet(0, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetCosserat0;
            parameterSet.cosseratStiffness = 0;
            cosseratRodAlignmentEnergy.setParameterSet(0, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetCosserat1;
            parameterSet.cosseratStiffness = 0;
            cosseratRodAlignmentEnergy.setParameterSet(1, parameterSet);
        }

        // TinyAD derivatives
        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        // Simulator derivatives

        // Check energy
        auto energy = massSpringEnergy.computeEnergy(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy and gradient
        mstate.clearGradient();
        energy = massSpringEnergy.computeEnergyAndGradient(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy, gradient and hessian
        mstate.clearGradient();
        mstate.clearHessian();
        energy = massSpringEnergy.computeEnergyGradientAndHessian(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.m_hessian - mandos::core::SparseMat(hessAD)).cwiseAbs().squaredNorm(),
                     Catch::Matchers::WithinAbs(0, 1e-8));
    }

    massSpringEnergy.setParameterSet(0, originalParameterSetMassSpring0);
    massSpringEnergy.setParameterSet(1, originalParameterSetMassSpring1);
    cosseratBendingRodEnergy.setParameterSet(0, originalParameterSetBending0);
    cosseratRodAlignmentEnergy.setParameterSet(0, originalParameterSetCosserat0);
    cosseratRodAlignmentEnergy.setParameterSet(1, originalParameterSetCosserat1);

    SECTION("BENDING ENERGY")
    {
        // Disable other energies
        {
            auto parameterSet = originalParameterSetMassSpring0;
            parameterSet.stiffness = 0;
            massSpringEnergy.setParameterSet(0, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetMassSpring1;
            parameterSet.stiffness = 0;
            massSpringEnergy.setParameterSet(1, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetCosserat0;
            parameterSet.cosseratStiffness = 0;
            cosseratRodAlignmentEnergy.setParameterSet(0, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetCosserat1;
            parameterSet.cosseratStiffness = 0;
            cosseratRodAlignmentEnergy.setParameterSet(1, parameterSet);
        }

        // TinyAD derivatives
        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        // Simulator derivatives

        // Check energy
        auto energy = cosseratBendingRodEnergy.computeEnergy(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy and gradient
        mstate.clearGradient();
        energy = cosseratBendingRodEnergy.computeEnergyAndGradient(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy, gradient and hessian
        mstate.clearGradient();
        mstate.clearHessian();
        energy = cosseratBendingRodEnergy.computeEnergyGradientAndHessian(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.m_hessian - mandos::core::SparseMat(hessAD)).cwiseAbs().squaredNorm(),
                     Catch::Matchers::WithinAbs(0, 1e-8));
    }

    massSpringEnergy.setParameterSet(0, originalParameterSetMassSpring0);
    massSpringEnergy.setParameterSet(1, originalParameterSetMassSpring1);
    cosseratBendingRodEnergy.setParameterSet(0, originalParameterSetBending0);
    cosseratRodAlignmentEnergy.setParameterSet(0, originalParameterSetCosserat0);
    cosseratRodAlignmentEnergy.setParameterSet(1, originalParameterSetCosserat1);

    SECTION("COSSERAT CONSTRAINT ENERGY")
    {
        // Disable other energies
        {
            auto parameterSet = originalParameterSetMassSpring0;
            parameterSet.stiffness = 0;
            massSpringEnergy.setParameterSet(0, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetMassSpring1;
            parameterSet.stiffness = 0;
            massSpringEnergy.setParameterSet(1, parameterSet);
        }

        {
            auto parameterSet = originalParameterSetBending0;
            parameterSet.stiffnessTensor.setZero();
            cosseratBendingRodEnergy.setParameterSet(0, parameterSet);
        }

        // TinyAD derivatives
        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        // Simulator derivatives
        // Check energy
        auto energy = cosseratRodAlignmentEnergy.computeEnergy(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy and gradient
        mstate.clearGradient();
        energy = cosseratRodAlignmentEnergy.computeEnergyAndGradient(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy, gradient and hessian
        mstate.clearGradient();
        mstate.clearHessian();
        energy = cosseratRodAlignmentEnergy.computeEnergyGradientAndHessian(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.m_hessian - mandos::core::SparseMat(hessAD)).cwiseAbs().squaredNorm(),
                     Catch::Matchers::WithinAbs(0, 1e-8));
    }

    massSpringEnergy.setParameterSet(0, originalParameterSetMassSpring0);
    massSpringEnergy.setParameterSet(1, originalParameterSetMassSpring1);
    cosseratBendingRodEnergy.setParameterSet(0, originalParameterSetBending0);
    cosseratRodAlignmentEnergy.setParameterSet(0, originalParameterSetCosserat0);
    cosseratRodAlignmentEnergy.setParameterSet(1, originalParameterSetCosserat1);

    SECTION("TOTAL ENERGY")
    {
        // TinyAD derivatives
        auto [energyAD, gradAD, hessAD] =
            func.eval_with_derivatives(func.x_from_data([&](int vIdx) { return vertices.row(vIdx); }));

        // Simulator derivatives
        // Check energy
        auto energy = massSpringEnergy.computeEnergy(mstate) +          //
                      cosseratBendingRodEnergy.computeEnergy(mstate) +  //
                      cosseratRodAlignmentEnergy.computeEnergy(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy and gradient
        mstate.clearGradient();
        energy = massSpringEnergy.computeEnergyAndGradient(mstate) +          //
                 cosseratBendingRodEnergy.computeEnergyAndGradient(mstate) +  //
                 cosseratRodAlignmentEnergy.computeEnergyAndGradient(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));

        // Check energy, gradient and hessian
        mstate.clearGradient();
        mstate.clearHessian();
        energy = massSpringEnergy.computeEnergyGradientAndHessian(mstate) +          //
                 cosseratBendingRodEnergy.computeEnergyGradientAndHessian(mstate) +  //
                 cosseratRodAlignmentEnergy.computeEnergyGradientAndHessian(mstate);
        REQUIRE_THAT(energy - energyAD, Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.gradientView() - gradAD).cwiseAbs().squaredNorm(), Catch::Matchers::WithinAbs(0, 1e-8));
        REQUIRE_THAT((mstate.m_hessian - mandos::core::SparseMat(hessAD)).cwiseAbs().squaredNorm(),
                     Catch::Matchers::WithinAbs(0, 1e-8));
    }
}
