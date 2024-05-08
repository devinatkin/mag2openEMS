import os
import numpy as np
from loadmag import load_mag_file, draw_rects, get_bounds
from matplotlib import pyplot as plt

from CSXCAD  import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import C0

from sky130_geometry import add_materials

import vtk
from vtk.util.numpy_support import numpy_to_vtk

simulation_path = "/workspaces/mag2openEMS/SIM"

if __name__ == "__main__":
    file_path = "/workspaces/mag2openEMS/example/inverter.mag"
    data = load_mag_file(file_path)
    print("\nMag File Loaded\n")

    draw_rects(data, "metal1", plt.gca())

    (xmin, xmax), (ymin, ymax) = get_bounds(data)
    plt.savefig("inverter_metal1.png")

    # setup FDTD parameter & excitation function
    f0 = 2e9 # center frequency
    fc = 1e9 # 20 dB corner frequency

    # size of the simulation box
    SimBox = np.array([xmax-xmin, ymax-ymin, 150])


    FDTD = openEMS(NrTS=30000, EndCriteria=1e-4)
    FDTD.SetGaussExcite( f0, fc )
    FDTD.SetBoundaryCond( ['MUR', 'MUR', 'MUR', 'MUR', 'MUR', 'MUR'] )

    CSX = ContinuousStructure()
    FDTD.SetCSX(CSX)
    
    
    mesh = CSX.GetGrid()
    mesh.SetDeltaUnit(1)

    ### Generate properties, primitives and mesh-grid
    #initialize the mesh with the "air-box" dimensions
    mesh.AddLine('x', np.linspace(-SimBox[0]/2, SimBox[0]/2, int(SimBox[0])+1))
    mesh.AddLine('y', np.linspace(-SimBox[1]/2, SimBox[1]/2, int(SimBox[1])+1))
    mesh.AddLine('z', np.linspace(-SimBox[2]/3, SimBox[2]*2/3, int(SimBox[2])+1))

    materials_dict = add_materials(CSX, xmin, xmax, ymin, ymax)

    # # create ground (same size as substrate)
    # gnd = CSX.AddMetal( 'gnd' ) # create a perfect electric conductor (PEC)
    # start = [-SimBox[0]/2, -SimBox[1]/2, 0]
    # stop  = [ SimBox[0]/2,  SimBox[1]/2, 0]
    # gnd.AddBox(start, stop, priority=10)

    # Load Data into CSX
    for layer in data:
        material = materials_dict.get(layer, None)

        if material is None:
            print("Material is None")
            continue
        for rect in data[layer]:
            xstart = float(rect[0])
            ystart = float(rect[1])
            xend = float(rect[2])
            yend = float(rect[3])
            zstart = 0
            zend = 1
            start = [xstart, ystart, zstart]
            stop = [xend, yend, zend]
            
            
            material.AddBox(start, stop)

    # apply the excitation & resist as a current source
    
    #setup feeding
    feed_pos = -6 #feeding position in x-direction
    feed_R = 50     #feed resistance
    start = [feed_pos, 0, 0]
    stop  = [feed_pos, 0, 1]
    port = FDTD.AddLumpedPort(1, feed_R, start, stop, 'z', 1.0, priority=5, edges2grid='xy')

    # Save the magnetic field data
    field = CSX.AddDump( 'H_field' , dump_type= 3, file_type = 1)
    field.AddBox([-SimBox[0]/2, -SimBox[1]/2, -SimBox[2]/3], [SimBox[0]/2, SimBox[1]/2, SimBox[2]*2/3])

    # WriteOpenEMS([Sim_Path '/' Sim_CSX], FDTD, CSX);
    # CSXGeomPlot([Sim_Path '/' Sim_CSX]);

    nf2ff = FDTD.CreateNF2FFBox()

    CSX_file = os.path.join(simulation_path, 'sim_3d_model.xml')
    if not os.path.exists(simulation_path):
        os.mkdir(simulation_path)
    CSX.Write2XML(CSX_file)
    from CSXCAD import AppCSXCAD_BIN
    os.system(AppCSXCAD_BIN + ' "{}"'.format(CSX_file))

    FDTD.Run(simulation_path,cleanup=False)


    
