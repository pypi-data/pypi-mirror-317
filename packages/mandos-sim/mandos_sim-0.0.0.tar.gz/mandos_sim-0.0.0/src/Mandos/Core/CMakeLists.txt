set(HEADERS
    utility_functions.hpp
    SimulationObject.hpp
    SimulationObjectHandle.hpp
    MechanicalState.hpp
    Energies.hpp
    KinematicGraph.hpp
    Model.hpp
    SystemMatrix.hpp
    Simulation.hpp
    KinematicGraph.hpp
    Colliders.hpp
    RotationUtilities.hpp
    MechanicalStates/Particle3D.hpp
    MechanicalStates/RigidBody.hpp
    MechanicalStates/RigidBodyGlobal.hpp
    MechanicalStates/RigidBodyCommon.hpp
    Energies/StableNeoHookean.hpp
    Energies/LumpedMassInertia.hpp
    Energies/GravityEnergy.hpp
    Energies/ConstantForce.hpp
    Energies/RigidBodyInertia.hpp
    Energies/MassSpring.hpp
    Energies/CosseratBendingRod.hpp
    Energies/CosseratRodAlignment.hpp
    Energies/CollisionSpring.hpp
    Projections/FixedProjection.hpp
    Mappings/IdentityMapping.hpp
    Mappings/BarycentricMapping.hpp
    Mappings/RigidBodyPointMapping.hpp
    Mappings/CollisionMapping.hpp
    Collisions/SDF.hpp
    Collisions/SimulationCollider.hpp
    Collisions/SphereCloud.hpp
    Collisions/ContactEvent.hpp
    Collisions/CollisionDetection.hpp
    # async_simulation_loop.hpp
    Differentiable.hpp
    DiffRigidBody.hpp
    # edge.hpp
    # fem_element.hpp
    # gravity.hpp
    # inertia_energies.hpp
    # integrators.hpp
    linear_algebra.hpp
    # mesh.hpp
    # particle.hpp
    # particle_rigid_body_coupling.hpp
    # physics_state.hpp
    # rigid_body.hpp
    # rod_segment.hpp
    # simulation.hpp
    # sinc.hpp
    # spring.hpp
    # mandos.hpp
)

set(SOURCES
    utility_functions.hpp
    Model.cpp
    Simulation.cpp
    SystemMatrix.cpp
    RotationUtilities.cpp
    MechanicalStates/Particle3D.cpp
    MechanicalStates/RigidBody.cpp
    MechanicalStates/RigidBodyGlobal.cpp
    MechanicalStates/RigidBodyCommon.cpp
    Energies/StableNeoHookean.cpp
    Energies/LumpedMassInertia.cpp
    Energies/GravityEnergy.cpp
    Energies/ConstantForce.cpp
    Energies/RigidBodyInertia.cpp
    Energies/MassSpring.cpp
    Energies/CosseratBendingRod.cpp
    Energies/CosseratRodAlignment.cpp
    Energies/CollisionSpring.cpp
    Projections/FixedProjection.cpp
    Mappings/IdentityMapping.cpp
    Mappings/BarycentricMapping.cpp
    Mappings/RigidBodyPointMapping.cpp
    Mappings/CollisionMapping.cpp
    Collisions/SDF.cpp
    Collisions/SphereCloud.cpp
    Collisions/CollisionDetection.cpp
    # async_simulation_loop.cpp
    # compute_tetrahedrons.cpp
    Differentiable.cpp
    DiffRigidBody.cpp
    # edge.cpp
    # fem_element.cpp
    # inertia_energies.cpp
    # integrators.cpp
    linear_algebra.cpp
    # mandos.cpp
    # particle_rigidbody_coupling.cpp
    # rigid_body.cpp
    # rod_segment.cpp
    # simulation.cpp
    # sinc.cpp
    # spring.cpp
)

add_library(Core ${HEADERS} ${SOURCES})

# Add the src directory as the include directory. Includes should be added as <Mandos/Core/Foo.hpp>
target_include_directories(
  Core
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../..>
         $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/../..>
)

if(MSVC)
  target_compile_definitions(Core PUBLIC _USE_MATH_DEFINES)
  target_compile_options(Core PRIVATE /bigobj)
endif()

target_link_libraries(
  Core
  PUBLIC OpenVDB::openvdb
         Eigen3::Eigen
         project_options
         project_warnings
         TinyAD
  PRIVATE Mandos::Tracing
          spdlog::spdlog
          onetbb::onetbb
)

add_library(Mandos::Core ALIAS Core)
generate_export_header(Core PREFIX_NAME MANDOS_)

install(TARGETS Core LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})