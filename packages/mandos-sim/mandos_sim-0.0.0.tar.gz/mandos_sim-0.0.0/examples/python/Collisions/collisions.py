import sys
import numpy as np
import meshio
import polyscope as ps

import pymandos

def create_model():

    # Load the Beam model
    mesh = meshio.read("beam.msh")
    npoints = mesh.points.shape[0]

    model = pymandos.Model()
    beam = model.add_deformable_3d()
    beam.size = npoints
    beam.x = mesh.points
    beam.v = np.zeros((npoints, 3))

    mass = 0.01 * np.ones(npoints)
    beam.particle_mass = mass

    snh = beam.snh

    tetras = mesh.get_cells_type("tetra")
    for tet in tetras:
      snh.add_element(tet, pymandos.energies.StableNeoHookean.ParameterSet(x0=mesh.points[tet, :], l=1000.0, mu=1000.0))

    # Fix some particles
    for i, p in enumerate(beam.x):
        if p[0] < 0.1:
            beam.fix_particle(i)
        if p[0] >  3:
            beam.fix_particle(i)

    beam_collider = beam.add_sphere_cloud(0.01)

    # Prepare the rigid body
    rigid_body = model.add_rigidbody()

    # Set initial conditions
    x = np.zeros(6)
    x[0] = 1.5
    x[2] = -0.5
    x[3] = 3.14/2
    rigid_body.x = x
    vel = np.zeros(6)
    rigid_body.v = vel

    rigid_body2 = model.add_rigidbody()

    # Set initial conditions
    x = np.zeros(6)
    x[0] = 1.8
    x[2] = 0.5
    x[3] = 3.14/2
    rigid_body2.x = x
    vel = np.zeros(6)
    rigid_body2.v = vel

    # Disable gravity
    rigid_body.disable_gravity()

    # Set up rigid body mass and inertia
    rigid_body.mass = 1.0
    rigid_body.inertiaTensor = 1*np.diag([2.0, 1.0, 4.0])

    rigid_body2.mass = 0.2
    rigid_body2.inertiaTensor = 0.2*np.diag([2.0, 1.0, 4.0])

    
    sdf_mesh = pymandos.SurfaceMesh()
    m = meshio.read("crossbar.obj")
    sdf_mesh.x = m.points
    sdf_mesh.indices = m.cells_dict["triangle"]

    print("Create collider SDF")
    crossbar_sdf = rigid_body.add_sdf(sdf_mesh, 0.1)
    crossbar_sdf2 = rigid_body2.add_sdf(sdf_mesh, 0.1)
    print("Created collider SDF")


    print("Add collision pair")
    collision_particles = model.add_collision_pair(crossbar_sdf, beam_collider, stiffness=500)
    collision_particles2 = model.add_collision_pair(crossbar_sdf2, beam_collider, stiffness=200)
    print("Collision pair added")

    print("Compute DAG")
    model.compute_dag()

    print("Finished")

    ps.register_volume_mesh("Tet0", beam.x, tets=tetras)
    ps.register_surface_mesh("Collider", sdf_mesh.x, m.cells_dict["triangle"])
    ps.register_surface_mesh("Collider2", sdf_mesh.x, m.cells_dict["triangle"])
    ps.get_surface_mesh("Collider").set_transform(rigid_body.get_transform())
    ps.get_surface_mesh("Collider2").set_transform(rigid_body2.get_transform())
    return model, beam, rigid_body, rigid_body2, collision_particles, collision_particles2

def simulate_callback(model, tetrahedron, rb, rb2, collision_particles, collision_particles2):
    step_parameters = pymandos.StepParameters()
    step_parameters.h = 0.002
    step_parameters.newton_iterations =50
    step_parameters.cg_iterations = 20
    step_parameters.cg_error = 1e-4
    step_parameters.grad_norm = 1e-2
    step_parameters.line_search_iterations = 5
    print(pymandos.step(model, step_parameters))


    ps.get_volume_mesh("Tet0").update_vertex_positions(tetrahedron.x)
    ps.get_surface_mesh("Collider").set_transform(rb.get_transform())
    ps.get_surface_mesh("Collider2").set_transform(rb2.get_transform())

    nCollisions = collision_particles.x.shape[0]
    if nCollisions > 0:
        ps.register_point_cloud("Collision", collision_particles.x)
    else:
        if ps.has_point_cloud("Collision"):
            ps.remove_point_cloud("Collision")

    nCollisions = collision_particles2.x.shape[0]
    if nCollisions > 0:
        ps.register_point_cloud("Collision2", collision_particles2.x)
    else:
        if ps.has_point_cloud("Collision2"):
            ps.remove_point_cloud("Collision2")



import time

if __name__ == "__main__":
    ps.init()
    model, beam, rb, rb2, collision_particles, collision_particles2 = create_model()
    ps.set_user_callback(lambda: simulate_callback(model, beam, rb, rb2, collision_particles, collision_particles2))

    ps.show()
        
    
