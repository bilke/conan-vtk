from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "bilke")

class VTKReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "VTK/7.0.0@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake . %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run(os.sep.join([".","bin", "myvtk"]))
