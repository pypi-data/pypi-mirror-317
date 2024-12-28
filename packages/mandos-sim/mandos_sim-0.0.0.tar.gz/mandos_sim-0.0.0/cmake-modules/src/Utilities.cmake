include_guard()

# Get all the CMake targets
function(get_all_targets var)
  set(targets)
  get_all_targets_recursive(targets ${CMAKE_CURRENT_SOURCE_DIR})
  set(${var} ${targets} PARENT_SCOPE)
endfunction()

# Get all the installable CMake targets
function(get_all_installable_targets var)
  set(targets)
  get_all_targets(targets)
  foreach(_target ${targets})
    get_target_property(_target_type ${_target} TYPE)
    if(NOT ${_target_type} MATCHES ".*LIBRARY|EXECUTABLE")
      list(REMOVE_ITEM targets ${_target})
    endif()
  endforeach()
  set(${var} ${targets} PARENT_SCOPE)
endfunction()

# Get all the CMake targets in the given directory
macro(get_all_targets_recursive targets dir)
  get_property(subdirectories DIRECTORY ${dir} PROPERTY SUBDIRECTORIES)
  foreach(subdir ${subdirectories})
    get_all_targets_recursive(${targets} ${subdir})
  endforeach()

  get_property(current_targets DIRECTORY ${dir} PROPERTY BUILDSYSTEM_TARGETS)
  list(APPEND ${targets} ${current_targets})
endmacro()

# Group source files in VS and other IDEs
function(group_sources target)
  get_target_property(sources ${target} SOURCES)
  get_target_property(target_src_dir ${target} SOURCE_DIR)
  foreach(file ${sources})
    get_filename_component(file "${file}" ABSOLUTE)
    string(REGEX REPLACE "^${target_src_dir}/" "" group "${file}")
    string(REGEX REPLACE "^${CMAKE_SOURCE_DIR}/" "" group "${file}")
    get_filename_component(group "${group}" DIRECTORY)
    string(REPLACE "/" "\\" group "${group}")
    source_group("${group}" FILES "${file}")
  endforeach()
endfunction()

# Function to get assets from a dependency given its target
function(import_third_party_assets target)

  # Conan defines a variable <lib_name>_PACKAGE_FOLDER_<CONFIG>
  # We have to compound the name of that variable to get the root folder.
  # Since the target created by conan has limited information we have to do several steps

  # 1. Get current configuration name in UPPERCASE
  string(TOUPPER ${CMAKE_BUILD_TYPE} upper_case_config)
  # 2. Get given target's name. It usually will come as namespace::target_name
  get_target_property(target_ns_name ${target} NAME)
  # 3. Remove the namespace prefix from the target name
  string(REGEX REPLACE "^.*::" "" target_name ${target_ns_name})
  # 4. Assemble the variables's name and store its content to $package_folder
  set(package_folder ${${target_name}_PACKAGE_FOLDER_${upper_case_config}})

  if(package_folder)
    # 5a. If it exists and has content

    include(GNUInstallDirs)
    # 6. Assemble the input path as <package_root_folder>/share and the output path as <build_dir>/share
    cmake_path(APPEND package_folder ${CMAKE_INSTALL_DATADIR} OUTPUT_VARIABLE input_assets_folder)
    cmake_path(APPEND CMAKE_BINARY_DIR ${CMAKE_INSTALL_DATADIR} OUTPUT_VARIABLE output_assets_folder)

    if(EXISTS ${input_assets_folder})
      # 7a. If input folder has assets we create the target to copy them when building all targets in this project
      message(STATUS "Creating target to copy assets from ${target}")
      add_custom_target(
        copy_${target_name}_assets ALL COMMAND ${CMAKE_COMMAND} -E copy_directory_if_different "${input_assets_folder}"
                                               "${output_assets_folder}"
        COMMENT "Copying ${target_name} assets from ${input_assets_folder} to ${output_assets_folder}"
      )
    else()
      # 7b. $target doesn't have assets. We shouldn't have called this function for this $target
      message(AUTHOR_WARNING "${target} doesn't have any assets")
    endif()
  else()
    # 5b. The package folder variable doesn't exist or doesn't have content. Probably we are calling this function for a library not packaged by Conan
    message(AUTHOR_WARNING "${target} root folder wasn't found. This only works with libraries packaged by Conan")
  endif()

endfunction()