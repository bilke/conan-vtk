cmake_minimum_required(VERSION 2.8.12)
project(MyVTK)

include(conanbuildinfo.cmake)
conan_basic_setup()

#find_package(VTK REQUIRED)
#include(${VTK_USE_FILE})

include_directories(${CONAN_INCLUDE_DIRS}/vtk-7.0)
add_executable(myvtk main.cpp)
target_link_libraries(myvtk ${CONAN_LIBS})
