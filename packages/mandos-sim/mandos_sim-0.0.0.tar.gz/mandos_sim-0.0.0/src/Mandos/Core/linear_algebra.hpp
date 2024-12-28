#ifndef MANDOS_LINEAR_ALGEBRA_H_
#define MANDOS_LINEAR_ALGEBRA_H_

#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <Mandos/Core/core_export.h>

#include <TinyAD/Utils/HessianProjection.hh>

namespace mandos::core
{

using Scalar = double;

// STATIC VECTORS AND MATRICES
using Vec2 = Eigen::Vector2<Scalar>;
using Vec3 = Eigen::Vector3<Scalar>;
using Mat23 = Eigen::Matrix<Scalar, 2, 3>;
using Mat26 = Eigen::Matrix<Scalar, 2, 6>;
using Mat3 = Eigen::Matrix3<Scalar>;
using Vec4 = Eigen::Vector4<Scalar>;
using Mat43 = Eigen::Matrix<Scalar, 4, 3>;
using Mat4 = Eigen::Matrix4<Scalar>;
using Mat6 = Eigen::Matrix<Scalar, 6, 6>;
using Mat9 = Eigen::Matrix<Scalar, 9, 9>;
using Vec6 = Eigen::Vector<Scalar, 6>;
using Vec9 = Eigen::Vector<Scalar, 9>;

// DYNAMIC VECTORS AND MATRICES
using Vec = Eigen::VectorX<Scalar>;
using Mat = Eigen::MatrixX<Scalar>;

// SPARSE MATRICES
using Triplet = Eigen::Triplet<Scalar>;
using SparseMat = Eigen::SparseMatrix<Scalar, Eigen::RowMajor>;

// Given a square DxD matrix mat, return a vector of D² components
// 1  3
// 2  4  ->  vec = 1, 2, 3, 4
template <int D>
Eigen::Vector<Scalar, D * D> vectorizeMatrix(const Eigen::Matrix<Scalar, D, D> &mat)
{
    // We vectorize by columns, so we can use reshaped
    return mat.reshaped();
}

template <int D>
Eigen::Vector<Scalar, D * D> vectorizeMatrixRowWise(const Eigen::Matrix<Scalar, D, D> &mat)
{
    Eigen::Vector<Scalar, D * D> result = Eigen::Vector<Scalar, D * D>::Zero();
    for (unsigned int i = 0; i < D; i++) {
        for (unsigned int j = 0; j < D; j++) {
            result(D * j + i) = mat(j, i);
        }
    }
    return result;
}

// Given a NxM matrix, return a 3Nx3M matrix where each matrix component m_i_j becomes now m_i_j*I
// where I is the 3x3 identity matrix
// A  B            A* I, B*I
// C  D  ->  mat = C* I, D*I
template <int N>
Eigen::Matrix<Scalar, 3 * N, 3 * N> blockMatrix(const Eigen::Matrix<Scalar, N, N> &mat)
{
    Eigen::Matrix<Scalar, 3 * N, 3 * N> result = Eigen::Matrix<Scalar, 3 * N, 3 * N>::Zero();
    for (unsigned int i = 0; i < N; i++) {
        for (unsigned int j = 0; j < N; j++) {
            // Wierd syntax we have to use because of templates
            // It just means result.block...
            result.template block<3, 3>(i * 3, j * 3) = mat(i, j) * Mat3::Identity();
        }
    }
    return result;
}

template <int N>
Eigen::Matrix<Scalar, 3 * N, 3 * N> blockDiagonalMatrix(const Eigen::Matrix<Scalar, N, N> &mat)
{
    Eigen::Matrix<Scalar, 3 * N, 3 * N> result = Eigen::Matrix<Scalar, 3 * N, 3 * N>::Zero();
    for (unsigned int i = 0; i < N; i++) {
        result.template block<N, N>(i * N, i * N) = mat * Mat3::Identity();
    }
    return result;
}

/**
 * https://en.wikipedia.org/wiki/Levi-Civita_symbol#Three_dimensions
 */
MANDOS_CORE_EXPORT Eigen::Matrix<Scalar, 3, 9> vectorizedLeviCivita();

template <int N>
Eigen::Vector<Scalar, N> transposeVectorizedVector(const Eigen::Vector<Scalar, N> &in)
{
    const auto n = static_cast<int>(sqrt(static_cast<double>(N)));
    Eigen::Vector<Scalar, N> v;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int index = n * i + j;
            int index_t = n * j + i;
            v(index) = in(index_t);
        }
    }
    return v;
}

template <int N, int M>
Eigen::Matrix<Scalar, N, M> transposeVectorizedMatrixRows(const Eigen::Matrix<Scalar, N, M> &in)
{
    Eigen::Matrix<Scalar, N, M> mat;
    const auto n = static_cast<int>(sqrt(static_cast<double>(N)));
    for (int i = 0; i < n; i++) {
        mat.col(i) = transposeVectorizedVector<N>(in.col(i));
    }
    return mat;
}

template <int N, int M>
Eigen::Matrix<Scalar, N, M> transposeVectorizedMatrixColumns(const Eigen::Matrix<Scalar, N, M> &in)
{
    Eigen::Matrix<Scalar, N, M> mat;
    const auto m = static_cast<int>(sqrt(M));
    for (int i = 0; i < m; i++) {
        mat.row(i) = transposeVectorizedVector<M>(in.row(i));
    }
    return mat;
}

// Code copied from TinyAD with our own tweak to allow clamp or reflection
template <int N, typename F>
void projectSPD(Eigen::Matrix<Scalar, N, N> &hessian, Scalar eps, F &&f)
{
    // Early out if sufficient condition is fulfilled
    if (TinyAD::positive_diagonally_dominant(hessian, eps)) {
        return;
    }

    // Compute eigen-decomposition (of symmetric matrix)
    Eigen::SelfAdjointEigenSolver<Eigen::Matrix<Scalar, N, N>> eig(hessian);
    Eigen::Matrix<Scalar, N, N> D = eig.eigenvalues().asDiagonal();

    // Clamp all eigenvalues to eps
    bool all_positive = true;
    for (Eigen::Index i = 0; i < hessian.rows(); ++i) {
        auto v = D(i, i);
        if (v < eps) {
            D(i, i) = f(v);
            all_positive = false;
        }
    }

    // Do nothing if all eigenvalues were already at least eps
    if (all_positive) {
        return;
    }

    // Re-assemble matrix using clamped eigenvalues
    hessian = eig.eigenvectors() * D * eig.eigenvectors().transpose();
}

}  // namespace mandos::core

#endif  // MANDOS_LINEAR_ALGEBRA_H_
