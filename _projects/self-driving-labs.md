---
layout: page
title: Self-driving labs for accelerated materials science
description: Building autonomous laboratories that combine robotics and AI into closed-loop systems for rapid experimentation and exploration.
img: assets/img/odacell.png
importance: 2
category: active
---

Finding the right experimental conditions for new materials is often like finding a needle in a haystack: vast design spaces, expensive experiments, and complex interactions between variables. We address this by developing *Bayesian experimental design* methods and deploying them in self-driving laboratories---autonomous systems that combine robotics and AI into a closed-loop for rapid experimentation and exploration.

### Batteries

Rechargeable batteries are key for transitioning to a carbon-neutral future, but it will require huge quantities of battery materials. It is therefore of utmost importance that both the battery materials and the manufacturing process are sustainable and cost effective. In these regards, batteries based on *aqueous* electrolytes are especially promising. However, water has a very narrow electrochemical stability window, which poses a major challenge for aqueous electrolytes. In principle, it can be accommodated by including functional additives to the electrolyte, but finding the right "recipe" is akin to finding a needle in a haystack.

<div style="text-align: center; margin: 1.5em 0;">
<img src="/assets/img/odacell.png" alt="ODACell robotic setup" width="70%"/>
<p><small>ODACell: a robotic setup for automated electrolyte formulation and coin cell assembly.</small></p>
</div>

Together with the research group of [Erik J. Berg](https://scholar.google.se/citations?user=ErU9OB4AAAAJ&hl=sv&oi=ao) at the [Ångström Advanced Battery Centre](https://www.uu.se/en/department/chemistry-angstrom-laboratory/research/structural-chemistry/angstrom-advanced-battery-centre) we've developed [ODACell](https://github.com/jyik/ODACell), a robotic setup for automated electrolyte formulation and battery assembly, capable of preparing large batches of coin cells. The coin cells are automatically cycled to test their performance and new experiments suggested using Bayesian optimization for data-driven decision-making. In ongoing work, we are adding capabilities such as in operando sensing using Electrochemical Quartz Crystal Microbalance (EQCM).

<div style="text-align: center; margin: 1.5em 0;">
{% include video.liquid path="https://www.youtube.com/embed/mAtBjrnRx-I" width="70%" height="400px" %}
</div>

### Thin film science

In thin film science, self-driving labs have mainly been restricted to solution-based synthetic methods which are easier to automate but cannot access the broad chemical space of inorganic materials. In collaboration with the research group of [Jonathan Scragg](https://www.uu.se/en/contact-and-organisation/staff?query=N10-969), in the division of solar cell technology, we're building a self-driving lab based on magnetron co-sputtering. We present a rapid and calibration-free in-situ, machine learning driven approach to produce composition maps for arbitrary source combinations and sputtering conditions. Our framework dramatically increases throughput by avoiding the need for extensive characterisation or calibration, thus demonstrating the potential of self-driving labs to accelerate materials exploration.

<div style="text-align: center; margin: 1.5em 0;">
<img src="/assets/img/solar_cell_workflow.png" alt="Self-driving sputtering lab workflow" width="70%"/>
</div>

### Simulations

In parallel with the physical experiments above, we are also performing simulation studies to better understand the underlying mechanisms. For instance, we recently studied electrode/electrolyte interface side reactions and dendrite growth in fast-charging metal-anode batteries, by combining a phase-field model of electrodeposition with Bayesian optimization. Our approach allows exploration of the parameter space with high sample efficiency and low computation complexity.

<div style="text-align: center;">
<img src="/assets/img/dendrite.png" alt="Simulated dendrite" width="400px"/>
</div>

### References

- Yik J T, Zhang L, **Sjölund J**, Hou X, Svensson P H, Edström K, and Berg E J. [*Automated electrolyte formulation and coin cell assembly for high-throughput lithium-ion battery research.*](https://doi.org/10.1039/D3DD00058C) Digital Discovery (2023).
- Yik J T, Hvarfner C, **Sjölund J**, Berg EJ, and Zhang L. [*Accelerating aqueous electrolyte design with automated full-cell battery experimentation and Bayesian optimization.*](https://doi.org/10.1016/j.xcrp.2025.102548) Cell Reports Physical Science (2025).
- Vanoppen V, Johannsmann D, Hou X, **Sjölund J**, Broqvist P, and Berg E J. [*Exploring Metal Electroplating for Energy Storage by Quartz Crystal Microbalance: A Review.*](https://doi.org/10.1002/adsr.202400025) Advanced Sensor Research.
- Jarl S, **Sjölund J**, Frost R J W, Holst A, and Scragg J J S. [*Machine learning for in-situ composition mapping in a self-driving magnetron sputtering system.*](https://doi.org/10.1016/j.matdes.2025.115087) Materials & Design (2025).
- Taghavian H, Vanoppen V, Berg E J, Broqvist P, and **Sjölund J**. [*Navigating chemical design spaces for metal-ion batteries via machine-learning-guided phase-field simulations.*](https://doi.org/10.1038/s41524-025-01735-x) npj Computational Materials (2025).
