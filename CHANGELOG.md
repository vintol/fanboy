# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

------------
## [Upcoming Release]
### Added
### Changed
### Removed
### Deprecated
### Fixed
### Security
------------
## [v2.11.0] - 2018-05-20
### Added
- a separate function to extract category and album links
- cross checking to avoid repetition of same links
### Changed
- changed default naming convention of file to store links in
### Removed
- cross referencing ability is temporarily disabled
### Fixed
- Multiple repetition of the same albums
- Carry-over of albums into the next crawl

------------
## [v2.1.0]
### Added
- Cross reference enabled by default
- default cross reference with previously retrieved links
### Changed
### Removed

-------
## [v2.0.0]
### Added
- Support for more fan sites.
- Command line options and invoking
- Support for using multiple threads
- Support for cross reference with previously scraped links
### Changed
- No external import of supported sites
- Merged category crawler with album crawler

