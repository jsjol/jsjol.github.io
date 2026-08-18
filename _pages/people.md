---
layout: page
title: group
permalink: /people/
description: Current and former members of the research group.
nav: true
nav_order: 4
---

{%- assign groups = "phd_students,postdocs,co_supervised" | split: "," -%}
{%- assign headings = "PhD Students,Postdoctoral Researchers,Co-supervised PhD Students" | split: "," -%}
{%- for group in groups -%}
{%- assign members = site.data.people[group] -%}
{%- if members and members.size > 0 %}
<h2>{{ headings[forloop.index0] }}</h2>
<ul class="people-grid">
{%- for person in members %}
<li class="person">
{%- if person.image %}
<img src="{{ '/assets/img/people/' | append: person.image | relative_url }}" alt="{{ person.name }}" loading="lazy">
{%- endif %}
{% if person.website -%}
<a class="person-name" href="{{ person.website }}">{{ person.name }}</a>
{%- else -%}
<span class="person-name">{{ person.name }}</span>
{%- endif %}
{%- if person.description %}
<span class="person-focus">{{ person.description }}</span>
{%- endif %}
</li>
{%- endfor %}
</ul>
{% endif -%}
{%- endfor %}

---

## Alumni

### PhD Students

<ul class="alumni-list">
{%- for person in site.data.people.alumni_phd %}
<li>{{ person.years }} ({{ person.role }}) {% if person.thesis_url %}<a href="{{ person.thesis_url }}">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}, <em>{{ person.thesis_title }}</em>, subsequently {{ person.now }}</li>
{%- endfor %}
</ul>

### Postdoctoral Researchers

<ul class="alumni-list">
{%- for person in site.data.people.alumni_postdoc %}
<li>{{ person.years }}, {% if person.website %}<a href="{{ person.website }}">{{ person.name }}</a>{% else %}{{ person.name }}{% endif %}, subsequently {{ person.now }}</li>
{%- endfor %}
</ul>

### Master's Thesis Students

<ul class="alumni-list">
{%- for person in site.data.people.alumni_msc %}
<li>{{ person.name }}, {% if person.url %}<a href="{{ person.url }}">{{ person.title }}</a>{% else %}{{ person.title }}{% endif %}, {{ person.year }}</li>
{%- endfor %}
</ul>
