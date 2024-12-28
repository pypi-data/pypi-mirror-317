#include <Mandos/Core/Energies/CosseratBendingRod.hpp>

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/RotationUtilities.hpp>

#include <fmt/format.h>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

Vec3 computeDarbouxVector(Scalar L0, const Mat3 &R1, const Mat3 &R2)
{
    const Mat3 dR_dx = (R2 - R1) / L0;
    const Mat3 R = (R1 + R2) / 2.0;
    const Mat3 skew_u = R.transpose() * dR_dx;
    return mandos::core::unskew(skew_u);
}

Scalar CosseratBendingRod::computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    std::vector<Triplet> triplets;
    for (auto i = 0UL; i < static_cast<size_t>(size()); ++i) {
        const auto iA = static_cast<std::size_t>(m_indices[i][0]);
        const auto iB = static_cast<std::size_t>(m_indices[i][1]);

        const Mat3 RA = mandos::core::rotationExpMap(mstate.m_x[iA].segment<3>(3));
        const Mat3 RB = mandos::core::rotationExpMap(mstate.m_x[iB].segment<3>(3));
        const auto &stiffnessTensor = m_stiffnessTensor[i];
        const Mat3 J = 0.5 * Vec3(-stiffnessTensor(0) + stiffnessTensor(1) + stiffnessTensor(2),
                                  stiffnessTensor(0) - stiffnessTensor(1) + stiffnessTensor(2),
                                  stiffnessTensor(0) + stiffnessTensor(1) - stiffnessTensor(2))
                                 .asDiagonal();

        const Mat3 Ak =
            0.5 * (mandos::core::skew(m_intrinsicDarboux[i]) * J + J * mandos::core::skew(m_intrinsicDarboux[i]));
        const Mat3 JAk = J * mandos::core::Scalar{1.0} / m_restLength[i] + Ak;
        energy += -(RB.transpose() * RA * JAk).trace();  // Bending energy

        const Mat3 RBA_J = RB.transpose() * RA * JAk;
        const Mat3 A = 0.5 * (RBA_J - RBA_J.transpose());
        const Mat3 &S = 0.5 * (RBA_J + RBA_J.transpose());

        const Vec3 gradVb = 2.0 * RB * mandos::core::unskew(A);

        mstate.m_grad[iA].segment<3>(3) += gradVb;
        mstate.m_grad[iB].segment<3>(3) -= gradVb;

        const Mat3 &hessVb = RB * (S.trace() * Mat3::Identity() - S) * RB.transpose();
        const Mat3 M = RA * JAk * RB.transpose();
        const Mat3 &hessVbAB = -(M.trace() * Mat3::Identity() - M);

        Mat6 hessianA = Mat6::Zero();
        Mat6 hessianB = Mat6::Zero();
        Mat6 hessianAB = Mat6::Zero();

        hessianA.block<3, 3>(3, 3) += hessVb;
        hessianB.block<3, 3>(3, 3) += hessVb;
        hessianAB.block<3, 3>(3, 3) += hessVbAB.transpose();

        // Construct Sparse hessian
        // ---------------------------------------------------------------
        for (auto k = 0; k < 6; k++) {
            for (auto j = 0; j < 6; j++) {
                triplets.emplace_back(
                    6 * static_cast<Eigen::Index>(iA) + k, 6 * static_cast<Eigen::Index>(iA) + j, hessianA(k, j));
                triplets.emplace_back(
                    6 * static_cast<Eigen::Index>(iA) + k, 6 * static_cast<Eigen::Index>(iB) + j, hessianAB(k, j));
                triplets.emplace_back(
                    6 * static_cast<Eigen::Index>(iB) + k, 6 * static_cast<Eigen::Index>(iA) + j, hessianAB(j, k));
                triplets.emplace_back(
                    6 * static_cast<Eigen::Index>(iB) + k, 6 * static_cast<Eigen::Index>(iB) + j, hessianB(k, j));
            }
        }
    }

    SparseMat energyHessian;
    energyHessian.resize(mstate.size(), mstate.size());
    energyHessian.setFromTriplets(triplets.begin(), triplets.end());
    mstate.m_hessian += energyHessian;

    return energy;
}
Scalar CosseratBendingRod::computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const auto iA = static_cast<std::size_t>(m_indices[i][0]);
        const auto iB = static_cast<std::size_t>(m_indices[i][1]);

        const Mat3 RA = mandos::core::rotationExpMap(mstate.m_x[iA].segment<3>(3));
        const Mat3 RB = mandos::core::rotationExpMap(mstate.m_x[iB].segment<3>(3));
        const auto &stiffnessTensor = m_stiffnessTensor[i];

        const Mat3 J = 0.5 * Vec3(-stiffnessTensor(0) + stiffnessTensor(1) + stiffnessTensor(2),
                                  stiffnessTensor(0) - stiffnessTensor(1) + stiffnessTensor(2),
                                  stiffnessTensor(0) + stiffnessTensor(1) - stiffnessTensor(2))
                                 .asDiagonal();

        const Mat3 Ak =
            0.5 * (mandos::core::skew(m_intrinsicDarboux[i]) * J + J * mandos::core::skew(m_intrinsicDarboux[i]));
        const Mat3 JAk = J * mandos::core::Scalar{1.0} / m_restLength[i] + Ak;
        energy += -(RB.transpose() * RA * JAk).trace();  // Bending energy
    }
    return energy;
}
Scalar CosseratBendingRod::computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<size_t>(size()); ++i) {
        const auto iA = static_cast<std::size_t>(m_indices[i][0]);
        const auto iB = static_cast<std::size_t>(m_indices[i][1]);

        const Mat3 RA = mandos::core::rotationExpMap(mstate.m_x[iA].segment<3>(3));
        const Mat3 RB = mandos::core::rotationExpMap(mstate.m_x[iB].segment<3>(3));
        const auto &stiffnessTensor = m_stiffnessTensor[i];
        const Mat3 J = 0.5 * Vec3(-stiffnessTensor(0) + stiffnessTensor(1) + stiffnessTensor(2),
                                  stiffnessTensor(0) - stiffnessTensor(1) + stiffnessTensor(2),
                                  stiffnessTensor(0) + stiffnessTensor(1) - stiffnessTensor(2))
                                 .asDiagonal();

        const Mat3 Ak =
            0.5 * (mandos::core::skew(m_intrinsicDarboux[i]) * J + J * mandos::core::skew(m_intrinsicDarboux[i]));
        const Mat3 JAk = J * mandos::core::Scalar{1.0} / m_restLength[i] + Ak;
        energy += -(RB.transpose() * RA * JAk).trace();  // Bending energy

        const Mat3 RBA_J = RB.transpose() * RA * JAk;
        const Mat3 A = 0.5 * (RBA_J - RBA_J.transpose());

        const Vec3 gradVb = 2.0 * RB * mandos::core::unskew(A);

        mstate.m_grad[iA].segment<3>(3) += gradVb;
        mstate.m_grad[iB].segment<3>(3) -= gradVb;
    }
    return energy;
}
int CosseratBendingRod::size() const
{
    return static_cast<int>(m_indices.size());
}
MANDOS_CORE_EXPORT void CosseratBendingRod::setParameterSet(int elementId, const ParameterSet &parameterSet)
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Can't set ParameterSet for element ({}). Energy container {}  elements", elementId, size()));
    }
    m_stiffnessTensor[static_cast<std::size_t>(elementId)] = parameterSet.stiffnessTensor;
    m_intrinsicDarboux[static_cast<std::size_t>(elementId)] = parameterSet.intrinsicDarboux;
    m_restLength[static_cast<std::size_t>(elementId)] = parameterSet.restLength;
}
MANDOS_CORE_EXPORT CosseratBendingRod::ParameterSet CosseratBendingRod::getParameterSet(int elementId) const
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Requested ParameterSet ({}) exceeds number of elements in energy ({})", elementId, size()));
    }

    return {
        m_restLength[static_cast<std::size_t>(elementId)],
        m_intrinsicDarboux[static_cast<std::size_t>(elementId)],
        m_stiffnessTensor[static_cast<std::size_t>(elementId)],  //
    };
}
MANDOS_CORE_EXPORT void CosseratBendingRod::addElement(const std::array<int, 2> &indices,
                                                       const ParameterSet &parameterSet)
{
    m_indices.push_back(indices);
    m_stiffnessTensor.push_back(parameterSet.stiffnessTensor);
    m_intrinsicDarboux.push_back(parameterSet.intrinsicDarboux);
    m_restLength.push_back(parameterSet.restLength);
}
CosseratBendingRod::ParameterSet::ParameterSet(mandos::core::Scalar restLength_,
                                               const mandos::core::Vec3 &intrinsicDarboux_,
                                               const mandos::core::Vec3 &stiffnessTensor_)
    : restLength(restLength_)
    , intrinsicDarboux(intrinsicDarboux_)
    , stiffnessTensor(stiffnessTensor_)
{
}
CosseratBendingRod::ParameterSet::ParameterSet(const std::array<Vec6, 2> &x0,
                                               const mandos::core::Vec3 &stiffnessTensor_)
    : restLength((x0[0] - x0[1]).segment<3>(0).norm())
    , stiffnessTensor(stiffnessTensor_)
{
    intrinsicDarboux =
        computeDarbouxVector(restLength, rotationExpMap(x0[0].segment<3>(3)), rotationExpMap(x0[1].segment<3>(3)));
}
CosseratBendingRod::ParameterSet::ParameterSet(const Mat26 &x0, const mandos::core::Vec3 &stiffnessTensor_)
    : restLength((x0.row(0) - x0.row(1)).segment<3>(0).norm())
    , stiffnessTensor(stiffnessTensor_)
{
    intrinsicDarboux = computeDarbouxVector(
        restLength, rotationExpMap(x0.row(0).segment<3>(3)), rotationExpMap(x0.row(1).segment<3>(3)));
}
}  // namespace mandos::core
