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
        <div class="col-md-6 mb-3">
          <div class="card h-100 shadow-sm border p-2">
            <div class="row no-gutters align-items-center flex-nowrap h-100">
              <div class="col-4 text-center pr-1 flex-shrink-0">
                <a href="${link}" target="_blank" rel="noopener noreferrer" class="d-block p-1">
                  ${!isNoPhoto 
                    ? `<img src="${coverUrl}" class="img-fluid rounded" alt="${title}" style="max-height: 145px; object-fit: contain;">` 
                    : `<div class="p-2 bg-light rounded text-muted extra-small border">No Cover</div>`}
                </a>
              </div>
              <div class="col-8 pl-2 pr-2" style="min-width: 0;">
                <div class="card-body p-0 d-flex flex-column justify-content-between h-100">
                  <div>
                    <h6 class="card-title font-weight-bold mb-1" style="font-size: 0.82rem; line-height: 1.25; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; word-break: break-word;" title="${title}">${title}</h6>
                    <p class="text-secondary mb-2" style="font-size: 0.75rem; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis;">by <strong>${author}</strong></p>
                  </div>

                  <ul class="list-unstyled border-top pt-1 mb-0" style="font-size: 0.72rem;">
                    ${published ? `<li class="d-flex justify-content-between py-0"><span class="text-muted">Published:</span> <span>${published}</span></li>` : ''}
                    ${avgRating ? `<li class="d-flex justify-content-between py-0"><span class="text-muted">Avg Rating:</span> <span>${avgRating} / 5</span></li>` : ''}
                    ${formattedDate ? `<li class="d-flex justify-content-between py-0"><span class="text-muted">Added:</span> <span>${formattedDate}</span></li>` : ''}
                    <li class="d-flex justify-content-between py-0"><span class="text-muted">My Rating:</span> <span>${myRatingHtml}</span></li>
                  </ul>
                </div>
              </div>
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
