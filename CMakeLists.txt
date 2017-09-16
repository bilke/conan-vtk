PROJECT(conanhello)
cmake_minimum_required(VERSION 2.8)
include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

if(MSVC)
    # Remove pdb-related flags
    string(REGEX REPLACE "/Z[iI7]" ""
        CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
    # Embed debug info into .lib-files
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_RELEASE} /Z7")
endif()

add_subdirectory(VTK-8.0.1)
install(FILES FindVTK.cmake DESTINATION .)
