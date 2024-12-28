cmake_minimum_required(VERSION 3.23)

# Set default application version if it does not exist on environment
if(NOT APP_VERSION)
  set(APP_VERSION 0.0.0)
endif()

# Cut APP_VERSION with possible syntax: Major.Minor.Patch-dev.Revision to just
# Major.Minor.Patch which is the only supported version syntax by Cmake
string(REGEX MATCH "^[^-]+" APP_VERSION_MAJOR_MINOR_PATCH ${APP_VERSION})

include_guard()

if(CMAKE_VERSION VERSION_GREATER_EQUAL "3.13.0")
  cmake_policy(SET CMP0077 NEW)
endif()

# fix DOWNLOAD_EXTRACT_TIMESTAMP warning in FetchContent
if(CMAKE_VERSION VERSION_GREATER_EQUAL "3.24.0")
  cmake_policy(SET CMP0135 NEW)
endif()

# only useable here
set(ProjectOptions_SRC_DIR ${CMAKE_CURRENT_LIST_DIR})

include(CMakeDependentOption)
include(CheckCXXCompilerFlag)

macro(supports_sanitizers)
  if((CMAKE_CXX_COMPILER_ID MATCHES ".*Clang.*" OR CMAKE_CXX_COMPILER_ID MATCHES ".*GNU.*") AND NOT WIN32)
    set(SUPPORTS_UBSAN ON)
  else()
    set(SUPPORTS_UBSAN OFF)
  endif()

  if((CMAKE_CXX_COMPILER_ID MATCHES ".*Clang.*" OR CMAKE_CXX_COMPILER_ID MATCHES ".*GNU.*") AND WIN32)
    set(SUPPORTS_ASAN OFF)
  else()
    set(SUPPORTS_ASAN ON)
  endif()
endmacro()

macro(setup_options)
  option(ENABLE_HARDENING "Enable hardening" OFF)
  option(ENABLE_COVERAGE "Enable coverage reporting" OFF)
  cmake_dependent_option(
    ENABLE_GLOBAL_HARDENING "Attempt to push hardening options to built dependencies" ON ENABLE_HARDENING OFF
  )

  option(BUILD_TESTING "Enable the tests" OFF)
  option(ENABLE_IPO "Enable IPO/LTO" OFF)
  option(WARNINGS_AS_ERRORS "Treat Warnings As Errors" OFF)
  option(ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" OFF)
  option(ENABLE_SANITIZER_LEAK "Enable leak sanitizer" OFF)
  option(ENABLE_SANITIZER_UNDEFINED "Enable undefined sanitizer" OFF)
  option(ENABLE_SANITIZER_THREAD "Enable thread sanitizer" OFF)
  option(ENABLE_SANITIZER_MEMORY "Enable memory sanitizer" OFF)
  option(ENABLE_UNITY_BUILD "Enable unity builds" OFF)
  option(ENABLE_CLANG_TIDY "Enable clang-tidy" OFF)
  option(ENABLE_CPPCHECK "Enable cpp-check analysis" OFF)
  option(ENABLE_PCH "Enable precompiled headers" OFF)
  option(ENABLE_CACHE "Enable ccache" OFF)

endmacro()

macro(global_options)
  if(ENABLE_IPO)
    include(${ProjectOptions_SRC_DIR}/Optimization.cmake)
    enable_ipo()
  endif()

  supports_sanitizers()

  if(ENABLE_HARDENING AND ENABLE_GLOBAL_HARDENING)
    include(${ProjectOptions_SRC_DIR}/Hardening.cmake)
    if(NOT SUPPORTS_UBSAN
       OR ENABLE_SANITIZER_UNDEFINED
       OR ENABLE_SANITIZER_ADDRESS
       OR ENABLE_SANITIZER_THREAD
       OR ENABLE_SANITIZER_LEAK
    )
      set(ENABLE_UBSAN_MINIMAL_RUNTIME FALSE)
    else()
      set(ENABLE_UBSAN_MINIMAL_RUNTIME TRUE)
    endif()
    enable_hardening(project_options ON ${ENABLE_UBSAN_MINIMAL_RUNTIME})
  endif()
endmacro()

macro(local_options)
  include(${ProjectOptions_SRC_DIR}/Common.cmake)
  common_project_options()

  add_library(project_warnings INTERFACE)
  add_library(project_options INTERFACE)

  include(${ProjectOptions_SRC_DIR}/CompilerWarnings.cmake)
  set_project_warnings(
    project_warnings
    ${WARNINGS_AS_ERRORS}
    ""
    ""
    ""
    ""
  )

  include(${ProjectOptions_SRC_DIR}/Sanitizers.cmake)
  enable_sanitizers(
    project_options
    ${ENABLE_SANITIZER_ADDRESS}
    ${ENABLE_SANITIZER_LEAK}
    ${ENABLE_SANITIZER_UNDEFINED}
    ${ENABLE_SANITIZER_THREAD}
    OFF #${ENABLE_SANITIZER_MEMORY}
  )

  set_target_properties(project_options PROPERTIES UNITY_BUILD ${ENABLE_UNITY_BUILD})

  if(ENABLE_PCH)
    target_precompile_headers(project_options INTERFACE "${PCH_HEADERS}")
  endif()

  if(ENABLE_CACHE)
    include(${ProjectOptions_SRC_DIR}/Cache.cmake)
    enable_cache()
  endif()

  include(${ProjectOptions_SRC_DIR}/StaticAnalyzers.cmake)
  if(ENABLE_CLANG_TIDY)
    enable_clang_tidy(project_options ${WARNINGS_AS_ERRORS})
  endif()

  if(ENABLE_CPPCHECK)
    enable_cppcheck(${WARNINGS_AS_ERRORS} "" # override cppcheck options
    )
  endif()

  if(ENABLE_COVERAGE)
    include(${ProjectOptions_SRC_DIR}/Coverage.cmake)
    enable_coverage(project_options)
  endif()

  if(WARNINGS_AS_ERRORS)
    check_cxx_compiler_flag("-Wl,--fatal-warnings" LINKER_FATAL_WARNINGS)
    if(LINKER_FATAL_WARNINGS)
      # This is not working consistently, so disabling for now
      # target_link_options(project_options INTERFACE -Wl,--fatal-warnings)
    endif()
  endif()

  if(ENABLE_HARDENING AND NOT ENABLE_GLOBAL_HARDENING)
    include(${ProjectOptions_SRC_DIR}/Hardening.cmake)
    if(NOT SUPPORTS_UBSAN
       OR ENABLE_SANITIZER_UNDEFINED
       OR ENABLE_SANITIZER_ADDRESS
       OR ENABLE_SANITIZER_THREAD
       OR ENABLE_SANITIZER_LEAK
    )
      set(ENABLE_UBSAN_MINIMAL_RUNTIME FALSE)
    else()
      set(ENABLE_UBSAN_MINIMAL_RUNTIME TRUE)
    endif()
    enable_hardening(project_options OFF ${ENABLE_UBSAN_MINIMAL_RUNTIME})
  endif()

  target_compile_definitions(project_options INTERFACE APP_VERSION="${APP_VERSION}")
endmacro()

include(${ProjectOptions_SRC_DIR}/PackageProject.cmake)
include(${ProjectOptions_SRC_DIR}/Utilities.cmake)
