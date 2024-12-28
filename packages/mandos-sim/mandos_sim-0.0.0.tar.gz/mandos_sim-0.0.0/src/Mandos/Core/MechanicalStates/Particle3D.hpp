#ifndef MANDOS_MECHANICALSTATES_PARTICLE3D_H
#define MANDOS_MECHANICALSTATES_PARTICLE3D_H

#include <Mandos/Core/MechanicalState.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

/**
 * @brief Tag to represent objects made of 3D particles in space
 *
 */
struct Particle3DTag {
};

template <>
struct MANDOS_CORE_EXPORT MechanicalState<Particle3DTag> {
    static constexpr bool HasGradient = true;
    static constexpr bool HasHessian = true;

    std::vector<Vec3> m_x;
    std::vector<Vec3> m_v;

    std::vector<Vec3> m_grad;
    SparseMat m_hessian;

    /**
     * @brief The state size of the MechanicalState
     *
     * @return int
     */
    [[nodiscard]] int size() const;

    /**
     * @brief Writes the state of the MechanicalState into the provided x and v parameters. This is generally used to
     * accumulate the DoF of the simulation into a generalized state vector
     *
     * @param x Where to write the x state vector of this MechanicalState
     * @param v Where to write the v state vector of this MechanicalState
     */
    void state(Eigen::Ref<Vec> x, Eigen::Ref<Vec> v) const;

    /**
     * @brief Retrieves the current gradient stored in the object into the generalized segment grad
     *
     * @param grad The generalized segment where to store the graph
     */
    void gradient(Eigen::Ref<Vec> grad) const;

    /**
     * @brief The gradient stored in this MechanicalState
     *
     * @return View of the gradient in generalized shape
     */
    Eigen::Map<Vec> gradientView();

    /**
     * @brief Set the current gradient of this MState. It is used during the Hessian * dx visitor, to store the
     * intermediate results
     *
     * @param gradient
     */
    void setGradient(const Eigen::Ref<const Vec> &gradient);

    /**
     * @brief Multiplies the current gradient by the current hessian
     *
     */
    void scaleGradByHessian();

    /**
     * @brief Copies the generalized state vectors x and v into the MechanicalState
     *
     * @param x The generalized x state that has to be copied into the MechanicalState
     * @param v The generalized v state that has to be copied into the MechanicalState
     */
    void setState(const Eigen::Ref<const Vec> &x, const Eigen::Ref<const Vec> &v);

    void setZero();

    void clearGradient();

    void clearHessian();

    void advect(std::vector<Vec3> &advX, Scalar h) const;

    void updateState(const Eigen::Ref<const Vec> &dx,
                     const Eigen::Ref<const Vec> &x0,
                     const Eigen::Ref<const Vec> &v0,
                     Scalar h);
};

}  // namespace mandos::core

#endif  //  MANDOS_MECHANICALSTATES_PARTICLE3D_H
