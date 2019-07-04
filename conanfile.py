import os
from conans import ConanFile, CMake, tools

class VTKConan(ConanFile):
    name = "vtk"
    version = "8.2.0"
    description = "Visualization Toolkit by Kitware"
    url = "http://github.com/bilke/conan-vtk"
    license = "MIT"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    exports = ["LICENSE.md", "CMakeLists.txt", "FindVTK.cmake"]
    source_subfolder = "source_subfolder"
    options = {"shared": [True, False], "qt": [True, False], "mpi": [True, False],
               "fPIC": [True, False], "minimal": [True, False], "ioxml": [True, False],
               "ioexport": [True, False], "mpi_minimal": [True, False]}
    default_options = ("shared=False", "qt=False", "mpi=False", "fPIC=False",
        "minimal=False", "ioxml=False", "ioexport=False", "mpi_minimal=False")

    short_paths = True

    version_split = version.split('.')
    short_version = "%s.%s" % (version_split[0], version_split[1])

    def source(self):
        tools.get("https://ogsstorage.blob.core.windows.net/tmp/{0}-{1}.tar.gz"
                  .format(self.name.upper(), self.version))
        extracted_dir = self.name.upper() + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def requirements(self):
        if self.options.qt:
            self.requires("qt/5.12.2@bincrafters/stable")
            self.options["qt"].shared = True
            if tools.os_info.is_linux:
                self.options["qt"].qtx11extras = True

    def _system_package_architecture(self):
        if tools.os_info.with_apt:
            if self.settings.arch == "x86":
                return ':i386'
            elif self.settings.arch == "x86_64":
                return ':amd64'

        if tools.os_info.with_yum:
            if self.settings.arch == "x86":
                return '.i686'
            elif self.settings.arch == 'x86_64':
                return '.x86_64'
        return ""

    def build_requirements(self):
        pack_names = None
        if not self.options.minimal and tools.os_info.is_linux:
            if tools.os_info.with_apt:
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
            for item in pack_names:
                installer.install(item + self._system_package_architecture())

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
        if self.options.ioexport:
            cmake.definitions["Module_vtkIOExport"] = "ON"
        if self.options.qt:
            cmake.definitions["VTK_Group_Qt"] = "ON"
            cmake.definitions["VTK_QT_VERSION"] = "5"
            cmake.definitions["VTK_BUILD_QT_DESIGNER_PLUGIN"] = "OFF"
        if self.options.mpi:
            cmake.definitions["VTK_Group_MPI"] = "ON"
            cmake.definitions["Module_vtkIOParallelXML"] = "ON"
        if self.options.mpi_minimal:
            cmake.definitions["Module_vtkIOParallelXML"] = "ON"
            cmake.definitions["Module_vtkParallelMPI"] = "ON"

        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"

        if self.settings.os == 'Macos':
            self.env['DYLD_LIBRARY_PATH'] = os.path.join(self.build_folder, 'lib')
            self.output.info("cmake build: %s" % self.build_folder)
            #os.environ['DYLD_LIBRARY_PATH'] = os.path.join(self.build_folder, 'lib') # + os.pathsep + os.environ['DYLD_LIBRARY_PATH']
            #self.output.info("DYLD_LIBRARY_PATH=%s" % (os.environ['DYLD_LIBRARY_PATH']))

        cmake.configure(build_folder='build')
        if self.settings.os == 'Macos':
            # run_environment does not work here because it appends path just from
            # requirements, not from this package itself
            # https://docs.conan.io/en/latest/reference/build_helpers/run_environment.html#runenvironment
            lib_path = os.path.join(self.build_folder, 'lib')
            self.run('DYLD_LIBRARY_PATH={0} cmake --build build {1} -j'.format(lib_path, cmake.build_config))
        else:
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
