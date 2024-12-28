#ifndef MANDOS_ENERGIES_COLLISIONSPRING_H
#define MANDOS_ENERGIES_COLLISIONSPRING_H

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>

namespace mandos::core
{
class CollisionSpring
{
public:
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

    /**
     * @brief Computes the potential energy and gradient for the spring elements given the current state of
     * the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Computes the potential energy, the gradient and the hessian for the spring elements given the
     * current state of the MechanicalState
     *
     * @param mstate Current state, and where to write the gradient and hessian
     * @return Scalar Sum of the potential energy of all the spring elements
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const;

    /**
     * @brief Add a new spring element. The particles involved in the spring element are implicit. Each pair of
     * particles in the MechanicalState will have a spring between them with rest length the set threshold
     *
     * @param stiffness Spring stiffness
     * @param threshold Threshold distance to start considering the contact as active
     * @param normal Direction to push the particle away from each other
     */
    void addElement(Scalar stiffness, Scalar threshold, const Vec3 &normal);

    void clear();

private:
    std::vector<Scalar> m_stiffness;
    std::vector<Scalar> m_threshold;
    std::vector<Vec3> m_normal;
};

}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_SPRINGS_H