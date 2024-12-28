#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from tqdm import tqdm

import pymandos
import rotation_utilities

stepParameters = pymandos.StepParameters()
stepParameters.h = 0.1
stepParameters.newton_iterations = 10
stepParameters.cg_error = 1e-8
stepParameters.grad_norm = 1e-6
stepParameters.line_search_iterations = 0


def compute_J_inertia_tensor(I):
    Ix = I[0, 0]
    Iy = I[1, 1]
    Iz = I[2, 2]
    return 0.5 * np.diag((-Ix + Iy + Iz, Ix - Iy + Iz, Ix + Iy - Iz))


def create_model(initial_pos: list, initial_vel: list):
    model = pymandos.Model()
    rb = model.add_rigidbody()
    rb.x = np.array(initial_pos)
    rb.v = np.array(initial_vel)

    # Disable gravity
    rb.disable_gravity()

    # Inertia
    rb.mass = 2.0
    rb.inertiaTensor = compute_J_inertia_tensor(np.diag([0.5, 1.0, 2.0]))

    model.commit()

    return model, rb


def simulate_callback(model, rigid_body):
    pymandos.step(model, stepParameters)


def simulate(initial_pos: list, initial_vel: list, diff_frames: int):
    model, rb = create_model(initial_pos, initial_vel)
    trajectory = pymandos.Trajectory()
    trajectory.append_state(model)
    for _ in range(diff_frames):
        pymandos.step(model, stepParameters)
        trajectory.append_state(model)
    return trajectory, model


def compute_loss(trajectory: pymandos.Trajectory) -> pymandos.LossFunctionAndGradients:
    loss = pymandos.LossFunctionAndGradients()

    lin_pos = trajectory.positions[-1][:3]
    target_pos = np.array([1.0, 1.0, 1.0])
    delta = lin_pos - target_pos
    loss_position = np.dot(delta, delta)
    loss_position_gradient = 2.0 * delta

    axis_angle = trajectory.positions[-1][3:]
    R = rotation_utilities.rotation_exp_map(axis_angle)
    R_target = rotation_utilities.rotation_exp_map(np.array([1.0, 0.0, 1.0]))
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
    loss.loss_parameter_partial_derivative = np.zeros(2 * dof)
    return loss


def sim_wrapper(x0: list, v0: list):
    trajectory, model = simulate(x0, v0, 100)
    loss = compute_loss(trajectory)
    dof = trajectory.get_n_dof()
    dx0_dp = np.block(
        [
            [np.eye(dof), np.zeros((dof, dof))],
        ]
    )
    dv0_dp = np.block(
        [
            [np.zeros((dof, dof)), np.eye(dof)],
        ]
    )
    # dx0_dp = np.zeros((dof, dof))
    # dv0_dp = np.identity(dof)
    gradient = pymandos.compute_loss_function_gradient_backpropagation(
        stepParameters.h, model, trajectory, loss, dx0_dp, dv0_dp, 10
    )
    return loss.loss, gradient


if __name__ == "__main__":
    positions = np.linspace(0.0, 2.0, 500 + 1)
    velocities = np.linspace(0.0, 2.0, 500 + 1)
    dx = positions[1] - positions[0]
    dv = velocities[1] - velocities[0]
    losses = []
    gradients = []
    for x in tqdm(positions):
        pos = [0.0, 0.0, 0.0, 1.0, x, 0]
        vel = [0.0, 0.0, 0.0, 1.0, 0, 0]
        loss, gradient = sim_wrapper(pos, vel)
        losses.append(loss)
        gradients.append(gradient[3 + 1])

    diff_gradient = np.gradient(losses, dx)

    """ Plot results """
    plt.grid()
    plt.title("Gradient with respect to initial orientation")
    plt.plot(positions, losses, label="Loss function")
    plt.plot(positions, gradients, label="BP")
    plt.plot(positions, diff_gradient, label="FD")
    plt.legend()
    plt.show()

    losses = []
    gradients = []
    for v in tqdm(velocities):
        pos = [0.0, 0.0, 0.0, 1.0, 0, 0]
        vel = [0.0, 0.0, 0.0, 1.0, v, 0]
        loss, gradient = sim_wrapper(pos, vel)
        losses.append(loss)
        gradients.append(gradient[6 + 3 + 1])

    diff_gradient = np.gradient(losses, dv)

    """ Plot results """
    plt.grid()
    plt.title("Gradient with respect to initial angular velocity")
    plt.plot(velocities, losses, label="Loss function")
    plt.plot(velocities, gradients, label="BP")
    plt.plot(velocities, diff_gradient, label="FD")
    plt.legend()
    plt.show()
