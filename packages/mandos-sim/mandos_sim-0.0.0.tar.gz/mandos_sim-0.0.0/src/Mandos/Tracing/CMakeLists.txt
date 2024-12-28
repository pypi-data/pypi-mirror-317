add_library(Tracing INTERFACE IMPORTED GLOBAL)

get_target_property(TRACY_INCLUDE_DIRECTORIES Tracy::TracyClient INTERFACE_INCLUDE_DIRECTORIES)
set_property(TARGET Tracing PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${TRACY_INCLUDE_DIRECTORIES} APPEND)

option(MANDOS_ENABLE_TRACING "Enable tracy profiling" OFF)
if(MANDOS_ENABLE_TRACING)
  message(STATUS "Tracy profiling is enabled")
  target_link_libraries(Tracing INTERFACE Tracy::TracyClient)
endif()

add_library(Mandos::Tracing ALIAS Tracing)
