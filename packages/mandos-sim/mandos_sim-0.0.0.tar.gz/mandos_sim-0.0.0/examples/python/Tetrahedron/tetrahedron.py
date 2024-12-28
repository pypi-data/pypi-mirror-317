import sys
import numpy as np
import polyscope as ps

import pymandos

def create_model():
    model = pymandos.Model()
    tetrahedron = model.add_deformable_3d(name="tetra")
    tetrahedron.size = 4
    tetrahedron.x = np.array([0,0,2]) + np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]])
    tetrahedron.v = np.array([[0,0,0], [0,0,0], [0,0,0], [0,0,0]])

    tetrahedron.particle_mass = [0.1,0.1,0.1,0.1]

    snh = tetrahedron.snh
    snh.add_element([0,1,2,3], pymandos.energies.StableNeoHookean.ParameterSet(x0=tetrahedron.x[[0,1,2,3], :], l=100.0, mu=100.0))

    tetrahedron.fix_particle(0)

    model.compute_dag()

    ps.register_volume_mesh("Tet0", tetrahedron.x, tets=np.array([[0,1,2,3,]]))
    return model

def simulate_callback(model, tetrahedron):
    stepParameters = pymandos.StepParameters()
    stepParameters.h = 0.01
    stepParameters.newton_iterations =5
    stepParameters.cg_iterations = 20
    stepParameters.cg_error = 1e-4
    stepParameters.grad_norm = 1e-3
    stepParameters.line_search_iterations = 5

    pymandos.step(model, stepParameters)
    ps.get_volume_mesh("Tet0").update_vertex_positions(tetrahedron.x)
    


if __name__ == "__main__":
    ps.init()
    model = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, model.get_deformable3d("tetra")))
    ps.show()
    
