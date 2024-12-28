#ifndef MANDOS_ENERGIES_RIGIDBODYINERTIA_H
#define MANDOS_ENERGIES_RIGIDBODYINERTIA_H

#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief Computes the inertial energy term of a rigid body
 * The inertia energy is divided in two terms, the traslation part
 * 1/(2*h*h) * (x - x_advect) * M * (x - x_advect)
 * and a rotation part, which is computed as
 * 1/(2*h*h) * tr((R - R_advect) * T * (R - R_advect))
 * Note the rotation is computed as the Rodrigues matrix
 *
 * The mass and the inertia tensor are not initialized and should be provided directly by the user
 */
class RigidBodyInertia
{
public:
    /**
     * @brief Performs the advection of the particles
     *
     * @param mstate Current state. Advection will update particles using current state velocity
     * @param h Time step for advection
     */
    void advect(const MechanicalState<RigidBodyTag> &mstate, Scalar h);
    void advect(const MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h);

    /**
     * @brief Computes the inertia energy
     *
     * @param mstate Current state
     * @param h Time span for moving from x to x_advect
     * @return Scalar
     */
    Scalar computeEnergy(const MechanicalState<RigidBodyTag> &mstate, Scalar h) const;
    Scalar computeEnergy(const MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h) const;

    /**
     * @brief Computes the inertia energy and its gradient
     *
     * @param mstate Current state, and where to write the gradient
     * @param h Time span for moving from x to x_advect
     * @return Scalar
     */
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate, Scalar h) const;
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h) const;

    /**
     * @brief Computes the inertia energy, its gradient and its hessian
     *
     * @param mstate Current state, and where to write the gradient and the hessian
     * @param h Time span for moving from x to x_advect
     * @return Scalar
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate, Scalar h) const;
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h) const;

    void computeEnergyRetardedPositionHessian(MechanicalState<RigidBodyTag> &mstate,
                                              Scalar h,
                                              unsigned int offset,
                                              std::vector<Triplet> &triplets) const;
    void computeEnergyRetardedVelocityHessian(MechanicalState<RigidBodyTag> &mstate,
                                              Scalar h,
                                              unsigned int offset,
                                              std::vector<Triplet> &triplets) const;

    void computeEnergyRetardedPositionHessian(MechanicalState<RigidBodyGlobalTag> &mstate,
                                              Scalar h,
                                              unsigned int offset,
                                              std::vector<Triplet> &triplets) const;
    void computeEnergyRetardedVelocityHessian(MechanicalState<RigidBodyGlobalTag> &mstate,
                                              Scalar h,
                                              unsigned int offset,
                                              std::vector<Triplet> &triplets) const;

    /**
     * @brief Read/Write accessor to rigid body mass
     *
     * @return std::vector<Scalar>&
     */
    MANDOS_CORE_EXPORT std::vector<Scalar> &mass();

    /**
     * @brief Read accessor to rigid body mass
     *
     * @return const std::vector<Scalar>&
     */
    MANDOS_CORE_EXPORT const std::vector<Scalar> &mass() const;

    /**
     * @brief Read/Write accessor to vertex inertia tensor
     *
     * @return std::vector<Mat3>&
     */
    MANDOS_CORE_EXPORT std::vector<Mat3> &inertiaTensor();

    /**
     * @brief Read accessor to vertex inertia tensor
     *
     * @return const std::vector<Mat3>&
     */
    MANDOS_CORE_EXPORT const std::vector<Mat3> &inertiaTensor() const;

private:
    std::vector<Scalar> m_mass;
    std::vector<Mat3> m_inertiaTensor0;

    std::vector<Vec3> m_advX;
    std::vector<Mat3> m_advXR;

    std::vector<Vec6> m_x0;
    std::vector<Vec6> m_v0;
};

}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_RIGIDBODYINERTIA_H
