import sys
import numpy as np
import meshio
import polyscope as ps
import polyscope.imgui as psim
import matplotlib.pyplot as plt

from scipy.optimize import minimize

import pymandos

def create_model():

    model = pymandos.Model()

    # Add a rigid body
    cube = model.add_rigidbody_cloud(name="Cube")
    cube.size = 1

    # Set initial conditions
    x = np.zeros((1,6))
    v = np.zeros((1,6))
    x[0,2] = 0.8
    cube.x = x
    cube.v = v

    # Set up rigid body mass and inertia
    cube.mass = [.1]
    cube.inertiaTensor = [np.diag([1.0, 1.0, 1.0])]

    mapping = model.add_rigidbody_point_mapping(cube)
    mapping.add_particle(np.array([0,0,0]), 0)
    deformable = mapping.deformable   
    cube_collider = deformable.add_sphere_cloud(0.1)

    # Add a floor
    floor = model.add_rigidbody(name="Floor")

    x = np.zeros(6)
    v = np.zeros(6)
    floor.x = x
    floor.v = v
    floor.disable_gravity()
    
    # Set up rigid body mass and inertia
    floor.mass = 1
    floor.inertiaTensor = np.diag([1.0, 1.0, 1.0])
    floor.fix()
    
    floor_mesh = pymandos.SurfaceMesh()
    m = meshio.read("floor.stl")
    floor_mesh.x = m.points
    floor_mesh.indices = m.cells_dict["triangle"]

    # ps.register_surface_mesh("Floor", floor_mesh.x , m.cells_dict["triangle"], transparency=0.3)


    m = meshio.read("axis.obj")
    t = cube.get_transform(0)
    # cube = ps.register_surface_mesh("Cube", m.points , m.cells_dict["triangle"], transparency=0.3)
    # cube.set_transform(t)

    floor_sdf = floor.add_sdf(floor_mesh, 1)
    
    collisions = model.add_collision_pair(floor_sdf, cube_collider, stiffness=2000, name="collisions")

    # ps.register_point_cloud("collisions", collisions.x)
    

    model.commit()

    print("Finished")

    return model

def energy(model, x, x0, h):
    v = (x - x0)/h
    model.set_state(x, v)
    model.advect(h)
    return model.energy(h)

def grad(model, x, x0, h):
    v = (x - x0)/h
    model.set_state(x, v)
    model.advect(h)
    return model.grad(h)

def sim(model):
    h = 0.03
    x0, v0 = model.state()

    model.detect_collisions()

    minimize(lambda x: energy(model, x, x0, h), x0, method='BFGS', jac=lambda x: grad(model, x, x0, h))

def simulate_callback(model):
    step_parameters = pymandos.StepParameters()
    step_parameters.h = 0.03
    step_parameters.newton_iterations = 50
    step_parameters.cg_iterations = 100
    step_parameters.cg_error = 1e-4
    step_parameters.grad_norm = 1e-1
    step_parameters.line_search_iterations = 5

    sim(model)

    t = model.get_rigidbody_cloud("Cube").get_transform(0)

    model.compute_forces(0)

    cube = model.get_rigidbody_cloud("Cube")
    floor = model.get_rigidbody("Floor")

    if len(model.get_collisions_state("collisions").x) > 0:
        ps.register_point_cloud("collisions", model.get_collisions_state("collisions").x)
        ps.get_point_cloud("collisions").add_vector_quantity("forces", model.get_collisions_state("collisions").f)

    ps.get_surface_mesh("Cube").set_transform(t)

def simulate(model):
    step_parameters = pymandos.StepParameters()
    step_parameters.h = 0.03
    step_parameters.newton_iterations = 15
    step_parameters.cg_iterations = 10
    step_parameters.cg_error = 1e-8
    step_parameters.grad_norm = 1e-2
    step_parameters.line_search_iterations = 25

    print(pymandos.step(model, step_parameters))
    potential = model.potential_energy()
    kinetic = model.kinetic_energy()
    x = model.get_rigidbody_cloud("Cube").x[0,2]

    return potential, kinetic, x

import time

if __name__ == "__main__":
    model = create_model()
    X = []
    K = []
    U = []
    X.append(model.get_rigidbody_cloud("Cube").x[0, 2])
    U.append(model.potential_energy())
    K.append(model.kinetic_energy())
    for i in range(1250):
        u, k, x = simulate(model)   
        X.append(x)
        U.append(u)
        K.append(k)

    plt.scatter(np.linspace(0, 1, len(X)), X)
    # plt.scatter(np.linspace(0, 1, len(K)), K)
    # plt.scatter(np.linspace(0, 1, len(U)), U)
    plt.show()
    
    # ps.init()
    # ps.set_user_callback(lambda: simulate_callback(model))

    # ps.show()
        
    
