"""
Load Files and Output Open EMS Simulations
"""
import re

from matplotlib import pyplot as plt
import os

import numpy as np

LAYER_DIRECTIVE_LINE = r"^<<\s*(.*?)\s*>>$"
RECT_SHAPE_LINE = r"^rect\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)$"
USE_LINE = r"^use\s+(.*?)\s+(.*?)$"
FLABEL_LINE = r"^flabel\s+(\S+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(\S+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(\S+)$"

def load_mag_file(file_path):
    """
    Load a .mag file and return the data

    Parameters
    ----------
    file_path : str

    Returns
    -------
    data : dict
    """

    data = {}

    # Load the file
    with open(file_path, "r") as file:
        line_number = 1

        assert file.readline().strip() == "magic", "File does not start with 'magic'"
        line_number += 1

        technology_line = file.readline().strip().split(" ")
        assert technology_line[0] == "tech", "Second line does not start with 'tech'"
        line_number += 1

        current_layer = None
        # Read the rest of the lines
        for line in file:
            line = line.strip()

            if line == "": # Skip empty lines
                print(f"Skipping empty line {line_number}")
            elif "timestamp" in line:
                timestamp_line = line.split(" ")
                assert timestamp_line[0] == "timestamp", "Timestamp line does not start with 'timestamp'"
            elif "magscale" in line:
                magscale_line = line.split(" ")
                assert magscale_line[0] == "magscale", "Magscale line does not start with 'magscale'"

            elif re.match(LAYER_DIRECTIVE_LINE, line):
                technology_line = re.match(LAYER_DIRECTIVE_LINE, line).groups()
                current_layer = technology_line[0]

            elif re.match(RECT_SHAPE_LINE, line):
                rect_line = re.match(RECT_SHAPE_LINE, line).groups()
                assert current_layer is not None, "Rect line does not have a layer"

                if current_layer not in data:
                    data[current_layer] = []
                data[current_layer].append(rect_line)

            elif re.match(USE_LINE, line):

                use_line = re.match(USE_LINE, line).groups()
                line_group = []
                while True:
                    line = next(file).strip()
                    line_group.append(line)
                    if "box" in line:
                        break

                transform_line = None
                for line in line_group:
                    if line.startswith("transform"):
                        transform_line = line
                        break
                
                # Parse the transform line to get the six integers
                a, b, c, d, e, f = map(int, transform_line.split()[1:])

                # Create the transformation matrix
                transform_matrix = np.array([[a, d, 0], [b, e, 0], [c, f, 1]])


                subcelldata = load_mag_file(os.path.join(os.path.dirname(file_path), use_line[0] + ".mag"))
                for layer in subcelldata:
                    if layer not in data:
                        data[layer] = []
                    subcelldata_layer = subcelldata[layer]

                    for rectangle in subcelldata_layer:
                        # Extract the bottom-left and top-right corners
                        xbot, ybot, xtop, ytop = map(float, rectangle)

                        # Convert the points to 3x1 matrices (or vectors)
                        bot_vector = np.array([xbot, ybot, 1])
                        top_vector = np.array([xtop, ytop, 1])

                        # Multiply the transformation matrix with the point vectors
                        transformed_bot = np.dot(bot_vector, transform_matrix)
                        transformed_top = np.dot(top_vector, transform_matrix)

                        # Append the transformed rectangle to the data
                        data[layer].append((*transformed_bot[:2], *transformed_top[:2]))  # We only need the first two elements of each point
                
            elif re.match(FLABEL_LINE, line):
                flabel_line = re.match(FLABEL_LINE, line).groups()
                assert current_layer is not None, "Flabel line does not have a layer"

                port_line = next(file).strip().split(" ")
                assert port_line[0] == "port", "Port line does not start with 'port'"

                if current_layer not in data:
                    data[current_layer] = []
                
                # data[current_layer].append({ "flabel": flabel_line, "port": port_line })

            else:
                print("Line Not Implemented: ", line)
                # raise NotImplementedError(f"Line {line_number} is not implemented: {line}")
        
            line_number += 1
            

        return data


def draw_rects(data, layer, ax):
    """
    Draw the rectangles on the axis

    Parameters
    ----------
    data : dict
    layer : str
    ax : matplotlib.axes._subplots.AxesSubplot
    """
    rects = data[layer]
    x_values = []
    y_values = []
    for rect in rects:
        x1, y1, x2, y2 = rect
        x_values.extend([int(x1), int(x2)])
        y_values.extend([int(y1), int(y2)])
        ax.add_patch(plt.Rectangle((int(x1), int(y1)), int(x2) - int(x1), int(y2) - int(y1), edgecolor='black', facecolor='none'))
    
    ax.set_xlim(min(x_values), max(x_values))
    ax.set_ylim(min(y_values), max(y_values))


def get_bounds(data):
    """
    Get the bounds of the data

    Parameters
    ----------
    data : dict

    Returns
    -------
    bounds : tuple
    """
    x_values = []
    y_values = []
    for layer in data:
        rects = data[layer]
        for rect in rects:
            x1, y1, x2, y2 = rect
            x_values.extend([int(x1), int(x2)])
            y_values.extend([int(y1), int(y2)])
    
    return (min(x_values), max(x_values)), (min(y_values), max(y_values))

if __name__ == "__main__":
    file_path = "/workspaces/mag2openEMS/example/inverter.mag"
    data = load_mag_file(file_path)
    print("\n\n")

    draw_rects(data, "metal1", plt.gca())
    plt.savefig("inverter.png")
