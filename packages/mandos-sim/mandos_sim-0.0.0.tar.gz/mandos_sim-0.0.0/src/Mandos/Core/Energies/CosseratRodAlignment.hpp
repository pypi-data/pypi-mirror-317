#ifndef MANDOS_ENERGIES_COSSERATRODALIGNMENT_H
#define MANDOS_ENERGIES_COSSERATRODALIGNMENT_H

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

namespace mandos::core
{
class MANDOS_CORE_EXPORT CosseratRodAlignment
{
public:
    struct MANDOS_CORE_EXPORT ParameterSet {
        ParameterSet(mandos::core::Scalar restLength_, mandos::core::Scalar cosseratStiffness_);
        ParameterSet(const std::array<Vec6, 2> &x0, mandos::core::Scalar cosseratStiffness_);
        ParameterSet(const Mat26 &x0, mandos::core::Scalar cosseratStiffness_);

        Scalar restLength;
        Scalar cosseratStiffness;  // Cosserat constraint stiffness
    };

    /**
     * @brief Number of energy elements
     *
     * @return int
     */
    int size() const;

    /**
     * @brief Computes the total potential energy for the Cosserat Rod given the current state of the
     * MechanicalState
     *
     * @param mstate Current state
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Computes the potential energy and gradient for all the Cosserat Rod elements given the current state of
     * the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar Sum of the potential energy of all the Cosserat Rod elements
     */
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Computes the potential energy, the gradient and the hessian for the Cosserat Rods elements given the
     * current state of the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient and hessian
     * @return Scalar Sum of the potential energy of all the Cosserat Rod elements
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const;

    MANDOS_CORE_EXPORT void addElement(const std::array<int, 2> &indices, const ParameterSet &parameterSet);

    MANDOS_CORE_EXPORT ParameterSet getParameterSet(int elementId) const;

    MANDOS_CORE_EXPORT void setParameterSet(int elementId, const ParameterSet &parameterSet);

private:
    // Conectivity
    std::vector<std::array<int, 2>> m_indices;

    // Stiffness
    std::vector<Scalar> m_cosseratStiffness;  // Cosserat constraint stiffness
    std::vector<Scalar> m_restLength;         // Cosserat constraint stiffness
};

}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_COSSERATRODALIGMENT_H
