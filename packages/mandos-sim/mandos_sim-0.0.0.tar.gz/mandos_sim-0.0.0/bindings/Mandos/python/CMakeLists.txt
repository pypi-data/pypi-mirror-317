set(SOURCES
    Mandos.cpp
    Model.cpp
    Mesh.cpp
    Deformable3D.cpp
    RigidBody.cpp
    RigidBodyPointMapping.cpp
    Differentiable.cpp
    Energies/StableNeoHookean.cpp
    Energies/MassSpring.cpp
    Energies/CosseratBendingRod.cpp
    Energies/CosseratRodAlignment.cpp
    Energies/ConstantForce.cpp
)

set(HEADERS
    Model.hpp
    Mesh.hpp
    Deformable3D.hpp
    RigidBody.hpp
    RigidBodyPointMapping.hpp
    Energies/StableNeoHookean.hpp
    Energies/MassSpring.hpp
    Energies/CosseratBendingRod.hpp
    Energies/CosseratRodAlignment.hpp
    Energies/ConstantForce.hpp
)

pybind11_add_module(mandos_cpp ${SOURCES} ${HEADERS})
target_link_libraries(
  mandos_cpp
  PRIVATE Mandos::Core
          fmt::fmt
          project_options
          project_warnings
          pybind11::pybind11
          pybind11::embed
          pybind11::module
)

target_include_directories(
  mandos_cpp
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../..>
         $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/../..>
)

install(TARGETS mandos_cpp LIBRARY DESTINATION .)
set_target_properties(mandos_cpp PROPERTIES INSTALL_RPATH "$ORIGIN/lib")

