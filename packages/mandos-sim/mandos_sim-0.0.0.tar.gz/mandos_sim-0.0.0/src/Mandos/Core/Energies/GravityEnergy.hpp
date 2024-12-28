#ifndef MANDOS_ENERGIES_GRAVITYENERGY_H
#define MANDOS_ENERGIES_GRAVITYENERGY_H

#include <vector>

#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/MechanicalStates/RigidBodyGlobal.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief Computes the gravity energy for several mechanical states
 *
 * The masses are not initialized and should be provided directly by the user
 */
class MANDOS_CORE_EXPORT GravityEnergy
{
public:
    /**
     * @brief Computes the gravity energy
     *
     * @param mstate Current state
     * @return Scalar
     */
    Scalar computeEnergy(const MechanicalState<Particle3DTag> &mstate) const;
    Scalar computeEnergy(const MechanicalState<RigidBodyTag> &mstate) const;
    Scalar computeEnergy(const MechanicalState<RigidBodyGlobalTag> &mstate) const;

    /**
     * @brief Computes the gravity energy and its gradient
     *
     * @param mstate Current state, and where to write the gradient
     * @return Scalar
     */
    Scalar computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const;
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate) const;
    Scalar computeEnergyAndGradient(MechanicalState<RigidBodyGlobalTag> &mstate) const;

    /**
     * @brief Computes the gravity energy, its gradient and its hessian
     *
     * @param mstate Current state, and where to write the gradient and the hessian
     * @return Scalar
     */
    Scalar computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const;
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate) const;
    Scalar computeEnergyGradientAndHessian(MechanicalState<RigidBodyGlobalTag> &mstate) const;

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

    const Vec3 &gravityVector() const;
    void setGravityVector(const Vec3 &gravityVector);

    bool isEnabled() const;
    void enable();
    void disable();

private:
    bool m_isEnabled{true};

    Vec3 m_gravityVector{Vec3{0, 0, -9.81}};
    std::vector<Scalar> m_vertexMass;
};
}  // namespace mandos::core

#endif  // MANDOS_ENERGIES_GRAVITYENERGY_H
