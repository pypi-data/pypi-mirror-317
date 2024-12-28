#ifndef MANDOS_ENERGIES_LUMPEDMASSINERTIA_H
#define MANDOS_ENERGIES_LUMPEDMASSINERTIA_H

#include <vector>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief Computes the inertial energy term using lumped masses
 * The inertial energy is computed as
 * 1/(2*h*h) * (x - x_advect) * M * (x - x_advect)
 * That is, the mass weighted difference between the position we would have if we just consider the velocity advection
 * of the particles and the actual position we really have
 *
 * The vertex masses are not initialized and should be provided directly by the user
 */
class MANDOS_CORE_EXPORT LumpedMassInertia
{
public:
    /**
     * @brief Performs the advection of the particles
     *
     * @param mstate Current state. Advection will update particles using current state velocity
     * @param h Time step for advection
     */
    void advect(const MechanicalState<Particle3DTag> &mstate, Scalar h);

    /**
     * @brief Computes the inertia energy
     *
     * @param mstate Current state
     * @param h Time span for moving from x to x_advect
     * @return Scalar
     */
    Scalar computeEnergy(const MechanicalState<Particle3DTag> &mstate, Scalar h) const;

    /**
     * @brief Computes the inertia energy and its gradient
     *
     * @param mstate Current state, and where to write the gradient
     * @param h Time span for moving from x to x_advect
     * @return Scalar
     */
    Scalar computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate, Scalar h) const;

    /**
     * @brief Computes the inertia energy, its gradient and its hessian
     *
     * @param mstate Current state, and where to write the gradient and the hessian
     * @param h Time span for moving from x to x_advect
     * @return Scalar
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate, Scalar h) const;

    void computeEnergyRetardedPositionHessian(MechanicalState<Particle3DTag> &mstate,
                                              Scalar h,
                                              unsigned int offset,
                                              std::vector<Triplet> &triplets) const;
    void computeEnergyRetardedVelocityHessian(MechanicalState<Particle3DTag> &mstate,
                                              Scalar h,
                                              unsigned int offset,
                                              std::vector<Triplet> &triplets) const;

    /**
     * @brief Read/Write accessor to vertex mass
     *
     * @return std::vector<Scalar>&
     */
    std::vector<Scalar> &vertexMass();

    /**
     * @brief Read accessor to vertex mass
     *
     * @return const std::vector<Scalar>&
     */
    const std::vector<Scalar> &vertexMass() const;

private:
    std::vector<Scalar> m_vertexMass;

    std::vector<Vec3> m_advX;
};
}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_LUMPEDMASSINERTIA_H
