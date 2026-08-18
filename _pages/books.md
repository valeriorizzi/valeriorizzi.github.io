---
layout: book-shelf
title: bookshelf
permalink: /books/
nav: true
nav_order: 6
collection: books
---

<div id="goodreads-recent" class="row mt-3">
  <div class="col-12 text-center py-4">
    <div class="spinner-border text-secondary" role="status">
      <span class="sr-only">Loading books...</span>
    </div>
  </div>
</div>

{% raw %}
<script>
document.addEventListener("DOMContentLoaded", function() {
  const GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read";
  
  // Configuration options:
  // DISPLAY_MODE: "random" for random selection, "recent" for most recent
  const DISPLAY_MODE = "random"; 
  const MAX_BOOKS = 10;

  // Fallback array of CORS proxies in case one is blocked
  const PROXIES = [
    "https://corsproxy.io/?" + encodeURIComponent(GOODREADS_RSS),
    "https://api.allorigins.win/raw?url=" + encodeURIComponent(GOODREADS_RSS)
  ];

  async function fetchFeed() {
    for (const proxy of PROXIES) {
      try {
        const res = await fetch(proxy);
        if (res.ok) {
          const text = await res.text();
          if (text && text.includes("<item>")) return text;
        }
      } catch (e) {
        console.warn("Proxy attempt failed:", proxy, e);
      }
    }
    return null;
  }

  fetchFeed().then(xmlText => {
    const container = document.getElementById("goodreads-recent");
    if (!xmlText) {
      container.innerHTML = "<div class='col-12'><p class='text-muted small'>Unable to fetch Goodreads feed. Please try refreshing.</p></div>";
      return;
    }

    const xml = new DOMParser().parseFromString(xmlText, "text/xml");
    let items = Array.from(xml.querySelectorAll("item"));

    if (!items || items.length === 0) {
      container.innerHTML = "<div class='col-12'><p class='text-muted small'>No books found on this shelf.</p></div>";
      return;
    }

    const getTagText = (item, tagName) => {
      const el = item.getElementsByTagName(tagName)[0];
      return el && el.textContent ? el.textContent.trim() : null;
    };

    // Apply sorting/selection based on DISPLAY_MODE
    if (DISPLAY_MODE === "random") {
      // Fisher-Yates shuffle
      for (let i = items.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [items[i], items[j]] = [items[j], items[i]];
      }
    }

    const displayBooks = items.slice(0, MAX_BOOKS);

    container.innerHTML = displayBooks.map(item => {
      const title = getTagText(item, "title") || "Untitled";
      const link = getTagText(item, "link") || "#";
      const author = getTagText(item, "author_name") || "Unknown Author";
      const published = getTagText(item, "book_published");
      const avgRating = getTagText(item, "average_rating");
      const myRatingVal = getTagText(item, "user_rating");
      const dateAdded = getTagText(item, "user_date_added") || getTagText(item, "pubDate");

      let coverUrl = getTagText(item, "book_large_image_url") 
                  || getTagText(item, "book_medium_image_url") 
                  || getTagText(item, "book_image_url") 
                  || "";
      
      coverUrl = coverUrl.replace(/\._S[YX]\d+_\./g, '.').replace(/\._S[YX]\d+_/g, '');
      const isNoPhoto = !coverUrl || coverUrl.includes("nophoto");

      let formattedDate = "";
      if (dateAdded) {
        const d = new Date(dateAdded);
        if (!isNaN(d.getTime())) {
          formattedDate = d.toLocaleDateString('en-GB', { year: 'numeric', month: '2-digit', day: '2-digit' });
        }
      }

      let myRatingHtml = '<span class="text-muted">Not rated</span>';
      const stars = parseInt(myRatingVal, 10);
      if (!isNaN(stars) && stars > 0) {
        myRatingHtml = `<span class="text-warning">${'★'.repeat(stars)}</span><span class="text-muted">${'☆'.repeat(5 - stars)}</span>`;
      }

      return `
        <div class="col-md-4 col-sm-6 mb-4">
          <div class="card h-100 shadow-sm border p-3">
            <a href="${link}" target="_blank" rel="noopener noreferrer" class="text-center mb-3 d-block">
              ${!isNoPhoto 
                ? `<img src="${coverUrl}" class="card-img-top rounded" alt="${title}" style="max-height: 250px; object-fit: contain;">` 
                : `<div class="p-4 bg-light rounded text-muted small border">No Cover Available</div>`}
            </a>
            <div class="card-body p-0 d-flex flex-column justify-content-between">
              <div>
                <h6 class="card-title font-weight-bold mb-1">${title}</h6>
                <p class="text-secondary small mb-3">by <strong>${author}</strong></p>
              </div>

              <ul class="list-unstyled small border-top pt-2 mb-0">
                ${published ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Published:</span> <strong>${published}</strong></li>` : ''}
                ${avgRating ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Avg Rating:</span> <strong>${avgRating} / 5</strong></li>` : ''}
                ${formattedDate ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Added:</span> <strong>${formattedDate}</strong></li>` : ''}
                <li class="d-flex justify-content-between py-1"><span class="text-muted">My Rating:</span> <span>${myRatingHtml}</span></li>
              </ul>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }).catch(err => {
    console.error("Error loading Goodreads feed:", err);
    document.getElementById("goodreads-recent").innerHTML = "<div class='col-12'><p class='text-muted small'>Failed to load book feed.</p></div>";
  });
});
</script>
{% endraw %}
