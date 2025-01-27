---
title: "Self-driving battery lab"
excerpt: "We're building an autonomous battery laboratory that combines robotics and AI into a closed-loop system for rapid experimentation and exploration.<br><br><img src='/images/odacell.png'>"
collection: portfolio
---

Rechargeable batteries are key for transitioning to a carbon-neutral future, but it will require huge quantities of battery materials. It is therefore of utmost importance that both the battery materials and the manufacturing process are sustainable and cost effective. In these regards, batteries based on _aqueous_ electrolytes are especially promising. However, water has a very narrow electrochemical stability window, which poses a major challenge for aqueous electrolytes. In principle, it can be accomated by including functional additives to the electrolyte, but finding the right "recipe" is akin to finding a needle in a haystack.
  
Together with the research group of [Erik J. Berg](https://scholar.google.se/citations?user=ErU9OB4AAAAJ&hl=sv&oi=ao) at the [Ångström Advanced Battery Centre](https://www.kemi.uu.se/angstrom/research/structural-chemistry/aabc) we're building an autonomous battery laboratory that combines robotics and AI into a closed-loop system for rapid experimentation and exploration. 

To this end, we've developed [ODACell](https://github.com/jyik/ODACell), a robotic setup for automated electrolyte formulation and battery assembly, capable of preparing large batches of coin cells \[[1](#references)\].
<iframe width="1250" height="703" src="https://www.youtube.com/embed/mAtBjrnRx-I" title="ODACell Coin Cell Assembly Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
The coin cells can be automatically cycled to test their performance. Recently, we have closed the feedback loop by using Bayesian optimization for data-driven decision-making \[[2](#references)\]. 

## References

###### \[1\] [<SPAN STYLE="font-weight:normal">Yik J T, Zhang L, **Sjölund J**, Hou X, Svensson P H, Edström K, and Berg E J (2023). _Automated electrolyte formulation and coin cell assembly for high-throughput lithium-ion battery research_. Digital Discovery.</SPAN>](https://doi.org/10.1039/D3DD00058C)

###### \[2\] [<SPAN STYLE="font-weight:normal">Yik J T, Hvarfner C, **Sjölund J**, Berg EJ, Zhang L. _Towards Self-Driving Labs for Better Batteries: Accelerating Electrolyte Discovery with Automation and Bayesian Optimization_. ChemRxiv. 2024; doi:10.26434/chemrxiv-2024-mqb6s-v2</SPAN>](https://doi.org/10.26434/chemrxiv-2024-mqb6s-v2)







