# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geant4(CMakePackage):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url = "https://gitlab.cern.ch/geant4/geant4/-/archive/v10.7.1/geant4-v10.7.1.tar.gz"

    tags = ["hep"]

    executables = ["^geant4-config$"]

    maintainers = ["drbenmorgan"]

    version("11.0.2", sha256="661e1ab6f42e58910472d771e76ffd16a2b411398eed70f39808762db707799e")
    version("11.0.1", sha256="fa76d0774346b7347b1fb1424e1c1e0502264a83e185995f3c462372994f84fa")
    version("11.0.0", sha256="04d11d4d9041507e7f86f48eb45c36430f2b6544a74c0ccaff632ac51d9644f1")
    version(
        "10.7.3",
        sha256="8615d93bd4178d34f31e19d67bc81720af67cdab1c8425af8523858dcddcf65b",
        preferred=True,
    )
    version("10.7.2", sha256="593fc85883a361487b17548ba00553501f66a811b0a79039276bb75ad59528cf")
    version("10.7.1", sha256="2aa7cb4b231081e0a35d84c707be8f35e4edc4e97aad2b233943515476955293")
    version("10.7.0", sha256="c991a139210c7f194720c900b149405090058c00beb5a0d2fac5c40c42a262d4")
    version("10.6.3", sha256="bf96d6d38e6a0deabb6fb6232eb00e46153134da645715d636b9b7b4490193d3")
    version("10.6.2", sha256="e381e04c02aeade1ed8cdd9fdbe7dcf5d6f0f9b3837a417976b839318a005dbd")
    version("10.6.1", sha256="4fd64149ae26952672a81ce5579d3806fda4bd251d486897093ac57633a42b7e")
    version("10.6.0", sha256="eebe6a170546064ff81ab3b00f513ccd1d4122a026514982368d503ac55a4ee4")
    version("10.5.1", sha256="2397eb859dc4de095ff66059d8bda9f060fdc42e10469dd7890946293eeb0e39")
    version("10.4.3", sha256="67f3bb6405a2c77e573936c2b933f5a4a33915aa379626a2eb3012009b91e1da")
    version("10.4.0", sha256="e919b9b0a88476e00c0b18ab65d40e6a714b55ee4778f66bac32a5396c22aa74")
    version("10.3.3", sha256="bcd36a453da44de9368d1d61b0144031a58e4b43a6d2d875e19085f2700a89d8")

    _cxxstd_values = ("11", "14", "17")
    variant(
        "cxxstd",
        default=_cxxstd_values[0],
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    conflicts("cxxstd=11", when="@11:", msg="geant4@11: only supports cxxstd=17")
    conflicts("cxxstd=14", when="@11:", msg="geant4@11: only supports cxxstd=17")

    variant("threads", default=True, description="Build with multithreading")
    variant("vecgeom", default=False, description="Enable vecgeom support")
    variant("opengl", default=False, description="Optional OpenGL support")
    variant("x11", default=False, description="Optional X11 support")
    variant("motif", default=False, description="Optional motif support")
    variant("qt", default=False, description="Enable Qt support")
    variant("python", default=False, when="@10.6.2:", description="Enable Python bindings")
    variant("tbb", default=False, description="Use TBB as a tasking backend", when="@11:")
    variant("vtk", default=False, description="Enable VTK support", when="@11:")

    depends_on("cmake@3.16:", type="build", when="@11.0.0:")
    depends_on("cmake@3.8:", type="build", when="@10.6.0:")
    depends_on("cmake@3.5:", type="build")

    for _vers in [
        "10.3.3",
        "10.4.0",
        "10.4.3",
        "10.5.1",
        "10.6.0",
        "10.6.1",
        "10.6.2",
        "10.6.3",
        "10.7.0",
        "10.7.1",
        "10.7.2",
        "10.7.3",
        "11.0:",
    ]:
        depends_on("geant4-data@" + _vers, type="run", when="@" + _vers)

    depends_on("expat")
    depends_on("zlib")

    depends_on("tbb", when="+tbb")
    depends_on("vtk@8.2:", when="+vtk")

    # Python, with boost requirement dealt with in cxxstd section
    depends_on("python@3:", when="+python")
    extends("python", when="+python")

    for std in _cxxstd_values:
        # CLHEP version requirements to be reviewed
        depends_on("clhep@2.4.5.1: cxxstd=" + std, when="@11.0.0: cxxstd=" + std)

        depends_on("clhep@2.4.4.0: cxxstd=" + std, when="@10.7.0: cxxstd=" + std)

        depends_on("clhep@2.3.3.0: cxxstd=" + std, when="@10.3.3:10.6 cxxstd=" + std)

        # Spack only supports Xerces-c 3 and above, so no version req
        depends_on("xerces-c netaccessor=curl cxxstd=" + std, when="cxxstd=" + std)

        # Vecgeom specific versions for each Geant4 version
        depends_on("vecgeom@1.1.18:1.1 cxxstd=" + std, when="@11.0.0: +vecgeom cxxstd=" + std)
        depends_on("vecgeom@1.1.8:1.1 cxxstd=" + std, when="@10.7.0: +vecgeom cxxstd=" + std)
        depends_on("vecgeom@1.1.5 cxxstd=" + std, when="@10.6.0:10.6 +vecgeom cxxstd=" + std)
        depends_on("vecgeom@1.1.0 cxxstd=" + std, when="@10.5.0:10.5 +vecgeom cxxstd=" + std)
        depends_on("vecgeom@0.5.2 cxxstd=" + std, when="@10.4.0:10.4 +vecgeom cxxstd=" + std)
        depends_on("vecgeom@0.3rc cxxstd=" + std, when="@10.3.0:10.3 +vecgeom cxxstd=" + std)

        # Boost.python, conflict handled earlier
        depends_on("boost@1.70: +python cxxstd=" + std, when="+python cxxstd=" + std)

    # Visualization driver dependencies
    depends_on("gl", when="+opengl")
    depends_on("glu", when="+opengl")
    depends_on("glx", when="+opengl+x11")
    depends_on("libx11", when="+x11")
    depends_on("libxmu", when="+x11")
    depends_on("motif", when="+motif")
    depends_on("qt@5: +opengl", when="+qt")

    # As released, 10.03.03 has issues with respect to using external
    # CLHEP.
    patch("CLHEP-10.03.03.patch", level=1, when="@10.3.3")
    # These patches can be applied independent of the cxxstd value?
    patch("cxx17.patch", when="@:10.3 cxxstd=17")
    patch("cxx17_geant4_10_0.patch", level=1, when="@10.4.0 cxxstd=17")
    patch("geant4-10.4.3-cxx17-removed-features.patch", level=1, when="@10.4.3 cxxstd=17")

    # NVHPC: "thread-local declaration follows non-thread-local declaration"
    conflicts("%nvhpc", when="+threads")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # We already get the correct format
        return output.strip()

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants = []
        cxxstd = Executable(exes[0])("--cxxstd", output=str, error=str)
        # output will be something like c++17, we only want the number
        variants.append("cxxstd={}".format(cxxstd[-3:]))

        def _has_feature(feature):
            res = Executable(exes[0])("--has-feature", feature, output=str, error=str)
            return res.strip() == "yes"

        def _add_variant(feature, variant):
            """Helper to determine whether a given feature is present and append the
            corresponding variant to the list"""
            if _has_feature(feature):
                variants.append("+{}".format(variant))
            else:
                variants.append("~{}".format(variant))

        _add_variant("qt", "qt")
        _add_variant("motif", "motif")
        _add_variant("multithreading", "threads")
        _add_variant("usolids", "vecgeom")

        if _has_feature("opengl-x11"):
            variants.append("+opengl")
            variants.append("+x11")
        else:
            variants.append("~opengl")
            # raytracer-x11 could still lead to the activation of the x11
            # variant without +opengl
            _add_variant("raytracer-x11", "x11")

        # TODO: The following variants cannot be determined from geant4-config.
        # - python
        # - tbb
        # - vtk
        # Should we have a (version dependent) warning message for these?

        return " ".join(variants)

    def flag_handler(self, name, flags):
        spec = self.spec
        if name == "cxxflags":
            if spec.satisfies("%nvhpc"):
                # error: excessive recursion at instantiation of class
                # "G4Number<191>" (G4CTCounter.hh)
                flags.append("-Wc,--pending_instantiations=256")
                return (None, flags, None)
        return (flags, None, None)

    def cmake_args(self):
        spec = self.spec

        # Core options
        options = [
            self.define("GEANT4_USE_SYSTEM_CLHEP", True),
            self.define("GEANT4_USE_SYSTEM_EXPAT", True),
            self.define("GEANT4_USE_SYSTEM_ZLIB", True),
            self.define("GEANT4_USE_G3TOG4", True),
            self.define("GEANT4_USE_GDML", True),
            self.define("XERCESC_ROOT_DIR", spec["xerces-c"].prefix),
        ]

        # Use the correct C++ standard option for the requested version
        if spec.version >= Version("11.0"):
            options.append(self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"))
        else:
            options.append(self.define_from_variant("GEANT4_BUILD_CXXSTD", "cxxstd"))

        if spec.version >= Version("10.6"):
            # When building a downstream library/app outside of Spack, make
            # sure that Geant4's dependencies are found
            options.append(self.define("GEANT4_INSTALL_PACKAGE_CACHE", True))

        # Multithreading
        options.append(self.define_from_variant("GEANT4_BUILD_MULTITHREADED", "threads"))
        options.append(self.define_from_variant("GEANT4_USE_TBB", "tbb"))

        if "+threads" in spec:
            # Locked at global-dynamic to allow use cases that load the
            # geant4 libs at application runtime
            options.append("-DGEANT4_BUILD_TLS_MODEL=global-dynamic")

        # Never install the data with geant4, but point to the dependent
        # geant4-data's install directory to correctly set up the
        # Geant4Config.cmake values for Geant4_DATASETS .
        options.append(self.define("GEANT4_INSTALL_DATA", False))
        options.append(self.define("GEANT4_INSTALL_DATADIR", self.datadir))

        # Vecgeom
        if "+vecgeom" in spec:
            options.append(self.define("GEANT4_USE_USOLIDS", True))
            options.append(self.define("USolids_DIR", spec["vecgeom"].prefix.lib.CMake.USolids))

        # Visualization options
        if "platform=darwin" not in spec:
            if "+x11" in spec and "+opengl" in spec:
                options.append(self.define("GEANT4_USE_OPENGL_X11", True))
            if "+motif" in spec and "+opengl" in spec:
                options.append(self.define("GEANT4_USE_XM", True))
            if "+x11" in spec:
                options.append(self.define("GEANT4_USE_RAYTRACER_X11", True))

        if "+qt" in spec:
            options.append(self.define("GEANT4_USE_QT", True))
            options.append(self.define("QT_QMAKE_EXECUTABLE", spec["qt"].prefix.bin.qmake))

        options.append(self.define_from_variant("GEANT4_USE_VTK", "vtk"))

        # Python
        if spec.version > Version("10.6.1"):
            options.append(self.define_from_variant("GEANT4_USE_PYTHON", "python"))

        return options

    @property
    def datadir(self):
        dataspec = self.spec["geant4-data"]
        return join_path(
            dataspec.prefix.share, "{0}-{1}".format(dataspec.name, dataspec.version.dotted)
        )
