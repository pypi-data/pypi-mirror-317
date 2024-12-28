#ifndef MANDOS_SYSTEMMATRIX_H
#define MANDOS_SYSTEMMATRIX_H

#include <Mandos/Core/linear_algebra.hpp>

#include <Mandos/Core/Model.hpp>
#include <Mandos/Core/Projections.hpp>
#include <Mandos/Core/Simulation.hpp>

#include <Eigen/IterativeLinearSolvers>
#include <Mandos/Core/utility_functions.hpp>
#include <unsupported/Eigen/IterativeSolvers>

#include <tracy/Tracy.hpp>

namespace mandos::core
{
struct SystemMatrix;
}

namespace Eigen::internal
{
// MatrixReplacement looks-like a SparseMatrix, so let's inherits its traits:
template <>
struct traits<mandos::core::SystemMatrix> : public traits<mandos::core::SparseMat> {
};
}  // namespace Eigen::internal

namespace mandos::core
{
/**
 * @brief The SystemMatrix class represents the system matrix that it is solved during the Newton solve.
 * Instead of assembling a big matrix for all the SimulationObjects and Couplings, we store ach generalized block of the
 * matrix directly, and we override the GMEV operation for using it with a CG solver.
 *
 * Since the system matrix is symmetric, we only store the blocks in the diagonal and below the diagonal. Each block has
 * associated two offsets. The `in` offset represents the offset in the generalized input vector and the `out` offset
 * represents the offset in the generalized output vector
 *
 * The projections are also stored in the SystemMatrix class, and are pre and post applied
 *
 */

struct SystemMatrix : public Eigen::EigenBase<SystemMatrix> {
public:
    using Scalar = mandos::core::Scalar;
    using RealScalar = mandos::core::Scalar;
    using StorageIndex = int;
    enum {
        ColsAtCompileTime = Eigen::Dynamic,  //
        MaxColsAtCompileTime = Eigen::Dynamic,
        IsRowMajor = static_cast<int>(false)
    };

    SystemMatrix(int rows, int cols);

    int rows() const;
    int cols() const;

    void clear();

    template <typename Rhs>
    Eigen::Product<SystemMatrix, Rhs, Eigen::AliasFreeProduct> operator*(const Eigen::MatrixBase<Rhs> &x) const
    {
        return ::Eigen::Product<SystemMatrix, Rhs, Eigen::AliasFreeProduct>(*this, x.derived());
    }

    void setModel(Model &model);
    Model &model() const;
    const Model::KinematicGraph &graph() const;

    void setFreeSimulationObject(const std::vector<Model::KinematicGraph::vertex_descriptor> &freeSimulationObjects);
    const std::vector<Model::KinematicGraph::vertex_descriptor> &freeSimulationObjects() const;

    void setForwardSortedList(const std::vector<Model::KinematicGraph::vertex_descriptor> &forwardSortedList);
    const std::vector<Model::KinematicGraph::vertex_descriptor> &forwardSortedList() const;

    void setBackwardSortedList(const std::vector<Model::KinematicGraph::vertex_descriptor> &backwardSortedList);
    const std::vector<Model::KinematicGraph::vertex_descriptor> &backwardSortedList() const;

private:
    int m_rows;
    int m_cols;

    Model *m_model{nullptr};
    const std::vector<Model::KinematicGraph::vertex_descriptor> *m_freeSimulationObjects{nullptr};
    const std::vector<Model::KinematicGraph::vertex_descriptor> *m_forwardSortedList{nullptr};
    const std::vector<Model::KinematicGraph::vertex_descriptor> *m_backwardSortedList{nullptr};
};

}  // namespace mandos::core

// Implementation of MatrixReplacement * Eigen::DenseVector though a specialization of internal::generic_product_impl:
namespace Eigen::internal
{

template <typename Rhs>
struct generic_product_impl<mandos::core::SystemMatrix, Rhs, SparseShape, DenseShape, GemvProduct>  // GEMV stands for
                                                                                                    // matrix-vector
    : generic_product_impl_base<mandos::core::SystemMatrix,
                                Rhs,
                                generic_product_impl<mandos::core::SystemMatrix, Rhs>> {
    typedef typename Product<mandos::core::SystemMatrix, Rhs>::Scalar Scalar;

    template <typename Dest>
    static void scaleAndAddTo(Dest &dst, const mandos::core::SystemMatrix &lhs, const Rhs &rhs, const Scalar &alpha)
    {
        ZoneScopedN("H*dx");
        // This method should implement "dst += alpha * lhs * rhs" inplace,
        // however, for iterative solvers, alpha is always equal to 1, so let's not bother about it.
        assert(alpha == Scalar(1) && "scaling is not implemented");
        EIGEN_ONLY_USED_FOR_DEBUG(alpha);

        // Clear the gradient so we can store there the dx
        for (auto node : lhs.forwardSortedList()) {
            std::visit(
                [&lhs](auto handle) {
                    auto &simulationObject = lhs.model().simulationObject(handle);
                    simulationObject.mstate.clearGradient();
                },
                lhs.graph()[node]);
        }

        // Set the dx for the free SimulationObjects, applying projections if needed
        int offset = 0;
        for (auto node : lhs.freeSimulationObjects()) {
            const auto &simObjectV = lhs.graph()[node];
            std::visit(
                [&lhs, &offset, &rhs](auto handle) {
                    auto &simulationObject = lhs.model().simulationObject(handle);
                    const auto size = simulationObject.mstate.size();
                    simulationObject.mstate.setGradient(rhs.segment(offset, size));

                    using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                    if constexpr (SimulationObjectT::hasProjections) {
                        mandos::core::utilities::static_for_each(
                            [&simulationObject](const auto &projection) {
                                projection.applyP(simulationObject.mstate.gradientView());
                            },
                            simulationObject.projections);
                    }

                    offset += size;
                },
                simObjectV);
        }

        // Propagate the dx to mapped objects
        for (auto node : lhs.forwardSortedList()) {
            const auto &simObjectV = lhs.graph()[node];
            std::visit(
                [&lhs](auto handle) {
                    const auto &simulationObject = lhs.model().simulationObject(handle);
                    using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                    if constexpr (SimulationObjectT::hasMappings) {
                        mandos::core::utilities::static_for_each(
                            [&lhs, &simulationObject](const auto &mappings) {
                                for (const auto &mapping : mappings) {
                                    auto to = mapping.to();

                                    mapping.applyJ(simulationObject.mstate.m_grad,
                                                   lhs.model().simulationObject(to).mstate.m_grad);
                                }
                            },
                            simulationObject.m_mappings);
                    }
                },
                simObjectV);
        }

        // For each object, multiply by its local hessian
        for (auto node : lhs.forwardSortedList()) {
            std::visit(
                [&lhs](auto handle) {
                    auto &simulationObject = lhs.model().simulationObject(handle);
                    simulationObject.mstate.scaleGradByHessian();
                },
                lhs.graph()[node]);
        }

        // And propagate back the H*dx through mappings
        for (auto node : lhs.backwardSortedList()) {
            const auto &simObjectV = lhs.graph()[node];
            std::visit(
                [&lhs](auto handle) {
                    const auto &simulationObject = lhs.model().simulationObject(handle);
                    using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                    if constexpr (SimulationObjectT::hasMappings) {
                        mandos::core::utilities::static_for_each(
                            [&lhs](const auto &mappings) {
                                for (const auto &mapping : mappings) {
                                    auto fromHandle = mapping.from();
                                    auto toHandle = mapping.to();

                                    auto &from = lhs.model().simulationObject(fromHandle);
                                    auto &to = lhs.model().simulationObject(toHandle);

                                    mapping.applyJT(from.mstate.m_grad, to.mstate.m_grad);
                                }
                            },
                            simulationObject.m_mappings);
                    }
                },
                simObjectV);
        }

        // And finally, accumulate on the dst, taking into account the projections if needed
        offset = 0;
        for (auto node : lhs.freeSimulationObjects()) {
            const auto &simObjectV = lhs.graph()[node];
            std::visit(
                [&lhs, &dst, &offset](auto handle) {
                    auto &simulationObject = lhs.model().simulationObject(handle);
                    const auto size = simulationObject.mstate.size();

                    using SimulationObjectT = std::remove_reference_t<std::remove_cvref_t<decltype(simulationObject)>>;
                    if constexpr (SimulationObjectT::hasProjections) {
                        mandos::core::utilities::static_for_each(
                            [&simulationObject](const auto &projection) {
                                projection.applyPT(simulationObject.mstate.gradientView());
                            },
                            simulationObject.projections);
                    }
                    simulationObject.mstate.gradient(dst.segment(offset, size));
                    offset += size;
                },
                simObjectV);
        }
    }
};

}  // namespace Eigen::internal

#endif  // MANDOS_SYSTEMMATRIX_H
