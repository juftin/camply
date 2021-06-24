# Changelog

All notable changes to `camply` will be documented in this file, this project adheres to semantic
versioning.

## [Unreleased]

To request new features or bugfixes the
[Camply Feedback for v1.0.0 Discussion](https://github.com/juftin/camply/discussions/12) is the best
place to go.

## [0.1.7] - 2021-06-24

### Fixed

- Fixed bug that returned matching night stays outside of the search window.

## [0.1.6] - 2021-06-23

### Added

- Ability to search for campsites by number of consecutive night stays.

## [0.1.5] - 2021-06-02

### Added

- Ability to filter on Yellowstone Campgrounds. See
  this [discussion](https://github.com/juftin/camply/discussions/15#discussioncomment-783657) for
  more detail.

### Fixed

- Allow endpoints to timeout after being unresponsive for 30 seconds

## [0.1.4] - 2021-06-01

### Added

- Pushbullet Notifications
- YAML Search Configuration Files

### Fixed

- PyPi Publishing CI on Release

## [0.1.3] - 2021-05-25

### Added

- CI/CD for publishing camply to Docker Hub and PyPi

### Fixed

- Addressed situations where campsites without addresses information were throwing a KeyError. (big
  thanks to @grantland)
    - This resolution presents an
      interesting [discussion](https://github.com/juftin/camply/pull/14#issuecomment-848302948)
      on whether campsites that have `Enabled` and `Reservable` = `False` should be searchable.
- Empty Email notifications issue resolved

## [0.1.2] - 2021-05-24

### Fixed

- Filter out `Checkout-Only` campsites by excluding `Open` availability status
- No longer trapping all errors with `exit(0)`
- Email notifications now attempt login at start, to throw errors early.

## [0.1.1] - 2021-05-18

### Added

- Updating Badges

### Fixed

- Excluded `Lottery` sites from being returned

## [0.1.0] - 2021-05-18

### Added

- Command Line Interface
- PyPI Package
- Docker Hub Image
- Integrations with https://recreation.gov and https://yellowstonenationalparklodges.com

[unreleased]: https://github.com/juftin/camply/compare/main...integration

[0.1.7]: https://github.com/juftin/camply/compare/v0.1.6...v0.1.7

[0.1.6]: https://github.com/juftin/camply/compare/v0.1.5...v0.1.6

[0.1.5]: https://github.com/juftin/camply/compare/v0.1.4...v0.1.5

[0.1.4]: https://github.com/juftin/camply/compare/v0.1.3...v0.1.4

[0.1.3]: https://github.com/juftin/camply/compare/v0.1.2...v0.1.3

[0.1.2]: https://github.com/juftin/camply/compare/v0.1.1...v0.1.2

[0.1.1]: https://github.com/juftin/camply/compare/v0.1.0...v0.1.1

[0.1.0]: https://github.com/juftin/camply/releases/tag/v0.1.0
