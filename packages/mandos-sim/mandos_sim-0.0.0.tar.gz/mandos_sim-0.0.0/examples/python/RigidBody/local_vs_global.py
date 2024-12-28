#!/usr/bin/env python3

import sys
import numpy as np
import meshio
import polyscope as ps

import pymandos


def create_model():
    model = pymandos.Model()
    rigid_body_local = model.add_rigidbody()
    rigid_body_global = model.add_rigidbody_global()

    # Set initial conditions
    pos = np.zeros(6)
    pos[0] = -3.0
    vel = np.zeros(6)
    vel[3] = 1.0
    vel[4] = 0.01
    rigid_body_local.x = pos
    rigid_body_local.v = vel

    rigid_body_global.x = -pos
    rigid_body_global.v = vel

    # Disable gravity
    rigid_body_local.disable_gravity()
    rigid_body_global.disable_gravity()

    # Set up rigid body mass and inertia
    rigid_body_local.mass = 1.0
    rigid_body_local.inertiaTensor = np.diag([2.0, 1.0, 4.0])
    rigid_body_global.mass = 1.0
    rigid_body_global.inertiaTensor = np.diag([2.0, 1.0, 4.0])

    model.compute_dag()

    # Render mesh
    mesh = meshio.read("tennis.obj")
    ps.register_surface_mesh(
        "rb_local_mesh", mesh.points, mesh.cells_dict.get("triangle")
    )
    ps.register_surface_mesh(
        "rb_global_mesh", mesh.points, mesh.cells_dict.get("triangle")
    )

    ps.get_surface_mesh("rb_local_mesh").set_transform(rigid_body_local.get_transform())
    ps.get_surface_mesh("rb_global_mesh").set_transform(
        rigid_body_global.get_transform()
    )

    return model, rigid_body_local, rigid_body_global


def simulate_callback(model, rigid_body_local, rigid_body_global):
    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.1
    stepParameters.newton_iterations = 5
    stepParameters.cg_error = 1e-7
    stepParameters.grad_norm = 1e-1
    stepParameters.line_search_iterations = 0

    pymandos.step(model, stepParameters)
    ps.get_surface_mesh("rb_local_mesh").set_transform(rigid_body_local.get_transform())
    ps.get_surface_mesh("rb_global_mesh").set_transform(
        rigid_body_global.get_transform()
    )


if __name__ == "__main__":
    ps.init()
    ps.set_ground_plane_mode("none")  # Disable the ground
    model, rigid_body_local, rigid_body_global = create_model()
    ps.set_user_callback(
        lambda: simulate_callback(model, rigid_body_local, rigid_body_global)
    )
    ps.show()
