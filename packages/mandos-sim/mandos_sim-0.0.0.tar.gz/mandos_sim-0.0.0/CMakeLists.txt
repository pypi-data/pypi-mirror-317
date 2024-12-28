cmake_minimum_required(VERSION 3.9)
project(mandos LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# CXX Standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED true)

# Make visibility hidden by default, as in Windows.
# Its the recommended way to separate private and public API
# https://www.youtube.com/watch?v=m0DwB4OvDXk
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN YES)

# Configure project options
include(cmake-modules/Index.cmake)

setup_options()
global_options()
local_options()

include(GenerateExportHeader)

find_package(Eigen3 REQUIRED)
find_package(spdlog REQUIRED)
find_package(Tracy REQUIRED)
find_package(OpenVDB REQUIRED)
find_package(TinyAD REQUIRED)

# Set output directories for libraries, archives and binaries
include(GNUInstallDirs)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

add_subdirectory(src)

if(MANDOS_BUILD_BINDINGS)
  find_package(pybind11 REQUIRED)
  add_subdirectory(bindings)
  # Handling building the python wheel with scikit-build
  if (SKBUILD)
    include(cmake/ThirdParty.cmake)
    copy_third_party_shared_libs(${CMAKE_INSTALL_PREFIX}/lib)
  endif()
endif()

if(BUILD_TESTING)
  include(CTest)
  find_package(Catch2 REQUIRED)
  add_subdirectory(tests)
endif()
