from conans import ConanFile, CMake

class HelloConan(ConanFile):
    name = "Hello"
    version = "0.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    exports = ["CMakeLists.txt"]
    url="http://github.com/bilke/conan-hello"
    license="none"

    def source(self):
        self.run("git clone https://github.com/memsharded/hello.git")

    def build(self):
        cmake = CMake(self.settings)
        self.run("cmake . %s" % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*.lib", dst="lib", src="hello/lib")
        self.copy("*.a", dst="lib", src="hello/lib")

    def package_info(self):
        self.cpp_info.libs = ["hello"]
