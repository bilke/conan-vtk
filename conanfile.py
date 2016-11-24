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
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindVTK.cmake"]
    url="http://github.com/bilke/conan-vtk"
    license="http://www.vtk.org/licensing/"

    ZIP_FOLDER_NAME = "VTK-%s" % version
    INSTALL_DIR = "_install"
    CMAKE_OPTIONS = "-DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF"

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("http://www.vtk.org/files/release/%s/%s" % (self.short_version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        if self.settings.os == "Linux":
            self.run("sudo apt-get update && sudo apt-get install -y \
                freeglut3-dev \
                mesa-common-dev \
                mesa-utils-extra \
                libgl1-mesa-dev \
                libglapi-mesa")
        CMAKE_OPTIONALS = ""
        BUILD_OPTIONALS = ""
        if self.options.shared == False:
            CMAKE_OPTIONALS += "-DBUILD_SHARED_LIBS=OFF"
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
            BUILD_OPTIONALS = "-- /maxcpucount"
        else:
            self.run("mkdir _build")
            if self.settings.os == "Macos":
                BUILD_OPTIONALS = "-- -j $(sysctl -n hw.ncpu)"
            else:
                BUILD_OPTIONALS = " -- -j $(nproc)"
        cd_build = "cd _build"
        self.run("%s && cmake .. -DCMAKE_INSTALL_PREFIX=../%s %s %s %s" % (cd_build, self.INSTALL_DIR, self.CMAKE_OPTIONS, CMAKE_OPTIONALS, cmake.command_line))
        self.run("%s && cmake --build . %s %s" % (cd_build, cmake.build_config, BUILD_OPTIONALS))
        self.run("%s && cmake --build . --target install %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy("FindVTK.cmake", ".", ".")
        self.copy("*", dst=".", src=self.INSTALL_DIR)

    def package_info(self):
        libs = [
            "vtkalglib-%s" % self.short_version,
            "vtkChartsCore-%s" % self.short_version,
            "vtkCommonColor-%s" % self.short_version,
            "vtkCommonComputationalGeometry-%s" % self.short_version,
            "vtkCommonCore-%s" % self.short_version,
            "vtkCommonDataModel-%s" % self.short_version,
            "vtkCommonExecutionModel-%s" % self.short_version,
            "vtkCommonMath-%s" % self.short_version,
            "vtkCommonMisc-%s" % self.short_version,
            "vtkCommonSystem-%s" % self.short_version,
            "vtkCommonTransforms-%s" % self.short_version,
            "vtkDICOMParser-%s" % self.short_version,
            "vtkDomainsChemistry-%s" % self.short_version,
            "vtkDomainsChemistryOpenGL2-%s" % self.short_version,
            "vtkexoIIc-%s" % self.short_version,
            "vtkexpat-%s" % self.short_version,
            "vtkFiltersAMR-%s" % self.short_version,
            "vtkFiltersCore-%s" % self.short_version,
            "vtkFiltersExtraction-%s" % self.short_version,
            "vtkFiltersFlowPaths-%s" % self.short_version,
            "vtkFiltersGeneral-%s" % self.short_version,
            "vtkFiltersGeneric-%s" % self.short_version,
            "vtkFiltersGeometry-%s" % self.short_version,
            "vtkFiltersHybrid-%s" % self.short_version,
            "vtkFiltersHyperTree-%s" % self.short_version,
            "vtkFiltersImaging-%s" % self.short_version,
            "vtkFiltersModeling-%s" % self.short_version,
            "vtkFiltersParallel-%s" % self.short_version,
            "vtkFiltersParallelImaging-%s" % self.short_version,
            "vtkFiltersProgrammable-%s" % self.short_version,
            "vtkFiltersSelection-%s" % self.short_version,
            "vtkFiltersSMP-%s" % self.short_version,
            "vtkFiltersSources-%s" % self.short_version,
            "vtkFiltersStatistics-%s" % self.short_version,
            "vtkFiltersTexture-%s" % self.short_version,
            "vtkFiltersVerdict-%s" % self.short_version,
            "vtkfreetype-%s" % self.short_version,
            "vtkGeovisCore-%s" % self.short_version,
            "vtkglew-%s" % self.short_version,
            "vtkhdf5_hl-%s" % self.short_version,
            "vtkhdf5-%s" % self.short_version,
            "vtkImagingColor-%s" % self.short_version,
            "vtkImagingCore-%s" % self.short_version,
            "vtkImagingFourier-%s" % self.short_version,
            "vtkImagingGeneral-%s" % self.short_version,
            "vtkImagingHybrid-%s" % self.short_version,
            "vtkImagingMath-%s" % self.short_version,
            "vtkImagingMorphological-%s" % self.short_version,
            "vtkImagingSources-%s" % self.short_version,
            "vtkImagingStatistics-%s" % self.short_version,
            "vtkImagingStencil-%s" % self.short_version,
            "vtkInfovisCore-%s" % self.short_version,
            "vtkInfovisLayout-%s" % self.short_version,
            "vtkInteractionImage-%s" % self.short_version,
            "vtkInteractionStyle-%s" % self.short_version,
            "vtkInteractionWidgets-%s" % self.short_version,
            "vtkIOAMR-%s" % self.short_version,
            "vtkIOCore-%s" % self.short_version,
            "vtkIOEnSight-%s" % self.short_version,
            "vtkIOExodus-%s" % self.short_version,
            "vtkIOExport-%s" % self.short_version,
            "vtkIOGeometry-%s" % self.short_version,
            "vtkIOImage-%s" % self.short_version,
            "vtkIOImport-%s" % self.short_version,
            "vtkIOInfovis-%s" % self.short_version,
            "vtkIOLegacy-%s" % self.short_version,
            "vtkIOLSDyna-%s" % self.short_version,
            "vtkIOMINC-%s" % self.short_version,
            "vtkIOMovie-%s" % self.short_version,
            "vtkIONetCDF-%s" % self.short_version,
            "vtkIOParallel-%s" % self.short_version,
            "vtkIOParallelXML-%s" % self.short_version,
            "vtkIOPLY-%s" % self.short_version,
            "vtkIOSQL-%s" % self.short_version,
            "vtkIOVideo-%s" % self.short_version,
            "vtkIOXML-%s" % self.short_version,
            "vtkIOXMLParser-%s" % self.short_version,
            "vtkjpeg-%s" % self.short_version,
            "vtkjsoncpp-%s" % self.short_version,
            "vtklibxml2-%s" % self.short_version,
            "vtkmetaio-%s" % self.short_version,
            "vtkNetCDF_cxx-%s" % self.short_version,
            "vtkNetCDF-%s" % self.short_version,
            "vtkoggtheora-%s" % self.short_version,
            "vtkParallelCore-%s" % self.short_version,
            "vtkpng-%s" % self.short_version,
            "vtkproj4-%s" % self.short_version,
            "vtkRenderingAnnotation-%s" % self.short_version,
            "vtkRenderingContext2D-%s" % self.short_version,
            "vtkRenderingContextOpenGL2-%s" % self.short_version,
            "vtkRenderingCore-%s" % self.short_version,
            "vtkRenderingFreeType-%s" % self.short_version,
            "vtkRenderingImage-%s" % self.short_version,
            "vtkRenderingLabel-%s" % self.short_version,
            "vtkRenderingLOD-%s" % self.short_version,
            "vtkRenderingOpenGL2-%s" % self.short_version,
            "vtkRenderingVolume-%s" % self.short_version,
            "vtkRenderingVolumeOpenGL2-%s" % self.short_version,
            "vtksqlite-%s" % self.short_version,
            "vtksys-%s" % self.short_version,
            "vtktiff-%s" % self.short_version,
            "vtkverdict-%s" % self.short_version,
            "vtkViewsContext2D-%s" % self.short_version,
            "vtkViewsCore-%s" % self.short_version,
            "vtkViewsInfovis-%s" % self.short_version,
            "vtkzlib-%s" % self.short_version
        ]
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version,
            "include/vtk-%s/vtknetcdf/include" % self.short_version,
        ]
