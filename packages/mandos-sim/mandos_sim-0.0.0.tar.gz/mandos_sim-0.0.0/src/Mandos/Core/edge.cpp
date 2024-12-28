#include <Mandos/Core/edge.hpp>

unsigned int std::hash<mandos::core::Edge>::operator()(const mandos::core::Edge &key) const
{
    return 100000 * key.a + key.b;
}

namespace mandos::core
{

bool operator==(const Edge &e1, const Edge &e2)
{
    return (e1.a == e2.a) and (e1.b == e2.b);
}

}  // namespace mandos::core