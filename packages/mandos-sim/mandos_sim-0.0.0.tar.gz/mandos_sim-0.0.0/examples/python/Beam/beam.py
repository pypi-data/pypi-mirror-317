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
    tetrahedron = model.add_deformable_3d()
    tetrahedron.size = npoints
    tetrahedron.x = mesh.points
    tetrahedron.v = np.zeros((npoints, 3))


    mass = 0.1 * np.ones(npoints)
    tetrahedron.particle_mass = mass

    snh = tetrahedron.snh

    tetras = mesh.get_cells_type("tetra")
    for tet in tetras:
      snh.add_element(tet, pymandos.energies.StableNeoHookean.ParameterSet(x0=mesh.points[tet, :], l=1000.0, mu=1000.0))

    # Fix some particles
    for i, p in enumerate(tetrahedron.x):
        if p[0] < 0.1:
            tetrahedron.fix_particle(i)
        if p[0] >  3:
            tetrahedron.fix_particle(i)

    model.compute_dag()

    ps.register_volume_mesh("Tet0", tetrahedron.x, tets=tetras)
    return model, tetrahedron

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
    model, tetrahedron = create_model()
    ps.set_user_callback(lambda : simulate_callback(model, tetrahedron))
    ps.show()
    
