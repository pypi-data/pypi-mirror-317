import os

from conan.tools.cmake import CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualRunEnv

from conan import ConanFile

# Force Conan 2.0
required_conan_version = ">=2.0.0"


class Mandos(ConanFile):
    name = "Mandos"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "build_bindings": [False, True],
        "build_tests": [False, True],
        "tracing": [False, True],
        "clang_tidy": [False, True],
        "asan": [False, True],
        "ubsan": [False, True],
        "warnings_as_errors": [False, True],
        "coverage": [False, True],
        "fPIC": [True, False],
        "shared": [True, False]
    }

    default_options = {
        "build_bindings": True,
        "build_tests": False,
        "tracing": False,
        "clang_tidy": True,
        "asan": True, 
        "ubsan": True,
        "warnings_as_errors": True,
        "coverage": False,
        "fPIC": True,
        "shared": True
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        self.requires("eigen/3.4.0") # Algebra library
        self.requires("spdlog/1.14.1") # Logging
        self.requires("tracy/0.11.1") # Tracing performance
        self.requires("catch2/3.6.0") # Unit testing framework
        self.requires("openvdb/11.0.0") # SDF
        self.requires("pybind11/2.12.0") # Python bindings
        self.requires("tinyad/cci.20240718") # Auto diff capabilities
    
    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def generate(self):
        cmake = CMakeDeps(self)
        cmake.generate()

        toolchain = CMakeToolchain(self)
        toolchain.absolute_paths = True ## Needed because we are building with pip and it copies the project to another location
        toolchain.cache_variables["WARNINGS_AS_ERRORS"] = self.options.warnings_as_errors
        toolchain.cache_variables["ENABLE_COVERAGE"] = self.options.coverage
        toolchain.cache_variables["ENABLE_SANITIZER_UNDEFINED"] = self.options.ubsan
        toolchain.cache_variables["ENABLE_SANITIZER_ADDRESS"] = self.options.asan
        toolchain.cache_variables["ENABLE_CLANG_TIDY"] = self.options.clang_tidy
        toolchain.cache_variables["MANDOS_ENABLE_TRACING"] = self.options.tracing
        toolchain.cache_variables["BUILD_TESTING"] = self.options.build_tests
        toolchain.cache_variables["MANDOS_BUILD_BINDINGS"] = self.options.build_bindings
        toolchain.generate()

    def layout(self):
        cmake_layout(self)
