#include <Mandos/Core/Energies/RigidBodyInertia.hpp>

#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/linear_algebra.hpp>
#include <Mandos/Core/utility_functions.hpp>

namespace
{

inline void rigidBodyLocalAdvect(const mandos::core::Vec6 &x0,
                                 const mandos::core::Vec6 &v0,
                                 mandos::core::Scalar h,
                                 mandos::core::Vec3 &advX,
                                 mandos::core::Mat3 &advR)
{
    const mandos::core::Vec3 &theta0 = x0.segment<3>(3);
    const mandos::core::Vec3 &omega0 = v0.segment<3>(3);

    const mandos::core::Mat3 R0 = mandos::core::rotationExpMap(theta0);
    // const mandos::core::Mat3 R0old = mandos::core::rotationExpMap(theta0 - omega0 * h);
    const mandos::core::Mat3 R0old = mandos::core::rotationExpMap(h * omega0).transpose() * R0;

    advX = x0.segment<3>(0) + h * v0.segment<3>(0);  // x0 + h * v0
    advR = R0 + (R0 - R0old);                        // x0 + h * v0
}
inline void rigidBodyGlobalAdvect(const mandos::core::Vec6 &x0,
                                  const mandos::core::Vec6 &v0,
                                  mandos::core::Scalar h,
                                  mandos::core::Vec3 &advX,
                                  mandos::core::Mat3 &advR)
{
    const mandos::core::Vec3 &theta0 = x0.segment<3>(3);
    const mandos::core::Vec3 &omega0 = v0.segment<3>(3);

    const mandos::core::Mat3 R0 = mandos::core::rotationExpMap(theta0);
    const mandos::core::Mat3 R0old = mandos::core::rotationExpMap(theta0 - omega0 * h);

    advX = x0.segment<3>(0) + h * v0.segment<3>(0);  // x0 + h * v0
    advR = R0 + (R0 - R0old);                        // x0 + h * v0
}

inline mandos::core::Scalar rigidBodyEnergy(const mandos::core::Vec3 &x,
                                            const mandos::core::Mat3 &R,
                                            const mandos::core::Vec3 &advX,
                                            const mandos::core::Mat3 &advXR,
                                            mandos::core::Scalar mass,
                                            const mandos::core::Mat3 &inertiaTensor,
                                            mandos::core::Scalar h)
{
    const mandos::core::Mat3 deltaR = R - advXR;
    const mandos::core::Scalar h2 = h * h;

    const mandos::core::Scalar rotationEnergy =
        (deltaR * inertiaTensor * deltaR.transpose()).trace() / (mandos::core::Scalar{2.0} * h2);
    const mandos::core::Scalar traslationEnergy = mass * (x - advX).dot((x - advX)) / (mandos::core::Scalar{2.0} * h2);

    return traslationEnergy + rotationEnergy;
}

inline mandos::core::Vec6 rigidBodyLocalGradient(const mandos::core::Vec3 &x,
                                                 const mandos::core::Mat3 &R,
                                                 const mandos::core::Vec3 &advX,
                                                 const mandos::core::Mat3 &advXR,
                                                 mandos::core::Scalar mass,
                                                 const mandos::core::Mat3 &inertiaTensor,
                                                 mandos::core::Scalar h)
{
    const mandos::core::Mat3 rot_inertia = R * inertiaTensor * advXR.transpose();
    const mandos::core::Mat3 A = (rot_inertia - rot_inertia.transpose()) / 2.0;
    const mandos::core::Scalar h2 = h * h;

    const mandos::core::Vec3 gradient =
        2.0 * mandos::core::Vec3(-A(1, 2), A(0, 2), -A(0, 1)) / h2;  // v s.t. A = skew(v)

    mandos::core::Vec6 grad;
    grad.segment<3>(0) = mass * (x - advX) / h2;
    grad.segment<3>(3) = gradient;

    return grad;
}

inline mandos::core::Mat6 rigidBodyLocalHessian(const mandos::core::Vec3 & /*x*/,
                                                const mandos::core::Mat3 &R,
                                                const mandos::core::Vec3 & /*advX*/,
                                                const mandos::core::Mat3 &advXR,
                                                mandos::core::Scalar mass,
                                                const mandos::core::Mat3 &inertiaTensor,
                                                mandos::core::Scalar h)
{
    const mandos::core::Mat3 rot_inertia = R * inertiaTensor * advXR.transpose();
    const mandos::core::Mat3 S = (rot_inertia + rot_inertia.transpose()) / 2.0;  // Exact hessian

    // const mandos::core::Mat3 S = R * inertiaTensor * R.transpose(); // Linear approximation

    const mandos::core::Scalar h2 = h * h;

    // Hessian
    mandos::core::Mat6 hess = mandos::core::Mat6::Zero();
    hess.block<3, 3>(0, 0) = mass / h2 * mandos::core::Mat3::Identity();
    hess.block<3, 3>(3, 3) = 1.0 / h2 * (S.trace() * mandos::core::Mat3::Identity() - S);

    return hess;
}

inline mandos::core::Vec6 rigidBodyGlobalGradient(const mandos::core::Vec6 &x,
                                                  const mandos::core::Vec3 &advX,
                                                  const mandos::core::Mat3 &advXR,
                                                  const mandos::core::Scalar mass,
                                                  const mandos::core::Mat3 &inertiaTensor,
                                                  mandos::core::Scalar h)
{
    const mandos::core::Vec3 phi = x.segment<3>(3);

    const mandos::core::Mat3 rot_inertia = inertiaTensor * advXR.transpose();
    const mandos::core::Mat3 A = rot_inertia.transpose() - rot_inertia;
    const mandos::core::Mat3 S = (rot_inertia + rot_inertia.transpose()) / 2.0;
    const mandos::core::Mat3 SS = (S.trace() * mandos::core::Mat3::Identity() - S);
    const mandos::core::Vec3 v = mandos::core::Vec3(A(1, 2), -A(0, 2), A(0, 1));
    const mandos::core::Scalar phi_norm = phi.norm();
    const mandos::core::Scalar sinc_phi_2 = mandos::core::sinc(phi_norm / 2);
    const mandos::core::Scalar one_over_h2 = 1.0 / (h * h);

    const mandos::core::Vec3 gradient =
        (2.0 * mandos::core::grad_sinc(phi) * v.dot(phi) + 2.0 * mandos::core::sinc(phi_norm) * v +
         sinc_phi_2 * mandos::core::grad_sinc(phi / 2) * phi.transpose() * SS * phi +
         2.0 * sinc_phi_2 * sinc_phi_2 * SS * phi) *
        one_over_h2 * 0.5;

    mandos::core::Vec6 grad;
    grad.segment<3>(0) = mass * (x.segment<3>(0) - advX) * one_over_h2;
    grad.segment<3>(3) = gradient;
    return grad;
}

inline mandos::core::Mat6 rigidBodyGlobalHessian(const mandos::core::Vec6 &x,
                                                 const mandos::core::Vec3 & /*advX*/,
                                                 const mandos::core::Mat3 &advXR,
                                                 const mandos::core::Scalar mass,
                                                 const mandos::core::Mat3 &inertiaTensor,
                                                 mandos::core::Scalar h)
{
    const mandos::core::Vec3 phi = x.segment<3>(3);

    const mandos::core::Mat3 rot_inertia = inertiaTensor * advXR.transpose();
    const mandos::core::Mat3 A = rot_inertia.transpose() - rot_inertia;
    const mandos::core::Mat3 S = (rot_inertia + rot_inertia.transpose()) / 2.0;
    const mandos::core::Mat3 SS = (S.trace() * mandos::core::Mat3::Identity() - S);
    const mandos::core::Vec3 v = mandos::core::Vec3(A(1, 2), -A(0, 2), A(0, 1));
    const mandos::core::Scalar phi_norm = phi.norm();
    const mandos::core::Scalar sinc_phi_2 = mandos::core::sinc(phi_norm / 2);
    const mandos::core::Vec3 grad_sinc_phi_2 = 0.5 * mandos::core::grad_sinc(phi / 2.0);
    const mandos::core::Scalar phiSphi = phi.transpose() * SS * phi;
    const mandos::core::Scalar one_over_h2 = 1.0 / (h * h);

    const mandos::core::Mat3 hessian =
        (2.0 * mandos::core::hess_sinc(phi) * v.dot(phi) +
         2.0 * (v * mandos::core::grad_sinc(phi).transpose() + mandos::core::grad_sinc(phi) * v.transpose()) +
         2.0 * grad_sinc_phi_2 * grad_sinc_phi_2.transpose() * phiSphi +
         2.0 * sinc_phi_2 * 0.25 * mandos::core::hess_sinc(phi / 2.0) * phiSphi +
         4.0 * sinc_phi_2 * ((SS * phi) * grad_sinc_phi_2.transpose() + grad_sinc_phi_2 * (SS * phi).transpose()) +
         2.0 * sinc_phi_2 * sinc_phi_2 * SS) *
        one_over_h2 * 0.5;

    mandos::core::Mat6 hess = mandos::core::Mat6::Zero();
    hess.block<3, 3>(0, 0) = mass * one_over_h2 * mandos::core::Mat3::Identity();
    hess.block<3, 3>(3, 3) = hessian;
    return hess;
}

inline mandos::core::Mat6 rigidBodyLocalRetardedPositionHessian(const mandos::core::Mat3 &R,
                                                                const mandos::core::Vec3 &theta0,
                                                                const mandos::core::Vec3 &omega0,
                                                                mandos::core::Scalar mass,
                                                                const mandos::core::Mat3 &inertiaTensor,
                                                                mandos::core::Scalar h)
{
    using mandos::core::Scalar;
    const mandos::core::Scalar h2 = h * h;

    const Eigen::Matrix<Scalar, 3, 9> vLeviCivita = mandos::core::vectorizedLeviCivita();
    // const Eigen::Matrix<Scalar, 3, 9> dvecRguess_dtheta0 =
    //     2 * computeVectorizedRotationMatrixDerivativeGlobal(theta0) -
    //     computeVectorizedRotationMatrixDerivativeGlobal(theta0 - omega0 * h);

    const Eigen::Matrix<Scalar, 9, 3> dvecRguess_dtheta0 =
        mandos::core::blockDiagonalMatrix<3>(2 * mandos::core::Mat3::Identity() -
                                             mandos::core::rotationExpMap(h * omega0).transpose()) *
        mandos::core::computeVectorizedRotationMatrixDerivativeLocal(theta0).transpose();

    const Eigen::Matrix<Scalar, 9, 3> dvecRMRguess_dtheta0 =
        mandos::core::blockMatrix<3>(R * inertiaTensor) * dvecRguess_dtheta0;

    const Eigen::Matrix<Scalar, 9, 3> dvecAdtheta0 =
        0.5 * (mandos::core::transposeVectorizedMatrixRows<9, 3>(dvecRMRguess_dtheta0) - dvecRMRguess_dtheta0);

    // Hessian
    mandos::core::Mat6 hess = mandos::core::Mat6::Zero();
    hess.block<3, 3>(0, 0) = -mass / h2 * mandos::core::Mat3::Identity();
    hess.block<3, 3>(3, 3) = 1.0 / h2 * vLeviCivita * dvecAdtheta0;

    return hess;
}

inline mandos::core::Mat6 rigidBodyLocalRetardedVelocityHessian(const mandos::core::Mat3 &R,
                                                                const mandos::core::Vec3 &theta0,
                                                                const mandos::core::Vec3 &omega0,
                                                                mandos::core::Scalar mass,
                                                                const mandos::core::Mat3 &inertiaTensor,
                                                                mandos::core::Scalar h)
{
    using mandos::core::Scalar;
    const mandos::core::Scalar h2 = h * h;
    const Eigen::Matrix<Scalar, 3, 9> vLeviCivita = mandos::core::vectorizedLeviCivita();

    // const Eigen::Matrix<Scalar, 3, 9> dvecRguess_domega0 =
    //     h * computeVectorizedRotationMatrixDerivativeGlobal(theta0 - omega0 * h);

    const mandos::core::Mat3 R0 = mandos::core::rotationExpMap(theta0);
    const Eigen::Matrix<Scalar, 9, 3> dvecRguess_domega0 =
        -h * mandos::core::transposeVectorizedMatrixRows<9, 3>(
                 mandos::core::blockDiagonalMatrix<3>(R0.transpose()) *
                 mandos::core::computeVectorizedRotationMatrixDerivativeLocal(h * omega0).transpose());

    const Eigen::Matrix<Scalar, 9, 3> dvecRMR_guess_domega0 =
        mandos::core::blockMatrix<3>(R * inertiaTensor) * dvecRguess_domega0;

    const Eigen::Matrix<Scalar, 9, 3> dvecAdomega0 =
        0.5 * (mandos::core::transposeVectorizedMatrixRows<9, 3>(dvecRMR_guess_domega0) - dvecRMR_guess_domega0);

    // Hessian
    mandos::core::Mat6 hess = mandos::core::Mat6::Zero();
    hess.block<3, 3>(0, 0) = -mass / h * mandos::core::Mat3::Identity();
    hess.block<3, 3>(3, 3) = 1.0 / h2 * vLeviCivita * dvecAdomega0;

    return hess;
}

}  // namespace

namespace mandos::core
{

void mandos::core::RigidBodyInertia::advect(const MechanicalState<RigidBodyTag> &mstate, Scalar h)
{
    m_advX.resize(mstate.m_x.size());
    m_advXR.resize(mstate.m_x.size());
    m_x0 = mstate.m_x;
    m_v0 = mstate.m_v;

    for (auto i = 0UL; i < mstate.m_x.size(); ++i) {
        rigidBodyLocalAdvect(mstate.m_x[i], mstate.m_v[i], h, m_advX[i], m_advXR[i]);
    }
}

void mandos::core::RigidBodyInertia::advect(const MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h)
{
    m_advX.resize(mstate.m_x.size());
    m_advXR.resize(mstate.m_x.size());
    for (auto i = 0UL; i < mstate.m_x.size(); ++i) {
        rigidBodyGlobalAdvect(mstate.m_x[i], mstate.m_v[i], h, m_advX[i], m_advXR[i]);
    }
}

Scalar RigidBodyInertia::computeEnergy(const MechanicalState<RigidBodyTag> &mstate, Scalar h) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        energy +=
            rigidBodyEnergy(mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
    }
    return energy;
}

Scalar RigidBodyInertia::computeEnergy(const MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        energy +=
            rigidBodyEnergy(mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
    }
    return energy;
}

Scalar RigidBodyInertia::computeEnergyAndGradient(MechanicalState<RigidBodyTag> &mstate, Scalar h) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        mstate.m_grad[i] += rigidBodyLocalGradient(
            mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
        energy +=
            rigidBodyEnergy(mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
    }
    return energy;
}

Scalar RigidBodyInertia::computeEnergyAndGradient(MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h) const
{
    Scalar energy{0};
    for (auto i = 0UL; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        mstate.m_grad[i] +=
            rigidBodyGlobalGradient(mstate.m_x[i], m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
        energy +=
            rigidBodyEnergy(mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
    }
    return energy;
}

Scalar RigidBodyInertia::computeEnergyGradientAndHessian(MechanicalState<RigidBodyTag> &mstate, Scalar h) const
{
    Scalar energy{0};
    std::vector<Triplet> triplets;
    for (unsigned int i = 0; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        mstate.m_grad[i] += rigidBodyLocalGradient(
            mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
        const Mat6 hess = rigidBodyLocalHessian(
            mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
        for (unsigned int j = 0; j < 3; ++j) {
            triplets.emplace_back(6 * i + j, 6 * i + j, hess(j, j));  // Diagonal translation hessian
            for (unsigned int k = 0; k < 3; ++k) {
                triplets.emplace_back(
                    6 * i + j + 3, 6 * i + k + 3, hess(3 + j, 3 + k));  // Non-diagonal rotation hessian
            }
        }
        energy +=
            rigidBodyEnergy(mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
    }

    SparseMat energyHessian;
    energyHessian.resize(mstate.size(), mstate.size());
    energyHessian.setFromTriplets(triplets.begin(), triplets.end());

    mstate.m_hessian += energyHessian;

    return energy;
}

Scalar RigidBodyInertia::computeEnergyGradientAndHessian(MechanicalState<RigidBodyGlobalTag> &mstate, Scalar h) const
{
    Scalar energy{0};
    std::vector<Triplet> triplets;
    for (unsigned int i = 0; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        mstate.m_grad[i] +=
            rigidBodyGlobalGradient(mstate.m_x[i], m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
        const Mat6 hess =
            rigidBodyGlobalHessian(mstate.m_x[i], m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
        for (unsigned int j = 0; j < 3; ++j) {
            triplets.emplace_back(6 * i + j, 6 * i + j, hess(j, j));  // Diagonal translation hessian
            for (unsigned int k = 0; k < 3; ++k) {
                triplets.emplace_back(
                    6 * i + j + 3, 6 * i + k + 3, hess(3 + j, 3 + k));  // Non-diagonal rotation hessian
            }
        }
        energy +=
            rigidBodyEnergy(mstate.m_x[i].segment<3>(0), R, m_advX[i], m_advXR[i], m_mass[i], m_inertiaTensor0[i], h);
    }

    SparseMat energyHessian;
    energyHessian.resize(mstate.size(), mstate.size());
    energyHessian.setFromTriplets(triplets.begin(), triplets.end());

    mstate.m_hessian += energyHessian;

    return energy;
}

void RigidBodyInertia::computeEnergyRetardedPositionHessian(MechanicalState<RigidBodyTag> &mstate,
                                                            Scalar h,
                                                            unsigned int offset,
                                                            std::vector<Triplet> &triplets) const
{
    for (unsigned int i = 0; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        const Mat6 hess = rigidBodyLocalRetardedPositionHessian(
            R, m_x0[i].segment<3>(3), m_v0[i].segment<3>(3), m_mass[i], m_inertiaTensor0[i], h);
        for (unsigned int j = 0; j < 3; ++j) {
            triplets.emplace_back(offset + 6 * i + j, offset + 6 * i + j, hess(j, j));  // Diagonal translation hessian
            for (unsigned int k = 0; k < 3; ++k) {
                triplets.emplace_back(offset + 6 * i + j + 3,
                                      offset + 6 * i + k + 3,
                                      hess(3 + j, 3 + k));  // Non-diagonal rotation hessian
            }
        }
    }
}

void RigidBodyInertia::computeEnergyRetardedVelocityHessian(MechanicalState<RigidBodyTag> &mstate,
                                                            Scalar h,
                                                            unsigned int offset,
                                                            std::vector<Triplet> &triplets) const
{
    for (unsigned int i = 0; i < mstate.m_x.size(); ++i) {
        const Mat3 R = rotationExpMap(mstate.m_x[i].segment<3>(3));
        const Mat6 hess = rigidBodyLocalRetardedVelocityHessian(
            R, m_x0[i].segment<3>(3), m_v0[i].segment<3>(3), m_mass[i], m_inertiaTensor0[i], h);
        for (unsigned int j = 0; j < 3; ++j) {
            triplets.emplace_back(offset + 6 * i + j, offset + 6 * i + j, hess(j, j));  // Diagonal translation hessian
            for (unsigned int k = 0; k < 3; ++k) {
                triplets.emplace_back(offset + 6 * i + j + 3,
                                      offset + 6 * i + k + 3,
                                      hess(3 + j, 3 + k));  // Non-diagonal rotation hessian
            }
        }
    }
}

void RigidBodyInertia::computeEnergyRetardedPositionHessian(MechanicalState<RigidBodyGlobalTag> & /*unused*/,
                                                            Scalar /*unused*/,
                                                            unsigned int /*unused*/,
                                                            std::vector<Triplet> & /*unused*/) const
{
    // TODO
}
void RigidBodyInertia::computeEnergyRetardedVelocityHessian(MechanicalState<RigidBodyGlobalTag> & /*unused*/,
                                                            Scalar /*unused*/,
                                                            unsigned int /*unused*/,
                                                            std::vector<Triplet> & /*unused*/) const
{
    // TODO
}

std::vector<Mat3> &mandos::core::RigidBodyInertia::inertiaTensor()
{
    return m_inertiaTensor0;
}

const std::vector<Mat3> &mandos::core::RigidBodyInertia::inertiaTensor() const
{
    return m_inertiaTensor0;
}

const std::vector<Scalar> &mandos::core::RigidBodyInertia::mass() const
{
    return m_mass;
}

std::vector<Scalar> &mandos::core::RigidBodyInertia::mass()
{
    return m_mass;
}

}  // namespace mandos::core
