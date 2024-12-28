#ifndef UTILITY_FUNCTIONS_H_
#define UTILITY_FUNCTIONS_H_

#include <Mandos/Core/linear_algebra.hpp>
#include <tuple>
#include <array>
#include <utility>

namespace mandos::core::utilities
{

template <typename... Ts>
struct typelist {
    template <template <typename...> class C>
    using as = C<Ts...>;

    template <template <typename...> class M>
    using map = typelist<M<Ts>...>;

    template <typename T>
    using add_front = typelist<T, Ts...>;
};

template <class... Fs>
struct overloaded : Fs... {
    using Fs::operator()...;
};

template <class... Fs>
overloaded(Fs...) -> overloaded<Fs...>;

/**
 * @brief Given a tuple style set of objects, perform an operation and all of them
 * This is the main functionality that allows to easily traverse the SimulationObjects, Energies and Mappings
 *
 * @tparam F
 * @tparam Tup
 * @param f  Function to be execute for each object in tup
 * @param tup  Tuple type collection of objects
 */
template <typename F, typename Tup>
void static_for_each(F &&f, Tup &&tup)
{
    std::apply([f = std::forward<F>(f)](auto &&...v) { return (f(std::forward<decltype(v)>(v)), ...); },
               std::forward<Tup>(tup));
}
}  // namespace mandos::core::utilities

// /**
//  * Compute the area of the triangle.
//  *
//  * @param AB, AC the 2 vectors defining the triangle.
//  */
// inline Scalar compute_trinagle_area(const Vec3 &AB, const Vec3 &AC)
// {
//     return (skew(AB) * AC).norm() / 2;
// }

// /**
//  * Compute the volume of the tetrahedron.
//  *
//  * @param AB, AC, AD the 3 vectors defining the tetrahedron
//  */
// Scalar compute_tetrahedron_volume(const Vec3 &AB, const Vec3 &AC, const Vec3 &AD);

// /**
//  * Compute the rotation matrix from a given axis-angle rotation vector using Rodrigues'.
//  *
//  * @param theta Rotation vector defined as angle * axis, where angle is a scalar and axis a normalized vector.
//  */
// Mat3 compute_rotation_matrix_rodrigues(const Vec3 &theta);

// /**
//  * Compute the cross product between 2 vectors.
//  */
// inline Vec3 cross(const Vec3 &v, const Vec3 &u)
// {
//     return Vec3(v.y() * u.z() - v.z() * u.y(), v.z() * u.x() - v.x() * u.z(), v.x() * u.y() - v.y() * u.x());
// }

#endif  // MANDOS_UTILITY_FUNCTIONS_H_
