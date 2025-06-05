import json
from unittest import TestCase

from py_igsdb_base_data.optical import (
    OpticalStandardMethodResultsFactory,
    OpticalStandardMethodResults,
    OpticalColorResultFactory,
    IntegratedSpectralAveragesSummaryValuesFactory,
    IntegratedSpectralAveragesSummaryValues,
    OpticalColorResult,
)


class TestPhysicalPropertiesDataclass(TestCase):
    def test_integrated_spectral_averages_summary_factory(self):
        instance = IntegratedSpectralAveragesSummaryValuesFactory.create()
        self.assertIsInstance(instance, IntegratedSpectralAveragesSummaryValues)

    def test_optical_standard_method_results_factory(self):
        instance = OpticalStandardMethodResultsFactory.create()
        self.assertIsInstance(instance, OpticalStandardMethodResults)

    def test_optical_color_result_factory(self):
        instance = OpticalColorResultFactory.create()
        self.assertIsInstance(instance, OpticalColorResult)

    def test_create_from_json(self):
        with open("tests/data/valid_summary_values.json", "r") as f:
            summary_dict = json.load(f)

        summary_values = IntegratedSpectralAveragesSummaryValues.from_dict(summary_dict)
        self.assertEqual(
            0.5165770985449425, summary_values.solar.reflectance_back.direct_direct
        )
