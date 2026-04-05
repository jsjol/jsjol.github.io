---
layout: page
title: Diffusion and generative models
description: Developing and applying diffusion-based generative models for image restoration, conditional inference, and scientific applications.
img: assets/img/irsde_overview.png
importance: 3
category: active
---

Generative models and Bayesian inference are key tools for accelerating scientific discovery by enabling efficient exploration of large design spaces. We work on both foundational aspects of these models and their application to scientific and engineering problems.

### Image restoration with mean-reverting SDEs

Our work on diffusion models for image restoration introduced a mean-reverting stochastic differential equation (SDE) that transforms a high-quality image into a degraded counterpart as a mean state with fixed Gaussian noise. By simulating the corresponding reverse-time SDE, we restore the original image without relying on any task-specific prior knowledge. This approach has a closed-form solution, allowing exact computation of the time-dependent score. The method achieves highly competitive performance on deraining, deblurring, denoising, super-resolution, inpainting, and dehazing, and has been widely adopted since its publication at ICML 2023.

<div style="text-align: center; margin: 1.5em 0;">
<img src="/assets/img/irsde_overview.png" alt="Mean-reverting SDE for image restoration" width="100%"/>
<p><small>The forward SDE degrades a clean image towards a noisy low-quality mean; the learned reverse-time SDE restores it.</small></p>
</div>

<div style="text-align: center; margin: 1.5em 0;">
<video autoplay loop muted playsinline width="60%" style="border-radius: 4px;">
  <source src="https://algolzw.github.io/ir-sde/images/derain.mp4" type="video/mp4">
  <source src="/assets/video/derain.mp4" type="video/mp4">
</video>
<p><small>IR-SDE progressively removes rain streaks via the reverse-time SDE.</small></p>
</div>

In a follow-up, we showed how vision-language models can be steered for universal image restoration across ten different degradation types, using degradation-aware CLIP embeddings to guide the restoration process.

<div style="text-align: center; margin: 1.5em 0;">
<img src="/assets/img/daclip_teaser.jpg" alt="DA-CLIP for universal image restoration" width="100%"/>
<p><small>DA-CLIP handles ten different image degradation types with a single model, using degradation-aware CLIP embeddings.</small></p>
</div>

- Luo Z, Gustafsson F K, Zhao Z, **Sjölund J**, and Schön T B. [*Image restoration with mean-reverting stochastic differential equations.*](https://proceedings.mlr.press/v202/luo23b.html) ICML (2023).
- Luo Z, Gustafsson F K, Zhao Z, **Sjölund J**, and Schön T B. [*Controlling vision-language models for universal image restoration.*](https://arxiv.org/abs/2310.01018) ICLR (2024).
- Luo Z, Gustafsson F K, **Sjölund J**, and Schön T B. [*Forward-only diffusion probabilistic models.*](https://arxiv.org/abs/2505.16733) arXiv (2025).

### Training-free conditional inference

A key challenge for incorporating pretrained generative models into Bayesian experimental design loops is performing conditional inference without costly retraining. We are developing methods for training-free guidance of flow-based and diffusion models, enabling conditional sampling from pretrained models by leveraging the source-space structure.

<div style="text-align: center; margin: 1.5em 0;">
<img src="/assets/img/publication_preview/essflow.png" alt="ESS-Flow: training-free guidance in source space" width="60%"/>
<p><small>ESS-Flow performs conditional inference by applying a potential function in the source space of a flow model, avoiding costly retraining.</small></p>
</div>

- Kalaivanan A, Zhao Z, **Sjölund J**, and Lindsten F. [*ESS-Flow: Training-free guidance of flow-based models as inference in source space.*](https://arxiv.org/abs/2510.05849) arXiv (2025).
- Corenflos A, Zhao Z, Särkkä S, **Sjölund J**, and Schön T B. [*Conditioning diffusion models by explicit forward-backward bridging.*](https://arxiv.org/abs/2405.13794) AISTATS (2025).

### Reviews and broader contributions

We have contributed two authoritative reviews to Philosophical Transactions of the Royal Society A, covering conditional sampling within generative diffusion models and the state of the art in diffusion-based image restoration. On the reinforcement learning side, we have shown how diffusion models can serve as expressive policy representations for offline RL.

- Zhao Z, Luo Z, **Sjölund J**, and Schön T B. [*Conditional sampling within generative diffusion models.*](https://doi.org/10.1098/rsta.2024.0253) Phil. Trans. R. Soc. A (2025).
- Zhao Z, Luo Z, **Sjölund J**, and Schön T B. [*Taming diffusion models for image restoration: a review.*](https://doi.org/10.1098/rsta.2024.0107) Phil. Trans. R. Soc. A (2025).
- Zhang R, Luo Z, Chen Z, **Sjölund J**, and Schön T B. [*Entropy-regularized diffusion policy with Q-ensembles for offline reinforcement learning.*](https://neurips.cc/virtual/2024/poster/93653) NeurIPS (2024).
