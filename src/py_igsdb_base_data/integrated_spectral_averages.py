from enum import Enum


# ENUMS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from py_igsdb_base_data.optical import AngularResolutionType


class DirectDiffuseType(Enum):
    DIRECT_DIRECT = "Direct - Direct"
    DIRECT_DIFFUSE = "Direct - Diffuse"
    DIFFUSE_DIFFUSE = "Diffuse - Diffuse"


class MeasurementType(Enum):
    MEASUREMENT_TYPE_TF = 'tf'  # implies dir-dir
    MEASUREMENT_TYPE_TB = 'tb'  # implies dir-dir
    MEASUREMENT_TYPE_RF = 'rf'  # implies dir-dir
    MEASUREMENT_TYPE_RB = 'rb'  # implies dir-dir

    MEASUREMENT_TYPE_TF_DIR_DIF = 'tf_dir_dif'
    MEASUREMENT_TYPE_TB_DIR_DIF = 'tb_dir_dif'
    MEASUREMENT_TYPE_RF_DIR_DIF = 'rf_dir_dif'
    MEASUREMENT_TYPE_RB_DIR_DIF = 'rb_dir_dif'

    MEASUREMENT_TYPE_TF_DIR_HEM = 'tf_dir_hem'
    MEASUREMENT_TYPE_TB_DIR_HEM = 'tb_dir_hem'
    MEASUREMENT_TYPE_RF_DIR_HEM = 'rf_dir_hem'
    MEASUREMENT_TYPE_RB_DIR_HEM = 'rb_dir_hem'

    @staticmethod
    def get_types(include_tb: bool = True):
        if include_tb:
            return [item.value for item in MeasurementType]
        else:
            return [item.value for item in MeasurementType if "_TB_" not in item.name]

    @staticmethod
    def specular_types():
        return [
            MeasurementType.MEASUREMENT_TYPE_TF.value,
            MeasurementType.MEASUREMENT_TYPE_TB.value,
            MeasurementType.MEASUREMENT_TYPE_RF.value,
            MeasurementType.MEASUREMENT_TYPE_RB.value,
        ]


class ReflectionType(Enum):
    """
    We group measurements for any given
    wavelength by these types, e.g. specular.tf.
    """
    SPECULAR = "specular"
    DIFFUSE = "diffuse"


class TransmittanceReflectanceChoice(Enum):
    TRANSMITTANCE_FRONT = "Transmittance front"
    TRANSMITTANCE_BACK = "Transmittance back"
    REFLECTANCE_FRONT = "Reflectance front"
    REFLECTANCE_BACK = "Reflectance back"


class WavelengthMeasurementType(Enum):
    """
    The strings used in Wavelength objects
    to denote measurements.
    """
    TRANSMITTANCE_FRONT = "tf"
    REFLECTANCE_FRONT = "rf"
    REFLECTANCE_BACK = "rb"
    # TODO: tb not used?
    TRANSMITTANCE_BACK = "tb"


class IntegratedSummaryValuesDataSource(Enum):
    IGDB = "IGDB"
    CGDB = "CGDB"
    PYWINCALC = "Pywincalc"
    # Optical uses pywincalc, but we still distinguish between two.
    OPTICALC = "Opticalc"


# CONSTANTS and lookups
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


INCIDENCE_ANGULAR_RESOLUTION_TYPES = [
    AngularResolutionType.DIRECT,
    AngularResolutionType.BSDF
]

OUTGOING_ANGULAR_RESOLUTION_TYPES = [
    AngularResolutionType.DIRECT,
    AngularResolutionType.BSDF
]
