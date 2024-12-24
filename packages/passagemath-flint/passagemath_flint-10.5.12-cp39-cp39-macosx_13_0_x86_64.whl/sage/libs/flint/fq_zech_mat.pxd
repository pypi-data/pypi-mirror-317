# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/fq_zech_mat.h

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
    void fq_zech_mat_init(fq_zech_mat_t mat, slong rows, slong cols, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_init_set(fq_zech_mat_t mat, const fq_zech_mat_t src, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_clear(fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_set(fq_zech_mat_t mat, const fq_zech_mat_t src, const fq_zech_ctx_t ctx) noexcept
    fq_zech_struct * fq_zech_mat_entry(const fq_zech_mat_t mat, slong i, slong j) noexcept
    void fq_zech_mat_entry_set(fq_zech_mat_t mat, slong i, slong j, const fq_zech_t x, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_nrows(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_ncols(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_swap(fq_zech_mat_t mat1, fq_zech_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_swap_entrywise(fq_zech_mat_t mat1, fq_zech_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_zero(fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_one(fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_set_nmod_mat(fq_zech_mat_t mat1, const nmod_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_set_fmpz_mod_mat(fq_zech_mat_t mat1, const fmpz_mod_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_concat_vertical(fq_zech_mat_t res, const fq_zech_mat_t mat1, const fq_zech_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_concat_horizontal(fq_zech_mat_t res, const fq_zech_mat_t mat1, const fq_zech_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_print_pretty(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_fprint_pretty(FILE * file, const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_print(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_fprint(FILE * file, const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_window_init(fq_zech_mat_t window, const fq_zech_mat_t mat, slong r1, slong c1, slong r2, slong c2, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_window_clear(fq_zech_mat_t window, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_randtest(fq_zech_mat_t mat, flint_rand_t state, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_randpermdiag(fq_zech_mat_t mat, flint_rand_t state, fq_zech_struct * diag, slong n, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_randrank(fq_zech_mat_t mat, flint_rand_t state, slong rank, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_randops(fq_zech_mat_t mat, slong count, flint_rand_t state, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_randtril(fq_zech_mat_t mat, flint_rand_t state, int unit, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_randtriu(fq_zech_mat_t mat, flint_rand_t state, int unit, const fq_zech_ctx_t ctx) noexcept
    bint fq_zech_mat_equal(const fq_zech_mat_t mat1, const fq_zech_mat_t mat2, const fq_zech_ctx_t ctx) noexcept
    bint fq_zech_mat_is_zero(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    bint fq_zech_mat_is_one(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    bint fq_zech_mat_is_empty(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    bint fq_zech_mat_is_square(const fq_zech_mat_t mat, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_add(fq_zech_mat_t C, const fq_zech_mat_t A, const fq_zech_mat_t B,  const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_sub(fq_zech_mat_t C, const fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_neg(fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_mul(fq_zech_mat_t C, const fq_zech_mat_t A, const fq_zech_mat_t B,  const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_mul_classical(fq_zech_mat_t C, const fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_mul_KS(fq_zech_mat_t C, const fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_submul(fq_zech_mat_t D, const fq_zech_mat_t C, const fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_mul_vec(fq_zech_struct * c, const fq_zech_mat_t A, const fq_zech_struct * b, slong blen, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_mul_vec_ptr(fq_zech_struct * const * c, const fq_zech_mat_t A, const fq_zech_struct * const * b, slong blen, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_vec_mul(fq_zech_struct * c, const fq_zech_struct * a, slong alen, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_vec_mul_ptr(fq_zech_struct * const * c, const fq_zech_struct * const * a, slong alen, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_lu(slong * P, fq_zech_mat_t A, int rank_check, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_lu_classical(slong * P, fq_zech_mat_t A, int rank_check, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_lu_recursive(slong * P, fq_zech_mat_t A, int rank_check, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_rref(fq_zech_mat_t A, const fq_zech_ctx_t ctx) noexcept
    slong fq_zech_mat_reduce_row(fq_zech_mat_t A, slong * P, slong * L, slong n, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_solve_tril(fq_zech_mat_t X, const fq_zech_mat_t L, const fq_zech_mat_t B, int unit, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_solve_tril_classical(fq_zech_mat_t X, const fq_zech_mat_t L, const fq_zech_mat_t B, int unit, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_solve_tril_recursive(fq_zech_mat_t X, const fq_zech_mat_t L, const fq_zech_mat_t B, int unit, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_solve_triu(fq_zech_mat_t X, const fq_zech_mat_t U, const fq_zech_mat_t B, int unit, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_solve_triu_classical(fq_zech_mat_t X, const fq_zech_mat_t U, const fq_zech_mat_t B, int unit, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_solve_triu_recursive(fq_zech_mat_t X, const fq_zech_mat_t U, const fq_zech_mat_t B, int unit, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_solve(fq_zech_mat_t X, const fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    int fq_zech_mat_can_solve(fq_zech_mat_t X, const fq_zech_mat_t A, const fq_zech_mat_t B, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_similarity(fq_zech_mat_t M, slong r, fq_zech_t d, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_charpoly_danilevsky(fq_zech_poly_t p, const fq_zech_mat_t M, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_charpoly(fq_zech_poly_t p, const fq_zech_mat_t M, const fq_zech_ctx_t ctx) noexcept
    void fq_zech_mat_minpoly(fq_zech_poly_t p, const fq_zech_mat_t M, const fq_zech_ctx_t ctx) noexcept
