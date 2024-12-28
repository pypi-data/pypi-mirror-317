#ifndef MANDOS_ENERGIES_CONSTANT_FORCE
#define MANDOS_ENERGIES_CONSTANT_FORCE

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{
class ConstantForce
{
public:
    /**
     * @brief Number of energy elements
     *
     * @return int
     */
    int size() const;

    /**
     * @brief Computes the total potential energy for the constant force elements given the current state of the
     * MechanicalState
     *
     * @param mstate Current state
     * @return Scalar Sum of the potential energy of all the constant force elements
     */
    Scalar computeEnergy(const MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Computes the potential energy and gradient for the constant force elements given the current state of
     * the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar Sum of the potential energy of all the constant force elements
     */
    Scalar computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Computes the potential energy, the gradient and the hessian for the constant force elements given the
     * current state of the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient and hessian
     * @return Scalar Sum of the potential energy of all the constant force elements
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Add a new constant force element.
     *
     * @param index Index of the particle to apply the constant force
     * @param forceVector force vector to be applied to the particle (Vector of 3, x,y,z)
     */
    MANDOS_CORE_EXPORT void addElement(int index, Vec3 const &forceVector);

    /**
     * @brief Set the force vector of an constant force element.
     * For example change the force's value during the simulation.
     *
     * @param index Index of the particle to apply the constant force
     * @param newforceVector new force vector to be applied to the particle (Vector of 3, x,y,z)
     */
    MANDOS_CORE_EXPORT void setForceVector(int index, Vec3 &newForceVector);

    /**
     * @brief get the force vector of an constant force element.
     *
     * @param index Index of the particle to apply the constant force
     * @param forceVector force vector to return of the particle (Vector of 3, x,y,z)
     */
    MANDOS_CORE_EXPORT Vec3 getForceVector(int index);

private:
    std::vector<int> m_indices;
    std::vector<Vec3> m_forceVector;
};

}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_CONSTANT_FORCE