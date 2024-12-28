#include <Mandos/Core/MechanicalStates/RigidBodyCommon.hpp>

namespace mandos::core
{

int RigidBodyCommon::size() const
{
    return 6 * static_cast<int>(m_x.size());
}

void RigidBodyCommon::state(Eigen::Ref<Vec> x, Eigen::Ref<Vec> v) const
{
    x = Vec::ConstMapType(this->m_x.data()->data(), size());
    v = Vec::ConstMapType(this->m_v.data()->data(), size());
}

void RigidBodyCommon::gradient(Eigen::Ref<Vec> grad) const
{
    grad += Vec::ConstMapType(this->m_grad.data()->data(), size());
}

Eigen::Map<Vec> RigidBodyCommon::gradientView()
{
    return {m_grad.data()->data(), size()};
}

void RigidBodyCommon::setState(const Eigen::Ref<const Vec> &x, const Eigen::Ref<const Vec> &v)
{
    Vec::MapType(this->m_x.data()->data(), size()) = x;
    Vec::MapType(this->m_v.data()->data(), size()) = v;
}

void RigidBodyCommon::clearGradient()
{
    Eigen::Matrix<Scalar, Eigen::Dynamic, 6>::MapType(
        m_grad.data()->data(), static_cast<Eigen::Index>(m_grad.size()), 6)
        .setZero();
}

void RigidBodyCommon::clearHessian()
{
    m_hessian.setZero();
}

void RigidBodyCommon::setZero()
{
    Vec::MapType(this->m_x.data()->data(), size()).setZero();
    Vec::MapType(this->m_v.data()->data(), size()).setZero();
}

void RigidBodyCommon::setGradient(const Eigen::Ref<const Vec> &gradient)
{
    Vec::MapType(this->m_grad.data()->data(), size()) = gradient;
}

void RigidBodyCommon::scaleGradByHessian()
{
    Vec::MapType(this->m_grad.data()->data(), size()) =
        m_hessian * Vec::ConstMapType(this->m_grad.data()->data(), size());
}

}  // namespace mandos::core
