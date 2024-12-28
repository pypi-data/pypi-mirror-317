#include <Mandos/Core/Collisions/CollisionDetection.hpp>

#include <tracy/Tracy.hpp>

#include <oneapi/tbb/blocked_range.h>
#include <oneapi/tbb/enumerable_thread_specific.h>

namespace mandos::core::collisions
{

std::vector<ContactEvent<SDF, SphereCloud>> collisions(const SDF &sdf, const SphereCloud &sc)
{
    ZoneScopedN("SDF/SphereCloud collision detection");

    const auto &centers{sc.centers()};
    const auto &radius{sc.radius()};

    tbb::enumerable_thread_specific<std::vector<ContactEvent<SDF, SphereCloud>>> contactsTLS;

    tbb::parallel_for(tbb::blocked_range<std::size_t>(0, centers.size()),
                      [&](const tbb::blocked_range<std::size_t> &range) {
                          auto &contacts = contactsTLS.local();
                          for (auto sId = range.begin(); sId != range.end(); ++sId) {
                              const auto &center = centers[sId];
                              const auto r = radius[sId];

                              auto d = sdf.vdb().distance(center);
                              // If the distance is below the radius of the sphere, we consider there is a contact
                              if (d < r) {
                                  // Compute the gradient of the distance field at this particular location using finite
                                  // differences
                                  const auto rdiff = 0.01 * sdf.vdb().voxelSize();
                                  auto xplus = sdf.vdb().distance(center + Vec3{rdiff, 0, 0});
                                  auto xminus = sdf.vdb().distance(center - Vec3{rdiff, 0, 0});
                                  auto yplus = sdf.vdb().distance(center + Vec3{0, rdiff, 0});
                                  auto yminus = sdf.vdb().distance(center - Vec3{0, rdiff, 0});
                                  auto zplus = sdf.vdb().distance(center + Vec3{0, 0, rdiff});
                                  auto zminus = sdf.vdb().distance(center - Vec3{0, 0, rdiff});

                                  const auto n = Vec3{xplus - xminus, yplus - yminus, zplus - zminus}.normalized();

                                  const auto primitiveId = sdf.vdb().closestPolygon(center);

                                  const ContactEventSide<SDF> c0Side{primitiveId, center - d * n};
                                  const ContactEventSide<SphereCloud> c1Side{static_cast<int>(sId)};

                                  contacts.emplace_back(c0Side, c1Side, d, n);
                              }
                          }
                      });

    std::vector<ContactEvent<SDF, SphereCloud>> contacts;
    const auto flattened = tbb::flatten2d(contactsTLS);
    contacts.reserve(flattened.size());
    contacts.insert(contacts.end(), flattened.begin(), flattened.end());
    return contacts;
}

}  // namespace mandos::core::collisions
