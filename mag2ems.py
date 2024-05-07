import numpy as np
from loadmag import load_mag_file, draw_rects, get_bounds
from matplotlib import pyplot as plt

from CSXCAD  import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import C0

from sky130_geometry import add_materials

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

    print(mesh.GetLines('x'))
    print(mesh.GetLines('y'))
    print(mesh.GetLines('z'))

    add_materials(CSX)

    # create ground (same size as substrate)
    gnd = CSX.AddMetal( 'gnd' ) # create a perfect electric conductor (PEC)
    start = [-SimBox[0]/2, -SimBox[1]/2, 0]
    stop  = [ SimBox[0]/2,  SimBox[1]/2, 0]
    gnd.AddBox(start, stop, priority=10)


    FDTD.AddEdges2Grid(dirs='xy', properties=gnd)


    # apply the excitation & resist as a current source
    
    #setup feeding
    feed_pos = -6 #feeding position in x-direction
    feed_R = 50     #feed resistance
    start = [feed_pos, 0, 0]
    stop  = [feed_pos, 0, 1]
    port = FDTD.AddLumpedPort(1, feed_R, start, stop, 'z', 1.0, priority=5, edges2grid='xy')


    FDTD.Run(simulation_path,verbose=3, cleanup=True)    
    
