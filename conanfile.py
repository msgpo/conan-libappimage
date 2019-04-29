from conans import ConanFile, CMake, tools
import os


class LibappimageConan(ConanFile):
    name = "libappimage"
    version = "1.0.0"
    license = "[LICENSE]"
    author = "Alexis Lopez Zubieta <contact@azubieta.net>"
    url = "https://github.com/appimage-conan-community/conan-libappimage"
    description = "Core library of the AppImage project. Reference implementation of the AppImage specification."
    topics = ("appimage",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = ("cmake", "pkg_config")
    build_requires = ("gtest/1.8.1@bincrafters/stable",
                      "cmake_installer/3.13.0@conan/stable")
    exports_sources = "patches/*"

    def requirements(self):
        self.requires("squashfuse/0.1.103@appimage-conan-community/stable", "private")
        self.requires("libarchive/3.3.3@appimage-conan-community/stable", "private")
        self.requires("xdg-utils-cxx/0.1.1@appimage-conan-community/stable", "private")
        self.requires("cairo/1.15.14@bincrafters/stable")
        # self.requires("glib/2.57.1@bincrafters/stable")
        self.requires("zlib/1.2.11@conan/stable")
        self.requires("boost_filesystem/1.69.0@bincrafters/stable")
        self.requires("boost_algorithm/1.69.0@bincrafters/stable")
        self.requires("boost_iostreams/1.69.0@bincrafters/stable")
        self.requires("cmake_findboost_modular/1.69.0@bincrafters/stable")

    def configure(self):
        self.options["squashfuse"].shared = False
        self.options["libarchive"].shared = False
        self.options["xdg-utils-cxx"].shared = False
        self.options["xdg-utils-cxx"].fPIC = True
        self.options["cairo"].shared = True
        # self.options["glib"].shared = True
        self.options["zlib"].shared = True

    def source(self):
        self.run("git clone https://github.com/AppImage/libappimage.git --branch=v1.0.0")
        tools.patch(base_path="libappimage", patch_file="patches/use_conan.patch")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_CONAN"] = True
        cmake.definitions["USE_SYSTEM_XZ"] = True
        cmake.definitions["USE_SYSTEM_SQUASHFUSE"] = True
        cmake.definitions["USE_SYSTEM_LIBARCHIVE"] = True
        cmake.definitions["USE_SYSTEM_BOOST"] = True
        cmake.definitions["USE_SYSTEM_XDGUTILS"] = True
        cmake.definitions["BUILD_TESTING"] = False
        cmake.configure(source_folder="libappimage")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.builddirs = ["lib/cmake/libappimage/"]
        common_libs = ["appimage_shared"]
        if (self.options["shared"]):
            self.cpp_info.libs = ["appimage"] + common_libs
        else:
            self.cpp_info.libs = ["appimage_static"] + common_libs
