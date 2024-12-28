#ifndef MANDOS_CORE_COLLISIONS_CONTACTEVENT_HPP
#define MANDOS_CORE_COLLISIONS_CONTACTEVENT_HPP

#include <Mandos/Core/linear_algebra.hpp>

namespace mandos::core::collisions
{

/**
 * @brief ContactEventSide containt the data related to a particular collider for a ContactEvent
 *
 * @tparam C
 */
template <typename C>
struct ContactEventSide {
};

/**
 * @brief ContactEvent is a small struct to store contacts events that happened between different colliders. It
 * contains a collision distance, which is the amount of interpenetration that has happened during the contact
 * event, and a normal, pointing from the first collider to the second, and information about the primitives that
 * collided for each side of the event
 *
 */
template <typename C0, typename C1>
struct ContactEvent {
    ContactEventSide<C0> c0Contact;
    ContactEventSide<C1> c1Contact;

    Scalar distance{0};
    Vec3 normal{Vec3::Zero()};
};

}  // namespace mandos::core::collisions

#endif  // MANDOS_CORE_COLLISIONS_CONTACTEVENT_HPP