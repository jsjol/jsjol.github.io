---
layout: page
title: research
permalink: /projects/
description: Research threads in machine learning and optimization.
nav: true
nav_order: 2
horizontal: false
---

<!-- pages/projects.md -->
<div class="projects">

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->
  <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>

</div>
