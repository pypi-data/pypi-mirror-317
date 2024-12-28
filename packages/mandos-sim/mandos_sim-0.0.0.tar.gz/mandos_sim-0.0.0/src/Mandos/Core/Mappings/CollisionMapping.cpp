
#include <Mandos/Core/Mappings/CollisionMapping.hpp>

#include <Mandos/Core/Collisions/SDF.hpp>
#include <Mandos/Core/MechanicalStates/Particle3D.hpp>
#include <Mandos/Core/MechanicalStates/RigidBody.hpp>
#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/SimulationObject.hpp>

#include <tracy/Tracy.hpp>

namespace mandos::core::collisions
{

void updateMapping(const collisions::ContactEventSide<SphereCloud> &contact,
                   CollisionMapping<Particle3DTag, SphereCloud> &mapping,
                   int collisionParticle)
{
    ZoneScopedN("updateMapping<Particle3DTag, SphereCloud>");
    const MappingInfo<Particle3DTag, SphereCloud> mappingInfo{static_cast<std::size_t>(contact.sphereId),
                                                              static_cast<std::size_t>(collisionParticle)};
    mapping.addMappingInfo(mappingInfo);
}

void updateMapping(const collisions::ContactEventSide<SDF> &contact,
                   CollisionMapping<RigidBodyTag, SDF> &mapping,
                   int collisionParticle)
{
    ZoneScopedN("updateMapping<RigidBodyTag, SDF>");
    // Compute the current RB transform
    const auto &mstate = mapping.from()->mstate;
    const Vec3 r = mandos::core::rotationExpMap(mstate.m_x[0].segment<3>(3)).transpose() *
                   (contact.contactPoint - mstate.m_x[0].segment<3>(0));

    const MappingInfo<RigidBodyTag, SDF> mappingInfo{
        r, mapping.from()->mstate, static_cast<std::size_t>(collisionParticle)};
    mapping.addMappingInfo(mappingInfo);
}

void MappingInfo<RigidBodyTag, SDF>::apply(const std::vector<Vec6> &from, std::vector<Vec3> &to) const
{
    ZoneScopedN("MappingInfo<RigidBody, SDF>.apply");

    const Vec3 centerOfMass = from[0].segment<3>(0);
    const Mat3 R = rotationExpMap(from[0].segment<3>(3));

    to[m_toId] += R * m_r + centerOfMass;
}

void MappingInfo<RigidBodyTag, SDF>::applyJ(const std::vector<Vec6> &from, std::vector<Vec3> &to) const
{
    const Mat3 R = rotationExpMap(mstate.m_x[0].segment<3>(3));
    const Mat3 thetaJ = -skew(R * m_r);
    to[m_toId] += from[0].segment<3>(0);
    to[m_toId] += thetaJ * from[0].segment<3>(3);
}
void MappingInfo<RigidBodyTag, SDF>::applyJT(std::vector<Vec6> &from, const std::vector<Vec3> &to) const
{
    const Mat3 R = rotationExpMap(mstate.m_x[0].segment<3>(3));
    const Mat3 thetaJT = skew(R * m_r);
    from[0].segment<3>(0) += to[m_toId];
    from[0].segment<3>(3) += thetaJT * to[m_toId];
}

void MappingInfo<Particle3DTag, SphereCloud>::apply(const std::vector<Vec3> &from, std::vector<Vec3> &to) const
{
    ZoneScopedN("MappingInfo<Particle3DTag, SphereCloud>.apply");
    to[m_toId] = from[m_fromId];
}
void MappingInfo<Particle3DTag, SphereCloud>::applyJ(const std::vector<Vec3> &from, std::vector<Vec3> &to) const
{
    ZoneScopedN("MappingInfo<Particle3DTag, SphereCloud>.applyJ");
    to[m_toId] = from[m_fromId];
}
void MappingInfo<Particle3DTag, SphereCloud>::applyJT(std::vector<Vec3> &from, const std::vector<Vec3> &to) const
{
    ZoneScopedN("MappingInfo<Particle3DTag, SphereCloud>.applyJT");
    from[m_fromId] += to[m_toId];
}
}  // namespace mandos::core::collisions
