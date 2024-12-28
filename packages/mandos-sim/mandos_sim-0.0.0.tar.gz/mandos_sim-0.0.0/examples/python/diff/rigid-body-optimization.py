#!/usr/bin/env python3

import numpy as np
from scipy.optimize import minimize
import polyscope as ps
import meshio

import pymandos
import rotation_utilities

stepParameters = pymandos.StepParameters()
stepParameters.h = 0.1
stepParameters.newton_iterations = 10
stepParameters.cg_error = 1e-8
stepParameters.grad_norm = 1e-6
stepParameters.line_search_iterations = 10

target_pos = 3.0 * (2.0 * np.random.rand(3) - 1.0)
R_target = rotation_utilities.rotation_exp_map(2.0 * np.random.rand(3) - 1.0)


def compute_J_inertia_tensor(I):
    Ix = I[0, 0]
    Iy = I[1, 1]
    Iz = I[2, 2]
    return 0.5 * np.diag((-Ix + Iy + Iz, Ix - Iy + Iz, Ix + Iy - Iz))


def create_model(initial_vel: list):
    model = pymandos.Model()
    rb = model.add_rigidbody()
    rb.x = np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    rb.v = np.array(initial_vel)

    # Inertia
    rb.mass = 2.0
    rb.inertiaTensor = compute_J_inertia_tensor(np.diag([0.5, 1.0, 2.0]))
    rb.disable_gravity()

    model.compute_dag()

    return model, rb


def simulate(initial_vel: list, diff_frames: int):
    model, rb = create_model(initial_vel)
    trajectory = pymandos.Trajectory()
    trajectory.append_state(model)
    for _ in range(diff_frames):
        pymandos.step(model, stepParameters)
        trajectory.append_state(model)
    return trajectory, model


def compute_loss(trajectory: pymandos.Trajectory) -> pymandos.LossFunctionAndGradients:
    loss = pymandos.LossFunctionAndGradients()

    lin_pos = trajectory.positions[-1][:3]
    delta = lin_pos - target_pos
    loss_position = np.dot(delta, delta)
    loss_position_gradient = 2.0 * delta

    axis_angle = trajectory.positions[-1][3:]
    R = rotation_utilities.rotation_exp_map(axis_angle)
    R_diff = R.T @ R_target
    loss_rotation = 0.5 * np.trace(np.identity(3) - R_diff)

    loss_rotation_gradient = -0.5 * rotation_utilities.unskew(R_diff - R_diff.T).T @ R.T

    dof = trajectory.get_n_dof()
    loss.loss = loss_position + loss_rotation
    loss_position_partial_derivative = [np.zeros(dof) for _ in trajectory.positions]
    loss_position_partial_derivative[-1][:3] = loss_position_gradient
    loss_position_partial_derivative[-1][3:] = loss_rotation_gradient
    loss.loss_position_partial_derivative = loss_position_partial_derivative
    loss.loss_velocity_partial_derivative = [
        np.zeros(dof) for _ in trajectory.positions
    ]
    loss.loss_parameter_partial_derivative = np.zeros(dof)
    return loss


def sim_wrapper(v0):
    trajectory, model = simulate(v0, 100)
    loss = compute_loss(trajectory)
    dof = trajectory.get_n_dof()
    dx0_dp = np.zeros((dof, dof))
    dv0_dp = np.identity(dof)
    gradient = pymandos.compute_loss_function_gradient_backpropagation(
        stepParameters.h, model, trajectory, loss, dx0_dp, dv0_dp, 0
    )
    return loss.loss, gradient


if __name__ == "__main__":
    v0 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    res = minimize(
        sim_wrapper,
        v0,
        jac=True,
        method="L-BFGS-B",
        options={"disp": True, "maxiter": 100},
    )

    trajectory, model = simulate(res.x, 100)
    R = rotation_utilities.rotation_exp_map(trajectory.positions[-1][3:].copy())
    print(f"R target =\n{R_target}, ")
    print(f"R optimized =\n{R}")
    print(f"Initial velocity vector: {res.x}")

    ps.init()
    ps.set_ground_plane_mode("none")  # Disable ground rendering
    ps.set_up_dir("z_up")
    ps.look_at((0.0, 20.0, 4.0), (0.0, 0.0, 0.0))
    mesh = meshio.read("../RigidBody/tennis.obj")
    ps.register_surface_mesh("rb_mesh", mesh.points, mesh.cells_dict.get("triangle"))
    ps.register_surface_mesh(
        "rb_mesh_target", mesh.points, mesh.cells_dict.get("triangle")
    )
    transform = np.eye(4)
    transform[:3, :3] = R_target
    transform[:3, 3] = target_pos
    print(transform)
    ps.get_surface_mesh("rb_mesh_target").set_transform(transform)

    model, rb = create_model(res.x)

    def simulate_callback(model, rigid_body):
        pymandos.step(model, stepParameters)
        ps.get_surface_mesh("rb_mesh").set_transform(rigid_body.get_transform())

    ps.set_user_callback(lambda: simulate_callback(model, rb))
    ps.show()
