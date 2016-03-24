import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class VTKConan(ConanFile):
    name = "VTK"
    version = "7.0.0"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    url="http://github.com/bilke/conan-vtk"
    license="http://www.vtk.org/licensing/"

    ZIP_FOLDER_NAME = "VTK-%s" % version
    INSTALL_DIR = "_install"
    CMAKE_OPTIONS = "-DBUILD_TESTING=OFF -DVTK_Group_StandAlone=OFF -DVTK_Group_Rendering=OFF -DModule_vtkCommonDataModel=ON"

    def source(self):
        #self.run("git clone https://github.com/memsharded/hello.git")
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("http://www.vtk.org/files/release/7.0/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        CMAKE_OPTIONALS = ""
        if self.options.shared == False:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=OFF"
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s %s" % (cd_build, self.INSTALL_DIR, self.CMAKE_OPTIONS, CMAKE_OPTIONALS, cmake.command_line))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        libs = ["vtksys-7.0",
                "vtkCommonCore-7.0",
                "vtkCommonDataModel-7.0"]
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = ['include/vtk-7.0']
