#include <Mandos/Core/Energies/GravityEnergy.hpp>

namespace mandos::core
{

const std::vector<Scalar> &GravityEnergy::vertexMass() const
{
    return m_vertexMass;
}

std::vector<Scalar> &GravityEnergy::vertexMass()
{
    return m_vertexMass;
}

Scalar GravityEnergy::computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const
{
    auto energy{Scalar{0}};
    if (m_isEnabled) {
        for (auto i = 0UL; i < m_vertexMass.size(); ++i) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].dot(m_gravityVector));
            mstate.m_grad[i] -= m_vertexMass[i] * m_gravityVector;
        }
    }

    return energy;
}

Scalar GravityEnergy::computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const
{
    auto energy{Scalar{0}};
    if (m_isEnabled) {
        for (auto i = 0UL; i < m_vertexMass.size(); ++i) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].dot(m_gravityVector));
            mstate.m_grad[i] -= m_vertexMass[i] * m_gravityVector;
        }
    }

    return energy;
}

Scalar GravityEnergy::computeEnergy(const MechanicalState<Particle3DTag> &mstate) const
{
    auto energy{Scalar{0}};
    if (m_isEnabled) {
        for (auto i = 0UL; i < m_vertexMass.size(); ++i) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].dot(m_gravityVector));
        }
    }

    return energy;
}

const Vec3 &GravityEnergy::gravityVector() const
{
    return m_gravityVector;
}

void GravityEnergy::setGravityVector(const Vec3 &gravityVector)
{
    m_gravityVector = gravityVector;
}

Scalar GravityEnergy::computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    if (m_isEnabled) {
        for (unsigned int i = 0; i < m_vertexMass.size(); ++i) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].segment<3>(0).dot(m_gravityVector));
        }
    }
    return energy;
}

Scalar GravityEnergy::computeEnergy(const MechanicalState<RigidBodyGlobalTag> &mstate) const
{
    Scalar energy{0};
    if (m_isEnabled) {
        for (unsigned int i = 0; i < m_vertexMass.size(); ++i) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].segment<3>(0).dot(m_gravityVector));
        }
    }
    return energy;
}

Scalar GravityEnergy::computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const
{
    Scalar energy{0};
    if (m_isEnabled) {
        for (unsigned int i = 0; i < m_vertexMass.size(); i++) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].segment<3>(0).dot(m_gravityVector));
            mstate.m_grad[i].segment<3>(0) -= m_vertexMass[i] * m_gravityVector;
        }
    }
    return energy;
}

Scalar GravityEnergy::computeEnergyAndGradient(MechanicalState<RigidBodyGlobalTag> &mstate) const
{
    Scalar energy{0};
    if (m_isEnabled) {
        for (unsigned int i = 0; i < m_vertexMass.size(); i++) {
            energy -= m_vertexMass[i] * (mstate.m_x[i].segment<3>(0).dot(m_gravityVector));
            mstate.m_grad[i].segment<3>(0) -= m_vertexMass[i] * m_gravityVector;
        }
    }
    return energy;
}

Scalar GravityEnergy::computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const
{
    return computeEnergyAndGradient(mstate);
}

Scalar GravityEnergy::computeEnergyGradientAndHessian(MechanicalState<RigidBodyGlobalTag> &mstate) const
{
    return computeEnergyAndGradient(mstate);
}

void GravityEnergy::disable()
{
    m_isEnabled = false;
}

void GravityEnergy::enable()
{
    m_isEnabled = true;
}

bool GravityEnergy::isEnabled() const
{
    return m_isEnabled;
}

}  // namespace mandos::core
