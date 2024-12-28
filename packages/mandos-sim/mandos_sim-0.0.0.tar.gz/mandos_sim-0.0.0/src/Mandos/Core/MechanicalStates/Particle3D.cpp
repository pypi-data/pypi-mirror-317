#include <Mandos/Core/MechanicalStates/Particle3D.hpp>

#include <Mandos/Core/linear_algebra.hpp>

#include <Eigen/Dense>

#include <vector>

namespace mandos::core
{

void mandos::core::MechanicalState<Particle3DTag>::advect(std::vector<Vec3> &advX, Scalar h) const
{
    for (auto i{0UL}; i < m_x.size(); ++i) {
        advX[i] = m_x[i] + h * m_v[i];
    }
}
void mandos::core::MechanicalState<Particle3DTag>::updateState(const Eigen::Ref<const Vec> &dx,
                                                               const Eigen::Ref<const Vec> &x0,
                                                               const Eigen::Ref<const Vec> & /*v0*/,
                                                               Scalar h)
{
    Vec::MapType(m_x.data()->data(), size()) += dx;
    Vec::MapType(m_v.data()->data(), size()) = (Vec::ConstMapType(m_x.data()->data(), size()) - x0) / h;
}
void mandos::core::MechanicalState<Particle3DTag>::clearGradient()
{
    Eigen::Matrix<Scalar, Eigen::Dynamic, 3>::MapType(
        m_grad.data()->data(), static_cast<Eigen::Index>(m_grad.size()), 3)
        .setZero();
}
void mandos::core::MechanicalState<Particle3DTag>::setState(const Eigen::Ref<const Vec> &x,
                                                            const Eigen::Ref<const Vec> &v)
{
    Vec::MapType(this->m_x.data()->data(), size()) = x;
    Vec::MapType(this->m_v.data()->data(), size()) = v;
}
void mandos::core::MechanicalState<Particle3DTag>::gradient(Eigen::Ref<Vec> grad) const
{
    grad += Vec::ConstMapType(this->m_grad.data()->data(), size());
}
Eigen::Map<Vec> mandos::core::MechanicalState<Particle3DTag>::gradientView()
{
    return {m_grad.data()->data(), size()};
}
void mandos::core::MechanicalState<Particle3DTag>::state(Eigen::Ref<Vec> x, Eigen::Ref<Vec> v) const
{
    x = Vec::ConstMapType(this->m_x.data()->data(), size());
    v = Vec::ConstMapType(this->m_v.data()->data(), size());
}
int mandos::core::MechanicalState<Particle3DTag>::size() const
{
    return static_cast<int>(3 * m_x.size());
}

void MechanicalState<Particle3DTag>::setZero()
{
    Vec::MapType(this->m_x.data()->data(), size()).setZero();
    Vec::MapType(this->m_v.data()->data(), size()).setZero();
}
void MechanicalState<Particle3DTag>::setGradient(const Eigen::Ref<const Vec> &gradient)
{
    Vec::MapType(this->m_grad.data()->data(), size()) = gradient;
}
void MechanicalState<Particle3DTag>::scaleGradByHessian()
{
    Vec::MapType(this->m_grad.data()->data(), size()) =
        m_hessian * Vec::ConstMapType(this->m_grad.data()->data(), size());
}
void MechanicalState<Particle3DTag>::clearHessian()
{
    m_hessian.setZero();
}
}  // namespace mandos::core
