# Changelog

All noticeable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.11] – 2024-12-27

### Added
– Added the new function `to_auth()` for getting user [Cropwise Operations API](https://cropwiseoperations.docs.apiary.io/) token

### Changed
- The README.md

### Fixed
- The bug with `agrimatrix_dataset()` function

## [0.0.10] – 2024-10-04

### Added
- Added requires for `numpy`

### Changed
- The README.md

### Fixed
- The bug with lack of attribute `create_orchard_rows()` and `fetch_changes()`

## [0.0.9] – 2024-10-02

### Added
- Added argument `start_row_number` in function `create_orchard_rows()` to allow using your own numeration of rows

### Changed
- The README.md

### Fixed
- The bug in function `create_orchard_rows()` while working with `MultiPolygon` objects


## [0.0.8] – 2024-08-02

### Changed
- The README.md
- Added argument `quarter_name` in function `create_orchard_rows()` to allow using a KML-file with several quarters


## [0.0.7] – 2024-07-25

### Changed
- The README.md
- The algorithm of function `create_orchard_rows()` was changed. Added the opportunity to create rows in individual direction using the LineString of row direction in KML-file


## [0.0.6] – 2024-07-16

### Added 
- Added a new function `fetch_changes()` for mass loading of changed object from Cropwise Operations

### Changed
- The README.md

### Fixed
- The bug with previous version downloading

## [0.0.5] – 2024-07-08

### Added 
- Added a new function `create_orchard_rows()` for geofencing

## [0.0.2] - 2024-04-12

### Added
- The project was created
- Added the function `data_downloader()` for mass loading of data on the [Cropwise Operations API](https://cropwiseoperations.docs.apiary.io/)
- Added the function `agrimatrix_dataset()` for creating an Agrimatrix report
- Integration with the external [Cropwise Operations API](https://cropwiseoperations.docs.apiary.io/)

