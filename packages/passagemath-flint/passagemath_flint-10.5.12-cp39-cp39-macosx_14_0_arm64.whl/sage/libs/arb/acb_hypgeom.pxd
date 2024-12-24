# sage_setup: distribution = sagemath-flint
# Deprecated header file; use sage/libs/flint/acb_hypgeom.pxd instead
# See https://github.com/sagemath/sage/pull/36449

from sage.libs.flint.acb_hypgeom cimport (
    acb_hypgeom_pfq_bound_factor,
    acb_hypgeom_pfq_choose_n,
    acb_hypgeom_pfq_sum_forward,
    acb_hypgeom_pfq_sum_rs,
    acb_hypgeom_pfq_sum_bs,
    acb_hypgeom_pfq_sum_fme,
    acb_hypgeom_pfq_sum,
    acb_hypgeom_pfq_sum_bs_invz,
    acb_hypgeom_pfq_sum_invz,
    acb_hypgeom_pfq_direct,
    acb_hypgeom_pfq_series_direct,
    acb_hypgeom_u_asymp,
    acb_hypgeom_u_use_asymp,
    acb_hypgeom_u_1f1_series,
    acb_hypgeom_u_1f1,
    acb_hypgeom_u,
    acb_hypgeom_m_asymp,
    acb_hypgeom_m_1f1,
    acb_hypgeom_m,
    acb_hypgeom_erf_1f1a,
    acb_hypgeom_erf_1f1b,
    acb_hypgeom_erf_asymp,
    acb_hypgeom_erf,
    acb_hypgeom_erfc,
    acb_hypgeom_erfi,
    acb_hypgeom_bessel_j_asymp,
    acb_hypgeom_bessel_j_0f1,
    acb_hypgeom_bessel_j,
    acb_hypgeom_bessel_jy,
    acb_hypgeom_bessel_y,
    acb_hypgeom_bessel_i_asymp,
    acb_hypgeom_bessel_i_0f1,
    acb_hypgeom_bessel_i,
    acb_hypgeom_bessel_k_asymp,
    acb_hypgeom_bessel_k_0f1_series,
    acb_hypgeom_bessel_k_0f1,
    acb_hypgeom_bessel_k,
    acb_hypgeom_gamma_upper_asymp,
    acb_hypgeom_gamma_upper_1f1a,
    acb_hypgeom_gamma_upper_1f1b,
    acb_hypgeom_gamma_upper_singular,
    acb_hypgeom_gamma_upper,
    acb_hypgeom_expint,
    acb_hypgeom_ei_asymp,
    acb_hypgeom_ei_2f2,
    acb_hypgeom_ei,
    acb_hypgeom_si_asymp,
    acb_hypgeom_si_1f2,
    acb_hypgeom_si,
    acb_hypgeom_ci_asymp,
    acb_hypgeom_ci_2f3,
    acb_hypgeom_ci,
    acb_hypgeom_shi,
    acb_hypgeom_chi_asymp,
    acb_hypgeom_chi_2f3,
    acb_hypgeom_chi,
    acb_hypgeom_li,
    acb_hypgeom_0f1,
    acb_hypgeom_2f1,
    acb_hypgeom_legendre_p,
    acb_hypgeom_legendre_q,
    acb_hypgeom_jacobi_p,
    acb_hypgeom_gegenbauer_c,
    acb_hypgeom_laguerre_l,
    acb_hypgeom_hermite_h,
    acb_hypgeom_chebyshev_t,
    acb_hypgeom_chebyshev_u,
    acb_hypgeom_spherical_y,
    acb_hypgeom_airy)
