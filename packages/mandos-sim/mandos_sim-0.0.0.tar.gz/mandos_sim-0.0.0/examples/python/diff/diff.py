#!/usr/bin/env python3

import numpy as np
import polyscope as ps
import matplotlib.pyplot as plt
import scipy as sp

import pymandos

TARGET = np.array([1.0, 0.0, 1.0])
stepParameters = pymandos.StepParameters()
stepParameters.h = 0.01
stepParameters.newton_iterations = 5
stepParameters.cg_iterations = 20
stepParameters.cg_error = 1e-8
stepParameters.grad_norm = 1e-5
stepParameters.line_search_iterations = 0


def create_model(initial_vel: list):
    model = pymandos.Model()
    particles = model.add_deformable_3d()
    particles.size = 1
    particles.x = np.array([[0, 0, 0]])
    particles.v = np.array([initial_vel])

    particles.particle_mass = [1.0]

    model.commit()

    points = np.array((particles.x[0], TARGET))
    ps.register_point_cloud("particles", points, radius=0.1)
    return model, particles


def simulate_callback(model, particles):
    pymandos.step(model, stepParameters)
    points = np.array((particles.x[0], TARGET))
    ps.get_point_cloud("particles").update_point_positions(points)


def simulate(initial_vel: list, diff_frames: int):
    model, particles = create_model(initial_vel)
    trajectory = pymandos.Trajectory()
    trajectory.append_state(model)
    for _ in range(diff_frames):
        pymandos.step(model, stepParameters)
        trajectory.append_state(model)
    return trajectory, model


def compute_loss(trajectory: pymandos.Trajectory) -> pymandos.LossFunctionAndGradients:
    loss = pymandos.LossFunctionAndGradients()
    delta = trajectory.positions[-1] - TARGET
    loss.loss = np.dot(delta, delta)
    loss_position_partial_derivative = [
        np.zeros(3) for _ in range(len(trajectory.positions))
    ]
    loss_position_partial_derivative[-1] = 2.0 * delta
    loss.loss_position_partial_derivative = loss_position_partial_derivative
    loss.loss_velocity_partial_derivative = [
        np.zeros(3) for _ in range(len(trajectory.positions))
    ]
    loss.loss_parameter_partial_derivative = np.zeros(
        3
    )  # 3 parameters (one for each initial velocity vector coefficient)
    return loss


def sim_wrapper(v0):
    trajectory, model = simulate(v0, 100)
    loss = compute_loss(trajectory)
    dx0_dp = np.zeros((3, 3))
    dv0_dp = np.identity(3)
    gradient = pymandos.compute_loss_function_gradient_backpropagation(
        stepParameters.h, model, trajectory, loss, dx0_dp, dv0_dp, 0
    )
    return loss.loss, gradient


if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")

    losses = []
    gradients = []
    for vel in np.linspace(1,5, 100):
        trajectory, model = simulate([0,0,vel], 100)
        loss = compute_loss(trajectory)
        dx0_dp = np.zeros((3,3))
        dv0_dp = np.identity(3)
        gradient = pymandos.compute_loss_function_gradient_backpropagation(stepParameters.h, model, trajectory, loss, dx0_dp, dv0_dp, 0)
        losses.append(loss.loss)
        gradients.append(gradient[-1])

    gradients2 = np.gradient(np.array(losses), 4.0/100.0)
    plt.plot(gradients2)
    plt.plot(gradients)
    plt.show()

    result = sp.optimize.minimize(sim_wrapper, [0, 0, 0], jac=True)
    # print(result)

    model, particles = create_model(result.x)
    # model, particles = create_model([0,0,0])
    ps.set_user_callback(lambda: simulate_callback(model, particles))
    ps.show()
