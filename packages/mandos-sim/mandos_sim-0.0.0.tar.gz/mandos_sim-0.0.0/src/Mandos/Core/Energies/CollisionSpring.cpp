#include "Mandos/Core/MechanicalStates/Particle3D.hpp"
#include <Mandos/Core/Energies/CollisionSpring.hpp>

#include <TinyAD/ScalarFunction.hh>
#include <TinyAD/Utils/HessianProjection.hh>
#include <tracy/Tracy.hpp>

#include <oneapi/tbb/enumerable_thread_specific.h>
#include <oneapi/tbb/parallel_for.h>

namespace
{
TinyAD::Double<6> computeEnergyAD(const mandos::core::MechanicalState<mandos::core::Particle3DTag> &mstate,
                                  mandos::core::Scalar stiffness,
                                  mandos::core::Scalar threshold,
                                  const mandos::core::Vec3 &normal,
                                  std::size_t collisionId,
                                  std::size_t nCollisions)
{
    Eigen::Vector<TinyAD::Double<6>, 3> x0;
    x0[0] = TinyAD::Double<6>(mstate.m_x[collisionId].x(), 0);
    x0[1] = TinyAD::Double<6>(mstate.m_x[collisionId].y(), 1);
    x0[2] = TinyAD::Double<6>(mstate.m_x[collisionId].z(), 2);
    Eigen::Vector<TinyAD::Double<6>, 3> x1;
    x1[0] = TinyAD::Double<6>(mstate.m_x[nCollisions + collisionId].x(), 3 + 0);
    x1[1] = TinyAD::Double<6>(mstate.m_x[nCollisions + collisionId].y(), 3 + 1);
    x1[2] = TinyAD::Double<6>(mstate.m_x[nCollisions + collisionId].z(), 3 + 2);

    const auto d = (normal.dot(x1 - x0));
    if (d < threshold) {
        return 0.5 * stiffness * (d - threshold) * (d - threshold);
    }
    return 0;
}
}  // namespace

namespace mandos::core
{
int CollisionSpring::size() const
{
    return static_cast<int>(m_stiffness.size());
}

Scalar CollisionSpring::computeEnergy(const MechanicalState<Particle3DTag> &mstate) const
{
    ZoneScopedN("CollisionSpring.computeEnergy");
    const auto nCollisions{m_stiffness.size()};
    if (nCollisions == 0) {
        return 0;
    }

    tbb::enumerable_thread_specific<Scalar> energyTLS;
    tbb::parallel_for(tbb::blocked_range<std::size_t>(0, nCollisions), [&](const tbb::blocked_range<std::size_t> &r) {
        bool exists{};
        auto &energy = energyTLS.local(exists);
        if (!exists) {
            energy = 0;
        }
        for (auto collisionId = r.begin(); collisionId != r.end(); ++collisionId) {
            energy += ::computeEnergyAD(mstate,
                                        m_stiffness[collisionId],
                                        m_threshold[collisionId],
                                        m_normal[collisionId],
                                        collisionId,
                                        nCollisions)
                          .val;
        }
    });

    return energyTLS.combine(std::plus{});
}

Scalar CollisionSpring::computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const
{  // TODO
    ZoneScopedN("CollisionSpring.computeEnergyGradientAndHessian");
    const auto nCollisions{m_stiffness.size()};
    if (nCollisions == 0) {
        return 0;
    }

    tbb::enumerable_thread_specific<Scalar> energyTLS;
    tbb::enumerable_thread_specific<std::vector<Triplet>> tripletsTLS;
    tbb::parallel_for(tbb::blocked_range<std::size_t>(0, nCollisions), [&](const tbb::blocked_range<std::size_t> &r) {
        bool exists{};
        auto &energy = energyTLS.local(exists);
        if (!exists) {
            energy = 0;
        }
        auto &triplets = tripletsTLS.local(exists);
        if (!exists) {
            triplets.reserve(6 * 6 * static_cast<std::size_t>(size()));
        }
        for (auto collisionId = r.begin(); collisionId != r.end(); ++collisionId) {
            auto e = ::computeEnergyAD(mstate,
                                       m_stiffness[collisionId],
                                       m_threshold[collisionId],
                                       m_normal[collisionId],
                                       collisionId,
                                       nCollisions);

            mstate.m_grad[collisionId] = e.grad.segment<3>(0);
            mstate.m_grad[nCollisions + collisionId] = e.grad.segment<3>(3);

            energy += e.val;

            auto hess = e.Hess;
            TinyAD::project_positive_definite(hess, 1e-8);

            // Fill Hessian
            auto fillHessian = [&triplets](std::size_t rowBlockStart, std::size_t colBlockStart, const auto &block) {
                triplets.emplace_back(rowBlockStart + 0, colBlockStart + 0, block(0, 0));
                triplets.emplace_back(rowBlockStart + 0, colBlockStart + 1, block(0, 1));
                triplets.emplace_back(rowBlockStart + 0, colBlockStart + 2, block(0, 2));

                triplets.emplace_back(rowBlockStart + 1, colBlockStart + 0, block(1, 0));
                triplets.emplace_back(rowBlockStart + 1, colBlockStart + 1, block(1, 1));
                triplets.emplace_back(rowBlockStart + 1, colBlockStart + 2, block(1, 2));

                triplets.emplace_back(rowBlockStart + 2, colBlockStart + 0, block(2, 0));
                triplets.emplace_back(rowBlockStart + 2, colBlockStart + 1, block(2, 1));
                triplets.emplace_back(rowBlockStart + 2, colBlockStart + 2, block(2, 2));
            };

            // Particle 0 with itself
            fillHessian(3 * collisionId, 3 * collisionId, e.Hess.block<3, 3>(0, 0));

            // Particle 1 with itself
            fillHessian(3 * (nCollisions + collisionId), 3 * (nCollisions + collisionId), e.Hess.block<3, 3>(3, 3));

            // Particle 0 with particle 1
            fillHessian(3 * collisionId, 3 * (nCollisions + collisionId), e.Hess.block<3, 3>(0, 3));

            // Particle 1 with particle 0
            fillHessian(3 * (nCollisions + collisionId), 3 * (collisionId), e.Hess.block<3, 3>(3, 0));
        }
    });

    {
        ZoneScopedN("StableNeoHookean.globalAssembly");
        auto triplets = tbb::flatten2d(tripletsTLS);
        mstate.m_hessian.setFromTriplets(triplets.begin(), triplets.end());
    }

    return energyTLS.combine(std::plus{});
}

Scalar CollisionSpring::computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const
{
    ZoneScopedN("CollisionSpring.computeEnergyGradient");
    return computeEnergyGradientAndHessian(mstate);
}

void CollisionSpring::addElement(Scalar stiffness, Scalar threshold, const Vec3 &n)
{
    m_normal.push_back(n.normalized());
    m_stiffness.push_back(stiffness);
    m_threshold.push_back(threshold);
}

void CollisionSpring::clear()
{
    m_normal.clear();
    m_stiffness.clear();
}

}  // namespace mandos::core
