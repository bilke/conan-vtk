cmake_minimum_required(VERSION 2.8.12)
project(MyVTK)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(APPLE)
    # Workaround for rpath error
    set(CMAKE_SKIP_RPATH 0)
endif(APPLE)

set(CMAKE_CXX_STANDARD 11)

find_package(VTK 8.1 REQUIRED)
include(${VTK_USE_FILE})

add_executable(myvtk main.cpp)
target_link_libraries(myvtk vtkCommonCore ${CMAKE_DL_LIBS})

if(UNIX AND NOT APPLE)
	set(THREADS_PREFER_PTHREAD_FLAG ON)
	find_package(Threads REQUIRED)
	target_link_libraries(myvtk Threads::Threads)
endif()
