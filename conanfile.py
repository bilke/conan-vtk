import os
from conans import ConanFile, CMake
from conans.tools import download, unzip

class VTKConan(ConanFile):
    name = "VTK"
    version = "7.1.0"
    version_split = version.split('.')
    short_version = "%s.%s" % (version_split[0], version_split[1])
    SHORT_VERSION = short_version
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "qt": [True, False],"cygwin_msvc": [True, False],"linux_use_sudo": [True, False]}
    default_options = "shared=False", "qt=False", "cygwin_msvc=False", "linux_use_sudo=True"
    exports = ["CMakeLists.txt", "FindVTK.cmake"]
    url="http://github.com/pkarasev3/conan-vtk"
    license="http://www.vtk.org/licensing/"
    short_paths=True

    ZIP_FOLDER_NAME = "VTK-%s" % version
    INSTALL_DIR = "_install"
    CMAKE_OPTIONS = "-DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF -DVTK_Group_StandAlone:BOOL=OFF"

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("http://www.vtk.org/files/release/%s/%s" % (self.short_version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def requirements(self):
        if self.options.qt == True:
            self.requires("Qt/5.6.1-1@osechet/testing")

    def build(self):
        if self.settings.os == "Linux":
            if self.options.linux_use_sudo:
                self.run("sudo apt-get update && sudo apt-get install -y \
                    freeglut3-dev \
                    mesa-common-dev \
                    mesa-utils-extra \
                    libgl1-mesa-dev \
                    libglapi-mesa")
        CMAKE_OPTIONALS = ""
        BUILD_OPTIONALS = ""
        if self.options.shared == False:
            CMAKE_OPTIONALS += " -DBUILD_SHARED_LIBS=OFF"
        if self.options.shared == True:
            CMAKE_OPTIONALS += " -DBUILD_SHARED_LIBS=ON"
        if self.options.qt == True:
            CMAKE_OPTIONALS += " -DVTK_Group_Qt:BOOL=ON -DVTK_QT_VERSION:STRING=5 -DVTK_BUILD_QT_DESIGNER_PLUGIN:BOOL=OFF"
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            if self.options.cygwin_msvc == False:
                self.run("IF not exist _build mkdir _build")
            else:
                self.run("mkdir -p _build")
            BUILD_OPTIONALS = "-- /maxcpucount"
        else:
            self.run("mkdir -p _build")
            if self.settings.os == "Macos":
                BUILD_OPTIONALS = "-- -j $(sysctl -n hw.ncpu)"
            else:
                BUILD_OPTIONALS = " -- -j $(nproc)"
        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            CMAKE_OPTIONALS += " -DCMAKE_DEBUG_POSTFIX=_d"
        cd_build = "cd _build"
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s %s" % (cd_build, self.INSTALL_DIR, self.CMAKE_OPTIONS, CMAKE_OPTIONALS, cmake.command_line))
        self.run("%s && cmake --build . %s %s" % (cd_build, cmake.build_config, BUILD_OPTIONALS))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("FindVTK.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        LIB_POSTFIX = ""
        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            LIB_POSTFIX = "_d"
        libs = [
            "vtkalglib-%s" % self.short_version + LIB_POSTFIX,
            "vtkChartsCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonColor-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonComputationalGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonDataModel-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonExecutionModel-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonMath-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonMisc-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonSystem-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonTransforms-%s" % self.short_version + LIB_POSTFIX,
            "vtkDICOMParser-%s" % self.short_version + LIB_POSTFIX,
            "vtkexpat-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersExtraction-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersFlowPaths-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeneral-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersHybrid-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersImaging-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersModeling-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSources-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersStatistics-%s" % self.short_version + LIB_POSTFIX,
            "vtkfreetype-%s" % self.short_version + LIB_POSTFIX,
            "vtkGeovisCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkglew-%s" % self.short_version + LIB_POSTFIX,
            "vtkhdf5_hl-%s" % self.short_version + LIB_POSTFIX,
            "vtkhdf5-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingColor-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingFourier-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingGeneral-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingHybrid-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingMath-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingMorphological-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingSources-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingStatistics-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingStencil-%s" % self.short_version + LIB_POSTFIX,
            "vtkInfovisCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkInfovisLayout-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionStyle-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionWidgets-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOExport-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOXML-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOXMLParser-%s" % self.short_version + LIB_POSTFIX,
            "vtkjpeg-%s" % self.short_version + LIB_POSTFIX,
            "vtkmetaio-%s" % self.short_version + LIB_POSTFIX,
            "vtkpng-%s" % self.short_version + LIB_POSTFIX,
            "vtkproj4-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingAnnotation-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingContext2D-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingContextOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingFreeType-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingLabel-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingLOD-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingVolume-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingVolumeOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtksys-%s" % self.short_version + LIB_POSTFIX,
            "vtktiff-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsContext2D-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsInfovis-%s" % self.short_version + LIB_POSTFIX,
            "vtkzlib-%s" % self.short_version + LIB_POSTFIX
        ]
        if self.options.qt:
            libs.append("vtkGUISupportQt-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkGUISupportQtSQL-%s" % self.short_version + LIB_POSTFIX)
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version,
        ]
