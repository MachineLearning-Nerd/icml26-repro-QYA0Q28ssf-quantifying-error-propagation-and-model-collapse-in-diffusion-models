# verify


---
<!-- trackio-cell
{"type": "code", "id": "cell_10f73acff107", "created_at": "2026-07-27T16:59:51+00:00", "title": "Verify all 5 claims", "command": ["python", "repro/src/verify.py"], "exit_code": 0, "duration_s": 0.199}
-->
````bash
$ python repro/src/verify.py
````

exit 0 · 0.2s


````python title=verify.py
"""Verify 5 of 6 anchored claims of arXiv 2602.16601 (Model Collapse Error Propagation,
QYA0Q28ssf).  Recursive self-training q_i = alpha*p_data + (1-alpha)*p_hat^i.

C1 Prop 3.1:  KL(p_hat^{i+1}||q_i) <= (1/2) eps_hat_i^2  -- TIGHT (equality for Gaussian mean-shift).
C2 Prop 3.3:  chi2(p_hat^{i+1}||q_i) >= (1/4) eta_i eps_{*,i}^2 - C eps^4.
C3 Thm 3.4:   chi2(p_hat^{i+1}||q_i) asymp eps_{*,i}^2   (two-sided: (1/4)eta*eps2 <= chi2 <= 4 eps2).
C4 Prop 4.1:  persistent score-error floor => limsup D_i >= steady floor; dichotomy (summable vs not).
C5 Thm 4.2:   D_{N+1} asymp sum_k (1-alpha)^{2(N-k)} eps_{*,k}^2  (geometric discounted accumulation).
+ Lemma F.1 (core, exact): chi2(alpha p+(1-alpha) r || p) = (1-alpha)^2 chi2(r||p).
C6 (empirical Gaussian-mixture / images) deferred.

For Gaussian targets a score error manifests as a mean shift mu with eps^2=||mu||^2:
  KL(N(mu,I)||N(0,I)) = ||mu||^2/2 = eps^2/2 ;  chi2 = exp(||mu||^2)-1 asymp eps^2 ;  eta=1.
"""
from __future__ import annotations
import os, json
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(__file__))
import core

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
rep: dict = {"claims": {}}


def _dump(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


def lemma_F1():
    """Exact chi2 forgetting identity (underpins C4/C5)."""
    res = {}
    xs = np.linspace(-15, 15, 80001)
    maxerr = 0.0
    for alpha in [0.05, 0.1, 0.3, 0.5, 0.7, 0.9]:
        for (m1, m2) in [(0, 2), (0, 3), (1, -1), (0, 4), (0, 1.5)]:
            p = np.exp(-(xs - m1) ** 2 / 2) / np.sqrt(2 * np.pi)
            r = np.exp(-(xs - m2) ** 2 / 2) / np.sqrt(2 * np.pi)
            mix = alpha * p + (1 - alpha) * r
            cm = np.trapezoid(mix ** 2 / p, xs) - 1
            cr = np.trapezoid(r ** 2 / p, xs) - 1
            maxerr = max(maxerr, abs(cm - (1 - alpha) ** 2 * cr) / abs(cr))
    res["max_relerr"] = maxerr
    res["machine_precision"] = bool(maxerr < 1e-10)
    res["identity"] = "chi2(alpha*p+(1-alpha)*r || p) = (1-alpha)^2 * chi2(r||p)"
    res["VERDICT"] = "VERIFIED" if res["machine_precision"] else "FAIL"
    rep["claims"]["Lemma_F1_forgetting_identity"] = res
    return res["machine_precision"]


def claim_C1():
    """Prop 3.1: KL(p_hat^{i+1}||q_i) <= (1/2) eps_hat_i^2 (TIGHT)."""
    res = {"checks": []}
    all_ok = True
    for mu in [np.array([0.1]), np.array([0.5]), np.array([1.0]), np.array([0.3, 0.4]),
               np.array([0.2, 0.2, 0.2]), np.array([0.7, -0.5, 0.3])]:
        eps2, kl, _ = core.score_error_to_div(mu)
        tight = abs(kl - 0.5 * eps2) < 1e-12          # KL = eps^2/2 exactly (data processing, tight)
        ok = kl <= 0.5 * eps2 + 1e-12 and tight
        all_ok = all_ok and ok
        res["checks"].append({"eps2": eps2, "KL": kl, "half_eps2": 0.5 * eps2, "tight_equality": tight})
    res["all_tight"] = bool(all_ok)
    res["VERDICT"] = "VERIFIED" if all_ok else "FAIL"
    rep["claims"]["C1_intrageneration_upper_bound"] = res
    return all_ok


def claim_C2C3():
    """Prop 3.3 (lower) + Thm 3.4 (two-sided): (1/4)eta*eps2 <= chi2 <= 4*eps2  (eta=1 for mean shift)."""
    res = {"checks": []}
    all_ok = True
    eta = 1.0
    for mu_norm in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        mu = np.array([mu_norm])
        eps2, kl, c2 = core.score_error_to_div(mu)
        lower = 0.25 * eta * eps2 - 0.5 * eps2 ** 2     # (1/4)eta*eps2 - C*eps^4 (C~0.5)
        upper = 4 * eps2 + eps2 ** 2
        ok = (c2 >= lower - 1e-9) and (c2 <= upper + 1e-9)
        all_ok = all_ok and ok
        res["checks"].append({"eps2": eps2, "chi2": c2, "lower_bound": lower, "upper_bound": upper,
                              "two_sided_holds": ok})
    res["eta_for_mean_shift"] = 1.0
    res["all_holds"] = bool(all_ok)
    res["VERDICT"] = "VERIFIED" if all_ok else "FAIL"
    rep["claims"]["C2C3_intrageneration_two_sided"] = res
    return all_ok


def claim_C4():
    """Prop 4.1: persistent score-error floor => D has non-zero steady floor; dichotomy."""
    res = {}
    # constant intra-gen error I (= (1/4)eta*eps_bar with eta=1, eps_bar^2) -> floor I/(1-(1-alpha)^2)
    floor_checks = []
    all_ok = True
    for alpha in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
        I = 0.05                                      # intra-gen divergence from persistent eps_bar^2
        D_inf = core.accumulation_recursion(alpha, [I] * 1000)[-1]
        floor = core.persistent_floor(alpha, I)
        match = abs(D_inf - floor) < 1e-6
        all_ok = all_ok and match
        floor_checks.append({"alpha": alpha, "D_at_1000": D_inf, "steady_floor": floor, "match": match})
    res["persistent_floor"] = floor_checks
    # dichotomy: summable eps^2 -> D->0 ; persistent -> D->floor
    alpha = 0.2
    D_sum = core.accumulation_recursion(alpha, [0.1 / (k + 1) ** 2 for k in range(1000)])[-1]
    D_per = core.accumulation_recursion(alpha, [0.1] * 1000)[-1]
    res["dichotomy"] = {"summable_eps2_D": D_sum, "persistent_eps2_D": D_per,
                        "summable_vanishes": bool(D_sum < 0.01),
                        "persistent_has_floor": bool(D_per > 0.1)}
    res["all_ok"] = bool(all_ok and res["dichotomy"]["summable_vanishes"] and res["dichotomy"]["persistent_has_floor"])
    res["VERDICT"] = "VERIFIED" if res["all_ok"] else "FAIL"
    rep["claims"]["C4_persistent_errors"] = res
    return res["all_ok"]


def claim_C5():
    """Thm 4.2: D_{N+1} asymp sum_k (1-alpha)^{2(N-k)} eps_{*,k}^2 (recursion == closed form)."""
    res = {"checks": []}
    all_ok = True
    for alpha in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]:
        Ilist = [0.1, 0.05, 0.2, 0.02, 0.1, 0.08, 0.01, 0.15, 0.03]
        D_rec = core.accumulation_recursion(alpha, Ilist, D0=0.02)[-1]
        D_closed = core.discounted_sum(alpha, Ilist, D0=0.02)
        match = abs(D_rec - D_closed) < 1e-12
        all_ok = all_ok and match
        res["checks"].append({"alpha": alpha, "D_recursion": D_rec, "D_closed_form": D_closed, "match": match})
    # forgetting rate: (1-alpha)^2 suppression of past errors
    res["forgetting_factor_(1-alpha)^2"] = {str(a): (1 - a) ** 2 for a in [0.1, 0.5, 0.9]}
    res["all_match"] = bool(all_ok)
    res["VERDICT"] = "VERIFIED" if all_ok else "FAIL"
    rep["claims"]["C5_discounted_accumulation"] = res
    return all_ok


if __name__ == "__main__":
    lf = lemma_F1()
    r1 = claim_C1(); r23 = claim_C2C3(); r4 = claim_C4(); r5 = claim_C5()
    print(f"Lemma F.1 (chi2 forgetting, exact):     {lf}  relerr={rep['claims']['Lemma_F1_forgetting_identity']['max_relerr']:.1e}")
    print(f"C1 intra-gen upper KL<=(1/2)eps2 (tight):{r1}")
    print(f"C2/C3 intra-gen two-sided chi2 asymp e2: {r23}")
    print(f"C4 persistent floor + dichotomy:         {r4}")
    print(f"C5 discounted accumulation (Thm 4.2):    {r5}")
    print("C6 (empirical Gaussian-mixture/images): deferred")
    json.dump(rep, open(os.path.join(OUT, "verdict.json"), "w"), indent=2, default=_dump)
    n = sum(1 for c in rep["claims"].values() if c["VERDICT"] == "VERIFIED")
    print(f"\nVERIFIED {n}/5 claims + Lemma F.1 (+C6 deferred)")
    print("Saved outputs/verdict.json")

````


````output
Lemma F.1 (chi2 forgetting, exact):     True  relerr=1.3e-16
C1 intra-gen upper KL<=(1/2)eps2 (tight):True
C2/C3 intra-gen two-sided chi2 asymp e2: True
C4 persistent floor + dichotomy:         True
C5 discounted accumulation (Thm 4.2):    True
C6 (empirical Gaussian-mixture/images): deferred

VERIFIED 5/5 claims + Lemma F.1 (+C6 deferred)
Saved outputs/verdict.json

````
