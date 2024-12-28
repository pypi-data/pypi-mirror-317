#include <Mandos/Core/SystemMatrix.hpp>

namespace mandos::core
{

SystemMatrix::SystemMatrix(int rows, int cols)
    : m_rows(rows)
    , m_cols(cols)
{
}

int SystemMatrix::rows() const
{
    return m_rows;
}

int SystemMatrix::cols() const
{
    return m_cols;
}

void SystemMatrix::clear()
{
}

void SystemMatrix::setForwardSortedList(const std::vector<Model::KinematicGraph::vertex_descriptor> &forwardSortedList)
{
    m_forwardSortedList = std::addressof(forwardSortedList);
}

const std::vector<Model::KinematicGraph::vertex_descriptor> &SystemMatrix::forwardSortedList() const
{
    return *m_forwardSortedList;
}

void SystemMatrix::setBackwardSortedList(
    const std::vector<Model::KinematicGraph::vertex_descriptor> &backwardSortedList)
{
    m_backwardSortedList = std::addressof(backwardSortedList);
}

const std::vector<Model::KinematicGraph::vertex_descriptor> &SystemMatrix::backwardSortedList() const
{
    return *m_backwardSortedList;
}

void SystemMatrix::setFreeSimulationObject(
    const std::vector<Model::KinematicGraph::vertex_descriptor> &freeSimulationObjects)
{
    m_freeSimulationObjects = std::addressof(freeSimulationObjects);
}

const std::vector<Model::KinematicGraph::vertex_descriptor> &SystemMatrix::freeSimulationObjects() const
{
    return *m_freeSimulationObjects;
}

const Model::KinematicGraph &SystemMatrix::graph() const
{
    return m_model->graph();
}

Model &SystemMatrix::model() const
{
    return *m_model;
}

void SystemMatrix::setModel(Model &model)
{
    m_model = std::addressof(model);
}

}  // namespace mandos::core