#!/usr/bin/env python3

import tkinter as tk
import numpy as np

import polyscope as ps
from scipy.optimize import minimize
import os, sys

sys.path.append(os.getcwd() + "/../Rod")
from parallel_transport import compute_rotations_parallel_transport
import pymandos


def compute_length(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw")

        # Create a canvas widget
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()

        # Create Widget
        self.save_button = tk.Button(
            self.root, text="Simulate", command=self.compute_points
        )
        self.save_button.pack()

        # Variables to track the current position
        self.last_x, self.last_y = None, None

        # Bind mouse events to canvas
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<Button-1>", self.clear_canvas)

        self.positions = []

    def draw(self, event):
        if self.last_x and self.last_y:
            # Create a line from the last position to the current position
            self.canvas.create_line(
                (self.last_x, self.last_y, event.x, event.y), fill="black", width=2
            )
            self.positions.append((event.x, event.y))

        # Update the last position
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        # Reset the last position when the mouse button is released
        self.last_x, self.last_y = None, None

    def clear_canvas(self, event):
        self.canvas.delete("all")
        self.last_x, self.last_y = None, None
        self.positions = []

    def compute_points(self):
        def compute_lengths(positions):
            lengths = []
            for i in range(len(self.positions) - 1):
                p1 = self.positions[i]
                p2 = self.positions[i + 1]
                lengths.append(compute_length(p1, p2))
            return lengths

        lengths = compute_lengths(self.positions)

        lengths = np.array(lengths)
        comulated_lengths = []
        total_len = 0
        for length in lengths:
            comulated_lengths.append(total_len)
            total_len += length
        if total_len < 300:
            print("Too short")
            return

        def sample_curve(s):
            if s > total_len:
                raise ValueError(
                    "The desired distance is bigger than the total curve distance!"
                )
            for i, length in enumerate(comulated_lengths):
                if s <= length:
                    p1 = self.positions[i - 1]
                    p2 = self.positions[i]
                    norm = compute_length(p1, p2)
                    if norm > 1e-8:
                        t = (length - s) / norm
                    else:
                        t = 0.0
                    return t * np.array(p1) + (1 - t) * np.array(p2)
            raise ValueError("Unreachable")

        target_points = 71
        delta = float(total_len) / float(target_points)
        positions = []
        for i in range(target_points):
            p = sample_curve(i * delta)
            positions.append(p)
            radius = 5
            self.canvas.create_oval(
                int(p[0]) - radius,
                int(p[1]) - radius,
                int(p[0]) + radius,
                int(p[1]) + radius,
                fill="blue",
            )
        desired_delta = 0.4
        scaling = desired_delta / delta
        positions = scaling * np.array(positions)
        positions = np.hstack((positions, np.zeros((target_points, 1))))
        self.root.destroy()
        self.positions = positions


# Create the Tkinter window
root = tk.Tk()

# Create the drawing app
app = DrawingApp(root)

# Run the application
root.mainloop()
print(app.positions)

direction = -(app.positions[0] - app.positions[-1]) / np.linalg.norm(
    app.positions[0] - app.positions[-1]
)
direction = np.array((direction[0], direction[1], 0))

points = app.positions
n_points = points.shape[0]
indices = np.array([(i, i + 1) for i in range(n_points - 1)])
delta_x = np.linalg.norm(points[1] - points[0])
origin = np.array(np.mean(points, axis=0))
print(f"Origin {origin}")
print(f"Curve with {n_points} points, and with a distance of {delta_x}")

linear_dof_matrix = []
for i in range(n_points):
    index = i * 6
    for j in range(3):
        row = np.zeros(6 * n_points)
        row[index + j] = 1.0
        linear_dof_matrix.append(row)
linear_dof_matrix = np.array(linear_dof_matrix)

stepParameters = pymandos.StepParameters()
stepParameters.h = 0.01
stepParameters.newton_iterations = 10
stepParameters.cg_error = 1e-8
stepParameters.grad_norm = 1e-7
stepParameters.line_search_iterations = 0

backward_iterations = 0


def create_model(initial_velocities):
    model = pymandos.Model()
    rigid_body_cloud = model.add_rigidbody_cloud()

    # Set initial conditions
    positions = np.zeros((n_points, 6))
    velocities = np.zeros((n_points, 6))
    for i, position in enumerate(positions):
        position[0:3] += (delta_x * i - 0.5 * n_points * delta_x) * direction
        position[0:3] += origin
    for i, vel in enumerate(velocities):
        vel[0:3] = initial_velocities[3 * i : 3 * i + 3]

    lin_pos = np.array([pos[:3] for pos in positions])
    rotvecs = compute_rotations_parallel_transport(lin_pos)
    for rotvec, pos in zip(rotvecs, positions):
        pos[3:] = rotvec
    rigid_body_cloud.size = n_points
    rigid_body_cloud.x = positions
    rigid_body_cloud.v = velocities
    rigid_body_cloud.disable_gravity()

    # Set up rigid body mass and inertia
    rigid_body_cloud.mass = 1.0 * np.ones(n_points)
    rigid_body_cloud.inertiaTensor = [np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)]

    # Rod energy
    Ks = [3000.0 for _ in range(n_points-1)]
    stiffness_tensor = [100.0 * np.ones(3) for _ in range(n_points-2)]
    cosserat_stiffness = [1000.0 for _ in range(n_points-1)]
    cosserat_rod = rigid_body_cloud.cosserat_rod
    cosserat_rod.set_parameters(Ks, cosserat_stiffness, stiffness_tensor)

    model.compute_dag()

    # Render
    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    indices = np.array([(i, i + 1) for i in range(n_points - 1)])
    ps.register_curve_network("rod_curve", positions, indices, radius=0.01)
    ps.register_curve_network("heart", points, indices, radius=0.01)

    return model, rigid_body_cloud


def compute_loss(trajectory: pymandos.Trajectory) -> pymandos.LossFunctionAndGradients:
    loss = pymandos.LossFunctionAndGradients()
    dof = trajectory.get_n_dof()
    x_final = trajectory.positions[-1]
    delta = linear_dof_matrix @ x_final.copy() - points.flatten()
    loss.loss = np.dot(delta, delta)
    loss_position_partial_derivative = [np.zeros(dof) for _ in trajectory.positions]
    loss_position_partial_derivative[-1] = 2.0 * linear_dof_matrix.T @ delta
    loss.loss_position_partial_derivative = loss_position_partial_derivative
    loss.loss_velocity_partial_derivative = [
        np.zeros(dof) for _ in trajectory.positions
    ]
    loss.loss_parameter_partial_derivative = np.zeros(int(dof / 6 * 3))
    return loss


def simulate(initial_vel: list, diff_frames: int):
    model, rb_cloud = create_model(initial_vel)
    trajectory = pymandos.Trajectory()
    trajectory.append_state(model)
    for _ in range(diff_frames):
        converged = pymandos.step(model, stepParameters)
        if not converged:
            print("Not converged:", converged)
        trajectory.append_state(model)
        # Render
        positions = np.array([x[:3] for x in rb_cloud.x])
        ps.get_curve_network("rod_curve").update_node_positions(positions)
        if ps.window_requests_close():
            exit()
        ps.frame_tick()
    return trajectory, model


def sim_wrapper(v0):
    trajectory, model = simulate(v0, 100)
    loss = compute_loss(trajectory)
    dof = trajectory.get_n_dof()
    dx0_dp = np.zeros((dof, int(dof / 6 * 3)))
    dv0_dp = linear_dof_matrix.copy().T
    # dv0_dp = np.diag(
    #     np.array(
    #         [[1.0, 1.0, 1.0, 0.0, 0.0, 0.0] for _ in range(int(dof / 6))]
    #     ).flatten()
    # )

    gradient = pymandos.compute_loss_function_gradient_backpropagation(
        stepParameters.h, model, trajectory, loss, dx0_dp, dv0_dp, backward_iterations
    )
    return loss.loss, gradient


def simulate_callback(model, rigid_body_cloud):
    pymandos.step(model, stepParameters)

    positions = np.array([x[:3] for x in rigid_body_cloud.x])
    ps.get_curve_network("rod_curve").update_node_positions(positions)


if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at(np.array((0, 1.0, 18.0)) + origin, origin)
    ps.set_ground_plane_mode("none")  # Disable ground rendering
    initial_velocities = np.zeros(n_points * 3)

    minimize(
        sim_wrapper,
        initial_velocities,
        method="L-BFGS-B",
        jac=True,
        options={"disp": True},
    )
    model, rigid_body_cloud = create_model(initial_velocities)
    ps.set_user_callback(lambda: simulate_callback(model, rigid_body_cloud))
    ps.show()
