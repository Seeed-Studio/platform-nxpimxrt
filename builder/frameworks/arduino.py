# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
build_mcu = env.get("BOARD_MCU", board.get("build.mcu", ""))

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoimxrt")
assert isdir(FRAMEWORK_DIR)
BUILD_CORE = board.get("build.core", "")
BUILD_SYSTEM = board.get("build.system", BUILD_CORE)
SDK_DIR = join(FRAMEWORK_DIR, "tools", "sdk")
LIB_DIR = join(FRAMEWORK_DIR, "tools", "lib", board.get("build.processor"))
USB_DIR = join(SDK_DIR, "middleware", "usb")
DRIVER_DIR = join(SDK_DIR, "devices", board.get("build.processor"))


#ld flags 
LIBLINK = '-Wl,--start-group\"'+ ' \"-Wl,--whole-archive\" '+ LIB_DIR + '\libfsl_bsp.a ' + LIB_DIR + '\libfsl_usb_drivers.a ' + LIB_DIR + '\libfsl_xip_drivers.a '+'\"-Wl,--no-whole-archive\" '+'\"-Wl,--end-group'

# USB flags
ARDUINO_USBDEFINES = [("ARDUINO", 10805)]
if "build.usb_product" in env.BoardConfig():
    ARDUINO_USBDEFINES += [
        ("USB_VID", board.get("build.hwids")[0][0]),
        ("USB_PID", board.get("build.hwids")[0][1]),
        ("USB_PRODUCT", '\\"%s\\"' %
         board.get("build.usb_product", "").replace('"', "")),
        ("USB_MANUFACTURER", '\\"%s\\"' %
         board.get("vendor", "").replace('"', ""))
    ]


env.Append(

    CFLAGS=[
        "-std=gnu99"
    ],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-w",
        "-Wall",
        "-mthumb",
        "-nostdlib",
        "-mfloat-abi=hard",
        "--param", "max-inline-insns-single=500",
        "-fno-common",
        "-ffreestanding",
        "-fno-builtin",
        "-nostdlib",
        "-MMD",
        "-mapcs"
    ],

    CXXFLAGS=[
        "-Os",  # optimize for size
        "-w",
        "-Wall",
        "-fno-rtti",
        "-fno-exceptions",
        "-std=gnu++11",
        "-mfloat-abi=hard",
        "-fno-threadsafe-statics",
        "-fno-common",
        "-ffunction-sections",
        "-fdata-sections",
        "-ffreestanding",
        "-fno-builtin",
        "-mthumb",
        "-mapcs",
        "--param", "max-inline-insns-single=500",
        "-nostdlib"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        "USBCON"
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE)
    ],

    LINKFLAGS=[
        "-Os",
        "-fno-common",
        "-ffunction-sections",
        "-fdata-sections",
        "-ffreestanding",
        "-fno-builtin",
        "-mthumb",
        "-mapcs",
        "-mthumb",
        "-mfloat-abi=hard",
        "-Xlinker", 
        "--gc-sections",
        "-static",
        "-z",
        "muldefs"
    ],

    LIBPATH=[
       join(SDK_DIR, "CMSIS", "LIB", "GCC"),
    ],

    LIBS=["arm_cortexM7lfdp_math", "arm_cortexM7lfsp_math"]
)

if "BOARD" in env:
    env.Append(
        CCFLAGS=[
            "-mcpu=%s" % board.get("build.cpu"),
            "-mfpu=%s" % board.get("build.fpu")
        ],
        LINKFLAGS=[
            "-mcpu=%s" % board.get("build.cpu"),
            "-mfpu=%s" % board.get("build.fpu")
        ]
    )

if ("imxrt" in build_mcu):
    env.Append(
        LINKFLAGS=[
            "--specs=nosys.specs",
            "--specs=nano.specs"
        ]
    )

if BUILD_SYSTEM == "imxrt":
    env.Append(
        CPPPATH=[
            join(SDK_DIR, "CMSIS", "Include"),
            join(SDK_DIR, "components", "serial_manager"),
            join(FRAMEWORK_DIR, "cores", BUILD_CORE, "USB"),
            join(USB_DIR, "include"),
            join(USB_DIR, "osa"),
            join(USB_DIR, "host"),
            join(USB_DIR, "phy"),
            join(USB_DIR,"device"),
            join(DRIVER_DIR),
            join(DRIVER_DIR, "drivers"),
            join(DRIVER_DIR, "utilities"),
            join(DRIVER_DIR, "utilities", "str"),
            join(DRIVER_DIR, "utilities", "debug_console")
        ],

        LIBPATH=[
            join(FRAMEWORK_DIR, "variants", board.get("build.variant")),
            join(LIB_DIR)
        ],

        LINKFLAGS=[
           "-Os",
           "-Wall",
           "-std=gnu99",
           "-mcpu=cortex-m7",
           "-mfloat-abi=hard",
           "-mfpu=fpv5-d16",
           "-MMD",
           "-Wl,-Map,output.map",
           join(LIBLINK)
        ],
    )

#
# Lookup for specific core's libraries
#

env.Append(
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants", board.get("build.variant")),
            ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", board.get("build.variant")),
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", BUILD_CORE)
))


env.Append(LIBS=libs)
