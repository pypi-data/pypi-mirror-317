# Common CMake Modules

Based on [this project](https://github.com/cpp-best-practices/cmake_template)

A general-purpose CMake library that provides functions that improve the CMake experience following the best practices.

## Features

- Project options:
  - compiler warnings,
  - compiler optimizations (intraprocedural, native),
  - caching (ccache, sccache),
  - sanitizers,
  - static code analyzers (clang-tidy, cppcheck, include-what-you-use),
  - test coverage analysis,
  - precompiled headers,
  - build time measurement,
  - unity builds
- `package_project`: automatic packaging/installation of the project for seamless usage via find_package/target_link through CMake's FetchContent, vcpkg, etc.

## Usage

Add this repository as a submodule of your project.

```sh
git submodule add -f git@gitlab.com:mslab-urjc/cmake-modules.git
```

Include `cmake/Index.cmake` to make the functions and options available. Here is a full example:

```cmake
cmake_minimum_required(VERSION 3.23) # For some presets features needed

# set a default CXX standard for the tools and targets that do not specify them.
# If commented, the latest supported standard for your compiler is automatically set.
set(CMAKE_CXX_STANDARD 20)
# Force the minimum CXX standard
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set the project name and language
project(myproject LANGUAGES CXX C)

# Common variables directly understood by cmake
option(BUILD_SHARED_LIBS "Enable compilation of shared libraries" ON)
option(BUILD_TESTING "Enable the tests" ON)

# Forcing an option:
# Unless forced, try to set them from a preset
set(ENABLE_CPPCHECK ON CACHE BOOL "" FORCE)

# Bring common options and functionality
include(cmake/Index.cmake)

# Then call this functions to setup everything accordingly
setup_options()
global_options()
local_options()

```

Then add the executables or libraries to the project, linking the project_options and project_warnings targets:

An executable:

```cmake
add_executable(main)
target_sources(main PRIVATE main.cpp)
target_link_libraries(main PRIVATE project_options project_warnings) # link project_options/warnings

# Find dependencies:
find_package(fmt CONFIG REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)

# Link dependencies
target_link_libraries(
  main
  PRIVATE
  Eigen3::Eigen
)

```

A header-only library:

```cmake
add_library(my_header_lib INTERFACE)
target_sources(
  my_header_lib
  INTERFACE FILE_SET
            HEADERS
            FILES
            mylib/lib.hpp
)
target_link_libraries(my_header_lib INTERFACE project_options project_warnings) # link project_options/warnings

# Includes
target_include_directories(my_header_lib INTERFACE
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
    "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>")

# Find dependencies:
find_package(fmt CONFIG REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)

# Link dependencies:
target_link_libraries(
  my_header_lib
  INTERFACE
  fmt::fmt
  Eigen3::Eigen
)

```

A library with separate header and source files:

```cmake
add_library(my_lib)
target_sources(my_lib PRIVATE mylib2/lib.cpp)
target_sources(
  my_lib
  PUBLIC FILE_SET
         HEADERS
         FILES
         mylib2/lib.hpp
)
target_link_libraries(my_lib PRIVATE project_options project_warnings) # link project_options/warnings

# Includes
target_include_directories(my_header_lib INTERFACE
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>"
    "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>")

# Find dependencies:
find_package(fmt CONFIG REQUIRED)
find_package(Eigen3 CONFIG REQUIRED)

# Link dependencies:
target_link_libraries(
  my_lib
  PRIVATE
  fmt::fmt
  Eigen3::Eigen
)

```

## Project options

Using this module will make available the following options. All default to `OFF`.

- `ENABLE_HARDENING`: Enable hardening.
- `ENABLE_COVERAGE`: Enable coverage reporting.
- `ENABLE_IPO`: Enable IPO/LTO.
- `WARNINGS_AS_ERRORS`: Treat Warnings As Errors.
- `ENABLE_SANITIZER_ADDRESS`: Enable address sanitizer.
- `ENABLE_SANITIZER_LEAK`:Enable leak sanitizer.
- `ENABLE_SANITIZER_UNDEFINED`: Enable undefined sanitizer.
- `ENABLE_SANITIZER_THREAD`: Enable thread sanitizer.
- `ENABLE_SANITIZER_MEMORY`: Enable memory sanitizer.
- `ENABLE_CLANG_TIDY`: Enable clang-tidy.

There exists some extra options that we don't current maintain or support, so consider them as unsupported

## Disabling static analysis for external targets

In somes cases, some external targets are added to the code base and might make static analysis to fail. You can disable checks for those targets with

```cmake
target_disable_static_analysis(some_external_target)
```
