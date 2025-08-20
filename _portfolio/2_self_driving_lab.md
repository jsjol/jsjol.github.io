---
title: "Self-driving labs for accelerated materials science"
excerpt: "We're building autonomous laboratories that combines robotics and AI into closed-loop systems for rapid experimentation and exploration.<br><br><img src='/images/odacell.png'>"
collection: portfolio
---

Automation, digitalisation, and AI in materials science represent a transformative shift in how fundamental science is conducted. These tools enable scientific exploration at a scale and level of complexity that manual experimentation cannot match. Capitalizing on this vision, we are building so-called self-driving labs - autonomous laboratories that combine robotics and AI into a closed-loop system for rapid experimentation and exploration - in collaboration with materials scientist at Uppsala University. 

### Batteries
Rechargeable batteries are key for transitioning to a carbon-neutral future, but it will require huge quantities of battery materials. It is therefore of utmost importance that both the battery materials and the manufacturing process are sustainable and cost effective. In these regards, batteries based on _aqueous_ electrolytes are especially promising. However, water has a very narrow electrochemical stability window, which poses a major challenge for aqueous electrolytes. In principle, it can be accomated by including functional additives to the electrolyte, but finding the right "recipe" is akin to finding a needle in a haystack.
  
Together with the research group of [Erik J. Berg](https://scholar.google.se/citations?user=ErU9OB4AAAAJ&hl=sv&oi=ao) at the [Ångström Advanced Battery Centre](https://www.kemi.uu.se/angstrom/research/structural-chemistry/aabc) we've developed [ODACell](https://github.com/jyik/ODACell), a robotic setup for automated electrolyte formulation and battery assembly, capable of preparing large batches of coin cells \[[1](#references)\].
<iframe width="1250" height="703" src="https://www.youtube.com/embed/mAtBjrnRx-I" title="ODACell Coin Cell Assembly Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
The coin cells are automatically cycled to test their performance and new experiments suggested using Bayesian optimization for data-driven decision-making \[[2](#references)\]. In ongoing work, we are adding capabilities such as in operando sensing using Electrochemical Quartz Crystal Microbalance (EQCM) \[[3](#references)\].


### Thin film science
In thin film science, self-driving labs have mainly been restricted to solution-based synthetic methods which are easier to automate but cannot access the broad chemical space of inorganic materials. In collaboration with the research group of [Jonathan Scragg](https://www.uu.se/en/contact-and-organisation/staff?query=N10-969), in the division of solar cell technology, we're building a self-driving lab based on magnetron co-sputtering.  In \[[4](#references)\], we present a rapid and calibration-free in-situ, machine learning driven approach to produce composition maps for arbitrary source combinations and sputtering conditions. Specifically, it predicts the composition distribution in a multi-element combinatorial thin film using in-situ measurements from quartz-crystal microbalance sensors placed in a sputter chamber. For a given source, the sensor readings are learned as a function of the sputtering pressure and magnetron power, through Bayesian optimization. The final model allows interpolation of the deposition rates from each source, at any position across the sample. 

Our framework dramatically increases throughput by avoiding the need for extensive characterisation or calibration, thus demonstrating the potential of self-driving labs to accelerate materials exploration.

### Simulations
In parallel with the physical experiments above, we are also performing simulation studies to better understand the underlying mechanisms. For instance, we recently studied electrode/electrolyte interface side reactions and dendrite growth in fast-charging metal-anode batteries, by combining a phase-field model of electrodeposition with Bayesian optimization \[[5](#references)\]. Our approach allows exploration the parameter space with a high sample efficiency and a low computation complexity. We use this framework to find the optimal cell for suppressing dendrite growth and accelerating charging speed under constant voltage. We identify interfacial mobility as a key parameter, which should be maximized to inhibit dendrites without compromising the charging speed.

<center>
<img src="/images/dendrite.png" alt="Simulated dendrite" width="400px"/>
</center>


## References

###### \[1\] [<SPAN STYLE="font-weight:normal">Yik J T, Zhang L, **Sjölund J**, Hou X, Svensson P H, Edström K, and Berg E J (2023). _Automated electrolyte formulation and coin cell assembly for high-throughput lithium-ion battery research_. Digital Discovery.</SPAN>](https://doi.org/10.1039/D3DD00058C)

###### \[2\] [<SPAN STYLE="font-weight:normal">Yik J T, Hvarfner C, **Sjölund J**, Berg EJ, and Zhang L (2025). _Accelerating aqueous electrolyte design with automated full-cell battery experimentation and Bayesian optimization_. Cell Reports Physical Science</SPAN>](https://doi.org/10.1016/j.xcrp.2025.102548)

###### \[3\] [<SPAN STYLE="font-weight:normal">Vanoppen V, Johannsmann D, Hou X, **Sjölund J**, Broqvist P, and Berg E J. _Exploring Metal Electroplating for Energy Storage by Quartz Crystal Microbalance: A Review_. Advanced Sensor Research</SPAN>](https://doi.org/10.1002/adsr.202400025)

###### \[4\] [<SPAN STYLE="font-weight:normal">Jarl S, **Sjölund J**, Frost R J W, Holst A, and Scragg J J S (2025). _Machine learning for in-situ composition mapping in a self-driving magnetron sputtering system_. arXiv preprint</SPAN>](https://doi.org/10.48550/arXiv.2506.05999)

###### \[5\] [<SPAN STYLE="font-weight:normal">Taghavian H, Vanoppen V, Berg E J, Broqvist P, and **Sjölund J** (2025). _Navigating chemical design spaces for metal-ion batteries via machine-learning-guided phase-field simulations_. npj Computational Materials</SPAN>](https://doi.org/10.1038/s41524-025-01735-x)







