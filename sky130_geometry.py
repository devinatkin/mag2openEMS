# Original Code was written in Matlab by diadatp
# https://github.com/diadatp/sky130_rf_tools

from CSXCAD  import ContinuousStructure

materials = {
    'PI1': {'Epsilon': 2.94},
    'TOPNIT': {'Epsilon': 7.5},
    'NILD6': {'Epsilon': 4},
    'NILD5': {'Epsilon': 4.1},
    'NILD4': {'Epsilon': 4.2},
    'NILD3': {'Epsilon': 4.5},
    'NILD2': {'Epsilon': 4.05},
    'LINT': {'Epsilon': 7.3},
    'PSG': {'Epsilon': 3.9},
    'FOX': {'Epsilon': 3.9},
    'substr': {'Kappa': 1.5e4},
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

def add_materials(CSX):
    """
    Add materials to the CSX object

    Parameters
    ----------
    CSX : ContinuousStructure
    materials : dict
    """
    print("Adding Materials")
    for material_name, material_data in materials.items():
        
        eps = material_data.get('Epsilon', 0)
        kappa = material_data.get('Kappa', 0)
        CSX.AddMaterial(material_name, epsilon=eps, kappa=kappa)