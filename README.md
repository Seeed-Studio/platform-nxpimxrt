# i.MX RT Series: development platform for [PlatformIO](http://platformio.org)

[![Build Status](https://travis-ci.org/platformio/platform-atmelsam.svg?branch=develop)](https://travis-ci.org/platformio/platform-atmelsam)
[![Build status](https://ci.appveyor.com/api/projects/status/dj1c3b2d6fyxkoxq/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-atmelsam/branch/develop)

The i.MX RT Series is the industry’s first crossover MCU, offering the highest performance Arm® Cortex®-M core, real-time functionality, and MCU usability at an affordable price.

* [Home](http://platformio.org/platforms/nxpimxrt) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/nxpimxrt.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = nxpimxrt
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/Seeed-Studio/platform-nxpimxrt.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/nxpimxrt.html).
