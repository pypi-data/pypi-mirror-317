#ifndef MANDOS_CORE_DIFF_RIGID_BODY_H_
#define MANDOS_CORE_DIFF_RIGID_BODY_H_

#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/linear_algebra.hpp>

namespace mandos::core
{

/**
 * @brief Transform the angular segments of a derivative vector from Global to Local Axis Angle derivatives.
 *
 * Global Axis Angle derivatives are done at the origin tangent plane (Lie Algebra), with the full exponential map.
 * Local Axis Angle derivatives are done at the point's tangent plane, with a linearization of the exponential map. Note
 * that we use left incremental rotations: exp(theta) * R.
 *
 * @param model The simulation model
 * @param x The derivative vector (size = nDof)
 */
void applyGlobalToLocal(const Model &model, Vec &x);

/**
 * @brief Transform the angular segments of a derivative vector from Local to Global Axis Angle derivatives.
 *
 * Global Axis Angle derivatives are done at the origin tangent plane (Lie Algebra), with the full exponential map.
 * Local Axis Angle derivatives are done at the point's tangent plane, with a linearization of the exponential map. Note
 * that we use left incremental rotations: exp(theta) * R.
 *
 * @param model The simulation model
 * @param x The derivative vector (size = nDof)
 */
void applyLocalToGlobal(const Model &model, Vec &x);

void applyComposeAxisAngleJacobian(Scalar h, const Model &model, Vec &v);

}  // namespace mandos::core

#endif  // MANDOS_CORE_DIFF_RIGID_BODY_H_
