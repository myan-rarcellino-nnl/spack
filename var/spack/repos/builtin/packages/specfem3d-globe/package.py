# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Specfem3dGlobe(AutotoolsPackage, CudaPackage):
    """Program specfem3D from SPECFEM3D_GLOBE is
    a 3-D spectral-element solver for the Earth.
    It uses a mesh generated by program meshfem3D."""

    homepage = "https://github.com/geodynamics/specfem3d_globe"
    url = "https://github.com/geodynamics/specfem3d_globe/archive/v7.0.2.tar.gz"

    version("7.0.2", sha256="78b4cfbe4e5121927ab82a8c2e821b65cdfff3e94d017303bf21af7805186d9b")

    variant("opencl", default=False, description="Build with OpenCL code generator")
    variant("openmp", default=True, description="Build with OpenMP code generator")
    variant("double-precision", default=False, description="Treat REAL as double precision")

    depends_on("mpi")
    depends_on("opencl", when="+opencl")

    # When building with the gcc compiler,'Werror' is added to FFLAGS.
    # In the case of using the gcc compiler and the default simulation
    # settings, there is the process which always causes
    # array out-of-bounds reference error.
    # This issue will be fixed in version 8.0.0,
    # so, remove '-Werror' when building with gcc compiler
    # in versions up to 7.0.2 of specfem3d-globe.
    # https://github.com/geodynamics/specfem3d_globe/issues/717
    patch("gcc_rm_werror.patch", when="@:7.0.2%gcc")

    def configure_args(self):
        args = []

        if "+cuda" in self.spec:
            args.append("--with-cuda")
            args.append("CUDA_LIB={0}".format(spec["cuda"].libs.directories[0]))
            args.append("CUDA_INC={0}".format(spec["cuda"].prefix.include))
            args.append("MPI_INC={0}".format(spec["mpi"].prefix.include))
        if "+opencl" in self.spec:
            args.append("--with-opencl")
            args.append("OCL_LIB={0}".format(spec["opencl"].libs.directories[0]))
            args.append("OCL_INC={0}".format(spec["opencl"].prefix.include))

        args.extend(self.enable_or_disable("openmp"))
        args.extend(self.enable_or_disable("double-precision"))

        return args

    def install(self, spec, prefix):
        install_tree(".", prefix)
