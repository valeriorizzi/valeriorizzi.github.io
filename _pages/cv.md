---
layout: cv
permalink: /cv/
title: CV
nav: true
nav_order: 5
cv_pdf: # you can also use external links here
cv_format: rendercv # options: rendercv, jsonresume
description: This is a description of the page. You can modify it in '_pages/cv.md'. You can also change or remove the top pdf download button.
toc:
  sidebar: left
---

<!-- Auto-rendered Publications from _bibliography/papers.bib -->
<div class="post">
  <header class="post-header">
    <h1 class="post-title">publications</h1>
  </header>

  <article>
    <div class="publications">
      {% bibliography %}
    </div>
  </article>
</div>
