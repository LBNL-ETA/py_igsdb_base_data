from src.py_igsdb_optical_data.optical import OpticalStandardMethodResultsFactory, OpticalStandardMethodResults, \
    OpticalColorResultFactory, IntegratedSpectralAveragesSummaryValuesFactory, \
    IntegratedSpectralAveragesSummaryValues, OpticalColorResult


def test_integrated_spectral_averages_summary_factory():
    instance = IntegratedSpectralAveragesSummaryValuesFactory.create()
    assert isinstance(instance, IntegratedSpectralAveragesSummaryValues)
    assert instance.color.transmittance_front.direct_direct.trichromatic.x is None


def test_optical_standard_method_results_factory():
    instance = OpticalStandardMethodResultsFactory.create()
    assert isinstance(instance, OpticalStandardMethodResults)


def test_optical_color_result_factory():
    instance = OpticalColorResultFactory.create()
    assert isinstance(instance, OpticalColorResult)
