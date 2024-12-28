#!/usr/bin/env python3

import sys
import numpy as np
import meshio
import polyscope as ps
import polyscope.imgui as psim

import pymandos
from parallel_transport import compute_rotations_parallel_transport

playing = False
total_length = 0.8
n_points = 50
delta_x = total_length / n_points
last_point = n_points - 1

def create_model():
    model = pymandos.Model()
    rigid_body_cloud = model.add_rigidbody_cloud()

    # Set initial conditions
    positions = np.zeros((n_points, 6))
    velocities = np.zeros((n_points, 6))
    for i, position in enumerate(positions):
        position[1] -= delta_x * i

    lin_pos = np.array([pos[:3] for pos in positions])
    rotvecs = compute_rotations_parallel_transport(lin_pos)
    for rotvec, pos in zip(rotvecs, positions):
        pos[3:] = rotvec
    rigid_body_cloud.size = n_points
    positions += np.array([0,0.3,0.2, 0,0,0])
    rigid_body_cloud.x = positions
    rigid_body_cloud.v = velocities
    # rigid_body_cloud.disable_gravity()

    # Set up rigid body mass and inertia
    mass = 1
    node_mass = mass / n_points
    rigid_body_cloud.mass = node_mass * np.ones(n_points)
    rigid_body_cloud.inertiaTensor = [node_mass * np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)]

    # Rod energy
    Ks = 10.0
    stiffness_tensor = 0.0 * np.ones(3)
    cosserat_stiffness = 1.0
    collider_stiffness = 100.0
    cosserat_rod = rigid_body_cloud.cosserat_rod
    for i in range(n_points - 1):
        cosserat_rod.add_element((i, i+1), Ks, stiffness_tensor, cosserat_stiffness, 0.0, 0.0)

    # Freeze one side
    rigid_body_cloud.fix_translation(last_point)
    rigid_body_cloud.fix_rotation(last_point)

    sphere_radius = 0.01
    mapping = model.add_rigidbody_point_mapping(rigid_body_cloud)
    for i in range(n_points):
        mapping.add_particle(0.45 * sphere_radius * np.array([1,0,0]), i)
        mapping.add_particle(0.45 * sphere_radius * np.array([-1,0,0]), i)
        mapping.add_particle(0.45 * sphere_radius * np.array([0,1,0]), i)
        mapping.add_particle(0.45 * sphere_radius * np.array([0,-1,0]), i)
        mapping.add_particle(0.45 * sphere_radius * np.array([0,0,1]), i)
        mapping.add_particle(0.45 * sphere_radius * np.array([0,0,-1]), i)
    mapped_particles = mapping.deformable
    rod_collider = mapped_particles.add_sphere_cloud(sphere_radius)

    tube = model.add_rigidbody()
    tube.x = np.zeros(6)
    tube.v = np.zeros(6)
    tube.disable_gravity()
    tube.mass = 1
    tube.inertiaTensor = 1*np.diag([1.0, 1.0, 1.0])
    tube.fix()
    m = meshio.read("tube.stl")
    tube_mesh = pymandos.SurfaceMesh()
    tube_mesh.x = m.points
    tube_mesh.indices = m.cells_dict["triangle"]
    collider_sdf = tube.add_sdf(tube_mesh, 0.1, nb_voxels=1024)

    collision_particles = model.add_collision_pair(collider_sdf, rod_collider, stiffness=collider_stiffness)

    model.compute_dag()

    # Render
    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    indices = np.array([(i, i+1) for i in range(n_points -1)])
    ps.register_curve_network("rod_curve", positions, indices, radius=0.001)
    ps.register_point_cloud("ColliderSC", mapped_particles.x, radius=sphere_radius)
    ps.register_surface_mesh("tube", tube_mesh.x , tube_mesh.indices, transparency=0.3)

    axis = meshio.read("axis.obj")
    for i in range(n_points):
        axis_ps = ps.register_surface_mesh(f"RB{i}", axis.points/20, axis.cells_dict["triangle"])
        axis_ps.set_transform(rigid_body_cloud.get_transform(i))
        axis_ps.add_color_quantity("xyz", axis.points, enabled=True)


    return model, rigid_body_cloud, mapped_particles

def simulate_callback(model, rigid_body_cloud, mapped_particles):

    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.001
    stepParameters.newton_iterations = 10
    stepParameters.cg_iterations = 10
    stepParameters.cg_error = 1e-8
    stepParameters.grad_norm = 5
    stepParameters.line_search_iterations = 5

    if psim.Button("Step"):
        x = rigid_body_cloud.x.copy()
        x[n_points-1,1] += 0.1*stepParameters.h
        rigid_body_cloud.x = x
        print(pymandos.step(model, stepParameters))
    
    global playing
    if playing:
        x = rigid_body_cloud.x.copy()
        x[n_points-1,1] += 0.1*stepParameters.h
        rigid_body_cloud.x = x
        print(pymandos.step(model, stepParameters))

        if psim.Button("Pause"):
            playing = False
    else:
        if psim.Button("Simulate"):
            playing = True


    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    ps.get_curve_network("rod_curve").update_node_positions(positions)
    # ps.get_curve_network("rod_curve").add_vector_quantity("forces", forces, length=1.0, enabled=True)
    model.compute_forces(0)
    forces = mapped_particles.f[:, 0:3]
    ps.get_point_cloud("ColliderSC").update_point_positions(mapped_particles.x)
    # ps.get_point_cloud("ColliderSC").add_vector_quantity("forces", forces, length=1.0, enabled=True)
    for i in range(n_points):
        axis_ps = ps.get_surface_mesh(f"RB{i}")
        axis_ps.set_transform(rigid_body_cloud.get_transform(i))

    if psim.Button("Compute forces"):
        model.compute_forces(0)
        forces = mapped_particles.f
        ps.get_point_cloud("ColliderSC").add_vector_quantity("forces", forces, length=1.0, enabled=True)



if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at((0.0, 2.0, 0.2), (0.0, 0.0, 0.0))
    ps.set_ground_plane_mode("none") # Disable ground rendering
    model, rigid_body_cloud, mapped_particles = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, rigid_body_cloud, mapped_particles))
    ps.show()
