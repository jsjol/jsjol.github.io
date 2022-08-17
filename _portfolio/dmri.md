---
title: "Optimization for diffusion MRI"
excerpt: "Our open-source library for numerical optimization of diffusion MRI experiments enables cutting-edge imaging technology on clinical scanners.<br/><img src='/images/NOW_demo.png'>"
collection: portfolio
---

Diffusion MRI (dMRI) is a useful probe of tissue microstructure, which can be used to derive biomarkers for diagnostics and treatment. Diffusion measurements using continuous gradient waveforms significantly expand the capabilities of conventional diffusion MRI [(Szczepankiewicz et al., 2021)](#references). However, implementing them on real-world MR scanners is challenging due to the plethora of constraints imposed by hardware limitations and physiology. 

# Contributions
In collaboration with Filip Szczepankiewicz and others, I've developed the open-source library [NOW](https://github.com/jsjol/NOW) which has established itself as the de facto standard tool for gradient waveform design for tensor-valued encoding in diffusion MRI. Since its introduction in [Sjölund et al. (2015)](#references), the methodology and software has been extended and refined to capture additional effects, including motion compensation [(Szczepankiewicz et al., 2021)](#references) and cross-term compensation [(Szczepankiewicz and Sjölund, 2021)][#references]. We have also demonstrated that NOW enables diffusional variance decomposition (DIVIDE) on clinical MRI systems [Szczepankiewicz et al., 2019](#references).

# References
[**Sjölund J**, Szczepankiewicz F, Nilsson M, Topgaard D, Westin C-F, and Knutsson H. _Constrained optimization of gradient waveforms for generalized diffusion encoding._ Journal of Magnetic Resonance 261 (2015), 157-168.](https://doi.org/10.1016/j.jmr.2015.10.012)

[Szczepankiewicz F , **Sjölund J**, Ståhlberg F, Lätt J, and Nilsson M. _Tensor-valued diffusion encoding for diffusional variance decomposition (DIVIDE): Technical feasibility in clinical MRI systems._ PLoS One (2019).](https://doi.org/10.1371/journal.pone.0214238)

[Szczepankiewicz F, **Sjölund J**, Dall’Armellina E, Plein S, Schneider E J, Teh I, and Westin C-F, _Motion-compensated gradient waveforms for tensor-valued diffusion encoding by constrained numerical optimization._ Magn Reson Med (2021)](https://onlinelibrary.wiley.com/doi/10.1002/mrm.28551)

[Szczepankiewicz F and **Sjölund J**, _Cross-term-compensated gradient waveform design for tensor-valued diffusion MRI._ Journal of Magnetic Resonance (2021)](https://doi.org/10.1016/j.jmr.2021.106991)

[Szczepankiewicz F, Westin C-F, and Nilsson, M, _Gradient waveform design for tensor-valued encoding in diffusion MRI._ Journal of Neuroscience Methods (2021)](https://doi.org/10.1016/j.jneumeth.2020.109007)