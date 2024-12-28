#include <Mandos/Core/Energies/CosseratRodAlignment.hpp>

#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/utility_functions.hpp>

#include <TinyAD/Utils/HessianProjection.hh>

#include <fmt/format.h>

#include <cmath>

namespace mandos::core
{

int CosseratRodAlignment::size() const
{
    return static_cast<int>(m_indices.size());
}

Scalar CosseratRodAlignment::computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<size_t>(size()); ++i) {
        const auto iA = static_cast<std::size_t>(m_indices[i][0]);
        const auto iB = static_cast<std::size_t>(m_indices[i][1]);

        // Get the relevant sate
        // ---------------------------------------------------------------
        const Vec3 xA = mstate.m_x[iA].segment<3>(0);
        const Vec3 xB = mstate.m_x[iB].segment<3>(0);
        const Mat3 RA = mandos::core::rotationExpMap(mstate.m_x[iA].segment<3>(3));

        energy += -m_restLength[i] * m_cosseratStiffness[i] * RA.col(2).dot((xA - xB).normalized());
    }
    return energy;
}

Scalar CosseratRodAlignment::computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<size_t>(size()); ++i) {
        const auto iA = static_cast<std::size_t>(m_indices[i][0]);
        const auto iB = static_cast<std::size_t>(m_indices[i][1]);

        // Get the relevant sate
        // ---------------------------------------------------------------
        const Vec3 xA = mstate.m_x[iA].segment<3>(0);
        const Vec3 xB = mstate.m_x[iB].segment<3>(0);
        const Mat3 RA = mandos::core::rotationExpMap(mstate.m_x[iA].segment<3>(3));

        const auto oneOverL = mandos::core::Scalar{1.0} / (xA - xB).norm();
        const auto u = ((xA - xB) * oneOverL).eval();
        const auto uut = (u * u.transpose()).eval();

        energy += -m_restLength[i] * m_cosseratStiffness[i] * RA.col(2).dot(u);

        const Vec3 &grad = -m_cosseratStiffness[i] * m_restLength[i] * (Mat3::Identity() - uut) * oneOverL * RA.col(2);
        mstate.m_grad[iA].segment<3>(0) += grad;
        mstate.m_grad[iA].segment<3>(3) +=
            m_cosseratStiffness[i] * m_restLength[i] * u.transpose() * mandos::core::skew(RA.col(2));

        mstate.m_grad[iB].segment<3>(0) -= grad;
    }
    return energy;
}

Scalar CosseratRodAlignment::computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    std::vector<Triplet> triplets;
    for (auto i = 0UL; i < static_cast<size_t>(size()); ++i) {
        const auto iA = static_cast<std::size_t>(m_indices[i][0]);
        const auto iB = static_cast<std::size_t>(m_indices[i][1]);

        // Get the relevant sate
        // ---------------------------------------------------------------
        const Vec3 xA = mstate.m_x[iA].segment<3>(0);
        const Vec3 xB = mstate.m_x[iB].segment<3>(0);
        const Mat3 RA = mandos::core::rotationExpMap(mstate.m_x[iA].segment<3>(3));

        const auto oneOverL = mandos::core::Scalar{1.0} / (xA - xB).norm();
        const auto u = ((xA - xB) * oneOverL).eval();
        const auto uut = (u * u.transpose()).eval();

        energy += -m_restLength[i] * m_cosseratStiffness[i] * RA.col(2).dot(u);

        const Vec3 &grad = -m_cosseratStiffness[i] * m_restLength[i] * (Mat3::Identity() - uut) * oneOverL * RA.col(2);
        mstate.m_grad[iA].segment<3>(0) += grad;
        mstate.m_grad[iA].segment<3>(3) +=
            m_cosseratStiffness[i] * m_restLength[i] * u.transpose() * mandos::core::skew(RA.col(2));

        mstate.m_grad[iB].segment<3>(0) -= grad;

        Mat6 hessianA = Mat6::Zero();
        Mat6 hessianB = Mat6::Zero();
        Mat6 hessianAB = Mat6::Zero();

        const Mat3 &du_dxa = (Mat3::Identity() - uut) * oneOverL;
        const Vec3 &d3 = RA.col(2);

        const Mat3 &d2u_dxa2_d3 =
            oneOverL * oneOverL *
            (u.dot(d3) * (3 * uut - Mat3::Identity()) - (u * d3.transpose() + d3 * u.transpose()));
        const Mat3 &hessEp_dx2 = -m_cosseratStiffness[i] * m_restLength[i] * d2u_dxa2_d3;
        const Mat3 &uRAz = mandos::core::skew(u) * mandos::core::skew(RA.col(2));
        const Mat3 &hessEp_dthetaA2 = -0.5 * m_cosseratStiffness[i] * m_restLength[i] * (uRAz + uRAz.transpose());
        const Mat3 &hessEp_dxdthetaA =
            m_cosseratStiffness[i] * m_restLength[i] * du_dxa * mandos::core::skew(RA.col(2));
        const Mat3 &hessEp_dthetaAdx =
            -m_cosseratStiffness[i] * m_restLength[i] * mandos::core::skew(RA.col(2)) * (-du_dxa);

        hessianA.block<3, 3>(0, 0) += hessEp_dx2;
        hessianA.block<3, 3>(0, 3) += hessEp_dxdthetaA;
        hessianA.block<3, 3>(3, 0) += hessEp_dxdthetaA.transpose();
        hessianA.block<3, 3>(3, 3) += hessEp_dthetaA2;

        hessianB.block<3, 3>(0, 0) += hessEp_dx2;

        hessianAB.block<3, 3>(0, 0) -= hessEp_dx2;
        hessianAB.block<3, 3>(3, 0) += hessEp_dthetaAdx;

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

void CosseratRodAlignment::addElement(const std::array<int, 2> &indices, const ParameterSet &parameterSet)
{
    m_indices.emplace_back(indices);
    m_cosseratStiffness.emplace_back(parameterSet.cosseratStiffness);
    m_restLength.emplace_back(parameterSet.restLength);
}

CosseratRodAlignment::ParameterSet::ParameterSet(mandos::core::Scalar restLength_,
                                                 mandos::core::Scalar cosseratStiffness_)
    : restLength(restLength_)
    , cosseratStiffness(cosseratStiffness_)
{
}
CosseratRodAlignment::ParameterSet::ParameterSet(const Mat26 &x0, mandos::core::Scalar cosseratStiffness_)
    : restLength((x0.row(1).segment<3>(0) - x0.row(1).segment<3>(0)).norm())
    , cosseratStiffness(cosseratStiffness_)
{
}
CosseratRodAlignment::ParameterSet::ParameterSet(const std::array<Vec6, 2> &x0, mandos::core::Scalar cosseratStiffness_)
    : restLength((x0[1].segment<3>(0) - x0[1].segment<3>(0)).norm())
    , cosseratStiffness(cosseratStiffness_)
{
}
MANDOS_CORE_EXPORT void CosseratRodAlignment::setParameterSet(int elementId, const ParameterSet &parameterSet)
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Requested ParameterSet ({}) exceeds number of elements in energy ({})", elementId, size()));
    }

    m_restLength[static_cast<std::size_t>(elementId)] = parameterSet.restLength;
    m_cosseratStiffness[static_cast<std::size_t>(elementId)] = parameterSet.cosseratStiffness;
}

MANDOS_CORE_EXPORT CosseratRodAlignment::ParameterSet CosseratRodAlignment::getParameterSet(int elementId) const
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Requested ParameterSet ({}) exceeds number of elements in energy ({})", elementId, size()));
    }

    return {m_restLength[static_cast<std::size_t>(elementId)],
            m_cosseratStiffness[static_cast<std::size_t>(elementId)]};
}
}  // namespace mandos::core
