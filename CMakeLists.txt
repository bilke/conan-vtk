cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
# Instead of conan_basic_setup():
conan_check_compiler()
conan_output_dirs_setup()
conan_set_find_library_paths()
# Disabled because Qt dependencies might interfere with VTK third-party libs
# conan_global_flags()
conan_define_targets()
conan_set_rpath()
conan_set_vs_runtime()
conan_set_std()
conan_set_libcxx()
conan_set_find_paths()
conan_set_fpic()

if(MSVC)
    # Remove pdb-related flags
    string(REGEX REPLACE "/Z[iI7]" ""
        CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
    # Embed debug info into .lib-files
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_RELEASE} /Z7")
endif()

add_subdirectory(source_subfolder)
