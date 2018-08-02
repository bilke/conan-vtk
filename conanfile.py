import os
from conans import ConanFile, CMake, tools


class VTKConan(ConanFile):
    name = "VTK"
    version = "8.1.1"
    description = "Visualization Toolkit by Kitware"
    url = "http://github.com/bilke/conan-vtk"
    license = "MIT"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    exports = ["LICENSE.md", "CMakeLists.txt", "FindVTK.cmake"]
    source_subfolder = "source_subfolder"
    options = {"shared": [True, False], "qt": [True, False], "mpi": [True, False],
               "fPIC": [True, False], "minimal": [True, False], "ioxml": [True, False]}
    default_options = ("shared=False", "qt=False", "mpi=False", "fPIC=False",
        "minimal=False", "ioxml=False")

    short_paths = True

    version_split = version.split('.')
    short_version = "%s.%s" % (version_split[0], version_split[1])

    def source(self):
        tools.get("http://www.vtk.org/files/release/{0}/{1}-{2}.tar.gz"
                  .format(self.short_version, self.name, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def requirements(self):
        if self.options.qt:
            self.requires("Qt/5.11.0@bilke/stable")
            self.options["Qt"].opengl = "dynamic"
            if tools.os_info.is_linux:
                self.options["Qt"].qtx11extras = True

    def system_requirements(self):
        pack_names = None
        if tools.os_info.linux_distro == "ubuntu" and not self.options.minimal:
            pack_names = [
                "freeglut3-dev",
                "mesa-common-dev",
                "mesa-utils-extra",
                "libgl1-mesa-dev",
                "libglapi-mesa",
                "libsm-dev",
                "libx11-dev",
                "libxext-dev",
                "libxt-dev",
                "libglu1-mesa-dev"]

        if pack_names:
            installer = tools.SystemPackageTool()
            installer.update()  # Update the package database
            installer.install(" ".join(pack_names))  # Install the package

    def config_options(self):
        if self.settings.compiler == "Visual Studio":
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = "OFF"
        cmake.definitions["BUILD_EXAMPLES"] = "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        if self.options.minimal:
            cmake.definitions["VTK_Group_StandAlone"] = "OFF"
            cmake.definitions["VTK_Group_Rendering"] = "OFF"
        if self.options.ioxml:
            cmake.definitions["Module_vtkIOXML"] = "ON"
        if self.options.qt:
            cmake.definitions["VTK_Group_Qt"] = "ON"
            cmake.definitions["VTK_QT_VERSION"] = "5"
            cmake.definitions["VTK_BUILD_QT_DESIGNER_PLUGIN"] = "OFF"
        cmake.definitions["VTK_Group_MPI"] = self.options.mpi

        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"

        if self.settings.os == 'Macos':
            self.env['DYLD_LIBRARY_PATH'] = os.path.join(self.build_folder, 'lib')
            self.output.info("cmake build: %s" % self.build_folder)
            #os.environ['DYLD_LIBRARY_PATH'] = os.path.join(self.build_folder, 'lib') # + os.pathsep + os.environ['DYLD_LIBRARY_PATH']
            #self.output.info("DYLD_LIBRARY_PATH=%s" % (os.environ['DYLD_LIBRARY_PATH']))

        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version,
            "include/vtk-%s/vtknetcdf/include" % self.short_version,
            "include/vtk-%s/vtknetcdfcpp" % self.short_version
        ]

        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('pthread')
