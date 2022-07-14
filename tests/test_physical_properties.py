from unittest import TestCase

from py_igsdb_base_data.product import PhysicalProperties


class TestPhysicalPropertiesDataclass(TestCase):

    def test_physical_properties_dataclass_library(self):
        p = PhysicalProperties()
        # should automatically create optical properties
        self.assertIsNotNone(p.optical_properties)
        self.assertIsNotNone(p.optical_properties.optical_data_type)
