# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/profiler.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# From the commit 3e2c3a3e091106a25ca9c6fba28e02f2cbcd654a
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    void timeit_start(timeit_t t) noexcept
    void timeit_stop(timeit_t t) noexcept
    void start_clock(int n) noexcept
    void stop_clock(int n) noexcept
    double get_clock(int n) noexcept
    void prof_repeat(double * min, double * max, profile_target_t target, void * arg) noexcept
    void get_memory_usage(meminfo_t meminfo) noexcept
