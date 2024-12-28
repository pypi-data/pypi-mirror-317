#!/usr/bin/env python3

import numpy as np
import polyscope as ps

import pymandos
from parallel_transport import compute_rotations_parallel_transport

total_length = 1.0  # meters
total_mass = 0.3  # Kg


def create_rod(model, n_points):
    delta_x = total_length / n_points
    rigid_body_cloud = model.add_rigidbody_cloud()

    # Set initial conditions
    positions = np.zeros((n_points, 6))
    velocities = np.zeros((n_points, 6))
    for i, position in enumerate(positions):
        position[0] += delta_x * i

    lin_pos = np.array([pos[:3] for pos in positions])
    rotvecs = compute_rotations_parallel_transport(lin_pos)
    for rotvec, pos in zip(rotvecs, positions):
        pos[3:] = rotvec
    rigid_body_cloud.size = n_points
    rigid_body_cloud.x = positions
    rigid_body_cloud.v = velocities

    # Set up rigid body mass and inertia
    node_mass = total_mass / n_points
    rigid_body_cloud.mass = node_mass * np.ones(n_points)
    rigid_body_cloud.inertiaTensor = [
        node_mass * np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)
    ]

    # A Rod is made of three diferent energies
    # - MassSpring energy, which tries to keep distance between frames at a particular rest length 
    # - CosseratBendingRod energy, which tries to keep frames aligned along the Z direction
    # - CosseratRodAlignment energy, 
    mass_spring = rigid_body_cloud.mass_spring
    cosserat_rod = rigid_body_cloud.cosserat_rod_alignment
    for i in range(n_points-1):
        mass_spring.add_element([i, i+1], pymandos.energies.MassSpring.ParameterSet(x0 = rigid_body_cloud.x[[i, i+1], 0:3], stiffness=100.0))
        cosserat_rod.add_element([i, i+1], pymandos.energies.CosseratRodAlignment.ParameterSet(x0 = rigid_body_cloud.x[[i, i+1], :], cosserat_stiffness=100.0))

    bending_rod = rigid_body_cloud.cosserat_bending_rod
    for i in range(n_points-2):
        bending_rod.add_element([i, i+1], pymandos.energies.CosseratBendingRod.ParameterSet(x0 = rigid_body_cloud.x[[i, i+1], :], stiffness_tensor=1.0*np.ones(3)))

    # Freeze one side
    rigid_body_cloud.fix_translation(0)
    rigid_body_cloud.fix_rotation(0)

    model.compute_dag()

    # Render
    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    indices = np.array([(i, i + 1) for i in range(n_points - 1)])
    ps.register_curve_network(
        f"rod_{n_points}", positions, indices, radius=total_length / 50
    )

    # mesh = meshio.read("axis.obj")
    # for i in range(n_points):
    #     psmesh = ps.register_surface_mesh("rod_element_"+str(i), mesh.points, mesh.get_cells_type("triangle"))
    #     psmesh.add_color_quantity("xyz", mesh.points, enabled=True)

    return rigid_body_cloud


def simulate_callback(model, rods):
    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations = 100
    stepParameters.cg_iterations = 20
    stepParameters.cg_error = 1e-8
    stepParameters.grad_norm = 1e-2
    stepParameters.line_search_iterations = 10

    result = pymandos.step(model, stepParameters)
    print(result)

    for rigid_body_cloud in rods:
        n_points = int(np.shape(rigid_body_cloud.x)[0])
        positions = np.array([x[:3] for x in rigid_body_cloud.x])
        ps.get_curve_network(f"rod_{n_points}").update_node_positions(positions)


if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at((0.5 * total_length, 2.0, 0.5), (0.5 * total_length, 0.0, 0.0))
    ps.set_ground_plane_mode("none")  # Disable ground rendering
    model = pymandos.Model()
    rod = create_rod(model, 20)
    ps.set_user_callback(lambda: simulate_callback(model, [rod]))
    ps.show()
