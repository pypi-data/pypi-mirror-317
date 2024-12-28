#ifndef MANDOS_ENERGIES_SPRINGS_H
#define MANDOS_ENERGIES_SPRINGS_H

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>

#include <Mandos/Core/core_export.h>

#include <span>

namespace mandos::core
{
class MANDOS_CORE_EXPORT MassSpring
{
public:
    struct MANDOS_CORE_EXPORT ParameterSet {
        ParameterSet(mandos::core::Scalar restLength, mandos::core::Scalar stiffness, mandos::core::Scalar damping = 0);
        ParameterSet(const std::array<Vec3, 2> &x0, mandos::core::Scalar stiffness, mandos::core::Scalar damping = 0);
        ParameterSet(const Mat23 &x0, mandos::core::Scalar stiffness, mandos::core::Scalar damping = 0);

        mandos::core::Scalar restLength;
        mandos::core::Scalar stiffness;
        mandos::core::Scalar damping;
    };

    /**
     * @brief Number of energy elements
     *
     * @return int
     */
    int size() const;

    /**
     * @brief Computes the total potential energy for the spring elements given the current state of the
     * MechanicalState
     *
     * @param mstate Current state
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergy(const MechanicalState<Particle3DTag> &mstate) const;
    Scalar computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Computes the potential energy and gradient for the spring elements given the current state of
     * the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const;
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Computes the potential energy, the gradient and the hessian for the spring elements given the
     * current state of the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient and hessian
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const;
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const;

    /**
     * @brief Add a new spring element. The rest length of the spring is taken from the current mechanical state
     *
     * @param x0 Position for static data computations (ie rest state)
     * @param indices Indices of the two particles
     * @param stiffness Spring stiffness
     * @param damping Damping coefficient
     */
    MANDOS_CORE_EXPORT void addElement(const std::array<int, 2> &indices, const ParameterSet &parameterSet);

    MANDOS_CORE_EXPORT ParameterSet getParameterSet(int elementId) const;

    MANDOS_CORE_EXPORT void setParameterSet(int elementId, const ParameterSet &parameterSet);

private:
    std::vector<std::array<int, 2>> m_indices;
    std::vector<Scalar> m_stiffness;
    std::vector<Scalar> m_damping;
    std::vector<Scalar> m_restLength;
};

}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_SPRINGS_H
