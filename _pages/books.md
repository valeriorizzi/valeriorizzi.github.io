---
layout: book-shelf
title: bookshelf
permalink: /books/
nav: true
nav_order: 6
collection: books
---

<style>
  /* Pointer (hand) cursor for all buttons and interactive controls */
  .btn,
  .btn-group .btn,
  #goodreads-controls button {
    cursor: pointer !important;
  }

  /* Title styling with strict 2-line clamp and fixed height to prevent layout breaks */
  .book-card-title {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    word-break: break-word;
    font-size: 0.82rem;
    line-height: 1.25;
    height: 2.5em; /* Fixed height for 2 lines to align cards perfectly */
  }
</style>

<div class="goodreads-shelf mb-5">
  <div class="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center mb-3 border-bottom pb-2">
    <h3 class="font-weight-bold mb-2 mb-sm-0" style="font-size: 1.25rem;">Bookshelf</h3>
    
    <!-- Dynamic Filter & Sort Controls -->
    <div id="goodreads-controls" class="d-flex flex-wrap align-items-center" style="display: none;">
      <div class="btn-group btn-group-sm mr-2 mb-1" role="group" aria-label="Sort Order">
        <button type="button" class="btn btn-outline-secondary" id="btn-recent">Most Recent</button>
        <button type="button" class="btn btn-outline-secondary active" id="btn-random">Random</button>
      </div>
      <div class="btn-group btn-group-sm mb-1" role="group" aria-label="Rating Filter">
        <button type="button" class="btn btn-outline-secondary active" id="btn-all-stars">All Books</button>
        <button type="button" class="btn btn-outline-secondary" id="btn-5-stars">★ 5 Stars Only</button>
      </div>
    </div>
  </div>

  <div id="goodreads-recent" class="row">
    <div class="col-12 text-center py-4">
      <div class="spinner-border text-secondary" role="status">
        <span class="sr-only">Loading books...</span>
      </div>
    </div>
  </div>
</div>

{% raw %}
<script>
document.addEventListener("DOMContentLoaded", function() {
  const GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read";
  
  // Default Configurations: Fully random selection out of all read books
  let currentMode = "random";  // "random" or "recent"
  let onlyFiveStars = false;   // false for all read books, true to filter 5 stars
  const MAX_BOOKS = 12;

  let cachedItems = [];

  // Fallback array of CORS proxies
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

  const getTagText = (item, tagName) => {
    const el = item.getElementsByTagName(tagName)[0];
    return el && el.textContent ? el.textContent.trim() : null;
  };

  function renderBooks() {
    const container = document.getElementById("goodreads-recent");
    if (!cachedItems || cachedItems.length === 0) {
      container.innerHTML = "<div class='col-12'><p class='text-muted small'>No books found on this shelf.</p></div>";
      return;
    }

    // 1. Filter by 5-star rating if enabled
    let filtered = cachedItems.slice();
    if (onlyFiveStars) {
      filtered = filtered.filter(item => {
        const rating = parseInt(getTagText(item, "user_rating"), 10);
        return rating === 5;
      });
    }

    if (filtered.length === 0) {
      container.innerHTML = "<div class='col-12'><p class='text-muted small'>No 5-star books found in the feed.</p></div>";
      return;
    }

    // 2. Sort or Shuffle
    if (currentMode === "recent") {
      filtered.sort((a, b) => {
        const dateA = new Date(getTagText(a, "user_date_added") || getTagText(a, "pubDate") || 0);
        const dateB = new Date(getTagText(b, "user_date_added") || getTagText(b, "pubDate") || 0);
        return dateB - dateA; // Descending order (newest first)
      });
    } else if (currentMode === "random") {
      // Fisher-Yates shuffle
      for (let i = filtered.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [filtered[i], filtered[j]] = [filtered[j], filtered[i]];
      }
    }

    // 3. Slice to MAX_BOOKS
    const displayBooks = filtered.slice(0, MAX_BOOKS);

    container.innerHTML = displayBooks.map(item => {
      const rawTitle = getTagText(item, "title") || "Untitled";
      
      // Strip parenthetical series metadata (e.g. "(La saga di Geralt di Rivia, #6)")
      let title = rawTitle.replace(/\s*\([^)]*\)/g, "").trim();
      
      // Hard length limit fallback to prevent overflow on extra long titles
      const MAX_TITLE_LEN = 35;
      if (title.length > MAX_TITLE_LEN) {
        title = title.substring(0, MAX_TITLE_LEN).trim() + "…";
      }

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
                    <h6 class="card-title font-weight-bold mb-1 book-card-title" title="${rawTitle}">${title}</h6>
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
  }

  // Bind Control Buttons
  const btnRecent = document.getElementById("btn-recent");
  const btnRandom = document.getElementById("btn-random");
  const btnAllStars = document.getElementById("btn-all-stars");
  const btn5Stars = document.getElementById("btn-5-stars");
  const feedControls = document.getElementById("goodreads-controls");

  if (btnRecent && btnRandom) {
    btnRecent.addEventListener("click", function() {
      currentMode = "recent";
      btnRecent.classList.add("active");
      btnRandom.classList.remove("active");
      renderBooks();
    });
    btnRandom.addEventListener("click", function() {
      currentMode = "random";
      btnRandom.classList.add("active");
      btnRecent.classList.remove("active");
      renderBooks();
    });
  }

  if (btnAllStars && btn5Stars) {
    btnAllStars.addEventListener("click", function() {
      onlyFiveStars = false;
      btnAllStars.classList.add("active");
      btn5Stars.classList.remove("active");
      renderBooks();
    });
    btn5Stars.addEventListener("click", function() {
      onlyFiveStars = true;
      btn5Stars.classList.add("active");
      btnAllStars.classList.remove("active");
      renderBooks();
    });
  }

  fetchFeed().then(xmlText => {
    const container = document.getElementById("goodreads-recent");
    if (!xmlText) {
      container.innerHTML = "<div class='col-12'><p class='text-muted small'>Unable to fetch Goodreads feed. Please try refreshing.</p></div>";
      return;
    }

    const xml = new DOMParser().parseFromString(xmlText, "text/xml");
    cachedItems = Array.from(xml.querySelectorAll("item"));

    if (feedControls) {
      feedControls.style.display = "flex";
    }

    renderBooks();
  }).catch(err => {
    console.error("Error loading Goodreads feed:", err);
    document.getElementById("goodreads-recent").innerHTML = "<div class='col-12'><p class='text-muted small'>Failed to load book feed.</p></div>";
  });
});
</script>
{% endraw %}
