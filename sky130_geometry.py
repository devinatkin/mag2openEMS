# Original Code was written in Matlab by diadatp
# https://github.com/diadatp/sky130_rf_tools

from CSXCAD  import ContinuousStructure

materials = {
    'PI1': {'Epsilon': 2.94, 'z_min': 5.7488, 'z_max': 11.8834},
    'TOPNIT': {'Epsilon': 7.5, 'z_min': 5.3711, 'z_max': 5.7488},
    'NILD6': {'Epsilon': 4, 'z_min': 4.0211, 'z_max': 5.3711},
    'NILD5': {'Epsilon': 4.1, 'z_min': 2.7861, 'z_max': 4.0211},
    'NILD4': {'Epsilon': 4.2, 'z_min': 2.0061, 'z_max': 2.7861},
    'NILD3': {'Epsilon': 4.5, 'z_min': 1.3761, 'z_max': 2.0061},
    'NILD2': {'Epsilon': 4.05, 'z_min': 1.0111, 'z_max': 1.3761},
    'LINT': {'Epsilon': 7.3, 'z_min': 0.9361, 'z_max': 1.0111},
    'PSG': {'Epsilon': 3.9, 'z_min': 0.3262, 'z_max': 0.9361},
    'FOX': {'Epsilon': 3.9, 'z_min': 0.0, 'z_max': 0.3262},
    'substr': {'Kappa': 1.5e4, 'z_min': -1.0, 'z_max': 0.0},
    'poly': {'Kappa': 1.152605e+05},
    'licon': {'Kappa': 0.9361e-6 / (152 * 0.17e-6 * 0.17e-6)},
    'li': {'Kappa': 7.812500e+05},
    'mcon': {'Kappa': 0.34e-6 / (9.3 * 0.17e-6 * 0.17e-6)},
    'metal1': {'Kappa': 2.222222e+07},
    'via1': {'Kappa': 0.27e-6 / (4.5 * 0.15e-6 * 0.15e-6)},
    'metal2': {'Kappa': 2.222222e+07},
    'via2': {'Kappa': 0.42e-6 / (3.41 * 0.2e-6 * 0.2e-6)},
    'metal3': {'Kappa': 2.517940e+07},
    'via3': {'Kappa': 0.39e-6 / (3.41 * 0.2e-6 * 0.2e-6)},
    'metal4': {'Kappa': 2.517940e+07},
    'via4': {'Kappa': 0.505e-6 / (0.38 * 0.8e-6 * 0.8e-6)},
    'metal5': {'Kappa': 2.784740e+07}
}

def add_materials(CSX, x_min, x_max, y_min, y_max):
    """
    Add materials to the CSX object

    Parameters
    ----------
    CSX : ContinuousStructure
    materials : dict
    """
    print("Adding Materials")

    materials = {}
    for material_name, material_data in materials.items():
        
        eps = material_data.get('Epsilon', 0)
        kappa = material_data.get('Kappa', 0)
        material = CSX.AddMaterial(material_name, epsilon=eps, kappa=kappa)

        z_min = material_data.get('z_min', 0)
        z_max = material_data.get('z_max', 0)

        materials[material_name] = material

        if z_min == 0 and z_max == 0:
            continue
        start = [x_min, y_min, z_min]
        stop = [x_max, y_max, z_max]

        material.AddBox(start, stop)

    return materials