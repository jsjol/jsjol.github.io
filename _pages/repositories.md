---
layout: page
permalink: /repositories/
title: code
description: Open-source software from the group.
nav: false
nav_order: 8
---

<ul class="repo-list">
{%- for repo in site.data.repositories.repositories %}
<li class="repo">
<a class="repo-name" href="https://github.com/{{ repo.name }}"><i class="fa-brands fa-github"></i> {{ repo.name }}</a>
<span class="repo-description">{{ repo.description }}</span>
{%- if repo.paper %}
<span class="repo-paper">{{ repo.paper }}</span>
{%- endif %}
</li>
{%- endfor %}
</ul>
