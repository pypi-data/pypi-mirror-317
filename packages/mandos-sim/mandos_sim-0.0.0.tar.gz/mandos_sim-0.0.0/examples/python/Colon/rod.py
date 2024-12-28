#!/usr/bin/env python3

import sys
import numpy as np
import meshio
import polyscope as ps

import pymandos
from parallel_transport import compute_rotations_parallel_transport

n_points = 10
delta_x = 0.5

def create_model():
    model = pymandos.Model()
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
    rigid_body_cloud.mass = np.ones(n_points)
    rigid_body_cloud.inertiaTensor = [np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)]

    # Rod energy
    Ks = 10000.0
    stiffness_tensor = 500.0 * np.ones(3)
    cosserat_stiffness = 2000.0
    cosserat_rod = rigid_body_cloud.cosserat_rod
    for i in range(n_points - 1):
        cosserat_rod.add_element((i, i+1), Ks, stiffness_tensor, cosserat_stiffness, 0.0, 0.0)

    # Freeze one side
    rigid_body_cloud.fixed_rigid_bodies = [0]

    model.compute_dag()

    # Render
    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    indices = np.array([(i, i+1) for i in range(n_points -1)])
    ps.register_curve_network("rod_curve", positions, indices, radius=0.1)

    # mesh = meshio.read("axis.obj")
    # for i in range(n_points):
    #     psmesh = ps.register_surface_mesh("rod_element_"+str(i), mesh.points, mesh.get_cells_type("triangle"))
    #     psmesh.add_color_quantity("xyz", mesh.points, enabled=True)

    return model, rigid_body_cloud

def simulate_callback(model, rigid_body_cloud):
    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations =5
    stepParameters.cg_iterations = 20
    stepParameters.cg_error = 1e-4
    stepParameters.grad_norm = 1e-3
    stepParameters.line_search_iterations = 5

    pymandos.step(model, stepParameters)

    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    ps.get_curve_network("rod_curve").update_node_positions(positions)
    # for i in range(n_points):
    #     transform = rigid_body_cloud.get_transform(i)
    #     ps.get_surface_mesh("rod_element_"+str(i)).set_transform(transform)


if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at((0.0, 10.0, 2.0), (0.0, 0.0, 0.0))
    ps.set_ground_plane_mode("none") # Disable ground rendering
    model, rigid_body_cloud = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, rigid_body_cloud))
    ps.show()
