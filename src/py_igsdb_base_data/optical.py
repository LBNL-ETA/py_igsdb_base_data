import typing
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from dataclasses_json import dataclass_json


class OpticalDataType(Enum):
    DISCRETE = "Discrete"
    BAND = "Band"


class AngularResolutionType(Enum):
    DIRECT = "Direct"
    DIFFUSE = "Diffuse"
    DIRECT_DIFFUSE = "Direct / Diffuse"
    BSDF = "BSDF"


INCIDENCE_ANGULAR_RESOLUTION_TYPES = [
    AngularResolutionType.DIRECT,
    AngularResolutionType.BSDF
]

OUTGOING_ANGULAR_RESOLUTION_TYPES = [
    AngularResolutionType.DIRECT,
    AngularResolutionType.BSDF
]


class AngularResolutionType(Enum):
    DIRECT = "Direct"
    DIRECT_DIFFUSE = "Direct / Diffuse"
    DIFFUSE_DIFFUSE = "Diffuse / Diffuse"
    BSDF = "BSDF"


@dataclass_json
@dataclass
class OpticalProperties:
    optical_data_type: str = OpticalDataType.DISCRETE.name
    incidence_angular_resolution_type: str = AngularResolutionType.DIRECT.name
    outgoing_angular_resolution_type: str = AngularResolutionType.DIRECT.name
    optical_data: Dict = field(default_factory=dict)


@dataclass
class WavelengthMeasurement:
    tf: Optional[float] = None
    tb: Optional[float] = None
    rf: Optional[float] = None
    rb: Optional[float] = None


@dataclass
class WavelengthMeasurementSet:
    w: float = 0
    specular: Optional[WavelengthMeasurement] = None
    diffuse: Optional[WavelengthMeasurement] = None


@dataclass
class AngleBlock:
    incidence_angle: int = 0
    num_wavelengths: int = 0

    # The shape of the dictionaries in this list is defined
    # above in WavelengthMeasurementSet.
    # However, casting to WavelengthMeasurementSet objects would be too
    # time intensive when we use the asdict() method. So for now we're
    # just leaving as a list of raw dictionaries.
    # wavelength_data: typing.List[WavelengthMeasurementSet] = field(default_factory=list)

    wavelength_data: typing.List[dict] = field(default_factory=list)


@dataclass
class OpticalData:
    number_incidence_angles: Optional[int] = None
    angle_blocks: typing.List[AngleBlock] = field(default_factory=list)


@dataclass
class OpticalProperties:
    optical_data_type: str = OpticalDataType.DISCRETE.name
    incidence_angular_resolution_type: str = AngularResolutionType.DIRECT.name
    outgoing_angular_resolution_type: str = AngularResolutionType.DIRECT.name
    optical_data: dict = None


@dataclass
class OpticalStandardMethodFluxResults:
    direct_direct: float = None  # "Specular" in CGDB ShadeMaterial
    direct_diffuse: float = None  # "Diffuse" in CGDB ShadeMaterial
    direct_hemispherical: float = None
    diffuse_diffuse: float = None
    matrix: typing.List[typing.List[float]] = None


@dataclass
class OpticalStandardMethodResults:
    transmittance_front: OpticalStandardMethodFluxResults = None
    transmittance_back: OpticalStandardMethodFluxResults = None
    reflectance_front: OpticalStandardMethodFluxResults = None
    reflectance_back: OpticalStandardMethodFluxResults = None
    absorptance_front_direct: float = None
    absorptance_back_direct: float = None
    absorptance_front_hemispheric: float = None
    absorptance_back_hemispheric: float = None
    error = None


@dataclass
class ThermalIRResults:
    transmittance_front_diffuse_diffuse: typing.Optional[float] = None
    transmittance_back_diffuse_diffuse: typing.Optional[float] = None
    absorptance_front_hemispheric: typing.Optional[float] = None
    absorptance_back_hemispheric: typing.Optional[float] = None

    error = None

    # Shortcut properties...

    @property
    def emissivity_front_hemispheric(self) -> typing.Optional[float]:
        if self.absorptance_front_hemispheric:
            return self.absorptance_front_hemispheric
        else:
            return None

    @property
    def emissivity_back_hemispheric(self) -> typing.Optional[float]:
        if self.absorptance_back_hemispheric:
            return self.absorptance_back_hemispheric
        else:
            return None

    @property
    def transmittance_front(self) -> typing.Optional[float]:
        if self.transmittance_front_diffuse_diffuse:
            return self.transmittance_front_diffuse_diffuse
        else:
            return None

    @property
    def transmittance_back(self) -> typing.Optional[float]:
        if self.transmittance_back_diffuse_diffuse:
            return self.transmittance_back_diffuse_diffuse
        else:
            return None


@dataclass
class TrichromaticResult:
    x: typing.Optional[float] = None
    y: typing.Optional[float] = None
    z: typing.Optional[float] = None


@dataclass
class LabResult:
    l: typing.Optional[float] = None
    a: typing.Optional[float] = None
    b: typing.Optional[float] = None


@dataclass
class RGBResult:
    r: typing.Optional[float] = None
    g: typing.Optional[float] = None
    b: typing.Optional[float] = None


@dataclass
class OpticalColorResult:
    trichromatic: typing.Optional[TrichromaticResult] = None
    lab: typing.Optional[LabResult] = None
    rgb: typing.Optional[RGBResult] = None


@dataclass
class OpticalColorFluxResults:
    direct_direct: typing.Optional[OpticalColorResult] = None
    direct_diffuse: typing.Optional[OpticalColorResult] = None
    direct_hemispherical: typing.Optional[OpticalColorResult] = None
    diffuse_diffuse: typing.Optional[OpticalColorResult] = None


@dataclass
class OpticalColorResults:
    transmittance_front: typing.Optional[OpticalColorFluxResults] = None
    transmittance_back: typing.Optional[OpticalColorFluxResults] = None
    reflectance_front: typing.Optional[OpticalColorFluxResults] = None
    reflectance_back: typing.Optional[OpticalColorFluxResults] = None
    error = None


class OpticalStandardMethodResultsFactory:

    @classmethod
    def create(cls) -> OpticalStandardMethodResults:
        """
        Create a fully initialized instance of OpticalStandardMethodResults
        """
        results = OpticalStandardMethodResults()
        results.transmittance_front = OpticalStandardMethodFluxResults()
        results.transmittance_back = OpticalStandardMethodFluxResults()
        results.reflectance_front = OpticalStandardMethodFluxResults()
        results.reflectance_back = OpticalStandardMethodFluxResults()
        return results


class OpticalColorResultFactory:

    @classmethod
    def create(cls) -> OpticalColorResult:
        result = OpticalColorResult()
        result.trichromatic = TrichromaticResult()
        result.rgb = RGBResult()
        result.lab = LabResult()
        return result


class OpticalColorResultsFactory:

    @classmethod
    def create(cls) -> OpticalColorResults:
        """
        Create a fully initialized instance of OpticalColorResult
        """
        results = OpticalColorResults()
        results.transmittance_front = OpticalColorFluxResultsFactory.create()
        results.transmittance_back = OpticalColorFluxResultsFactory.create()
        results.reflectance_front = OpticalColorFluxResultsFactory.create()
        results.reflectance_back = OpticalColorFluxResultsFactory.create()
        return results


class OpticalColorFluxResultsFactory:

    @classmethod
    def create(cls) -> OpticalColorFluxResults:
        """
        Create a fully initialized instance of OpticalColorResult
        """
        results = OpticalColorFluxResults()

        results.direct_direct = OpticalColorResultFactory.create()
        results.direct_diffuse = OpticalColorResultFactory.create()
        results.direct_hemispherical = OpticalColorResultFactory.create()
        results.diffuse_diffuse = OpticalColorResultFactory.create()

        return results


@dataclass_json
@dataclass
class IntegratedSpectralAveragesSummaryValues:

    solar: typing.Optional[OpticalStandardMethodResults] = None
    photopic: typing.Optional[OpticalStandardMethodResults] = None
    thermal_ir: typing.Optional[ThermalIRResults] = None
    tuv: typing.Optional[OpticalStandardMethodResults] = None
    spf: typing.Optional[OpticalStandardMethodResults] = None
    tdw: typing.Optional[OpticalStandardMethodResults] = None
    tkr: typing.Optional[OpticalStandardMethodResults] = None
    color: typing.Optional[OpticalColorResults] = None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Convenience getters
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @property
    def tf_sol(self):
        try:
            return self.solar.transmittance_front.direct_direct
        except AttributeError:
            return None

    @property
    def tf_sol_dir_dif(self):
        try:
            return self.solar.transmittance_front.direct_diffuse
        except AttributeError:
            return None

    @property
    def tf_sol_dir_hem(self):
        try:
            return self.solar.transmittance_front.direct_hemispherical
        except AttributeError:
            return None

    @property
    def tb_sol(self):
        try:
            return self.solar.transmittance_back.direct_direct
        except AttributeError:
            return None

    @property
    def tb_sol_dir_dif(self):
        try:
            return self.solar.transmittance_back.direct_diffuse
        except AttributeError:
            return None

    @property
    def tb_sol_dir_hem(self):
        try:
            return self.solar.transmittance_back.direct_hemispherical
        except AttributeError:
            return None

    @property
    def rf_sol(self):
        try:
            return self.solar.reflectance_front.direct_direct
        except AttributeError:
            return None

    @property
    def rf_sol_dir_dif(self):
        try:
            return self.solar.reflectance_front.direct_diffuse
        except AttributeError:
            return None

    @property
    def rf_sol_dir_hem(self):
        try:
            return self.solar.reflectance_front.direct_hemispherical
        except AttributeError:
            return None

    @property
    def rb_sol(self):
        try:
            return self.solar.reflectance_back.direct_direct
        except AttributeError:
            return None

    @property
    def rb_sol_dir_dif(self):
        try:
            return self.solar.reflectance_back.direct_diffuse
        except AttributeError:
            return None

    @property
    def rb_sol_dir_hem(self):
        try:
            return self.solar.reflectance_back.direct_hemispherical
        except AttributeError:
            return None

    @property
    def tf_vis(self):
        try:
            return self.photopic.transmittance_front.direct_direct
        except AttributeError:
            return None

    @property
    def tb_vis(self):
        try:
            return self.photopic.transmittance_back.direct_direct
        except AttributeError:
            return None

    @property
    def tb_vis_dir_dif(self):
        try:
            return self.photopic.transmittance_back.direct_diffuse
        except AttributeError:
            return None

    @property
    def tb_vis_dir_hem(self):
        try:
            return self.photopic.transmittance_back.direct_hemispherical
        except AttributeError:
            return None

    @property
    def rf_vis(self):
        try:
            return self.photopic.reflectance_front.direct_direct
        except AttributeError:
            return None

    @property
    def rf_vis_dir_dif(self):
        try:
            return self.photopic.reflectance_front.direct_diffuse
        except AttributeError:
            return None

    @property
    def rf_vis_dir_hem(self):
        try:
            return self.photopic.reflectance_front.direct_hemispherical
        except AttributeError:
            return None

    @property
    def rb_vis(self):
        try:
            return self.photopic.reflectance_back.direct_direct
        except AttributeError:
            return None

    @property
    def rb_vis_dir_dif(self):
        try:
            return self.photopic.reflectance_back.direct_diffuse
        except AttributeError:
            return None

    @property
    def rb_vis_dir_hem(self):
        try:
            return self.photopic.reflectance_back.direct_hemispherical
        except AttributeError:
            return None

    @property
    def tf_tuv(self):
        try:
            return self.tuv.reflectance_back.direct_direct
        except AttributeError:
            return None

    @property
    def tf_spf(self):
        try:
            return self.spf.reflectance_back.direct_direct
        except AttributeError:
            return None

    @property
    def tf_tdw(self):
        try:
            return self.tdw.reflectance_back.direct_direct
        except AttributeError:
            return None

    @property
    def tf_tkr(self):
        try:
            return self.tkr.reflectance_back.direct_direct
        except AttributeError:
            return None

    @property
    def tf_ciex(self):
        try:
            return self.color.transmittance_front.direct_direct.trichromatic.x
        except AttributeError:
            return None

    @property
    def tf_ciey(self):
        try:
            return self.color.transmittance_front.direct_direct.trichromatic.y
        except AttributeError:
            return None

    @property
    def tf_ciez(self):
        try:
            return self.color.transmittance_front.direct_direct.trichromatic.z
        except AttributeError:
            return None

    @property
    def rf_ciex(self):
        try:
            return self.color.reflectance_front.direct_direct.trichromatic.x
        except AttributeError:
            return None

    @property
    def rf_ciey(self):
        try:
            return self.color.reflectance_front.direct_direct.trichromatic.y
        except AttributeError:
            return None

    @property
    def rf_ciez(self):
        try:
            return self.color.reflectance_front.direct_direct.trichromatic.z
        except AttributeError:
            return None

    @property
    def rb_ciex(self):
        try:
            return self.color.reflectance_back.direct_direct.trichromatic.x
        except AttributeError:
            return None

    @property
    def rb_ciey(self):
        try:
            return self.color.reflectance_back.direct_direct.trichromatic.y
        except AttributeError:
            return None

    @property
    def rb_ciez(self):
        try:
            return self.color.reflectance_back.direct_direct.trichromatic.z
        except AttributeError:
            return None

    @property
    def tf_r(self):
        try:
            return self.color.transmittance_front.direct_direct.rgb.r
        except AttributeError:
            return None

    @property
    def tf_b(self):
        try:
            return self.color.transmittance_front.direct_direct.rgb.g
        except AttributeError:
            return None

    @property
    def tf_g(self):
        try:
            return self.color.transmittance_front.direct_direct.rgb.b
        except AttributeError:
            return None

    @property
    def rf_r(self):
        try:
            return self.color.reflectance_front.direct_direct.rgb.r
        except AttributeError:
            return None

    @property
    def rf_b(self):
        try:
            return self.color.reflectance_front.direct_direct.rgb.g
        except AttributeError:
            return None

    @property
    def rf_g(self):
        try:
            return self.color.reflectance_front.direct_direct.rgb.b
        except AttributeError:
            return None

    @property
    def rb_r(self):
        try:
            return self.color.reflectance_back.direct_direct.rgb.r
        except AttributeError:
            return None

    @property
    def rb_b(self):
        try:
            return self.color.reflectance_back.direct_direct.rgb.g
        except AttributeError:
            return None

    @property
    def rb_g(self):
        try:
            return self.color.reflectance_back.direct_direct.rgb.b
        except AttributeError:
            return None

    @property
    def tir_front(self) -> Optional[str]:
        """
        Returns the front TIR.

        Returns:

        """
        try:
            return self.thermal_ir.transmittance_front
        except AttributeError:
            return None

    @property
    def tir_back(self) -> Optional[str]:
        """
        Returns the back TIR.

        Returns:

        """
        try:
            return self.thermal_ir.transmittance_back
        except AttributeError:
            return None

    @property
    def emissivity_front(self) -> Optional[str]:
        """
        Returns the front emissivity.

        Returns:

        """
        try:
            return self.thermal_ir.emissivity_front_hemispheric
        except AttributeError:
            return None

    @property
    def emissivity_back(self) -> Optional[str]:
        """
        Returns the back emissivity.

        Returns:

        """
        try:
            return self.thermal_ir.emissivity_back_hemispheric
        except AttributeError:
            return None


class IntegratedSpectralAveragesSummaryValuesFactory:

    @classmethod
    def create(cls) -> IntegratedSpectralAveragesSummaryValues:
        """
        Create a fully initialized instance of IntegratedSpectralAveragesSummaryValues
        """

        summary = IntegratedSpectralAveragesSummaryValues()
        summary.solar = OpticalStandardMethodResultsFactory.create()
        summary.photopic = OpticalStandardMethodResultsFactory.create()
        summary.thermal_ir = ThermalIRResults()
        summary.tuv = OpticalStandardMethodResultsFactory.create()
        summary.spf = OpticalStandardMethodResultsFactory.create()
        summary.tdw = OpticalStandardMethodResultsFactory.create()
        summary.tkr = OpticalStandardMethodResultsFactory.create()
        summary.color = OpticalColorResultsFactory.create()
        return summary
