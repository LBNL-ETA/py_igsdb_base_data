import logging
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from math import sqrt
from typing import List, Dict
from typing import Optional

from dataclasses_json import dataclass_json

from py_igsdb_base_data.material import MaterialBulkProperties
from py_igsdb_base_data.optical import IntegratedSpectralAveragesSummaryValues
from py_igsdb_base_data.optical import OpticalProperties

logger = logging.getLogger(__name__)


# ENUMS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Remember that ...
# SPD = Submitted Product Document, the format for
# describing a product being submitted to the IGSDB via the Checkertool
# APD = Accepted Product Document, a product that has been accepted to and published in
# the IGSDB


class TokenType(Enum):
    # PUBLISHED means the product has been added to the IGSDB
    # and has been marked PUBLISHED
    PUBLISHED = "published"

    # UNDEFINED means no token has been provided
    # (and might not even be applicable)
    UNDEFINED = "undefined"

    # PROPOSED means the token is part of a new submission
    # to the IGSDB and therefore is "proposed" as a new token.
    # We say proposed because there may be some reason it never
    # gets into the IGSDB and becomes a PUBLISHED token.
    PROPOSED = "proposed"

    # INTRAGROUP only applies to child products and therefore only
    # appears in the product composition.
    # It means the child product defined in the product composition
    # exists as a separate submission in the *SAME* submission group.
    INTRAGROUP = "intragroup"

    # INTERGROUP only applies to child products and therefore only
    # appears in the product composition.
    # It means the child product defined in the product composition
    # exists as a separate submission in a *DIFFERENT* submission group.
    INTERGROUP = "intergroup"

    def igsdb_types(self) -> List[str]:
        # These types can appear in the IGSDB
        return [TokenType.PUBLISHED.name, TokenType.UNDEFINED.name]


class ProductType(Enum):
    GLAZING = "glazing"
    SHADING = "shading"
    MATERIAL = "material"


class ProductSubtype(Enum):
    # GLAZING Subtypes
    # ----------------------------------------
    MONOLITHIC = "Monolithic"
    LAMINATE = "Laminate"
    INTERLAYER = "Interlayer"
    EMBEDDED_COATING = "Embedded coating"
    COATED = "Coated glass"
    COATING = "Coating"
    APPLIED_FILM = "Applied film"
    FILM = "Film"

    # HYBRID GLAZING / SHADING Subtypes
    # ----------------------------------------
    FRITTED_GLASS = "Fritted glass"
    SANDBLASTED_GLASS = "Sandblasted glass"
    ACID_ETCHED_GLASS = "Acid etched glass"
    CHROMOGENIC = "Chromogenic"

    # SHADING Subtypes
    # ----------------------------------------

    # These have a geometry associated with them:
    VENETIAN_BLIND = "Venetian blind"
    VERTICAL_LOUVER = "Vertical louver"
    PERFORATED_SCREEN = "Perforated screen"
    WOVEN_SHADE = "Woven shade"

    # These must have a BSDF associated:
    ROLLER_SHADE = "Roller shade"

    # These must have a GEN_BSDF file attached
    # (and may have a THMX -- a precursor to GEN_BSDF -- file attached):
    CELLULAR_SHADE = "Cellular shade"
    PLEATED_SHADE = "Pleated Shade"
    ROMAN_SHADE = "Roman shade"

    # TODO: What qualities do these have?
    DIFFUSING_SHADE = "Diffusing shade"
    SOLAR_SCREEN = "Solar screen"

    # Shading materials:
    SHADE_MATERIAL = "Shade material"

    # other
    UNKNOWN = "Unknown"


class CoatedSideType(Enum):
    MULTIPLE = (
        "multiple"  # embedded and either 1) front or back or 2) both front and back.
    )
    FRONT = "front"
    BACK = "back"
    BOTH = "both"  # both front and back
    EMBEDDED = "embedded"  # embedded coating, usually in a LAMINATE product.
    NEITHER = "neither"  # neither front nor back
    UNKNOWN = "unknown"
    # "NA" Was used in legacy submission files. In IGSDB and Checkertool v2
    # we use the more descriptive "NOT_APPLICABLE" instead.
    #NA = "not applicable"
    NOT_APPLICABLE = "not applicable"


class DataFileType(Enum):
    """
    The original data file that was used to
    submit a product to Checkertool / IGSDB.
    """

    IGDB_LEGACY_SUBMISSION_FILE = "IGDB_LEGACY_SUBMISSION_FILE"
    CGDB_LEGACY_SUBMISSION_FILE = "CGDB_LEGACY_SUBMISSION_FILE"
    SPD = "SPD"
    SPREADSHEET = "SPREADSHEET"
    OTHER = "OTHER"

    # These are 'legacy' file types that were used
    # in the old IGDB database to describe shading types
    # like rollershade and roman/pleated/cellular shades.
    BSDF_XML = "BSDF XML"
    THERM = "THERM"


# CONSTANTS and lookups
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


GLAZING_SUBTYPES = [
    ProductSubtype.MONOLITHIC,
    ProductSubtype.LAMINATE,
    ProductSubtype.INTERLAYER,
    ProductSubtype.EMBEDDED_COATING,
    ProductSubtype.COATED,
    ProductSubtype.COATING,
    ProductSubtype.APPLIED_FILM,
    ProductSubtype.FILM,
]

GLAZING_SUBTYPE_NAMES = [item.name for item in GLAZING_SUBTYPES]

SHADING_SUBTYPES = [
    # 'ShadingLayer' subtypes...
    ProductSubtype.VENETIAN_BLIND,
    ProductSubtype.DIFFUSING_SHADE,
    ProductSubtype.ROLLER_SHADE,
    ProductSubtype.WOVEN_SHADE,
    ProductSubtype.VERTICAL_LOUVER,
    ProductSubtype.PERFORATED_SCREEN,
    ProductSubtype.CELLULAR_SHADE,
    ProductSubtype.PLEATED_SHADE,
    ProductSubtype.ROMAN_SHADE,
    # 'ShadeMaterial' subtypes
    ProductSubtype.SHADE_MATERIAL,
    # Diffusing hybrids
    ProductSubtype.FRITTED_GLASS,
    ProductSubtype.ACID_ETCHED_GLASS,
    ProductSubtype.SANDBLASTED_GLASS,
    ProductSubtype.CHROMOGENIC,
]

# Subset of shading subtypes.
# These will have a composition layer.
SHADING_LAYER_SUBTYPES = [
    ProductSubtype.VENETIAN_BLIND,
    ProductSubtype.DIFFUSING_SHADE,
    ProductSubtype.ROLLER_SHADE,
    ProductSubtype.WOVEN_SHADE,
    ProductSubtype.VERTICAL_LOUVER,
    ProductSubtype.PERFORATED_SCREEN,
    ProductSubtype.CELLULAR_SHADE,
    ProductSubtype.PLEATED_SHADE,
    ProductSubtype.ROMAN_SHADE,
]

"""
Historical Note: 
In the old CGDB database:

Subtype             CGDB Type
VENETIAN_BLIND      0
DIFFUSING_SHADE     1
ROLLER_SHADE        2
WOVEN_SHADE         3
FRITTED_GLASS       4
VERTICAL_LOUVER     5
PERFORATED_SCREEN   6
CELLULAR_SHADE      7
PLEATED_SHADE       7
ROMAN_SHADE         7


Note: Legacy CGDB mdb database had no way of determining if
type 7 was cellular, pleated or roman. So when porting
CGDB to IGSDB, when we see 7 we assume CELLULAR_SHADE, unless 
'pleated' or 'roman' is in the product name (per team decision).
"""

SHADING_SUBTYPE_NAMES = [item.name for item in SHADING_SUBTYPES]


@dataclass_json
@dataclass
class Manufacturer:
    id: int = None
    name: str = None
    extension: str = None


@dataclass_json
@dataclass
class ProductDescription:
    name: Optional[str] = None
    short_description: Optional[str] = None
    marketing_name: Optional[str] = None
    manufacturer_by_marketing_name: Optional[str] = None
    marketing_url: Optional[str] = None
    marketing_text: Optional[str] = None
    marketing_appearance: Optional[str] = None


@dataclass_json
@dataclass
class BaseGeometry:
    pass


@dataclass_json
@dataclass
class GeometricProperties:
    geometry: Optional[BaseGeometry] = None


@dataclass_json
@dataclass
class PhysicalProperties:
    thickness: Optional[Decimal] = None
    permeability_factor: Optional[Decimal] = None
    optical_openness: Optional[Decimal] = None
    bulk_properties_override: Dict = field(default_factory=dict)
    is_specular: bool = True
    optical_properties: Optional[OpticalProperties] = None
    # The predefined_ fields correspond to user defined
    # 'Emissivity' and 'TIR values provided in submission files.
    # If present, this information has use in Checkertool but is
    # ignored by the IGSDB when products are built from IGDB or
    # submitted by Checkertool.
    # These are stored as Decimal values to capture the *exact* value
    # provided in the submission file.
    predefined_tir_front: Optional[Decimal] = None
    predefined_tir_back: Optional[Decimal] = None
    predefined_emissivity_front: Optional[Decimal] = None
    predefined_emissivity_back: Optional[Decimal] = None

    # Geometric properties of product. (Currently only used by
    # shading products. In the CGDB -> ISDB migration, holds values
    # defined in CGDB tables WovenShades, VenetianBlinds and PerforatedScreens.)
    geometric_properties: Optional[GeometricProperties] = None

    def __post_init__(self):
        if self.optical_properties is None:
            self.optical_properties = OpticalProperties()


@dataclass_json
@dataclass
class BlindGeometry(BaseGeometry):
    """
    Geometry definition for ven blinds.

    IMPORTANT: To maintain exact precision,
    all values are stored as strings.

    """

    _rise: Optional[str] = None

    # Units: mm
    slat_width: Optional[Decimal] = None

    # Units: mm
    slat_spacing: Optional[Decimal] = None

    # Units: mm
    slat_curvature: Optional[Decimal] = None

    # Units: degrees
    slat_tilt: Optional[Decimal] = None

    # Segments are used to represent curvature
    # (Defaults to 5)
    n_segments: Optional[int] = 5

    # Value can be an integer or string like "CUSTOM"
    # so declaring this field as str.
    tilt_choice: Optional[str] = None

    @property
    def rise(self) -> Optional[Decimal]:
        if not self._rise and self.slat_curvature:
            self.set_rise_from_curvature()
        return self._rise

    def set_rise_from_curvature(self) -> Decimal:
        """
        Calculate rise in mm from curvature in mm, using Decimal arithmetic.
        """
        if self.slat_curvature is None:
            raise ValueError("Slat curvature must be defined before calling this method.")

        # If curvature is zero or negative, rise is zero.
        if self.slat_curvature <= Decimal(0):
            self._rise = Decimal(0)
            return self._rise

        if self.slat_width is None:
            raise ValueError("Slat width must be defined to calculate rise from curvature.")

        curvature = self.slat_curvature
        slat_width = self.slat_width

        val = (curvature * curvature) - (slat_width * slat_width / Decimal(4))

        if val < Decimal(0):
            rise = slat_width / Decimal(2)
        else:
            r_prime = val.sqrt()
            rise = curvature - r_prime

        self._rise = rise
        return self._rise

    def set_curvature_from_rise(self) -> Decimal:
        """
        Calculate curvature in mm from rise in mm, using Decimal arithmetic.
        """
        if self._rise is None:
            raise ValueError("Rise must be defined before calling this method.")

        # If rise is zero or negative, curvature is zero.
        if self._rise <= Decimal(0):
            self.slat_curvature = Decimal(0)
            return self.slat_curvature

        rise = self._rise

        if self.slat_width is None:
            raise ValueError("Slat width must be defined to calculate curvature from rise.")

        slat_width = self.slat_width
        max_rise = slat_width / Decimal(2)
        if rise > max_rise:
            raise ValueError(f"Rise must be ≤ {max_rise} (slat_width/2).")

        # val = (rise^2 + slat_width^2/4) / (2*rise)
        numerator = (rise * rise) + (slat_width * slat_width / Decimal(4))
        denominator = rise * Decimal(2)
        val = numerator / denominator

        if val < Decimal(0):
            curvature = slat_width / Decimal(2)
        else:
            curvature = val

        self.slat_curvature = curvature
        return self.slat_curvature


@dataclass_json
@dataclass
class VenetianBlindGeometry(BlindGeometry):
    pass


@dataclass_json
@dataclass
class VerticalLouverGeometry(BlindGeometry):
    pass


class PerforatedScreenGeometryType(Enum):
    CIRCULAR = "0"
    SQUARE = "1"
    RECTANGULAR = "2"


@dataclass_json
@dataclass
class PerforatedScreenGeometry(BaseGeometry):
    """
    Defines the geometric properties of a Perforated screen.
    Type indicates shape of perforations:
    0 : circular
    1 : square
    2 : rectangular
    """

    type: Optional[str] = None

    # dim_x is "radius" when type = 3
    dim_x: Optional[Decimal] = None
    # dim_y is not used when type = 1 or 3
    dim_y: Optional[Decimal] = None

    spacing_x: Optional[Decimal] = None
    spacing_y: Optional[Decimal] = None

    @property
    def diameter(self) -> Optional[Decimal]:
        if self.type == PerforatedScreenGeometryType.CIRCULAR.value:
            return self.dim_x
        return None


@dataclass_json
@dataclass
class WovenShadeGeometry(BaseGeometry):
    thread_diameter: Optional[Decimal] = None
    thread_spacing: Optional[Decimal] = None
    shade_thickness: Optional[Decimal] = None


@dataclass_json
@dataclass
class InterlayerDetails:
    interlayer_id: Optional[int] = None
    interlayer_appearance: Optional[str] = None
    interlayer_product_name: Optional[str] = None
    interlayer_code: Optional[str] = None
    interlayer_nominal_thickness: Optional[Decimal] = None
    interlayer_material: Optional[str] = None


@dataclass_json
@dataclass
class IntegratedSpectralAveragesSummary:
    summary_values: Optional[IntegratedSpectralAveragesSummaryValues] = None
    calculation_standard: Optional[str] = None
    source: Optional[str] = None
    # source_version helps us track changes to standards
    # if they version over time, e.g. pywincalc versions.
    source_version: Optional[str] = None


@dataclass_json
@dataclass
class CompositionDetails:
    """
    Some composition layers have a composition_details dictionary
    that may...
    1.  store layer-specific that cannot be genericized and stored in
        the child product model, e.g. layer thickness.
    2.  store information from IGDB that doesn't directly translate

    """

    # used for laminate layers
    flipped: Optional[bool] = None
    thickness: Optional[Decimal] = None

    # Used during IGDB port
    layer_filename: Optional[str] = None
    substrate_data_file_name: Optional[str] = None
    coating_id: Optional[int] = None
    coating_name: Optional[str] = None

    # coated_side_faces_exterior is a convenience property.
    # Sometimes we might not have access to the child product's
    # coated_side property, which we would need to decide if the coating
    # faces external side. For example, a LAMINATE product where the COATED
    # child product is UNKNOWN.
    #
    # So this property can be set to describe which side the coated side is on.
    coated_side_faces_exterior: Optional[bool] = None


@dataclass_json
@dataclass
class NewProductDefinition:
    """
    A simpler version of the Product dataclass, meant for
    embedding in a parent product's composition when the submitter
    is creating a new dependent product as part of a parent product submission.

    This is really only applicable to the creation of dependent products as part
    of a submission.

    For example, a COATED submission might create a dependent COATING product
    as part of the submission. This dataclass describes that COATING in the
    new_product_definition property of the composition layer.

    """

    id: Optional[int] = None
    type: Optional[str] = None
    subtype: Optional[str] = None
    token: Optional[str] = None

    material: Optional[str] = None
    appearance: Optional[str] = None
    token_type: Optional[str] = None
    owner: Optional[str] = None
    manufacturer: Optional[str] = None
    hidden: Optional[bool] = None

    product_description: Optional[ProductDescription] = None
    physical_properties: Optional[PhysicalProperties] = None

    # For interlayers
    code: Optional[str] = None

    # IGDB parsing
    # TODO: Don't think I need legacy_filename since
    # TODO: it is stored in the ProductComposition dataclass.
    # legacy_filename: Optional[str] = None


@dataclass_json
@dataclass
class ProductComposition:
    """
    A simple dataclass to represent composition layers in a Product.
    """

    type: Optional[str] = None
    subtype: Optional[str] = None
    token_type: Optional[str] = None
    token: Optional[str] = None
    index: Optional[int] = None
    name: Optional[str] = None
    thickness: Optional[Decimal] = None
    composition_details: Optional[CompositionDetails] = None
    new_product_definition: Optional[NewProductDefinition] = None

    # Hold on to legacy data if we want...
    legacy_filename: str = None

    # Fields for carrying over IGDB information
    # when loading from IGDB .mdb
    igdb_layer_filename: Optional[str] = None
    igdb_layer_glazing_id: Optional[int] = None


@dataclass_json
@dataclass
class ShadeLayerProperties:
    """
    Holds ShadingLayer properties from CGDB
    during CGDB -> IGSDB migration.
    """

    shade_material_id: Optional[int] = None
    hole_area: Optional[Decimal] = None  # Float in CGDB, max six decimal places.
    bsdf_path: Optional[str] = None
    convection_factor: Optional[Decimal] = None  # Float in CGDB, max 1 decimal place.
    timestamp: Optional[int] = None


@dataclass_json
@dataclass
class IGSDBObject:
    token: Optional[str] = None
    uuid: Optional[str] = None


# NOTE: It's difficult to do getters/setters on a dataclass and handle init correctly
# Settled on this approach: https://github.com/florimondmanca/www/issues/102#issuecomment-733947821


@dataclass_json
@dataclass
class BaseProduct(IGSDBObject):
    type: Optional[str] = None
    subtype: Optional[str] = None
    token_type: Optional[str] = None

    units_system: str = "SI"  # or IP
    id: Optional[int] = None

    product_id: Optional[int] = None
    data_file_name: Optional[str] = None
    data_file_type: Optional[str] = None

    # This product can be decomposed into parts
    # None indicates this property has not yet been determined.
    deconstructable: Optional[bool] = None

    # This product is a 'reference' product, meaning it's sole purpose is
    # to get a child product into the IGSDB using reference substrates.
    # This is method of submittal is  only valid for APPLIED_FILM and LAMINATE products.
    reference: bool = False

    # The official version of this product.
    # The version is incremented each time the product is updated in the IFGSDB.
    version: int = 1

    # The version of the IGSDB database.
    # (a superset of IGDB versions, e.g. 80, 81, etc).
    igsdb_version: Optional[Decimal] = None

    coated_side: Optional[str] = None
    coating_name: Optional[str] = None

    # For legacy IGDB products:
    # If this is a FILM or COATING, this
    # value comes from the CoatingID column in the Coatings table
    # Otherwise, it comes from the GlazingID column in the GlazingProperties table.
    igdb_id: Optional[int] = None
    igdb_database_version: Optional[Decimal] = None

    # If this is a legacy IGDB or CGDB product,
    # this value comes from the Time_Created column in the GlazingProperties table.
    mdb_time_created: Optional[str] = None

    # For legacy CGDB shading products
    cgdb_id: Optional[int] = None
    cgdb_database_version: Optional[Decimal] = None

    # Abstract shade properties during CGDB -> IGSDB Migration.
    shade_properties: Optional[ShadeLayerProperties] = None

    owner: Optional[str] = None
    manufacturer: Optional[str] = None
    material: Optional[str] = None
    product_description: ProductDescription = None
    publish_status: Optional[str] = None
    published_date: Optional[str] = None
    hidden: bool = False
    appearance: Optional[str] = None
    acceptance: Optional[str] = None
    nfrc_id: Optional[int] = None
    igdb_checksum: Optional[str] = None
    cgdb_checksum: Optional[str] = None
    checksum_date: Optional[datetime] = None
    material_bulk_properties: Optional[MaterialBulkProperties] = None

    # Composition is a list of dictionaries holding
    # information about each composition layer. This information
    # will be transformed into ProductComposition entries in Checkertool
    composition: List[ProductComposition] = field(default_factory=list)

    # Integrated spectral averages summaries are usually generated by Checkertool.
    # We initialize this field to an empty list.
    integrated_spectral_averages_summaries: List[IntegratedSpectralAveragesSummary] = (
        field(default_factory=list)
    )

    # The extra_data field is a catch-all for data that does not fit
    # into standard dataclasses. Right now that's just one field: interlayer_nominal_thickness
    extra_data: Dict = field(default_factory=dict)

    # When rendered to json, the physical_properties should always be
    # last of 'official' IGSDB values so that in json output, the (really long)
    # spectral_data is at the bottom of the page. This helps developers debug.
    physical_properties: Optional[PhysicalProperties] = None

    # LEGACY IGDB VALUES. IGNORED BY IGSDB!
    # Properties we store as part of this library to help us
    # manage relationships. They're not a part of the new IGSDB
    # world, but rather IGDB artifacts. These properties will be
    # ignored by the IGSDB serializer.
    coating_id: Optional[int] = None  # The CoatingID from the Coatings table

    # The GlazingID from the GlazingProperties table
    # NOTE: Shading materials may have this set because the CGDB
    # database links ShadeMaterial to spectral data via the GlazingProperties database.
    glazing_id: Optional[int] = None

    substrate_filename: Optional[str] = (
        None  # The Substrate_Filename from the GlazingProperties table
    )
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    structure_line: Optional[str] = None  # Hold on to the original structure line
    interlayer_details: Optional[InterlayerDetails] = (
        None  # Keep interlayer information for building composition
    )

    # IGSDB fields
    # The IGSDB stores the submitted product in a related model
    # We may need that information when processing 'published' products...
    # if so store it here.
    product_json: Dict = field(default_factory=dict)

    # GETTERS and SETTERS
    def get_type(self) -> str:
        return self._type

    def set_type(self, v: str) -> None:
        if v is not None:
            try:
                ProductType[v]
            except KeyError:
                raise ValueError(f"Invalid product type: {v}")
        self._type = v

    def get_subtype(self) -> str:
        return self._subtype

    def set_subtype(self, v: str) -> None:
        if v is not None:
            try:
                ProductSubtype[v]
            except KeyError:
                raise ValueError(f"Invalid product subtype: {v}")
        self._subtype = v

    def get_token_type(self) -> Optional[str]:
        return self._token_type

    def set_token_type(self, v: str) -> None:
        if v is not None:
            try:
                TokenType[v]
            except KeyError:
                raise ValueError(f"Invalid product token type: {v}")
        self._token_type = v

    @property
    def igdb_time_created(self) -> Optional[datetime]:
        if self.type == ProductType.GLAZING.name and self.mdb_time_created:
            return datetime.strptime(self.mdb_time_created, "%Y-%m-%d %H:%M:%S")
        return None

    @property
    def cgdb_time_created(self) -> Optional[datetime]:
        if self.type == ProductType.GLAZING.name and self.mdb_time_created:
            return datetime.strptime(self.mdb_time_created, "%Y-%m-%d %H:%M:%S")
        return None

    @property
    def name(self) -> Optional[str]:
        if self.product_description:
            return self.product_description.name
        return None

    @property
    def marketing_name(self) -> Optional[str]:
        if self.product_description:
            return self.product_description.marketing_name
        return None

    @marketing_name.setter
    def marketing_name(self, v: str) -> None:
        if self.product_description:
            self.product_description.marketing_name = v
        else:
            self.product_description = ProductDescription(marketing_name=v)

    @name.setter
    def name(self, v: str) -> None:
        if self.product_description:
            self.product_description.name = v
        else:
            self.product_description = ProductDescription(name=v)

    @property
    def has_thermal_ir_wavelengths(self) -> bool:
        """
        Returns True if the product has thermal IR wavelength data.

        Returns:
            bool
        """
        if not self.physical_properties:
            return False
        if not self.physical_properties.optical_properties:
            return False
        return self.physical_properties.optical_properties.has_thermal_ir_wavelengths

    # GETTERS for TIR and Emissivity

    def get_tir_front(self, calculation_standard_name: str = "NFRC") -> Optional[Decimal|float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    try:
                        value = summary.summary_values.thermal_ir.transmittance_front
                        if value is not None:
                            return value
                    except Exception:
                        # not defined
                        pass
        # If we don't have a calculated value, return a 'user defined' value, if any.
        if self.physical_properties:
            return self.physical_properties.predefined_tir_front

        return None

    def get_tir_back(self, calculation_standard_name: str = "NFRC") -> Optional[Decimal|float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    try:
                        value = summary.summary_values.thermal_ir.transmittance_back
                        if value is not None:
                            return value
                    except Exception:
                        # not defined
                        pass
        # If we don't have a calculated value, return a 'user defined' value, if any.
        if self.physical_properties:
            return self.physical_properties.predefined_tir_back

        return None

    def get_emissivity_front(
        self, calculation_standard_name: str = "NFRC"
    ) -> Optional[Decimal|float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    try:
                        value = summary.summary_values.thermal_ir.emissivity_front_hemispheric
                        if value is not None:
                            return value
                    except Exception:
                        # not defined
                        pass
        # If we don't have a calculated value, return a 'user defined' value, if any.
        if self.physical_properties:
            return self.physical_properties.predefined_emissivity_front

        return None

    def get_emissivity_back(
        self, calculation_standard_name: str = "NFRC"
    ) -> Optional[Decimal|float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    try:
                        value = summary.summary_values.thermal_ir.emissivity_back_hemispheric
                        if value is not None:
                            return value
                    except Exception:
                        # not defined
                        pass
        # If we don't have a calculated value, return a 'user defined' value, if any.
        if self.physical_properties:
            return self.physical_properties.predefined_emissivity_back

        return None

    @property
    def can_have_predefined_thermal_values(self) -> bool:
        """
        Historically, in the IGDB only MONOLITHIC or uncoated LAMINATE products
        were allowed to have TIR and Emissivity set in the header of a submission file.
        These values were stored in the IGDB database.

        Factoid: The old checkertool had also stored an entry in the Ef_Source
        and Eb_Source with a "TEXT FILE" string indicating the
        value had come from a header line in the submission file.

        This property encapsulates a check for this condition.

        Returns:
        Boolean value, true if product can have predefined values defined for emissivity or TIR.
        """
        if self.subtype not in [
            ProductSubtype.MONOLITHIC.name,
            ProductSubtype.LAMINATE.name,
        ]:
            # only MONOLITHIC and uncoated LAMINATE can have predefined thermal values
            return False
        if self.subtype == ProductSubtype.LAMINATE.name:
            if self.has_coating_on_surface:
                # only an uncoated LAMINATE can have predefined thermal values
                return False
        return True

    @property
    def has_coating_on_surface(self) -> bool:
        """
        This property is only for LAMINATE products.
        Indicates whether a substrate layer is a COATED product and that
        product's coating is on the surface of the product.

        Returns:
        Boolean indicating whether product has a COATING on an outward facing
        surface.
        """
        if self.subtype != ProductSubtype.LAMINATE.name:
            return False
        if self.composition:
            for layer_index, composition_layer in enumerate(self.composition):
                if composition_layer.subtype == ProductSubtype.COATED.name:
                    composition_details: CompositionDetails = (
                        composition_layer.composition_details
                    )
                    if (
                        composition_details
                        and composition_details.coated_side_faces_exterior
                    ):
                        return composition_details.coated_side_faces_exterior
        return False


BaseProduct.type = property(BaseProduct.get_type, BaseProduct.set_type)
BaseProduct.subtype = property(BaseProduct.get_subtype, BaseProduct.set_subtype)
BaseProduct.token_type = property(
    BaseProduct.get_token_type, BaseProduct.set_token_type
)
