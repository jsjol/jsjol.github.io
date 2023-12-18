---
title: "Optimization for diffusion MRI"
excerpt: "Our open-source library for numerical optimization of diffusion MRI experiments enables cutting-edge imaging technology on clinical scanners.<br/><img src='/images/NOW_demo.png'>"
collection: portfolio
---

Diffusion MRI (dMRI) is a useful probe of tissue microstructure, which can be used to derive biomarkers for diagnostics and treatment. Diffusion measurements using continuous gradient waveforms significantly expand the capabilities of conventional diffusion MRI \[[J5](#references)\]. However, implementing them on real-world MR scanners is challenging due to the plethora of constraints imposed by hardware limitations and physiology. 

## Contributions
In collaboration with Filip Szczepankiewicz and others, I've developed the open-source library [NOW](https://github.com/jsjol/NOW) which has established itself as the de facto standard tool for gradient waveform design for tensor-valued encoding in diffusion MRI. Since its introduction in 2015 \[[J1](#references)\], the methodology and software has been extended and refined to capture additional effects, including motion compensation \[[J3](#references)\] and cross-term compensation \[[J4](#references)\]. We have also demonstrated that NOW enables diffusional variance decomposition (DIVIDE) on clinical MRI systems \[[J2](#references)\].

## References

#### Journal papers
###### \[J1\] [<SPAN STYLE="font-weight:normal">**Sjölund J**, Szczepankiewicz F, Nilsson M, Topgaard D, Westin C-F, and Knutsson H. _Constrained optimization of gradient waveforms for generalized diffusion encoding._ Journal of Magnetic Resonance 261 (2015), 157-168.</SPAN>](https://doi.org/10.1016/j.jmr.2015.10.012)

###### \[J2\] [<SPAN STYLE="font-weight:normal">Szczepankiewicz F , **Sjölund J**, Ståhlberg F, Lätt J, and Nilsson M. _Tensor-valued diffusion encoding for diffusional variance decomposition (DIVIDE): Technical feasibility in clinical MRI systems._ PLoS One (2019).</SPAN>](https://doi.org/10.1371/journal.pone.0214238)

###### \[J3\] [<SPAN STYLE="font-weight:normal">Szczepankiewicz F, **Sjölund J**, Dall’Armellina E, Plein S, Schneider E J, Teh I, and Westin C-F, _Motion-compensated gradient waveforms for tensor-valued diffusion encoding by constrained numerical optimization._ Magn Reson Med (2021)</SPAN>](https://onlinelibrary.wiley.com/doi/10.1002/mrm.28551)

###### \[J4\] [<SPAN STYLE="font-weight:normal">Szczepankiewicz F and **Sjölund J**, _Cross-term-compensated gradient waveform design for tensor-valued diffusion MRI._ Journal of Magnetic Resonance (2021)</SPAN>](https://doi.org/10.1016/j.jmr.2021.106991)

###### \[J5\] [<SPAN STYLE="font-weight:normal">Szczepankiewicz F, Westin C-F, and Nilsson, M, _Gradient waveform design for tensor-valued encoding in diffusion MRI._ Journal of Neuroscience Methods (2021)</SPAN>](https://doi.org/10.1016/j.jneumeth.2020.109007)