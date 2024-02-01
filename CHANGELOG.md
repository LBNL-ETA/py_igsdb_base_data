# Changelog : py_igsdb_base_data

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
