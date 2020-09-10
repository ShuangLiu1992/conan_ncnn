from conans import ConanFile, CMake, tools
import os.path


class NCNNConan(ConanFile):
    name = "ncnn"
    version = "20200727"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Hello here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "toolchain.cmake"

    def package(self):
        self.copy("toolchain.cmake")

    def init(self):
        self.source_path = f"{self.name}-{self.version}"

    def source(self):
        tools.download(f"https://github.com/Tencent/ncnn/archive/{self.version}.tar.gz", "src.tar.gz", md5="57f02e7a0888d55b69462d2ad2bd78ea")
        md5 = tools.md5sum("src.tar.gz")
        self.output.success(f"md5: {md5}")
        tools.unzip("src.tar.gz")

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions['NCNN_BUILD_TESTS'] = "OFF"
        cmake.definitions['NCNN_DISABLE_RTTI'] = "OFF"
        cmake.definitions['NCNN_DISABLE_EXCEPTION'] = "OFF"
        cmake.definitions['NCNN_BUILD_TESTS'] = "OFF"
        cmake.definitions['NCNN_BUILD_EXAMPLES'] = "OFF"

        cmake.definitions['CMAKE_TOOLCHAIN_FILE'] = os.path.join(self.source_folder, "toolchain.cmake")

        cmake.configure(source_folder=self.source_path)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include/ncnn/layer", src=f"{self.name}-{self.version}/src/layer")

    def package_info(self):
        self.cpp_info.libs = ["ncnn"]
