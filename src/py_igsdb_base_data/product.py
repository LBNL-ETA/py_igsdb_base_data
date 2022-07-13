from enum import Enum
from typing import List


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
