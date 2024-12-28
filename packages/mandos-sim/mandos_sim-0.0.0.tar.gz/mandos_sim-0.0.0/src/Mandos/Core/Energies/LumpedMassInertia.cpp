#include <Mandos/Core/Energies/LumpedMassInertia.hpp>

namespace mandos::core
{

void LumpedMassInertia::advect(const MechanicalState<Particle3DTag> &mstate, Scalar h)
{
    m_advX.resize(mstate.m_x.size());
    mstate.advect(m_advX, h);
}

Scalar LumpedMassInertia::computeEnergy(const MechanicalState<Particle3DTag> &mstate, Scalar h) const
{
    auto energy{mandos::core::Scalar{0}};
    for (auto i{0UL}; i < m_vertexMass.size(); ++i) {
        energy += 1.0 / (2.0 * h * h) * m_vertexMass[i] * (mstate.m_x[i] - m_advX[i]).squaredNorm();
    }

    return energy;
}

Scalar LumpedMassInertia::computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate, Scalar h) const
{
    auto energy{mandos::core::Scalar{0}};
    for (auto i{0UL}; i < m_vertexMass.size(); ++i) {
        energy += 1.0 / (2.0 * h * h) * m_vertexMass[i] * (mstate.m_x[i] - m_advX[i]).squaredNorm();

        mstate.m_grad[i] += 1.0 / (h * h) * m_vertexMass[i] * (mstate.m_x[i] - m_advX[i]);
    }

    return energy;
}

Scalar LumpedMassInertia::computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate, Scalar h) const
{
    auto energy{mandos::core::Scalar{0}};
    std::vector<Triplet> triplets;
    for (auto i{0UL}; i < m_vertexMass.size(); ++i) {
        energy += 1.0 / (2.0 * h * h) * m_vertexMass[i] * (mstate.m_x[i] - m_advX[i]).squaredNorm();

        mstate.m_grad[i] += 1.0 / (h * h) * m_vertexMass[i] * (mstate.m_x[i] - m_advX[i]);

        triplets.emplace_back(3 * i + 0, 3 * i + 0, 1.0 / (h * h) * m_vertexMass[i]);
        triplets.emplace_back(3 * i + 1, 3 * i + 1, 1.0 / (h * h) * m_vertexMass[i]);
        triplets.emplace_back(3 * i + 2, 3 * i + 2, 1.0 / (h * h) * m_vertexMass[i]);
    }

    SparseMat energyHessian;
    energyHessian.resize(mstate.size(), mstate.size());
    energyHessian.setFromTriplets(triplets.begin(), triplets.end());

    mstate.m_hessian += energyHessian;

    return energy;
}

std::vector<Scalar> &LumpedMassInertia::vertexMass()
{
    return m_vertexMass;
}
const std::vector<Scalar> &LumpedMassInertia::vertexMass() const
{
    return m_vertexMass;
}

void LumpedMassInertia::computeEnergyRetardedPositionHessian(MechanicalState<Particle3DTag> & /*unused*/,
                                                             Scalar h,
                                                             unsigned int offset,
                                                             std::vector<Triplet> &triplets) const
{
    for (auto i{0UL}; i < m_vertexMass.size(); ++i) {
        const Scalar dgradE_dx0 = -1.0 / (h * h) * m_vertexMass[i];
        triplets.emplace_back(offset + 3 * i + 0, offset + 3 * i + 0, dgradE_dx0);
        triplets.emplace_back(offset + 3 * i + 1, offset + 3 * i + 1, dgradE_dx0);
        triplets.emplace_back(offset + 3 * i + 2, offset + 3 * i + 2, dgradE_dx0);
    }
}

void LumpedMassInertia::computeEnergyRetardedVelocityHessian(MechanicalState<Particle3DTag> & /*unused*/,
                                                             Scalar h,
                                                             unsigned int offset,
                                                             std::vector<Triplet> &triplets) const
{
    for (auto i{0UL}; i < m_vertexMass.size(); ++i) {
        const Scalar dgradE_dv0 = -1.0 / h * m_vertexMass[i];
        triplets.emplace_back(offset + 3 * i + 0, offset + 3 * i + 0, dgradE_dv0);
        triplets.emplace_back(offset + 3 * i + 1, offset + 3 * i + 1, dgradE_dv0);
        triplets.emplace_back(offset + 3 * i + 2, offset + 3 * i + 2, dgradE_dv0);
    }
}

}  // namespace mandos::core
