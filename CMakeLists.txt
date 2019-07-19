cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

# include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
# conan_basic_setup()
if(DEFINED CONAN_CMAKE_POSITION_INDEPENDENT_CODE)
    message(STATUS "Conan: Adjusting fPIC flag (${CONAN_CMAKE_POSITION_INDEPENDENT_CODE})")
    set(CMAKE_POSITION_INDEPENDENT_CODE ${CONAN_CMAKE_POSITION_INDEPENDENT_CODE})
endif()

if(MSVC)
    # Remove pdb-related flags
    string(REGEX REPLACE "/Z[iI7]" ""
        CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
    # Embed debug info into .lib-files
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_RELEASE} /Z7")
endif()

add_subdirectory(source_subfolder)
