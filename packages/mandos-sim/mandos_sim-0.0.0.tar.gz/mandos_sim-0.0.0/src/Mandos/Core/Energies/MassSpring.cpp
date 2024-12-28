#include <Mandos/Core/Energies/MassSpring.hpp>

#include <Mandos/Core/linear_algebra.hpp>

#include <limits>

#include <fmt/format.h>

namespace
{
mandos::core::Scalar computeEnergy(const mandos::core::Vec3 &xA,
                                   const mandos::core::Vec3 &xB,
                                   mandos::core::Scalar stiffness,
                                   mandos::core::Scalar /*damping*/,
                                   mandos::core::Scalar restLength)
{
    const mandos::core::Scalar L = (xA - xB).norm();

    // TODO add "damping potential"
    if (restLength > std::numeric_limits<mandos::core::Scalar>::epsilon()) {
        stiffness = stiffness / restLength;
    }
    return 0.5 * stiffness * (L - restLength) * (L - restLength);
}

std::tuple<mandos::core::Scalar, mandos::core::Vec3> computeEnergyAndGradient(const mandos::core::Vec3 &xA,
                                                                              const mandos::core::Vec3 &xB,
                                                                              mandos::core::Scalar stiffness,
                                                                              mandos::core::Scalar /*damping*/,
                                                                              mandos::core::Scalar restLength)
{
    const mandos::core::Scalar L = (xA - xB).norm();
    const mandos::core::Vec3 u = (xA - xB) / L;

    if (restLength > std::numeric_limits<mandos::core::Scalar>::epsilon()) {
        stiffness = stiffness / restLength;
    }

    const mandos::core::Vec3 grad = stiffness * (L - restLength) * u;  // Elastic gradient
    const auto energy = 0.5 * stiffness * (L - restLength) * (L - restLength);

    return {energy, grad};
}
std::tuple<mandos::core::Scalar, mandos::core::Vec3, mandos::core::Mat3> computeEnergyGradientAndHessian(
    const mandos::core::Vec3 &xA,
    const mandos::core::Vec3 &xB,
    mandos::core::Scalar stiffness,
    mandos::core::Scalar /*damping*/,
    mandos::core::Scalar restLength)
{
    const mandos::core::Scalar L = (xA - xB).norm();
    const mandos::core::Vec3 u = (xA - xB) / L;
    const mandos::core::Mat3 uut = u * u.transpose();

    if (restLength > std::numeric_limits<mandos::core::Scalar>::epsilon()) {
        stiffness = stiffness / restLength;
    }

    const mandos::core::Vec3 grad = stiffness * (L - restLength) * u;  // Elastic gradient
    const auto energy = 0.5 * stiffness * (L - restLength) * (L - restLength);
    const mandos::core::Mat3 hessian =
        stiffness / L * ((L - restLength) * mandos::core::Mat3::Identity() + restLength * uut);
    return {energy, grad, hessian};
}
}  // namespace

namespace mandos::core
{

int MassSpring::size() const
{
    return static_cast<int>(m_indices.size());
}

Scalar MassSpring::computeEnergy(const MechanicalState<Particle3DTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const Vec3 xA = mstate.m_x[static_cast<std::size_t>(m_indices[i][0])];
        const Vec3 xB = mstate.m_x[static_cast<std::size_t>(m_indices[i][1])];
        energy += ::computeEnergy(xA, xB, m_stiffness[i], m_damping[i], m_restLength[i]);
    }
    return energy;
}

Scalar MassSpring::computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const Vec3 xA = mstate.m_x[static_cast<std::size_t>(m_indices[i][0])].segment<3>(0);
        const Vec3 xB = mstate.m_x[static_cast<std::size_t>(m_indices[i][1])].segment<3>(0);

        // TODO add "damping potential"
        energy += ::computeEnergy(xA, xB, m_stiffness[i], m_damping[i], m_restLength[i]);
    }
    return energy;
}

Scalar MassSpring::computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const auto &indices{m_indices[i]};
        const Vec3 xA = mstate.m_x[static_cast<std::size_t>(indices[0])];
        const Vec3 xB = mstate.m_x[static_cast<std::size_t>(indices[1])];

        const auto [lenergy, grad] = ::computeEnergyAndGradient(xA, xB, m_stiffness[i], m_damping[i], m_restLength[i]);
        energy += lenergy;

        mstate.m_grad[static_cast<std::size_t>(indices[0])] += grad;
        mstate.m_grad[static_cast<std::size_t>(indices[1])] -= grad;

        // TODO add "damping potential"
    }
    return energy;
}

Scalar MassSpring::computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const auto &indices{m_indices[i]};
        const Vec3 xA = mstate.m_x[static_cast<std::size_t>(indices[0])].segment<3>(0);
        const Vec3 xB = mstate.m_x[static_cast<std::size_t>(indices[1])].segment<3>(0);

        const auto [lenergy, grad] = ::computeEnergyAndGradient(xA, xB, m_stiffness[i], m_damping[i], m_restLength[i]);
        energy += lenergy;

        mstate.m_grad[static_cast<std::size_t>(indices[0])].segment<3>(0) += grad;
        mstate.m_grad[static_cast<std::size_t>(indices[1])].segment<3>(0) -= grad;
    }
    return energy;
}

Scalar MassSpring::computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const
{
    Scalar energy{0};
    std::vector<Triplet> triplets;
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const auto &indices{m_indices[i]};
        const Vec3 xA = mstate.m_x[static_cast<std::size_t>(indices[0])];
        const Vec3 xB = mstate.m_x[static_cast<std::size_t>(indices[1])];

        const auto [lenergy, grad, hessian] =
            ::computeEnergyGradientAndHessian(xA, xB, m_stiffness[i], m_damping[i], m_restLength[i]);
        energy += lenergy;

        mstate.m_grad[static_cast<std::size_t>(indices[0])] += grad;
        mstate.m_grad[static_cast<std::size_t>(indices[1])] -= grad;

        for (auto j = 0; j < 3; ++j) {
            for (auto k = 0; k < 3; ++k) {
                triplets.emplace_back(3 * indices[0] + j, 3 * indices[0] + k, hessian(j, k));
                triplets.emplace_back(3 * indices[0] + j, 3 * indices[1] + k, -hessian(j, k));
                triplets.emplace_back(3 * indices[1] + j, 3 * indices[0] + k, -hessian(j, k));
                triplets.emplace_back(3 * indices[1] + j, 3 * indices[1] + k, hessian(j, k));
            }
        }
    }

    SparseMat energyHessian;
    energyHessian.resize(mstate.size(), mstate.size());
    energyHessian.setFromTriplets(triplets.begin(), triplets.end());
    mstate.m_hessian += energyHessian;

    return energy;
}

Scalar MassSpring::computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    std::vector<Triplet> triplets;
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        const auto &indices{m_indices[i]};
        const Vec3 xA = mstate.m_x[static_cast<std::size_t>(indices[0])].segment<3>(0);
        const Vec3 xB = mstate.m_x[static_cast<std::size_t>(indices[1])].segment<3>(0);

        const auto [lenergy, grad, hessian] =
            ::computeEnergyGradientAndHessian(xA, xB, m_stiffness[i], m_damping[i], m_restLength[i]);
        energy += lenergy;

        mstate.m_grad[static_cast<std::size_t>(indices[0])].segment<3>(0) += grad;
        mstate.m_grad[static_cast<std::size_t>(indices[1])].segment<3>(0) -= grad;

        for (auto j = 0; j < 3; ++j) {
            for (auto k = 0; k < 3; ++k) {
                triplets.emplace_back(6 * indices[0] + j, 6 * indices[0] + k, hessian(j, k));
                triplets.emplace_back(6 * indices[0] + j, 6 * indices[1] + k, -hessian(j, k));
                triplets.emplace_back(6 * indices[1] + j, 6 * indices[0] + k, -hessian(j, k));
                triplets.emplace_back(6 * indices[1] + j, 6 * indices[1] + k, hessian(j, k));
            }
        }
    }

    SparseMat energyHessian;
    energyHessian.resize(mstate.size(), mstate.size());
    energyHessian.setFromTriplets(triplets.begin(), triplets.end());
    mstate.m_hessian += energyHessian;

    return energy;
}

void MassSpring::addElement(const std::array<int, 2> &indices, const ParameterSet &parameterSet)
{
    // Store parameters
    m_indices.push_back(indices);
    m_stiffness.push_back(parameterSet.stiffness);
    m_damping.push_back(parameterSet.damping);
    m_restLength.push_back(parameterSet.restLength);
}

MassSpring::ParameterSet MassSpring::getParameterSet(int elementId) const
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Requested ParameterSet ({}) exceeds number of elements in energy ({})", elementId, size()));
    }

    return {m_restLength[static_cast<std::size_t>(elementId)],
            m_stiffness[static_cast<std::size_t>(elementId)],  //
            m_damping[static_cast<std::size_t>(elementId)]};
}
void MassSpring::setParameterSet(int elementId, const ParameterSet &parameterSet)
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Can't set ParameterSet for element ({}). Energy container {}  elements", elementId, size()));
    }
    m_stiffness[static_cast<std::size_t>(elementId)] = parameterSet.stiffness;
    m_damping[static_cast<std::size_t>(elementId)] = parameterSet.damping;
    m_restLength[static_cast<std::size_t>(elementId)] = parameterSet.restLength;
}
MassSpring::ParameterSet::ParameterSet(mandos::core::Scalar restLength_,
                                       mandos::core::Scalar stiffness_,
                                       mandos::core::Scalar damping_)
    : restLength(restLength_)
    , stiffness(stiffness_)
    , damping(damping_)
{
}
MassSpring::ParameterSet::ParameterSet(const std::array<Vec3, 2> &x0,
                                       mandos::core::Scalar stiffness_,
                                       mandos::core::Scalar damping_)
    : restLength((x0[1] - x0[0]).norm())
    , stiffness(stiffness_)
    , damping(damping_)
{
}
MassSpring::ParameterSet::ParameterSet(const Mat23 &x0, mandos::core::Scalar stiffness_, mandos::core::Scalar damping_)
    : restLength((x0.row(1) - x0.row(0)).norm())
    , stiffness(stiffness_)
    , damping(damping_)
{
}
}  // namespace mandos::core
