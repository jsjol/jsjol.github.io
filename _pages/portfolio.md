---
layout: archive
title: "Research"
permalink: /portfolio/
author_profile: true
---

{% include base_path %}

My overarching goal is to **accelerate scientific and technological progress using machine learning and optimization**. Before moving to Uppsala University, I mainly worked on applications to medical imaging and radiotherapy planning. Some of these are described in more detail below. Recently, however, I've also made new forays into scientific computing, rechargeable batteries, and astrophysics.

For a complete list of publications, please refer to [my Google Scholar page](https://scholar.google.se/citations?user=AlF2g-YAAAAJ&hl=en).



{% for post in site.portfolio %}
  {% include archive-single.html %}
{% endfor %}

