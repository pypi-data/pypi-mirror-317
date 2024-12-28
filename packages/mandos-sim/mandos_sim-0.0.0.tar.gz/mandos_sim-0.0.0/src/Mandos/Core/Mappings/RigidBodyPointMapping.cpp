#include <Mandos/Core/Mappings/RigidBodyPointMapping.hpp>
#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/SimulationObject.hpp>

namespace mandos::core
{

RigidBodyPointMapping::RigidBodyPointMapping(SimulationObjectHandle<RigidBodyTag> from,
                                             SimulationObjectHandle<Particle3DTag> to)
    : m_from(from)
    , m_to(to)
{
}

int RigidBodyPointMapping::size() const
{
    return static_cast<int>(m_rigidBodyIndex.size());
}

void RigidBodyPointMapping::applyJT(std::vector<Vec6> &from, const std::vector<Vec3> &to) const
{
    assert(m_rigidBodyIndex.size() == to.size());
    for (unsigned int i = 0; i < m_rigidBodyIndex.size(); ++i) {
        const auto iR = static_cast<std::size_t>(m_rigidBodyIndex[i]);
        const Mat3 R = rotationExpMap(m_from->mstate.m_x[iR].segment<3>(3));
        const Mat3 thetaJT = skew(R * m_localCoord[i]);
        from[iR].segment<3>(0) += to[i];
        from[iR].segment<3>(3) += thetaJT * to[i];
    }
}

void RigidBodyPointMapping::applyJ(const std::vector<Vec6> &from, std::vector<Vec3> &to) const
{
    assert(m_rigidBodyIndex.size() == to.size());
    for (unsigned int i = 0; i < m_rigidBodyIndex.size(); ++i) {
        const auto iR = static_cast<std::size_t>(m_rigidBodyIndex[i]);
        const Mat3 R = rotationExpMap(m_from->mstate.m_x[iR].segment<3>(3));
        const Mat3 thetaJ = -skew(R * m_localCoord[i]);
        to[i] += from[iR].segment<3>(0);
        to[i] += thetaJ * from[iR].segment<3>(3);
    }
}

void RigidBodyPointMapping::apply(const std::vector<Vec6> &from, std::vector<Vec3> &to) const
{
    for (unsigned int i = 0; i < m_rigidBodyIndex.size(); ++i) {
        const auto iR = static_cast<std::size_t>(m_rigidBodyIndex[i]);
        const Vec3 centerOfMass = from[iR].segment<3>(0);
        const Mat3 R = rotationExpMap(from[iR].segment<3>(3));

        to[i] += R * m_localCoord[i] + centerOfMass;
    }
}

SimulationObjectHandle<Particle3DTag> RigidBodyPointMapping::to() const
{
    return m_to;
}

SimulationObjectHandle<RigidBodyTag> RigidBodyPointMapping::from() const
{
    return m_from;
}

SparseMat RigidBodyPointMapping::J() const
{
    SparseMat J = SparseMat(m_to->mstate.size(), m_from->mstate.size());
    std::vector<Triplet> triplets;

    for (unsigned int i = 0; i < m_rigidBodyIndex.size(); ++i) {
        const auto iR = static_cast<std::size_t>(m_rigidBodyIndex[i]);
        const Mat3 R = rotationExpMap(m_from->mstate.m_x[iR].segment<3>(3));
        const Mat3 thetaJ = -skew(R * m_localCoord[i]);
        for (unsigned int j = 0; j < 3; ++j) {
            triplets.emplace_back(3 * i + j, 6 * iR + j, 1.0);  // Identity
            for (unsigned int k = 0; k < 3; ++k) {
                triplets.emplace_back(3 * i + j, 6 * iR + 3 + k, thetaJ(j, k));
            }
        }
    }
    J.setFromTriplets(triplets.begin(), triplets.end());
    return J;
}

void RigidBodyPointMapping::addLocalPoint(const Vec3 &localPoint, int rigidBodyIndex)
{
    m_localCoord.push_back(localPoint);
    m_rigidBodyIndex.push_back(rigidBodyIndex);
}
}  // namespace mandos::core
