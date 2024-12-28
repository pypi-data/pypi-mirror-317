#include <Mandos/Core/linear_algebra.hpp>

namespace mandos::core
{

Eigen::Matrix<Scalar, 3, 9> vectorizedLeviCivita()
{
    Eigen::Matrix<Scalar, 3, 9> e{{0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0},  //
                                  {0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0},  //
                                  {0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
    return e;
}
}  // namespace mandos::core
