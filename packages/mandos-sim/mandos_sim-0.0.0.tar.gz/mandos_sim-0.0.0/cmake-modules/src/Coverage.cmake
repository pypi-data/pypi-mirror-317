include_guard()

# Enable coverage reporting for gcc/clang
function(enable_coverage target)
  if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES ".*Clang")
    target_compile_options(${target} INTERFACE --coverage -O0 -g)
    target_link_libraries(${target} INTERFACE --coverage)
  endif()
endfunction()
