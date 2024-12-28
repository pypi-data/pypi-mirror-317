#!/usr/bin/env python3

import sys
import numpy as np
import meshio
import polyscope as ps
import polyscope.imgui as psim

import pymandos
from parallel_transport import compute_rotations_parallel_transport

playing = False
total_length = 0.2
spring_radius = 0.02
delta_x = 0.001
number_rows = 25
n_points = 500
last_point = n_points - 1

def create_model():
    model = pymandos.Model()
    spring0 = model.add_rigidbody_cloud(name="spring0")

    # Set initial conditions
    positions = []
    current_length = 0
    while current_length < total_length:
        position.append(np.array([]))
        position[0] = spring_radius * np.cos(8 *2.0 * np.pi * i/n_points)
        position[1] = spring_radius * np.sin(8* 2.0 * np.pi * i/n_points)
        position[2] = delta_x * i

    n_points = 500

    lin_pos = np.array([pos[:3] for pos in positions])
    rotvecs = compute_rotations_parallel_transport(lin_pos)
    for rotvec, pos in zip(rotvecs, positions):
        pos[3:] = rotvec
    spring0.size = n_points
    positions += np.array([0,0.3,0.2, 0,0,0])
    spring0.x = positions
    spring0.v = velocities
    # rigid_body_cloud.disable_gravity()

    # Set up rigid body mass and inertia
    density = 7860
    total_mass = density * spring_radius
    node_mass = mass / n_points
    spring0.mass = node_mass * np.ones(n_points)
    spring0.inertiaTensor = [node_mass * np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)]


    # Rod energy
    mass_spring = spring0.mass_spring
    cosserat_rod = spring0.cosserat_rod
    for i in range(n_points-1):
        mass_spring.add_element([i, i+1], pymandos.energies.MassSpring.ParameterSet(x0 = spring0.x[[i, i+1], 0:3], stiffness=10000.0))
        cosserat_rod.add_element([i, i+1], pymandos.energies.CosseratRodAlignment.ParameterSet(x0 = spring0.x[[i, i+1], :], cosserat_stiffness=10000.0))

    bending_rod = spring0.bending_rod
    for i in range(n_points-2):
        bending_rod.add_element([i, i+1], pymandos.energies.CosseratBendingRod.ParameterSet(x0 = spring0.x[[i, i+1], :], stiffness_tensor=10000*np.ones(3)))

    # Freeze one side
    for i in range(n_points//10):
        spring0.fix_translation(i)
        spring0.fix_rotation(i)

    sphere_radius = 0.01
    mapping = model.add_rigidbody_point_mapping(spring0)
    for i in range(n_points):
        mapping.add_particle(np.array([0,0,0]), i)
    mapped_particles = mapping.deformable
    rod_collider = mapped_particles.add_sphere_cloud(sphere_radius)

    # cube = model.add_rigidbody(name="cube")
    # x = np.zeros(6)
    # x[2] = 0.6
    # x[0] = -spring_radius/4
    # x[1] = spring_radius
    # x[3] = np.pi/2
    # cube.x = x
    # cube.v = np.zeros(6)
    # cube.mass = 1
    # cube.inertiaTensor = 1*np.diag([1.0, 1.0, 1.0])


    # m = meshio.read("crossbar.obj")
    # cube_mesh = pymandos.SurfaceMesh()
    # cube_mesh.x = m.points
    # cube_mesh.indices = m.cells_dict["triangle"]
    # collider_sdf = cube.add_sdf(cube_mesh, 0.1, nb_voxels=64)

    # collision_particles = model.add_collision_pair(collider_sdf, rod_collider, stiffness=100)

    model.compute_dag()

    # Render
    positions = np.array([x[:3] for x in spring0.x])
    indices = np.array([(i, i+1) for i in range(n_points -1)])
    ps.register_curve_network("spring0", positions, indices, radius=0.001)

    # cube_ps = ps.register_surface_mesh("cube", cube_mesh.x, cube_mesh.indices)
    # cube_ps.set_transform(cube.get_transform())

    return model

def simulate_callback(model):

    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations = 100
    stepParameters.cg_iterations = 100
    stepParameters.cg_error = 1e-8
    stepParameters.grad_norm = 1e-4
    stepParameters.line_search_iterations = 0
    stepParameters.accept_failed_solution = True

    if psim.Button("Step"):
        print(pymandos.step(model, stepParameters))
    
    global playing
    if playing:
        print(pymandos.step(model, stepParameters))

        if psim.Button("Pause"):
            playing = False
    else:
        if psim.Button("Simulate"):
            playing = True

    spring0 = model.get_rigidbody_cloud("spring0")
    positions = np.array([x[:3] for x in spring0.x])
    ps.get_curve_network("spring0").update_node_positions(positions)

    # cube = model.get_rigidbody("cube")
    # ps.get_surface_mesh("cube").set_transform(cube.get_transform())


if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at((0.0, 2.0, 0.2), (0.0, 0.0, 0.0))
    ps.set_ground_plane_mode("none") # Disable ground rendering
    model = create_model()
    ps.set_user_callback(lambda : simulate_callback(model))
    ps.show()
