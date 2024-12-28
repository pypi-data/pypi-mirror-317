include_guard()

# Common project settings run by default for all the projects that call `project_options()`
macro(common_project_options)
  include("${ProjectOptions_SRC_DIR}/PreventInSourceBuilds.cmake")

  # Generate compile_commands.json to make it easier to work with clang based tools
  set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
  set_property(GLOBAL PROPERTY USE_FOLDERS ON)

  # cmake-format: off
# if(NOT DEFINED CMAKE_CXX_VISIBILITY_PRESET AND NOT DEFINED CMAKE_VISIBILITY_INLINES_HIDDEN)
#   set(CMAKE_CXX_VISIBILITY_PRESET hidden)
#   set(CMAKE_VISIBILITY_INLINES_HIDDEN YES)
# endif()
# cmake-format: on

  # Set output directories for libraries and binaries.
  set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
  set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
  set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
endmacro()
