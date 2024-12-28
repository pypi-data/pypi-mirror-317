#!/usr/bin/env python3

import sys
import numpy as np
import meshio
import polyscope as ps

import pymandos

from mesh_boundary import compute_tension_and_bending_spring_indices

def create_model():

    # Load the Beam model
    mesh = meshio.read("grid.obj")
    npoints = mesh.points.shape[0]

    model = pymandos.Model()
    deformable = model.add_deformable_3d()
    deformable.size = npoints
    deformable.x = mesh.points
    deformable.v = np.zeros((npoints, 3))

    mass = np.ones(npoints)
    deformable.particle_mass = mass

    mass_spring = deformable.mass_spring

    triangles = mesh.get_cells_type("triangle")
    tension_edges, bending_edges = compute_tension_and_bending_spring_indices(triangles)

    # We can add elements using directly the rest length and the stiffness
    for edge in tension_edges:
        L0 = np.linalg.norm(deformable.x[edge[0], :] - deformable.x[edge[1], :])
        mass_spring.add_element(edge, pymandos.energies.MassSpring.ParameterSet(rest_length = L0, stiffness = 10000.0))

    # Or we can add elements using positions for the rest state
    for edge in bending_edges:
        mass_spring.add_element(edge, pymandos.energies.MassSpring.ParameterSet(x0 = deformable.x[edge, :], stiffness = 100.0))

    # Fix some particles
    deformable.fix_particle(0, x=False,y=False)

    model.compute_dag()

    ps.register_surface_mesh("mesh", deformable.x, triangles)
    return model, deformable

def simulate_callback(model, deformable):
    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations = 10
    stepParameters.cg_iterations = 50
    stepParameters.cg_error = 1e-4
    stepParameters.grad_norm = 1e-3
    stepParameters.line_search_iterations = 5

    pymandos.step(model, stepParameters)
    ps.get_surface_mesh("mesh").update_vertex_positions(deformable.x)

if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at((0.0, 10.0, 2.0), (0.0, 0.0, 0.0))
    ps.set_ground_plane_mode("none") # Disable ground rendering
    model, deformable = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, deformable))
    ps.show()
