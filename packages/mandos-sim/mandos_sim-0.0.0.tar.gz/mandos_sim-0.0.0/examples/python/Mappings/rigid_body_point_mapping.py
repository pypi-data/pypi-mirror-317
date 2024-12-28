import sys
import numpy as np
import meshio
import polyscope as ps

import pymandos

n_points = 2
delta_x = 2.0

def create_model():
    model = pymandos.Model()
    rigid_body_cloud = model.add_rigidbody_cloud()

    # Set initial conditions
    positions = np.zeros((n_points, 6))
    velocities = np.zeros((n_points, 6))
    for i, position in enumerate(positions):
        position[0] += delta_x * i

    initial_vel = 1.0
    for i, velocity in enumerate(velocities):
        velocity[5] = -initial_vel + 2.0*initial_vel*i

    rigid_body_cloud.size = n_points
    rigid_body_cloud.x = positions
    rigid_body_cloud.v = velocities

    # Disable gravity
    # rigid_body_cloud.disable_gravity()
    rigid_body_cloud.fix_translation(1)

    # Set up rigid body mass and inertia
    rigid_body_cloud.mass = np.ones(n_points)
    rigid_body_cloud.inertiaTensor = [np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)]

    # Create the mapping
    mapping = model.add_rigidbody_point_mapping(rigid_body_cloud);
    mapping.add_particle([2.0,0.0,0.0], 0);
    mapping.add_particle([0.0,2.0,0.0], 1);
    # mapping.add_particle([-4.0, 0.0,0.0], 0);

    mass_spring = mapping.deformable.mass_spring
    mass_spring.add_element((0,1), 10.0, 0.0)
    mapping.deformable.particle_mass = np.zeros(mapping.deformable.size)
    mapping.deformable.particle_mass = np.ones(mapping.deformable.size)

    model.compute_dag()

    # Render mesh
    mesh = meshio.read("../Rod/axis.obj")
    for i in range(n_points):
        ps_mesh = ps.register_surface_mesh("rigid_body_"+str(i), mesh.points, mesh.get_cells_type("triangle"))
        ps_mesh.add_color_quantity("xyz", mesh.points, enabled=True)

    ps.register_curve_network("spring", mapping.deformable.x, np.array([[0,1]]))
    ps.register_point_cloud("particles", mapping.deformable.x, radius=0.1)

    return model, rigid_body_cloud, mapping

def simulate_callback(model, rigid_body_cloud, mapping):

    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations =5
    stepParameters.cg_iterations = 20
    stepParameters.cg_error = 1e-4
    stepParameters.grad_norm = 1e-3
    stepParameters.line_search_iterations = 5

    pymandos.step(model, stepParameters)

    for i in range(n_points):
        transform = rigid_body_cloud.get_transform(i)
        ps.get_surface_mesh("rigid_body_"+str(i)).set_transform(transform)

    ps.get_curve_network("spring").update_node_positions(mapping.deformable.x)
    ps.get_point_cloud("particles").update_point_positions(mapping.deformable.x)

if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    ps.look_at((0.0, 10.0, 2.0), (0.0, 0.0, 0.0))
    ps.set_ground_plane_mode("none") # Disable ground rendering
    model, rigid_body_cloud, mapping = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, rigid_body_cloud, mapping))
    ps.show()
