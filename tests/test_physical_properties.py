from unittest import TestCase

from py_igsdb_base_data.product import PhysicalProperties

from src.py_igsdb_base_data.product import BlindGeometry


class TestPhysicalPropertiesDataclass(TestCase):

    def test_physical_properties_dataclass_library(self):
        p = PhysicalProperties()
        # should automatically create optical properties
        self.assertIsNotNone(p.optical_properties)
        self.assertIsNotNone(p.optical_properties.optical_data_type)

    def test_venetian_blind_get_rise_when_curvature_defined(self):
        p = BlindGeometry()
        p.slat_width = "16"
        p.slat_curvature = "1"
        rise = p.rise # calls getter
        self.assertEqual(rise, "8.0") 