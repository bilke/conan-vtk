project(MyHello)
cmake_minimum_required(VERSION 2.8.12)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(greet main.cpp)
target_link_libraries(greet ${CONAN_LIBS})
