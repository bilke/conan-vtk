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
    exports = ["CMakeLists.txt", "FindVTK.cmake"]
    url="http://github.com/bilke/conan-vtk"
    license="http://www.vtk.org/licensing/"

    ZIP_FOLDER_NAME = "VTK-%s" % version
    INSTALL_DIR = "_install"
    CMAKE_OPTIONS = \
        " -DBUILD_TESTING=OFF " + \
        " -DBUILD_EXAMPLES=OFF " + \
        " -DCMAKE_POSITION_INDEPENDENT_CODE=ON " # -fPIC

    def source(self):
        zip_name = self.ZIP_FOLDER_NAME + ".zip"
        download("http://www.vtk.org/files/release/7.0/%s" % zip_name , zip_name)
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
            "vtkalglib-7.0",
            "vtkChartsCore-7.0",
            "vtkCommonColor-7.0",
            "vtkCommonComputationalGeometry-7.0",
            "vtkCommonCore-7.0",
            "vtkCommonDataModel-7.0",
            "vtkCommonExecutionModel-7.0",
            "vtkCommonMath-7.0",
            "vtkCommonMisc-7.0",
            "vtkCommonSystem-7.0",
            "vtkCommonTransforms-7.0",
            "vtkDICOMParser-7.0",
            "vtkDomainsChemistry-7.0",
            "vtkDomainsChemistryOpenGL2-7.0",
            "vtkexoIIc-7.0",
            "vtkexpat-7.0",
            "vtkFiltersAMR-7.0",
            "vtkFiltersCore-7.0",
            "vtkFiltersExtraction-7.0",
            "vtkFiltersFlowPaths-7.0",
            "vtkFiltersGeneral-7.0",
            "vtkFiltersGeneric-7.0",
            "vtkFiltersGeometry-7.0",
            "vtkFiltersHybrid-7.0",
            "vtkFiltersHyperTree-7.0",
            "vtkFiltersImaging-7.0",
            "vtkFiltersModeling-7.0",
            "vtkFiltersParallel-7.0",
            "vtkFiltersParallelImaging-7.0",
            "vtkFiltersProgrammable-7.0",
            "vtkFiltersSelection-7.0",
            "vtkFiltersSMP-7.0",
            "vtkFiltersSources-7.0",
            "vtkFiltersStatistics-7.0",
            "vtkFiltersTexture-7.0",
            "vtkFiltersVerdict-7.0",
            "vtkfreetype-7.0",
            "vtkGeovisCore-7.0",
            "vtkglew-7.0",
            "vtkhdf5_hl-7.0",
            "vtkhdf5-7.0",
            "vtkImagingColor-7.0",
            "vtkImagingCore-7.0",
            "vtkImagingFourier-7.0",
            "vtkImagingGeneral-7.0",
            "vtkImagingHybrid-7.0",
            "vtkImagingMath-7.0",
            "vtkImagingMorphological-7.0",
            "vtkImagingSources-7.0",
            "vtkImagingStatistics-7.0",
            "vtkImagingStencil-7.0",
            "vtkInfovisCore-7.0",
            "vtkInfovisLayout-7.0",
            "vtkInteractionImage-7.0",
            "vtkInteractionStyle-7.0",
            "vtkInteractionWidgets-7.0",
            "vtkIOAMR-7.0",
            "vtkIOCore-7.0",
            "vtkIOEnSight-7.0",
            "vtkIOExodus-7.0",
            "vtkIOExport-7.0",
            "vtkIOGeometry-7.0",
            "vtkIOImage-7.0",
            "vtkIOImport-7.0",
            "vtkIOInfovis-7.0",
            "vtkIOLegacy-7.0",
            "vtkIOLSDyna-7.0",
            "vtkIOMINC-7.0",
            "vtkIOMovie-7.0",
            "vtkIONetCDF-7.0",
            "vtkIOParallel-7.0",
            "vtkIOParallelXML-7.0",
            "vtkIOPLY-7.0",
            "vtkIOSQL-7.0",
            "vtkIOVideo-7.0",
            "vtkIOXML-7.0",
            "vtkIOXMLParser-7.0",
            "vtkjpeg-7.0",
            "vtkjsoncpp-7.0",
            "vtklibxml2-7.0",
            "vtkmetaio-7.0",
            "vtkNetCDF_cxx-7.0",
            "vtkNetCDF-7.0",
            "vtkoggtheora-7.0",
            "vtkParallelCore-7.0",
            "vtkpng-7.0",
            "vtkproj4-7.0",
            "vtkRenderingAnnotation-7.0",
            "vtkRenderingContext2D-7.0",
            "vtkRenderingContextOpenGL2-7.0",
            "vtkRenderingCore-7.0",
            "vtkRenderingFreeType-7.0",
            "vtkRenderingImage-7.0",
            "vtkRenderingLabel-7.0",
            "vtkRenderingLOD-7.0",
            "vtkRenderingOpenGL2-7.0",
            "vtkRenderingVolume-7.0",
            "vtkRenderingVolumeOpenGL2-7.0",
            "vtksqlite-7.0",
            "vtksys-7.0",
            "vtktiff-7.0",
            "vtkverdict-7.0",
            "vtkViewsContext2D-7.0",
            "vtkViewsCore-7.0",
            "vtkViewsInfovis-7.0",
            "vtkzlib-7.0"
        ]
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = [
            'include/vtk-7.0',
            'include/vtk-7.0/vtknetcdf/include',
        ]
