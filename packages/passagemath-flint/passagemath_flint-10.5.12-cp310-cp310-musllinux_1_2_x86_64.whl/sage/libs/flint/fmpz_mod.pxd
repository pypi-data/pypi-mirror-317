# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/fmpz_mod.h

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
    void fmpz_mod_ctx_init(fmpz_mod_ctx_t ctx, const fmpz_t n) noexcept
    void fmpz_mod_ctx_clear(fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_ctx_set_modulus(fmpz_mod_ctx_t ctx, const fmpz_t n) noexcept
    void fmpz_mod_set_fmpz(fmpz_t a, const fmpz_t b, const fmpz_mod_ctx_t ctx) noexcept
    bint fmpz_mod_is_canonical(const fmpz_t a, const fmpz_mod_ctx_t ctx) noexcept
    bint fmpz_mod_is_one(const fmpz_t a, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_add(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_add_fmpz(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_add_ui(fmpz_t a, const fmpz_t b, ulong c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_add_si(fmpz_t a, const fmpz_t b, slong c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_sub(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_sub_fmpz(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_sub_ui(fmpz_t a, const fmpz_t b, ulong c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_sub_si(fmpz_t a, const fmpz_t b, slong c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_fmpz_sub(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_ui_sub(fmpz_t a, ulong b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_si_sub(fmpz_t a, slong b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_neg(fmpz_t a, const fmpz_t b, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_mul(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_inv(fmpz_t a, const fmpz_t b, const fmpz_mod_ctx_t ctx) noexcept
    int fmpz_mod_divides(fmpz_t a, const fmpz_t b, const fmpz_t c, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_pow_ui(fmpz_t a, const fmpz_t b, ulong e, const fmpz_mod_ctx_t ctx) noexcept
    int fmpz_mod_pow_fmpz(fmpz_t a, const fmpz_t b, const fmpz_t e, const fmpz_mod_ctx_t ctx) noexcept
    void fmpz_mod_discrete_log_pohlig_hellman_init(fmpz_mod_discrete_log_pohlig_hellman_t L) noexcept
    void fmpz_mod_discrete_log_pohlig_hellman_clear(fmpz_mod_discrete_log_pohlig_hellman_t L) noexcept
    double fmpz_mod_discrete_log_pohlig_hellman_precompute_prime(fmpz_mod_discrete_log_pohlig_hellman_t L, const fmpz_t p) noexcept
    const fmpz * fmpz_mod_discrete_log_pohlig_hellman_primitive_root(fmpz_mod_discrete_log_pohlig_hellman_t L) noexcept
    void fmpz_mod_discrete_log_pohlig_hellman_run(fmpz_t x, const fmpz_mod_discrete_log_pohlig_hellman_t L, const fmpz_t y) noexcept
    int fmpz_next_smooth_prime(fmpz_t a, const fmpz_t b) noexcept
