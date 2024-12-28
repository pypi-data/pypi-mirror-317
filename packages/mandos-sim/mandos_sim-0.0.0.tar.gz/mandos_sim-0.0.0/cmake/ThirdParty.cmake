include(CMakeDependentOption)

# Copy third-party shared libs to the build directory for tests
function(copy_third_party_shared_libs target_dir)
    if(NOT DEFINED CONAN_RUNTIME_LIB_DIRS)
        if(USE_CONAN)
            message(FATAL_ERROR "Failed to load CONAN_RUNTIME_LIB_DIRS")
        endif()
        # TODO: Add support for vcpkg
        message(STATUS "Not using Conan, skipping copying third-party shared libraries.")
        return()
    endif()

    message(STATUS "Copying third-party shared libraries to ${target_dir}...")

    if(WIN32)
        set(pattern "*.dll")
    elseif(APPLE)
        set(pattern "*.dylib")
    else()
        set(pattern "*.so*")
    endif()

    set(copied_files)
    foreach(path ${CONAN_RUNTIME_LIB_DIRS})
        message(STATUS "Copying shared libraries from ${path}")
        file(GLOB libs "${path}/${pattern}")
        file(COPY ${libs} DESTINATION "${target_dir}")
        list(APPEND copied_files ${libs})
    endforeach()

    # Set RPATH to $ORIGIN for the copied libraries
    if(NOT WIN32)
        find_program(PATCHELF_EXECUTABLE patchelf REQUIRED)
        foreach(lib ${copied_files})
            get_filename_component(lib_name ${lib} NAME)
            if(APPLE)
                execute_process(COMMAND install_name_tool -add_rpath @loader_path "${target_dir}/${lib_name}"
                    COMMAND_ERROR_IS_FATAL ANY)
            else()
                execute_process(COMMAND "${PATCHELF_EXECUTABLE}" --set-rpath \$ORIGIN "${target_dir}/${lib_name}"
                    COMMAND_ERROR_IS_FATAL ANY)
            endif()
        endforeach()
    endif()
endfunction()
