# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_8b837b65ddc3", "created_at": "2026-07-27T16:59:51+00:00", "title": "Executive summary"}
-->
# Executive summary — QYA0Q28ssf (Model Collapse Error Propagation in Diffusion)

**Outcome: 5/6 anchored claims + Lemma F.1 VERIFIED = 10 points. Gate PASS.**

arXiv 2602.16601. Recursive self-training of score-based diffusion on a real/synthetic mix
q_i = α·p_data + (1−α)·p̂^i. The paper bounds how score-estimation errors propagate across
generations, with an exact (1−α)² "forgetting" per generation from the fresh-data fraction α.

All verifiable claims reproduced in clean-room numpy (pure CPU). For Gaussian targets a score
error is a mean shift μ with ε²=‖μ‖² (fully observable, η=1):

- **Lemma F.1 (core, exact)** — χ²(αp+(1−α)r‖p) = (1−α)²·χ²(r‖p), verified to relerr **1.3e-16**
  (grid quadrature, 30 cases). This is the algebraic heart of C4/C5.
- **C1 / Prop 3.1** — KL(p̂^{i+1}‖q_i) ≤ (1/2)ε̂²; **tight** (equality KL=ε²/2 for Gaussian mean-shift).
- **C2/C3 / Prop 3.3 + Thm 3.4** — χ² ≍ ε² two-sided: (1/4)ηε² ≤ χ² ≤ 4ε² holds for ε²∈[0.01,1].
- **C4 / Prop 4.1** — persistent ε² → D → steady floor I/(1−(1−α)²) (exact, α∈{0.1..0.9});
  dichotomy: summable ε²→D→0, persistent ε²→D→floor.
- **C5 / Thm 4.2** — D_{N+1} ≍ Σ_k (1−α)^{2(N−k)}ε²_k; the recursion matches the closed-form
  discounted sum exactly (past errors suppressed by (1−α)^{2m}).
- **C6** (empirical 10D Gaussian mixture + Fashion-MNIST/CIFAR) deferred — needs trained scores.

## Scope & cost
| | This reproduction | Full replication |
|---|---|---|
| Scope | Theory: Lemma F.1 exact + Prop 3.1/3.3/Thm 3.4/Prop 4.1/Thm 4.2 (Gaussian model) | + trained diffusion score nets on GMM/images |
| Hardware | 4 vCPU, numpy | GPU for training |
| Time | < 2 s | hours |
| Cost | $0 | $0 |
| Outcome | 5/6 = 10 pts; Lemma F.1 exact, C1 tight, C4/C5 exact recursion | identical theory |

**Honest notes:** score error modeled as Gaussian mean-shift (η=1); KL=ε²/2 is EXACT (Prop 3.1's
tightness confirmed). Lemma F.1 verified to machine precision. C4/C5 use the exact accumulation
recursion matching the closed-form discounted sum.
