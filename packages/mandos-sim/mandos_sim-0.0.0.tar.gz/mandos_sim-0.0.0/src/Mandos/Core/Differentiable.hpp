#ifndef MANDOS_CORE_DIFFERENTIABLE_HPP
#define MANDOS_CORE_DIFFERENTIABLE_HPP

#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/linear_algebra.hpp>

namespace mandos::core
{
struct MANDOS_CORE_EXPORT Trajectory {
    std::vector<Vec> positions;
    std::vector<Vec> velocities;

    int getNDof() const
    {
        return static_cast<int>(positions[0].size());
    }
    int getNStates() const
    {
        return static_cast<int>(positions.size());
    }
    int getNSteps() const
    {
        return getNStates() - 1;
    }
};

struct MANDOS_CORE_EXPORT LossFunctionAndGradients {
    Scalar loss;                                     // g
    std::vector<Vec> lossPositionPartialDerivative;  // dg_dx_i
    std::vector<Vec> lossVelocityPartialDerivative;  // dg_dv_i
    Vec lossParameterPartialDerivative;              // dg_dp

    int getNParameters() const
    {
        return static_cast<int>(lossParameterPartialDerivative.size());
    }
};

MANDOS_CORE_EXPORT Vec computeLossFunctionGradientBackpropagation(Scalar h,
                                                                  Model &model,
                                                                  const Trajectory &trajectory,
                                                                  const LossFunctionAndGradients &loss,
                                                                  const Mat &dx0_dp,
                                                                  const Mat &dv0_dp,
                                                                  unsigned int maxIterations = 0);

}  // namespace mandos::core

#endif  // MANDOS_CORE_DIFFERENTIABLE_HPP
