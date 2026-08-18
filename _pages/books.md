---
layout: book-shelf
title: bookshelf
permalink: /books/
nav: true
nav_order: 6
collection: books
---

<div id="goodreads-recent" class="row mt-3"></div>

<script>
  const GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read";
  const PROXY_URL = "https://api.allorigins.win/raw?url=";
  const MAX_AGE_DAYS = 180;
  const MAX_BOOKS = 20;

  fetch(PROXY_URL + encodeURIComponent(GOODREADS_RSS))
    .then(res => {
      if (!res.ok) throw new Error("Network response failed");
      return res.text();
    })
    .then(str => new DOMParser().parseFromString(str, "text/xml"))
    .then(xml => {
      const container = document.getElementById("goodreads-recent");
      const items = Array.from(xml.querySelectorAll("item"));

      if (!items || items.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books found.</p>";
        return;
      }

      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - MAX_AGE_DAYS);

      // Helper to safely extract text from XML elements
      const getTagText = (item, tagName) => {
        const el = item.getElementsByTagName(tagName)[0];
        return el && el.textContent ? el.textContent.trim() : null;
      };

      const recentBooks = items.filter(item => {
        const dateStr = getTagText(item, "user_date_added") || getTagText(item, "pubDate");
        if (!dateStr) return true;
        return new Date(dateStr) >= cutoffDate;
      }).slice(0, MAX_BOOKS);

      if (recentBooks.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books added in the last 180 days.</p>";
        return;
      }

      container.innerHTML = recentBooks.map(item => {
        const title = getTagText(item, "title") || "Untitled";
        const link = getTagText(item, "link") || "#";
        const author = getTagText(item, "author_name") || "Unknown Author";
        const published = getTagText(item, "book_published");
        const avgRating = getTagText(item, "average_rating");
        const myRatingVal = getTagText(item, "user_rating");
        const dateAdded = getTagText(item, "user_date_added") || getTagText(item, "pubDate");

        // High-resolution image extraction
        let coverUrl = getTagText(item, "book_large_image_url") 
                    || getTagText(item, "book_medium_image_url") 
                    || getTagText(item, "book_image_url") 
                    || "";
        coverUrl = coverUrl.replace(/\._S[YX]\d+_\./g, '.').replace(/\._S[YX]\d+_/g, '');
        const isNoPhoto = !coverUrl || coverUrl.includes("nophoto");

        // Star Rating Formatting
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
                  ${dateAdded ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Added:</span> <strong>${dateAdded}</strong></li>` : ''}
                  <li class="d-flex justify-content-between py-1"><span class="text-muted">My Rating:</span> <span>${myRatingHtml}</span></li>
                </ul>
              </div>
            </div>
          </div>
        `;
      }).join('');
    })
    .catch(err => {
      console.error("Error fetching Goodreads RSS:", err);
      document.getElementById("goodreads-recent").innerHTML = "<p class='text-muted small'>Failed to load book feed.</p>";
    });
</script>
