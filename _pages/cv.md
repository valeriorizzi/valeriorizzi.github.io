---
layout: page
title: CV
permalink: /cv/
nav: true
nav_order: 5
description: Curriculum Vitae
---

<div class="cv">
  {% for section in site.data.cv.sections %}
    <div class="card mt-4 p-3 shadow-sm">
      <h3 class="card-title font-weight-medium border-bottom pb-2">{{ section[0] }}</h3>

      <!-- Education Section -->
      {% if section[0] == "Education" %}
        {% for entry in section[1] %}
          <div class="mb-3">
            <div class="d-flex justify-content-between align-items-baseline">
              <h5 class="mb-0">
                <strong>{{ entry.studyType }} in {{ entry.area }}</strong>
                {% if entry.url %}<a href="{{ entry.url }}" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-link fa-xs ml-1"></i></a>{% endif %}
              </h5>
              <span class="text-muted small">{{ entry.start_date }} – {{ entry.end_date }}</span>
            </div>
            <div class="text-secondary font-weight-bold">{{ entry.institution }}{% if entry.location %}, <span class="font-weight-normal">{{ entry.location }}</span>{% endif %}</div>
            {% if entry.score %}<div class="text-muted small">Grade: {{ entry.score }}</div>{% endif %}
            {% if entry.highlights %}
              <ul class="mt-2 pl-3 small">
                {% for hl in entry.highlights %}
                  <li>{{ hl }}</li>
                {% endfor %}
              </ul>
            {% endif %}
          </div>
        {% endfor %}

      <!-- Experience Section -->
      {% elsif section[0] == "Experience" %}
        {% for entry in section[1] %}
          <div class="mb-3">
            <div class="d-flex justify-content-between align-items-baseline">
              <h5 class="mb-0"><strong>{{ entry.position }}</strong></h5>
              <span class="text-muted small">{{ entry.start_date }} – {{ entry.end_date }}</span>
            </div>
            <div class="text-secondary font-weight-bold">{{ entry.company }}{% if entry.location %}, <span class="font-weight-normal">{{ entry.location }}</span>{% endif %}</div>
            {% if entry.highlights %}
              <ul class="mt-2 pl-3 small">
                {% for hl in entry.highlights %}
                  <li>{{ hl }}</li>
                {% endfor %}
              </ul>
            {% endif %}
          </div>
        {% endfor %}

      <!-- Skills and Categorized Research Interests -->
      {% elsif section[0] == "Skills" or section[0] == "Research Interests" %}
        {% for entry in section[1] %}
          {% if entry.name %}
            <div class="mb-2">
              <strong>{% if entry.icon %}<i class="{{ entry.icon }} mr-1"></i>{% endif %}{{ entry.name }}:</strong>
              <span class="text-muted">{{ entry.keywords }}</span>
            </div>
          {% else %}
            <div class="py-1">• {{ entry }}</div>
          {% endif %}
        {% endfor %}

      <!-- Languages Section -->
      {% elsif section[0] == "Languages" %}
        <div class="row">
          {% for entry in section[1] %}
            <div class="col-md-6 py-1">
              <strong>{{ entry.name }}:</strong> <span class="text-muted">{{ entry.summary }}</span>
            </div>
          {% endfor %}
        </div>

      <!-- General Fallback -->
      {% else %}
        {% for entry in section[1] %}
          <div class="py-1">
            {% if entry.name %}<strong>{{ entry.name }}</strong>{% endif %}{% if entry.summary %}: {{ entry.summary }}{% endif %}
          </div>
        {% endfor %}
      {% endif %}
    </div>
  {% endfor %}
</div>

<!-- Live Publications Sync from _bibliography/papers.bib -->
<div class="card mt-4 p-3 shadow-sm">
  <h3 class="card-title font-weight-medium border-bottom pb-2">Publications</h3>
  <div class="publications mt-3">
    {% bibliography %}
  </div>
</div>
