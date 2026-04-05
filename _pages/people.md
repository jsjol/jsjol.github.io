---
layout: page
title: group
permalink: /people/
description: Current and former members of the research group.
nav: true
nav_order: 4
---

## PhD Students

<div class="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-4 mb-5">
{% for person in site.data.people.phd_students %}
<div class="col">
  <div class="card h-100 text-center border-0">
    {% if person.image %}
    <img src="{{ '/assets/img/people/' | append: person.image | relative_url }}" class="card-img-top rounded-circle mx-auto mt-3" alt="{{ person.name }}" style="width: 150px; height: 150px; object-fit: cover;">
    {% endif %}
    <div class="card-body p-2">
      {% if person.website %}
      <a href="{{ person.website }}"><strong>{{ person.name }}</strong></a>
      {% else %}
      <strong>{{ person.name }}</strong>
      {% endif %}
      {% if person.description %}<br><small class="text-muted">{{ person.description }}</small>{% endif %}
    </div>
  </div>
</div>
{% endfor %}
</div>

## Postdoctoral Researchers

<div class="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-4 mb-5">
{% for person in site.data.people.postdocs %}
<div class="col">
  <div class="card h-100 text-center border-0">
    {% if person.image %}
    <img src="{{ '/assets/img/people/' | append: person.image | relative_url }}" class="card-img-top rounded-circle mx-auto mt-3" alt="{{ person.name }}" style="width: 150px; height: 150px; object-fit: cover;">
    {% endif %}
    <div class="card-body p-2">
      {% if person.website %}
      <a href="{{ person.website }}"><strong>{{ person.name }}</strong></a>
      {% else %}
      <strong>{{ person.name }}</strong>
      {% endif %}
      {% if person.description %}<br><small class="text-muted">{{ person.description }}</small>{% endif %}
    </div>
  </div>
</div>
{% endfor %}
</div>

## Co-supervised PhD Students

<div class="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-4 mb-5">
{% for person in site.data.people.co_supervised %}
<div class="col">
  <div class="card h-100 text-center border-0">
    {% if person.image %}
    <img src="{{ '/assets/img/people/' | append: person.image | relative_url }}" class="card-img-top rounded-circle mx-auto mt-3" alt="{{ person.name }}" style="width: 150px; height: 150px; object-fit: cover;">
    {% endif %}
    <div class="card-body p-2">
      {% if person.website %}
      <a href="{{ person.website }}"><strong>{{ person.name }}</strong></a>
      {% else %}
      <strong>{{ person.name }}</strong>
      {% endif %}
      {% if person.description %}<br><small class="text-muted">{{ person.description }}</small>{% endif %}
    </div>
  </div>
</div>
{% endfor %}
</div>

---

## Alumni

### PhD Students

{% for person in site.data.people.alumni_phd %}
{{ person.years }} ({{ person.role }}) [{{ person.name }}]({{ person.thesis_url }}), *{{ person.thesis_title }}*, subsequently {{ person.now }}
{% endfor %}

### Postdoctoral Researchers

{% for person in site.data.people.alumni_postdoc %}
{{ person.years }}, [{{ person.name }}]({{ person.website }}), subsequently {{ person.now }}
{% endfor %}

### Master's Thesis Students

{% for person in site.data.people.alumni_msc %}
{{ person.name }}, [{{ person.title }}]({{ person.url }}), {{ person.year }}
{% endfor %}
