#ifndef MANDOS_ENERGIES_COSSEATRODBENDING_H
#define MANDOS_ENERGIES_COSSEATRODBENDING_H

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

#include <Mandos/Core/RotationUtilities.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{
class MANDOS_CORE_EXPORT CosseratBendingRod
{
public:
    struct MANDOS_CORE_EXPORT ParameterSet {
        ParameterSet(mandos::core::Scalar restLength,
                     const mandos::core::Vec3 &intrinsicDarboux,
                     const mandos::core::Vec3 &stiffnessTensor);
        ParameterSet(const std::array<Vec6, 2> &x0, const mandos::core::Vec3 &stiffnessTensor);
        ParameterSet(const Mat26 &x0, const mandos::core::Vec3 &stiffnessTensor);

        mandos::core::Scalar restLength;
        mandos::core::Vec3 intrinsicDarboux;
        mandos::core::Vec3 stiffnessTensor;
    };

    /**
     * @brief Number of energy elements
     *
     * @return int
     */
    int size() const;

    /**
     * @brief Computes the total potential energy for the bending elements given the current state of the
     * MechanicalState
     *
     * @param mstate Current state
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Computes the potential energy and gradient for the bending elements given the current state of
     * the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Computes the potential energy, the gradient and the hessian for the bending elements given the
     * current state of the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient and hessian
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Add a new bending element
     *
     */
    MANDOS_CORE_EXPORT void addElement(const std::array<int, 2> &indices, const ParameterSet &parameterSet);

    MANDOS_CORE_EXPORT ParameterSet getParameterSet(int elementId) const;

    MANDOS_CORE_EXPORT void setParameterSet(int elementId, const ParameterSet &parameterSet);

private:
    std::vector<std::array<int, 2>> m_indices;

    std::vector<Scalar> m_restLength;
    std::vector<Vec3> m_intrinsicDarboux;  // Intrinsic curvature of the rod
    std::vector<Vec3> m_stiffnessTensor;
};

MANDOS_CORE_EXPORT Vec3 computeDarbouxVector(Scalar L0, const Mat3 &R1, const Mat3 &R2);
}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_COSSEATRODBENDING_H
