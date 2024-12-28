import sys
import numpy as np
import meshio
import polyscope as ps

import pymandos


def create_model():
    model = pymandos.Model()
    rigid_body = model.add_rigidbody()

    # Set initial conditions
    rigid_body.x = np.zeros(6)
    vel = np.zeros(6)
    vel[3] = 1.0
    vel[4] = 0.01
    rigid_body.v = vel

    # Disable gravity
    rigid_body.disable_gravity()

    # Set up rigid body mass and inertia
    rigid_body.mass = 1.0
    rigid_body.inertiaTensor = np.diag([2.0, 1.0, 4.0])

    model.compute_dag()

    # Render mesh
    mesh = meshio.read("tennis.obj")
    ps.register_surface_mesh("rb_mesh", mesh.points, mesh.cells_dict.get("triangle"))

    return model, rigid_body


def simulate_callback(model, rigid_body):
    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations = 5
    stepParameters.cg_iterations = 20
    stepParameters.cg_error = 1e-4
    stepParameters.grad_norm = 1e-3
    stepParameters.line_search_iterations = 0

    pymandos.step(model, stepParameters)
    ps.get_surface_mesh("rb_mesh").set_transform(rigid_body.get_transform())


if __name__ == "__main__":
    ps.init()
    ps.set_ground_plane_mode("none")  # Disable ground rendering
    model, rigid_body = create_model()
    ps.set_user_callback(lambda: simulate_callback(model, rigid_body))
    ps.show()
