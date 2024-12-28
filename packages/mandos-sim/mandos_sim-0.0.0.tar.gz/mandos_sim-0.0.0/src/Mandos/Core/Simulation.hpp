#ifndef MANDOS_SIMULATION_H_
#define MANDOS_SIMULATION_H_

#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/core_export.h>

namespace mandos::core
{

class Model;

struct SystemMatrix;

/**
 * @brief Parameters for configuring the integration step
 *
 */
struct StepParameters {
    /**
     * @brief The time step used for the integration step
     *
     */
    Scalar h{0.01};

    /**
     * @brief The minimum norm for the gradient. If the gradient is below this value, the step is considered successful
     *
     */
    Scalar gradNorm{1e-6};

    /**
     * @brief The allowed error for the CG solver
     *
     */
    Scalar cgError{1e-6};

    /**
     * @brief The maximum allowed number of Newton iterations
     *
     */
    int newtonIterations{10};

    /**
     * @brief The maximum allowed number of CG iterations
     *
     */
    int cgIterations{500};

    /**
     * @brief The maximum allowed number of line search iterations
     *
     */
    int lineSearchIterations{5};

    /**
     * @brief When the solver fail to converge, accept the failed solution or reset to the initial state.
     * Default is to reject the failed solution and reset to the initial state
     *
     */
    bool acceptFailedSolution{false};
};

enum class SimulationStepResult { Success = 0, LineSearchFailed = 1, NewtonFailed = 2 };

/**
 * @brief Implements a simulation step using an implicit backward euler time discretization scheme and a Newton
 * based integrator
 *
 * @param model The simulation model
 * @param stepParameters A StepParameters object to specify the step thresholds and iterations
 */
SimulationStepResult MANDOS_CORE_EXPORT step(Model &model, const StepParameters &stepParameters);

}  // namespace mandos::core

#endif  // SIMULABLE_H_
