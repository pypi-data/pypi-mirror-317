import sys
import numpy as np
import polyscope as ps
import pymandos

def create_model():
    #create the simulation scene
    model = pymandos.Model()
    #Create two particles, in the second of them, we will apply a force
    particles = model.add_deformable_3d()
    particles.size = 2
    # set their initial position and velocity
    particles.x = np.array([[0,0,0], [0,0,1]]) 
    particles.v = np.array([[0,0,0], [0,0,0]])
    # set their mass
    particles.particle_mass = [0.1,0.1]

    # fix the first one (zero index)    
    particles.fix_particle(0)

    # create a force instance and apply a force in the second particle
    cforce = particles.constant_force
    cforce.add_element(1,[0.0,1.0,1.0])

    model.compute_dag()

    ps.register_point_cloud("particles",particles.x, radius=0.1)
    return model, particles

def simulate_callback(model, particles):
    step_parameters = pymandos.StepParameters()
    step_parameters.h = 0.001
    step_parameters.newton_iterations =20
    step_parameters.cg_iterations = 100
    step_parameters.cg_error = 1e-8
    step_parameters.grad_norm = 1e-1
    step_parameters.line_search_iterations = 0
    result = pymandos.step(model, step_parameters)
    print(result)
    ps.get_point_cloud("particles").update_point_positions(particles.x)
    


if __name__ == "__main__":
    ps.init()
    ps.set_up_dir("z_up")
    model, particles = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, particles))
    ps.show()
    
