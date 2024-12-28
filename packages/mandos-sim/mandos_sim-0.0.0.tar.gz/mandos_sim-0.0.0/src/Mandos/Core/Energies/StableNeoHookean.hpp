#ifndef MANDOS_ENERGIES_SNH_H
#define MANDOS_ENERGIES_SNH_H

#include <array>
#include <span>
#include <utility>
#include <vector>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{
/**
 * @brief An implementation of Stable Neo Hookean energy by [https://www.tkim.graphics/DYNAMIC_DEFORMABLES/]
 *
 * Note: The energy described in the mentioned document doesn't correspond exactly with (Smith et al(219))
 * [https://dl.acm.org/doi/10.1145/3180491]
 */
class MANDOS_CORE_EXPORT StableNeoHookean
{
public:
    struct MANDOS_CORE_EXPORT ParameterSet {
        ParameterSet(const Mat3 &restPoseMatrix, Scalar lambda_, Scalar mu_);
        ParameterSet(const Mat43 &x0, Scalar lambda_, Scalar mu_);
        ParameterSet(const std::array<Vec3, 4> &x0, Scalar lambda_, Scalar mu_);

        Mat3 restPoseMatrix;
        Scalar lambda;
        Scalar mu;
    };

    /**
     * @brief Number of energy elements
     *
     * @return int
     */
    int size() const;

    /**
     * @brief Initialize the structures needed for computing StableNeoHookean energy terms in parallel
     *
     */
    void initialize(const MechanicalState<Particle3DTag> &mstate);

    /**
     * @brief Computes the total potential energy for the Stable Neo Hookean elements given the current state of the
     * MechanicalState
     *
     * @param mstate Current state
     * @return Scalar Sum of the potential energy of all the Stable Neo Hooken elements
     */
    Scalar computeEnergy(const MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Computes the potential energy and gradient for the Stable Neo Hookean elements given the current state of
     * the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar Sum of the potential energy of all the Stable Neo Hooken elements
     */
    Scalar computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Computes the potential energy, the gradient and the hessian for the Stable Neo Hookean elements given the
     * current state of the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient and hessian
     * @return Scalar Sum of the potential energy of all the Stable Neo Hooken elements
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Add a new Stable Neo Hookean element. The element static data, such as the rest pose for the deformation
     * gradient computation is taken from the current mechanical state
     *
     * @param x0 Position for static data computations (ie rest state)
     * @param indices Indices of the particles involved in the new element
     * @param parameterSet Parameters for this element
     */
    void addElement(const std::array<int, 4> &indices, const ParameterSet &parameterSet);

    ParameterSet getParameterSet(int elementId) const;

    void setParameterSet(int elementId, const ParameterSet &parameterSet);

    bool &projectSPD();

    bool projectSPD() const;

private:
    void configureElement(std::size_t elementId, const ParameterSet &parameterSet);
    bool m_projectSPD{false};

    std::vector<std::array<int, 4>> m_indices;
    std::vector<Scalar> m_volume;
    std::vector<Scalar> m_lambda;
    std::vector<Scalar> m_mu;
    std::vector<Eigen::Matrix<mandos::core::Scalar, 3, 3>> m_invDm;
    std::vector<Eigen::Matrix<mandos::core::Scalar, 9, 12>> m_dFdx;

    std::vector<std::vector<std::size_t>> m_parallelGroups;
};

void initialize(StableNeoHookean &snh, const MechanicalState<Particle3DTag> &mstate);

}  // namespace mandos::core

#endif  //  MANDOS_ENERGIES_SNH_H