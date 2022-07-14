from dataclasses import dataclass, field
from decimal import *
from enum import Enum
from typing import List, Dict
from typing import Optional

from dataclasses_json import dataclass_json

from py_igsdb_base_data.material import MaterialBulkProperties
from py_igsdb_base_data.optical import IntegratedSpectralAveragesSummaryValues
from py_igsdb_base_data.optical import OpticalProperties


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
    # exists as a separate submission in the same submission group.
    INTRAGROUP = "intragroup"

    # INTERGROUP only applies to child products and therefore only
    # appears in the product composition.
    # It means the child product defined in the product composition
    # exists as a separate submission in a different submission group.
    INTERGROUP = "intergroup"

    def igsdb_types(self) -> List[str]:
        # These types can appear in the IGSDB
        return [
            TokenType.PUBLISHED.name,
            TokenType.UNDEFINED.name
        ]


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

    # These have a geometry (GeometricProperties object)
    # associated with them:
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
    FRONT = "front"
    BACK = "back"
    BOTH = "both"
    NEITHER = "neither"
    UNKNOWN = "unknown"
    NA = "not applicable"


class DataFileType(Enum):
    BSDF_XML = "BSDF XML"
    THERM = "THERM"
    IGDB_LEGACY_SUBMISSION_FILE = "IGDB_LEGACY_SUBMISSION_FILE"
    CGDB_LEGACY_SUBMISSION_FILE = "CGDB_LEGACY_SUBMISSION_FILE"
    SPD = "SPD"
    OTHER = "OTHER"


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
    ProductSubtype.FRITTED_GLASS,
    ProductSubtype.CHROMOGENIC,
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
    ProductSubtype.SHADE_MATERIAL
]

# Subset of shading subtypes.
# These ones will have a composition layer
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
    predefined_tir_front: Optional[str] = None
    predefined_tir_back: Optional[str] = None
    predefined_emissivity_front: Optional[str] = None
    predefined_emissivity_back: Optional[str] = None


@dataclass_json
@dataclass
class BaseGeometry:
    pass


@dataclass_json
@dataclass
class BlindGeometry(BaseGeometry):
    slat_width: Optional[str] = None
    slat_spacing: Optional[str] = None
    slat_tilt: Optional[str] = None
    slat_curvature: Optional[str] = None
    n_segments: Optional[int] = None


@dataclass_json
@dataclass
class VenetianBlindGeometry(BlindGeometry):
    pass


@dataclass_json
@dataclass
class VerticalLouverGeometry(BlindGeometry):
    pass


@dataclass_json
@dataclass
class PerforatedScreenGeometry(BaseGeometry):
    dim_x: Optional[str] = None
    dim_y: Optional[str] = None
    spacing_x: Optional[str] = None
    spacing_y: Optional[str] = None
    type: Optional[int] = None


@dataclass_json
@dataclass
class WovenShadeGeometry(BaseGeometry):
    thread_diameter: Optional[str] = None
    thread_spacing: Optional[str] = None
    shade_thickness: Optional[str] = None


@dataclass_json
@dataclass
class GeometricProperties:
    geometry: Optional[BaseGeometry] = None


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
    that may
    1.  stores layer-specific that cannot be genericized and stored in
        the child product model, e.g. layer thickness.
    2.  stores information from IGDB that doesn't directly translate

    """

    # used for laminate layers
    flipped: Optional[bool] = None
    thickness: Optional[Decimal] = None

    # Used during IGDB port
    layer_filename: Optional[str] = None
    substrate_data_file_name: Optional[str] = None
    CoatingID: Optional[int] = None

    # coated_side_faces_exterior is a convenience property.
    # Sometimes we might not have access to the child product's
    # coated_side property, which we would need to decide if the coating
    # faces external side. So this property can be set when that
    # information is available for use later when it's not.
    coated_side_faces_exterior: bool = False


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
    thickness: Optional[float] = None
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
    convection_factor: Optional[str] = None  # Float in CGDB, max 1 decimal place.
    timestamp: Optional[int] = None


@dataclass_json
@dataclass
class BaseProduct:

    # How do you get getters and setters in a dataclasses
    # to validate incoming values and not mess up the
    # auto-generated init? It's not easy:
    # https://florimond.dev/en/posts/2018/10/reconciling-dataclasses-and-properties-in-python/
    # We have to do this:
    type: Optional[str]
    _type: Optional[str] = field(init=False, repr=False)

    subtype: Optional[str]
    _subtype: Optional[str] = field(init=False, repr=False)

    token_type: Optional[str]
    _token_type: Optional[str] = field(init=False, repr=False)

    units_system: str = "SI"  # or IP
    active: bool = True
    id: Optional[int] = None
    token: Optional[str] = None

    product_id: Optional[int] = None
    data_file_name: Optional[str] = None
    data_file_type: Optional[str] = None

    # This product can be decomposed into parts
    deconstructable: bool = False

    # This product is a 'reference' product, meaning it's sole purpose is
    # to get a child product into the IGSDB using reference substrates.
    # This is method of submittal is  only valid for APPLIED_FILM and LAMINATE products.
    reference: bool = False

    # The official version of this product.
    # The version is incremented each time the product is updated in the IGSDB.
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
    igdb_database_version: Optional[int] = None

    # For legacy CGDB shading products
    cgdb_id: Optional[int] = None
    cgdb_database_version: Optional[str] = None

    # Abstract shade properties during CGDB -> IGSDB Migration.
    shade_properties: Optional[ShadeLayerProperties] = None

    owner: Optional[str] = None
    manufacturer: Optional[str] = None
    material: Optional[str] = None
    product_description: ProductDescription = None
    published_date: Optional[str] = None
    hidden: bool = False
    appearance: Optional[str] = None
    acceptance: Optional[str] = None
    nfrc_id: Optional[str] = None
    igsdb_checksum: Optional[str] = None
    material_bulk_properties: Optional[MaterialBulkProperties] = None

    # Composition is a list of dictionaries holding
    # information about each composition layer. This information
    # will be transformed into ProductComposition entries in Checkertool
    composition: List[ProductComposition] = field(default_factory=list)

    # Integrated spectral averages summaries are usually generated by Checkertool.
    # We initialize this field to an empty list.
    integrated_spectral_averages_summaries: List[IntegratedSpectralAveragesSummary] = field(default_factory=list)

    # The extra_data field is a catch-all for data that does not fit
    # into standard dataclasses. Right now that's just one field: interlayer_nominal_thickness
    extra_data: Dict = field(default_factory=dict)

    # When rendered to json, the physical_properties should always be
    # last of 'official' IGSDB values so that in json output, the (really long)
    # spectral_data is at the bottom of the page. This helps developers debug.
    physical_properties: Optional[PhysicalProperties] = None

    # Geometric properties of product. (Currently only used by
    # shading products. In the CGDB -> ISDB migration, holds values
    # defined in CGDB tables WovenShades, VenetianBlinds and PerforatedScreens.)
    geometric_properties: Optional[GeometricProperties] = None

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

    substrate_filename: Optional[str] = None  # The Substrate_Filename from the GlazingProperties table
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    structure_line: Optional[str] = None  # Hold on to the original structure line
    interlayer_details: Optional[InterlayerDetails] = None  # Keep interlayer information for building composition

    # IGSDB fields
    # The IGSDB stores the submitted product in a related model
    # We may need that information when processing 'published' products...
    # if so store it here.
    product_json: Dict = field(default_factory=dict)

    # GETTERS and SETTERS
    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, v: str) -> None:
        if v is not None:
            try:
                ProductType[v]
            except KeyError:
                raise ValueError(f"Invalid product type: {v}")
        self._type = v

    @property
    def subtype(self) -> str:
        return self._subtype

    @subtype.setter
    def subtype(self, v: str) -> None:
        if v is not None:
            try:
                ProductSubtype[v]
            except KeyError:
                raise ValueError(f"Invalid product subtype: {v}")
        self._subtype = v

    @property
    def token_type(self) -> Optional[str]:
        return self._token_type

    @token_type.setter
    def token_type(self, v: str) -> None:
        if v is not None:
            try:
                TokenType[v]
            except KeyError:
                raise ValueError(f"Invalid product token type: {v}")
        self._token_type = v

    @property
    def name(self) -> Optional[str]:
        if self.product_description:
            return self.product_description.name
        return None

    @name.setter
    def name(self, v: str) -> None:
        if self.product_description:
            self.product_description.name = v
        else:
            self.product_description = ProductDescription(name=v)

    def get_tir_front(self, calculation_standard_name: str = "NFRC") -> Optional[float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    value = summary.summary_values.thermal_ir.transmittance_front
                    if value:
                        return value
        # If we don't have a calculated value, we might have a 'user defined' value (from
        # a header line in submission file). If so, return that...
        if self.physical_properties and self.physical_properties.predefined_emissivity_front:
            return self.physical_properties.predefined_tir_front
        return None

    def get_tir_back(self, calculation_standard_name: str = "NFRC") -> Optional[float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    value = summary.summary_values.thermal_ir.transmittance_back
                    if value:
                        return value
        # If we don't have a calculated value, we might have a 'user defined' value (from
        # a header line in submission file). If so, return that...
        if self.physical_properties and self.physical_properties.predefined_tir_back:
            return self.physical_properties.predefined_emissivity_back
        return None

    def get_emissivity_front(self, calculation_standard_name: str = "NFRC") -> Optional[float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    value = summary.summary_values.thermal_ir.emissivity_front_hemispheric
                    if value:
                        return value
        # If we don't have a calculated value, we might have a 'user defined' value (from
        # a header line in submission file). If so, return that...
        if self.physical_properties and self.physical_properties.predefined_emissivity_front:
            return self.physical_properties.predefined_emissivity_front
        return None

    def get_emissivity_back(self, calculation_standard_name: str = "NFRC") -> Optional[float]:
        # If we have a calculated value for the given standard, return that...
        if self.integrated_spectral_averages_summaries:
            for summary in self.integrated_spectral_averages_summaries:
                if summary.calculation_standard == calculation_standard_name:
                    value = summary.summary_values.thermal_ir.emissivity_back_hemispheric
                    if value:
                        return value
        # If we don't have a calculated value, we might have a 'user defined' value (from
        # a header line in submission file). If so, return that...
        if self.physical_properties and self.physical_properties.predefined_emissivity_front:
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
        if self.subtype not in [ProductSubtype.MONOLITHIC.name, ProductSubtype.LAMINATE.name]:
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
                if composition_layer.get('subtype', None) == ProductSubtype.COATED.name:
                    composition_details: CompositionDetails = composition_layer.composition_details
                    if composition_details:
                        return composition_details.coated_side_faces_exterior
        return False
