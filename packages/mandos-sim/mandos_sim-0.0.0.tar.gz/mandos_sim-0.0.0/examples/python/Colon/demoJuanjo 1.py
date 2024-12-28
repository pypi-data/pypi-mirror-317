import sys
import numpy as np
import meshio
import polyscope as ps

import os
import pymandos

from parallel_transport import compute_rotations_parallel_transport
import polyscope.imgui as psim


division_Coef = 1  ### divie by 1000 to make the mm of the colon in meters


n_points = int (160)
total_length = int (1000 * 1.5) /division_Coef


delta_x = total_length / n_points
insertion_speed = 100 /division_Coef
total_mass = 1
vUnit = np.zeros(3)
m_point = []

playing = False

def create_model():
    
    ## load the colon
    # mesh = meshio.read("14/3D_10mm_3109.msh")
    mesh = meshio.read("colon.stl")
    x = mesh.points /division_Coef
    
    # ##  find the coordinates to place the endoscope
    minZ = np.min(x[:,2])
    
    initalIndices = np.where (x[:,2]< minZ + 5 /division_Coef)
    average = np.average(x[initalIndices], axis=(0))
    print(average)
    middlePoint = np.zeros((1,3))
    middlePoint[0,0] = average[0]
    middlePoint[0,1] = average[1]
    middlePoint[0,2] = average[2]
    m_point.extend(middlePoint)

    print(average)

    # ## find a vector, perpendicular to the colons' whole
    p = x[initalIndices[0][0]]; q = x[initalIndices[0][1]]; r = x[initalIndices[0][2]]
    pq = q-p
    pr = r-p
    v = np.cross(pq,pr)
    global vUnit 
    vUnit = -v / (v**2).sum()**0.5   ##### carefull with the sign, I am not defining a sign until now!

    # ### Creat the pymandos model
    model = pymandos.Model()
    # ## create the rod model
    endoscope = model.add_rigidbody_cloud(name="endoscope")
    
    # Set initial conditions
    positions = np.zeros((n_points, 6))
    velocities = np.zeros((n_points, 6))

    startingPos= np.array([middlePoint[0,0], middlePoint[0,1], middlePoint[0,2]])
    for i, position in enumerate(positions):
        if i==0:
            position[0] = startingPos[0] 
            position[1] = startingPos[1] 
            position[2] = startingPos[2] 
        else:
            position[0] = startingPos[0] - delta_x * vUnit[0]
            position[1] = startingPos[1] - delta_x * vUnit[1]
            position[2] = startingPos[2] - delta_x * vUnit[2]
    
        startingPos[0] = position[0]
        startingPos[1] = position[1]
        startingPos[2] = position[2]

    positions = np.flip(positions,0) 
    lin_pos = np.array([pos[:3] for pos in positions])
    rotvecs = compute_rotations_parallel_transport(lin_pos)
    for rotvec, pos in zip(rotvecs, positions):
        pos[3:] = rotvec
    endoscope.size = n_points
    endoscope.x = positions
    endoscope.v = velocities
    # # Set up rigid body mass and inertia
    endoscope.mass = total_mass / n_points * np.ones(n_points)
    endoscope.inertiaTensor = [total_mass / n_points *np.diag([1.0, 1.0, 1.0]) for _ in range(n_points)]
    endoscope.disable_gravity()

    # # Rod energy
    cosserat_rod = endoscope.cosserat_rod
    Ks = [5000.0 for _ in range(n_points - 1)]
    stiffness_tensor = [20000 * np.ones(3) for _ in range(n_points - 2)]
    cosserat_stiffness = [100.0 for _ in range(n_points - 1)]

    cosserat_rod = endoscope.cosserat_rod
    cosserat_rod.set_parameters(Ks, cosserat_stiffness, stiffness_tensor)
    
    
    # ########### Map particles to rigid bodies for contact ####
    mapping = model.add_rigidbody_point_mapping(endoscope, to_name="Collider")

    # # The tube entrance has a diameter of 0.014, so dont go too crazy with the size of the collision radius
    # collision_radius = 0.003
    for i in range(n_points):
        mapping.add_particle(0 * np.array([1,0,0]), i)
        # mapping.add_particle(collision_radius * np.array([1,0,0]), i)
        # mapping.add_particle(collision_radius * np.array([-1,0,0]), i)
        # mapping.add_particle(collision_radius * np.array([0,1,0]), i)
        # mapping.add_particle(collision_radius * np.array([0,-1,0]), i)
        # mapping.add_particle(collision_radius * np.array([0,0,1]), i)
        # mapping.add_particle(collision_radius * np.array([0,0,-1]), i)
    deformable = mapping.deformable   

    collision_radius = 0.1 /division_Coef
    rod_collider = deformable.add_sphere_cloud(collision_radius)
    ps.register_point_cloud("ColliderSC", deformable.x, radius=0.0)
    
    ########################## Prepare the rigid body
    colon = model.add_rigidbody(name="colon")
    # Set initial conditions
    x = np.zeros(6)
    colon.x = x
    vel = np.zeros(6)
    colon.v = vel
    # Disable gravity
    colon.disable_gravity()
    
    # Set up rigid body mass and inertia
    colon.mass = 1
    colon.inertiaTensor = 1*np.diag([2.0, 1.0, 4.0])
    colon.fix()
    
    ##### Prepare Contact  for the rigid body######
    colon_mesh = pymandos.SurfaceMesh()
    # m = meshio.read("colon.stl")
    colon_mesh.x = mesh.points /division_Coef
    colon_mesh.indices = mesh.cells_dict["triangle"]
    colon_sdf = colon.add_sdf(colon_mesh, 0.1*np.max((np.max(colon_mesh.x, axis=0) - np.min(colon_mesh.x, axis=0))/512) , 512)

    # bound_low = np.min(colon_mesh.x, axis=0)
    # bound_high = np.max(colon_mesh.x, axis=0)
    # print(bound_low)
    # print(bound_high)
    # dims = (512, 512, 512)

    # def distance(x):
    #     if len(np.shape(x)) == 2:
    #         return np.array([colon_sdf.distance(x[i, :]) for i in range(np.shape(x)[0])])
    
    # ps.register_volume_grid("SDF", dims, bound_low, bound_high).add_scalar_quantity_from_callable("distance", distance)
    
    model.add_collision_pair(colon_sdf, rod_collider, stiffness=1000, name="collision_points", threshold=0.1)
    model.compute_dag()
    
    # Render
    axis_mesh = meshio.read("axis.obj")
    positions = np.array([x[:3] for x in endoscope.x])

    # for i in range(n_points):
    #     endoscope_view = ps.register_surface_mesh(f"Endoscope_{i}", axis_mesh.points, axis_mesh.cells_dict["triangle"], transparency=None)
    #     endoscope_view.set_transform(endoscope.get_transform(i))
    #     endoscope_view.add_color_quantity("c", axis_mesh.points, enabled=True)
    indices = np.array([(i, i+1) for i in range(n_points -1)])
    endoscope_view = ps.register_curve_network("Endoscope", positions, indices, radius = 0.005)
    
    ps.register_surface_mesh("Colon", mesh.points / division_Coef , mesh.cells_dict["triangle"], transparency=0.3)
    ps.get_surface_mesh("Colon").set_transform(colon.get_transform())
    
    return model

def simulate_callback(model):

    step_parameters = pymandos.StepParameters()
    step_parameters.h = 0.01
    step_parameters.newton_iterations = 5
    step_parameters.cg_iterations = 250
    step_parameters.cg_error = 1e-8
    step_parameters.grad_norm = 1e-2
    step_parameters.line_search_iterations = 0
    step_parameters.accept_failed_solution = True
    global playing
    if playing:
        if psim.Button("Pause"):
            playing = False
    elif psim.Button("Simulate"):
        playing=True

    doStep = playing
    if psim.Button("Step"):
        doStep = True

    endoscope = model.get_rigidbody_cloud("endoscope")

    if doStep:
        print(pymandos.step(model, step_parameters))
    
        dx = np.array([0, 0, step_parameters.h * insertion_speed])

        pos = endoscope.x.copy()

        # pos[0, 0:3] -= endoscope.get_transform(n_points-2)[0:3, 0:3] @ dx

        # endoscope.x = pos
        # index = 0
        # pos[index,2] = pos[index,2] + dx 
        # endoscope.clear_fixing()
        # endoscope.fix_translation(index)
        # endoscope.fix_rotation(index)

        A = np.abs(np.asarray(pos[:, 0:3]) - np.asarray(m_point[0]))
        index = (A ** 2).sum(1).argmin() -1

        pos = np.array([x for x in endoscope.x])
        endoscope.clear_fixing()
        for i in range(index, -1, -1):
            endoscope.fix_translation(i)
            pos[i,0:3] = pos[i,0:3] + dx * vUnit
            pos[i,0]= m_point[0][0]
            pos[i,1]= m_point[0][1]
        
        endoscope.x = pos

    model.detect_collisions()
    model.compute_forces(0)

    collision_points = model.get_collisions_state("collision_points")
    collider = model.get_deformable3d("Collider")

    if doStep:
        if collision_points.size > 0:
            n_collisions = collision_points.size // 2
            x = collision_points.x[n_collisions:2*n_collisions, :]
            collisions = ps.register_point_cloud("collision_points", x, radius = 0)
            collisions.add_vector_quantity("f", collision_points.f[n_collisions:2*n_collisions, :], enabled=True)
            # playing = False
        else:
            if ps.has_point_cloud("collision_points"):
                ps.remove_point_cloud("collision_points")

    # positions = np.array([x[:3] for x in endoscope.x])  
    # for i in range(n_points):
    #     ps.get_surface_mesh(f"Endoscope_{i}").set_transform(endoscope.get_transform(i))
    ps.get_curve_network("Endoscope").update_node_positions(endoscope.x[:,0:3])
    ps.get_point_cloud("ColliderSC").update_point_positions(collider.x)
        
if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    # ps.look_at((0.0, 10.0, 2.0), (0.0, 0.0, 0.0))
    ps.set_ground_plane_mode("none") # Disable ground rendering
    model = create_model()
    ps.set_user_callback(lambda: simulate_callback(model))
    ps.show()
