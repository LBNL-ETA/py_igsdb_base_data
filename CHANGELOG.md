# Changelog : py_igsdb_base_data

## v0.0.73

- Add extra error handling in geometric properties calcs

## v0.0.72

- Set Decimal precision locally before calculating rise or curvature

## v0.0.71

- Use Decimal instead of string for some fields

## v0.0.70

- For MaterialType, use "NOT_APPLICABLE" instead of the more ambiguous "NA"

## v0.0.69

- For CoatedSideType, use "NOT_APPLICABLE" instead of the more ambiguous "NA"

## v0.0.68

- Make 'GeometricProperties' a property of 'PhysicalProperties'

## v0.0.67

- Updated CoatedSideType to include new values.

## v0.0.66

- Change 'RECTANGLE' to 'RECTANGULAR' to match wincalc convention

## v0.0.65

- Add 'diameter' property to PerforatedScreenGeometry 

## v0.0.64

- Change PerforatedScreenGeometry 'type' property's type from int to string

## v0.0.63

- Add 'publish_status' property to BaseProduct.

## v0.0.62

- Fix bug in has_thermal_ir_wavelengths method.

## v0.0.61

- Fix bugs in getters to IntegratedSpectralAveragesSummaryValues

## v0.0.60

- Added missing getters to IntegratedSpectralAveragesSummaryValues

## v0.0.59

- Added flatten() method to IntegratedSpectralAveragesSummaryValues

## v0.0.58

- Refactored BlindGeometry dataclass.

## v0.0.57

- Update dependencies.

## v0.0.56

- Add rise property to `BlindGeometry`.
- Update `set_curvature_from_rise` to use instance's rise property (not argument).
- Add 'set_rise_from_curvature' method to `BlindGeometry` class.

## v0.0.55

- Bump dependency versions

## v0.0.54

- Add has_thermal_wavelength_data property to Product and OpticalProperties classes

## v0.0.53

- Add marketing name to product

## v0.0.52

- Adding SPREADSHEET type to DataFileType

## v0.0.51

- Adding set_curvature_from_rise method to BlindGeometry class

## v0.0.50

- Adding tilt choice to BlindGeometry class

## v0.0.49

- Consolidate igdb_time_created to mdb_time_created and use for cgdb_time_created as well.

## v0.0.48

- Added cgdb_checksum property
- Added checksum_date (used for either igdb_checksum or cgdb_checksum, whichever is defined for a product).

## v0.0.47

- Refactor ThermalIRResults to have 'emissivity' as base property and 'absorptance' as shortcut property.

## v0.0.46

- Remove extra FRITTED_GLASS in SHADING_SUBTYPES

## v0.0.45

- Bump requirements

## v0.0.44

- Bump requirements

## v0.0.43

- Add coating_name in composition details.

## v0.0.42

- Rename CoatingID to coating_id in composition details.

## v0.0.41

- Rename igsdb_checksum to igdb_checksum

## v0.0.40

- Update dataclasses-json version to 0.6.1

## v0.0.39

- Use Decimals for all database_version fields

## v0.0.38

- Created new base dataclass IGSDBObject with token and uuid properties.

## v0.0.37

- Change BaseEntity property from legacy_id to igdb_id

## v0.0.36

- Added a base object for "Entity" objects.
- Updated dependency dataclasses-json to 0.6.0
- Removed unused dependencies
