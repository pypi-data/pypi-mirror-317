#include <Mandos/Core/Energies/StableNeoHookean.hpp>

#include <stdexcept>
#include <vector>

#include <Eigen/Dense>
#include <Eigen/Sparse>

#include <Mandos/Core/RotationUtilities.hpp>
#include <Mandos/Core/linear_algebra.hpp>

#include <tracy/Tracy.hpp>

#include <boost/graph/compressed_sparse_row_graph.hpp>
#include <boost/graph/sequential_vertex_coloring.hpp>

#include <oneapi/tbb/blocked_range.h>
#include <oneapi/tbb/enumerable_thread_specific.h>
#include <oneapi/tbb/parallel_for.h>

#include <fmt/format.h>

namespace mandos::core
{

int StableNeoHookean::size() const
{
    return static_cast<int>(m_indices.size());
}

Scalar StableNeoHookean::computeEnergy(const MechanicalState<Particle3DTag> &mstate) const
{
    ZoneScopedN("StableNeoHookean.computeEnergy");
    tbb::enumerable_thread_specific<Scalar> energyTLS;
    for (const auto &parallelGroup : m_parallelGroups) {
        ZoneScopedN("StableNeoHookean.computeEnergy.group");
        tbb::parallel_for(tbb::blocked_range<std::size_t>(0, parallelGroup.size()),
                          [&](const tbb::blocked_range<std::size_t> &r) {
                              bool exists{};
                              auto &energy = energyTLS.local(exists);
                              if (!exists) {
                                  energy = 0;
                              }
                              ZoneScopedN("StableNeoHookean.computeEnergy.range");
                              for (auto rId = r.begin(); rId != r.end(); ++rId) {
                                  const auto elementId = parallelGroup[rId];

                                  const auto &indices{m_indices[elementId]};

                                  auto ds{Eigen::Matrix<Scalar, 3, 3>{}};
                                  ds.col(0) = mstate.m_x[static_cast<std::size_t>(indices[1])] -
                                              mstate.m_x[static_cast<std::size_t>(indices[0])];
                                  ds.col(1) = mstate.m_x[static_cast<std::size_t>(indices[2])] -
                                              mstate.m_x[static_cast<std::size_t>(indices[0])];
                                  ds.col(2) = mstate.m_x[static_cast<std::size_t>(indices[3])] -
                                              mstate.m_x[static_cast<std::size_t>(indices[0])];

                                  const auto &F{(ds * m_invDm[elementId]).eval()};

                                  const auto &mu = m_mu[elementId];
                                  const auto &lambda = m_lambda[elementId];

                                  const auto I2{(F.transpose() * F).trace()};
                                  const auto I3{F.determinant()};

                                  energy += m_volume[elementId] * (mu / Scalar{2.0} * (I2 - 3) - mu * (I3 - 1) +
                                                                   lambda / Scalar{2.0} * (I3 - 1) * (I3 - 1));
                              }
                          });
    }

    return energyTLS.combine(std::plus{});
}

void StableNeoHookean::addElement(const std::array<int, 4> &indices, const ParameterSet &parameterSet)
{
    ZoneScopedN("StableNeoHookean.addElement");
    m_indices.push_back(indices);

    m_lambda.emplace_back();
    m_mu.emplace_back();
    m_volume.emplace_back();
    m_invDm.emplace_back();
    m_dFdx.emplace_back();

    configureElement(static_cast<std::size_t>(size() - 1), parameterSet);
}

void StableNeoHookean::configureElement(std::size_t elementId, const ParameterSet &parameterSet)
{
    m_lambda[elementId] = parameterSet.lambda;
    m_mu[elementId] = parameterSet.mu;

    const auto dm = parameterSet.restPoseMatrix;

    m_volume[elementId] = Scalar{1.0} / Scalar{6.0} * dm.determinant();

    const auto &invDm = dm.inverse();
    m_invDm[elementId] = invDm;

    // Apendix E from T.Kim Siggraph course
    const Scalar m = invDm(0, 0);
    const Scalar n = invDm(0, 1);
    const Scalar o = invDm(0, 2);
    const Scalar p = invDm(1, 0);
    const Scalar q = invDm(1, 1);
    const Scalar r = invDm(1, 2);
    const Scalar s = invDm(2, 0);
    const Scalar t = invDm(2, 1);
    const Scalar u = invDm(2, 2);

    const Scalar t1 = -m - p - s;
    const Scalar t2 = -n - q - t;
    const Scalar t3 = -o - r - u;

    auto &PFPx{m_dFdx[elementId]};
    PFPx.setZero();
    PFPx(0, 0) = t1;
    PFPx(0, 3) = m;
    PFPx(0, 6) = p;
    PFPx(0, 9) = s;
    PFPx(1, 1) = t1;
    PFPx(1, 4) = m;
    PFPx(1, 7) = p;
    PFPx(1, 10) = s;
    PFPx(2, 2) = t1;
    PFPx(2, 5) = m;
    PFPx(2, 8) = p;
    PFPx(2, 11) = s;
    PFPx(3, 0) = t2;
    PFPx(3, 3) = n;
    PFPx(3, 6) = q;
    PFPx(3, 9) = t;
    PFPx(4, 1) = t2;
    PFPx(4, 4) = n;
    PFPx(4, 7) = q;
    PFPx(4, 10) = t;
    PFPx(5, 2) = t2;
    PFPx(5, 5) = n;
    PFPx(5, 8) = q;
    PFPx(5, 11) = t;
    PFPx(6, 0) = t3;
    PFPx(6, 3) = o;
    PFPx(6, 6) = r;
    PFPx(6, 9) = u;
    PFPx(7, 1) = t3;
    PFPx(7, 4) = o;
    PFPx(7, 7) = r;
    PFPx(7, 10) = u;
    PFPx(8, 2) = t3;
    PFPx(8, 5) = o;
    PFPx(8, 8) = r;
    PFPx(8, 11) = u;
}

Scalar StableNeoHookean::computeEnergyAndGradient(MechanicalState<Particle3DTag> &mstate) const
{
    ZoneScopedN("StableNeoHookean.computeEnergyAndGradient");
    auto energy = Scalar{0};
    for (auto i = 0UL; i < static_cast<std::size_t>(size()); ++i) {
        // Compute deformation gradient

        const auto &indices{m_indices[i]};

        auto ds{Eigen::Matrix<Scalar, 3, 3>{}};
        ds.col(0) = mstate.m_x[static_cast<std::size_t>(indices[1])] - mstate.m_x[static_cast<std::size_t>(indices[0])];
        ds.col(1) = mstate.m_x[static_cast<std::size_t>(indices[2])] - mstate.m_x[static_cast<std::size_t>(indices[0])];
        ds.col(2) = mstate.m_x[static_cast<std::size_t>(indices[3])] - mstate.m_x[static_cast<std::size_t>(indices[0])];

        const auto &F{(ds * m_invDm[i]).eval()};

        const auto &mu = m_mu[i];
        const auto &lambda = m_lambda[i];

        const auto I2{(F.transpose() * F).trace()};
        const auto I3{F.determinant()};

        auto dI2dF = (2 * F).eval();
        auto dI3dF = Eigen::Matrix<Scalar, 3, 3>{};
        dI3dF.col(0) = skew(F.col(1)) * F.col(2);
        dI3dF.col(1) = skew(F.col(2)) * F.col(0);
        dI3dF.col(2) = skew(F.col(0)) * F.col(1);

        energy +=
            m_volume[i] * (mu / Scalar{2.0} * (I2 - 3) - mu * (I3 - 1) + lambda / Scalar{2.0} * (I3 - 1) * (I3 - 1));

        const auto dEdF = (m_volume[i] * (mu / Scalar{2.0} * dI2dF - mu * dI3dF + lambda * (I3 - 1) * dI3dF)).eval();
        const auto grad = (m_dFdx[i].transpose() * dEdF.reshaped()).eval();

        mstate.m_grad[static_cast<std::size_t>(indices[0])] += grad.segment<3>(0);
        mstate.m_grad[static_cast<std::size_t>(indices[1])] += grad.segment<3>(3);
        mstate.m_grad[static_cast<std::size_t>(indices[2])] += grad.segment<3>(6);
        mstate.m_grad[static_cast<std::size_t>(indices[3])] += grad.segment<3>(9);
    }

    return energy;
}

Scalar StableNeoHookean::computeEnergyGradientAndHessian(MechanicalState<Particle3DTag> &mstate) const
{
    ZoneScopedN("StableNeoHookean.computeEnergyGradientAndHessian");

    tbb::enumerable_thread_specific<std::vector<Triplet>> tripletsTLS;
    tbb::enumerable_thread_specific<Scalar> energyTLS;

    for (const auto &parallelGroup : m_parallelGroups) {
        ZoneScopedN("StableNeoHookean.computeEnergyGradientAndHessian.group");
        tbb::parallel_for(
            tbb::blocked_range<std::size_t>(0, parallelGroup.size()), [&](const tbb::blocked_range<std::size_t> &r) {
                bool exists{};
                auto &triplets = tripletsTLS.local(exists);
                if (!exists) {
                    triplets.reserve(9 * static_cast<std::size_t>(size()));
                }

                auto &energy = energyTLS.local(exists);
                if (!exists) {
                    energy = 0;
                }
                ZoneScopedN("StableNeoHookean.computeEnergyGradientAndHessian.range");
                for (auto rId = r.begin(); rId != r.end(); ++rId) {
                    const auto elementId = parallelGroup[rId];
                    const auto &indices{m_indices[elementId]};

                    auto ds{Eigen::Matrix<Scalar, 3, 3>{}};
                    ds.col(0) = mstate.m_x[static_cast<std::size_t>(indices[1])] -
                                mstate.m_x[static_cast<std::size_t>(indices[0])];
                    ds.col(1) = mstate.m_x[static_cast<std::size_t>(indices[2])] -
                                mstate.m_x[static_cast<std::size_t>(indices[0])];
                    ds.col(2) = mstate.m_x[static_cast<std::size_t>(indices[3])] -
                                mstate.m_x[static_cast<std::size_t>(indices[0])];

                    const auto &F{(ds * m_invDm[elementId]).eval()};

                    const auto &mu = m_mu[elementId];
                    const auto &lambda = m_lambda[elementId];

                    const auto I2{(F.transpose() * F).trace()};
                    const auto I3{F.determinant()};

                    const auto dI2dF = (2 * F).eval();
                    auto dI3dF = Eigen::Matrix<Scalar, 3, 3>{};
                    dI3dF.col(0) = skew(F.col(1)) * F.col(2);
                    dI3dF.col(1) = skew(F.col(2)) * F.col(0);
                    dI3dF.col(2) = skew(F.col(0)) * F.col(1);

                    auto d2I2dF2{2 * Eigen::Matrix<Scalar, 9, 9>::Identity()};
                    auto d2I3dF2 = Eigen::Matrix<Scalar, 9, 9>::Zero().eval();

                    d2I3dF2.block<3, 3>(0, 3) = -skew(F.col(2));
                    d2I3dF2.block<3, 3>(0, 6) = skew(F.col(1));

                    d2I3dF2.block<3, 3>(3, 0) = skew(F.col(2));
                    d2I3dF2.block<3, 3>(3, 6) = -skew(F.col(0));

                    d2I3dF2.block<3, 3>(6, 0) = -skew(F.col(1));
                    d2I3dF2.block<3, 3>(6, 3) = skew(F.col(0));

                    energy += m_volume[elementId] * (mu / Scalar{2.0} * (I2 - 3)  //
                                                     - mu * (I3 - 1)              //
                                                     + lambda / Scalar{2.0} * (I3 - 1) * (I3 - 1));

                    const auto dEdF = (m_volume[elementId] * ((mu / Scalar{2.0} * dI2dF  //
                                                               - mu * dI3dF              //
                                                               + lambda * (I3 - 1) * dI3dF)))
                                          .eval();
                    const auto grad = (m_dFdx[elementId].transpose() * dEdF.reshaped()).eval();

                    mstate.m_grad[static_cast<std::size_t>(indices[0])] += grad.segment<3>(0);
                    mstate.m_grad[static_cast<std::size_t>(indices[1])] += grad.segment<3>(3);
                    mstate.m_grad[static_cast<std::size_t>(indices[2])] += grad.segment<3>(6);
                    mstate.m_grad[static_cast<std::size_t>(indices[3])] += grad.segment<3>(9);

                    const auto d2EdF2{
                        (m_volume[elementId] *
                         (mu / Scalar{2.0} * d2I2dF2  //
                          - mu * d2I3dF2              //
                          + lambda * (dI3dF.reshaped() * dI3dF.reshaped().transpose() + (I3 - 1) * d2I3dF2)))
                            .eval()};
                    auto hessian = (m_dFdx[elementId].transpose() * d2EdF2 * m_dFdx[elementId]).eval();

                    if (m_projectSPD) {
                        mandos::core::projectSPD(hessian, 1e-8, [](const auto v) { return -v; });
                    }

                    // TODO Dont use triplets. Accumulate directly on a warm up hessian matrix
                    for (int i = 0; i < 4; ++i) {
                        for (int j = 0; j < 4; ++j) {
                            // Get the block corresopnding to the relation between index i and index j
                            const auto block{hessian.block<3, 3>(3 * i, 3 * j)};

                            // Assemble the 9 elements of this block
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 0,
                                                  3 * indices[static_cast<std::size_t>(j)] + 0,
                                                  block(0, 0));
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 1,
                                                  3 * indices[static_cast<std::size_t>(j)] + 0,
                                                  block(1, 0));
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 2,
                                                  3 * indices[static_cast<std::size_t>(j)] + 0,
                                                  block(2, 0));

                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 0,
                                                  3 * indices[static_cast<std::size_t>(j)] + 1,
                                                  block(0, 1));
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 1,
                                                  3 * indices[static_cast<std::size_t>(j)] + 1,
                                                  block(1, 1));
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 2,
                                                  3 * indices[static_cast<std::size_t>(j)] + 1,
                                                  block(2, 1));

                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 0,
                                                  3 * indices[static_cast<std::size_t>(j)] + 2,
                                                  block(0, 2));
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 1,
                                                  3 * indices[static_cast<std::size_t>(j)] + 2,
                                                  block(1, 2));
                            triplets.emplace_back(3 * indices[static_cast<std::size_t>(i)] + 2,
                                                  3 * indices[static_cast<std::size_t>(j)] + 2,
                                                  block(2, 2));
                        }
                    }
                }
            });
    }

    {
        ZoneScopedN("StableNeoHookean.globalAssembly");
        auto triplets = tbb::flatten2d(tripletsTLS);

        SparseMat energyHessian;
        energyHessian.resize(mstate.size(), mstate.size());
        energyHessian.setFromTriplets(triplets.begin(), triplets.end());
        mstate.m_hessian += energyHessian;
    }

    return energyTLS.combine(std::plus{});
}

void StableNeoHookean::initialize(const MechanicalState<Particle3DTag> &mstate)
{
    // Each stencil in the SNH energy is a node in the graph
    // Each node is connected to another node is they share a vertex
    // using Graph = boost::adjacency_list<listS, vecS, undirectedS, std::size_t>;

    // We create a sparse matrix NxM where N is the number of stencils and M the number of vertex
    // It has a 1 if the stencil contains a vertex and 0 otherwise
    if (m_indices.empty()) {
        return;
    }

    std::vector<Eigen::Triplet<int>> triplets;

    for (int i = 0; i < size(); ++i) {
        auto [i0, i1, i2, i3] = m_indices[static_cast<std::size_t>(i)];
        triplets.emplace_back(i, i0, 1);
        triplets.emplace_back(i, i1, 1);
        triplets.emplace_back(i, i2, 1);
        triplets.emplace_back(i, i3, 1);
    }

    Eigen::SparseMatrix<int> svMatrix;
    svMatrix.resize(size(), mstate.size());
    svMatrix.setFromTriplets(triplets.begin(), triplets.end());

    // We multiply the matrix by its transpose to obtain the relation between stencils
    // If a stencil is connected to another one, the matrix contains a value different than 0
    const Eigen::SparseMatrix<int> ssMatrix = svMatrix * svMatrix.transpose();

    // auto _ = ssMatrix.eval();

    // Get the edges
    std::vector<std::pair<int, int>> edges;
    edges.reserve(static_cast<std::size_t>(ssMatrix.nonZeros() / 2));

    for (int row = 0; row < ssMatrix.outerSize(); ++row) {
        for (Eigen::SparseMatrix<int>::InnerIterator it(ssMatrix, row); it; ++it) {
            assert(row == it.col());
            edges.emplace_back(it.row(), it.col());
        }
    }

    using Graph = boost::compressed_sparse_row_graph<boost::directedS, std::size_t>;
    Graph g(boost::edges_are_unsorted_multi_pass, edges.begin(), edges.end(), static_cast<std::size_t>(size()));

    const auto nColors = sequential_vertex_coloring(g, boost::get(boost::vertex_bundle, g));

    m_parallelGroups.clear();
    m_parallelGroups.resize(nColors);

    for (auto vId = 0UL; vId < boost::num_vertices(g); vId++) {
        auto color = g[vId];
        m_parallelGroups[color].emplace_back(vId);
    }
}

void initialize(StableNeoHookean &snh, const MechanicalState<Particle3DTag> &mstate)
{
    snh.initialize(mstate);
}
bool &StableNeoHookean::projectSPD()
{
    return m_projectSPD;
}
bool StableNeoHookean::projectSPD() const
{
    return m_projectSPD;
}
void StableNeoHookean::setParameterSet(int elementId, const ParameterSet &parameterSet)
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Can't set ParameterSet for element ({}). Energy container {}  elements", elementId, size()));
    }

    configureElement(static_cast<std::size_t>(elementId), parameterSet);
}
StableNeoHookean::ParameterSet StableNeoHookean::getParameterSet(int elementId) const
{
    if (elementId > size()) {
        throw std::runtime_error(
            fmt::format("Requested ParameterSet ({}) exceeds number of elements in energy ({})", elementId, size()));
    }

    return {m_invDm[static_cast<std::size_t>(elementId)].inverse().eval(),
            m_lambda[static_cast<std::size_t>(elementId)],  //
            m_mu[static_cast<std::size_t>(elementId)]};
}

StableNeoHookean::ParameterSet::ParameterSet(const std::array<Vec3, 4> &x0, Scalar lambda_, Scalar mu_)
    : lambda(lambda_)
    , mu(mu_)
{
    restPoseMatrix.col(0) = x0[1] - x0[0];
    restPoseMatrix.col(1) = x0[2] - x0[0];
    restPoseMatrix.col(2) = x0[3] - x0[0];
}

StableNeoHookean::ParameterSet::ParameterSet(const Mat3 &restPoseMatrix_, Scalar lambda_, Scalar mu_)
    : restPoseMatrix(restPoseMatrix_)
    , lambda(lambda_)
    , mu(mu_)
{
}

StableNeoHookean::ParameterSet::ParameterSet(const Mat43 &x0, Scalar lambda_, Scalar mu_)
    : restPoseMatrix(x0({1, 2, 3}, Eigen::all) - x0({0, 0, 0}, Eigen::all))
    , lambda(lambda_)
    , mu(mu_)
{
}
}  // namespace mandos::core
