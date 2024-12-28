#ifndef MANDOS_GRAVITY_H_
#define MANDOS_GRAVITY_H_

#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/physics_state.hpp>
#include <Mandos/Core/utility_functions.hpp>

namespace mandos::core
{

struct GravityParameters {
    Scalar intensity;
};

struct Gravity {
    Gravity(unsigned int index, GravityParameters params)
        : parameters(params)
        , index(index)
    {
    }

    const GravityParameters parameters;
    const unsigned int index;

    inline Scalar compute_energy(Scalar TimeStep, const PhysicsState &state) const
    {
        const Scalar height = state.x(index);
        Scalar energy = -parameters.intensity * (height + default_height);
        return energy;
    }

    inline void compute_energy_gradient(Scalar TimeStep, const PhysicsState &state, Vec &grad) const
    {
        grad(index) += -parameters.intensity;  // Grad = - force
    }

    inline void compute_energy_and_derivatives(Scalar TimeStep,
                                               const PhysicsState &state,
                                               EnergyAndDerivatives &out) const
    {
        const Scalar height = state.x(index);
        out.energy += -parameters.intensity * (height + default_height);

        out.gradient(index) += -parameters.intensity;  // Grad = - force

        // ** Higher order derivatives banish **
    }

private:
    const Scalar default_height = 100;  // To avoid negative energies
};
}  // namespace mandos::core

#endif  // MANDOS_GRAVITY_H_
