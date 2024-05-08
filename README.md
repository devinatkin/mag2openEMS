# mag2openEMS
Python Script to Read Mag Files and then Write openEMS commands

loadmag.py will load mag files and produce a data file which can be rendered with PLT. (Some elements such as labels aren't yet being grabbed)

mag2ems is not yet loading the data over to produce simulations. It's producing an XML file but it won't load in paraview and simulations aren't yet running. The end goal will be to find the ports from the mag file and use those to act as stimulation points on the design. 