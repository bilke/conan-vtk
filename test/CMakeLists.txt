cmake_minimum_required(VERSION 2.8.12)
project(MyVTK)

include(conanbuildinfo.cmake)
set(CMAKE_MODULE_PATH ${CONAN_CMAKE_MODULE_PATH} ${CMAKE_MODULE_PATH})
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})

add_executable(myvtk main.cpp)
target_link_libraries(myvtk ${VTK_LIBRARIES})

if(UNIX AND NOT APPLE)
	set(THREADS_PREFER_PTHREAD_FLAG ON)
	find_package(Threads REQUIRED)
	target_link_libraries(myvtk Threads::Threads)
endif()
