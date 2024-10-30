import json

with open("tests/data/sample_wavelength_data.json", "r") as f:
    SAMPLE_WAVELENGTH_DATA = json.load(f)

SAMPLE_OPTICAL_DATA = {
    "number_incidence_angles": 1,
    "angle_blocks": [
        {
            "incidence_angle": 0,
            "num_wavelengths": 477,
            "wavelength_data": SAMPLE_WAVELENGTH_DATA
        }
    ]
}