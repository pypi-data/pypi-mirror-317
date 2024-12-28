#include <Mandos/Core/Energies/ConstantForce.hpp>

#include <fmt/format.h>

namespace mandos::core
{

int ConstantForce::size() const
{
    return static_cast<int>(m_indices.size());
}

Scalar ConstantForce::computeEnergy(const MechanicalState<Particle3DTag> &mstate) const
{
    auto energy{Scalar{0}};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        energy -= (mstate.m_x[static_cast<std::size_t>(m_indices[i])].dot(m_forceVector[i]));
    }
    return energy;
}

Scalar ConstantForce::computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const
{
    auto energy{Scalar{0}};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        energy -= (mstate.m_x[static_cast<std::size_t>(m_indices[i])].dot(m_forceVector[i]));
        mstate.m_grad[static_cast<std::size_t>(m_indices[i])] -= m_forceVector[i];
    }
    return energy;
}

Scalar ConstantForce::computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const
{
    return ConstantForce::computeEnergyAndGradient(mstate);
}

void ConstantForce::addElement(int index, Vec3 const &forceVector)
{
    // Store parameters
    m_indices.push_back(index);
    m_forceVector.push_back(forceVector);
}

void ConstantForce::setForceVector(int index, Vec3 &newForceVector)
{
    if (index > size()) {
        throw std::runtime_error(
            fmt::format("Requested force vector ({}) exceeds number of forces in energy ({})", index, size()));
    }
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        if (m_indices[i] == index) {
            m_forceVector[i] = newForceVector;
        }
    }
}

Vec3 ConstantForce::getForceVector(int index)
{
    if (index > size()) {
        throw std::runtime_error(
            fmt::format("Requested force vector ({}) exceeds number of forces in energy ({})", index, size()));
    }
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        if (m_indices[i] == index) {
            return m_forceVector[i];
        }
    }
    throw std::invalid_argument("There is no forceVector for this index");
    return Vec3::Zero();
}

}  // namespace mandos::core
