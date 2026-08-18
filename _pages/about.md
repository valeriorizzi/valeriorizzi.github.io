---
layout: about
title: about
permalink: /
subtitle: Senior Researcher (CS II), University of Geneva

profile:
  align: right
  image: DSC_9398_red.jpg #prof_pic.jpg
  image_circular: true # crops the image to make it circular
  more_info: >
    <p>rue Michel Servet 1</p>
    <p>Geneva 1205, Switzerland</p>
    <p>Office: CMU, B09.2018.a</p>
    <p>Phone: +41 (0)22 379 33 98</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

<style>
  /* Slightly scales down the profile image from al-folio default */
  .profile img {
    max-width: 82% !important;
    margin: 0 auto;
    display: block;
  }
</style>

I am a computational scientist and method developer at the University of Geneva, working at the intersection of statistical mechanics, biophysics and computational chemistry. My research focuses on advancing molecular dynamics simulations by developing enhanced sampling methodologies, particularly the OneOPES framework, and data-driven collective variables. Through the integration of statistical theory and efficient software implementation, I seek to overcome the timescale limitations of classical atomistic simulations, enabling the exploration and convergence of complex free energy landscapes.

<!-- Scholar Metrics & Publications CTA -->
<div class="scholar-section mt-4 pt-3 border-top text-center">
  <small class="text-muted d-block mb-3 font-weight-bold" style="letter-spacing: 0.5px; text-transform: uppercase; font-size: 0.75rem;">
    Google Scholar Impact & Metrics
  </small>
  
  <div class="d-flex flex-column flex-sm-row align-items-center justify-content-center" style="gap: 1.25rem;">
    <div>
      <img src="/assets/img/scholar_stats.svg" class="img-fluid rounded" alt="Google Scholar Stats" style="width: 100%; max-width: 320px;">
    </div>

    <div>
      <a href="{{ '/publications/' | relative_url }}" class="btn btn-outline-primary btn-sm">
        View All Publications &rarr;
      </a>
    </div>
  </div>
</div>
