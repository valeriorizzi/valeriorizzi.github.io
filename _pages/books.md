---
layout: book-shelf
title: bookshelf
permalink: /books/
nav: true
collection: books
---

<div id="goodreads-recent" class="row mt-3"></div>

<script>
  const GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read";
  const MAX_AGE_DAYS = 180;
  const MAX_BOOKS = 20;

  fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(GOODREADS_RSS)}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("goodreads-recent");
      if (!data || !data.items || data.items.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books found.</p>";
        return;
      }

      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - MAX_AGE_DAYS);

      const recentBooks = data.items
        .filter(item => new Date(item.pubDate) >= cutoffDate)
        .slice(0, MAX_BOOKS);

      if (recentBooks.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books added in the last 180 days.</p>";
        return;
      }

      const parser = new DOMParser();

      container.innerHTML = recentBooks.map(book => {
        const doc = parser.parseFromString(book.description, 'text/html');
        const img = doc.querySelector('img');
        
        // Extract image source and upscale resolution by removing compression filters
        let coverUrl = book.thumbnail || (img ? img.src : '');
        coverUrl = coverUrl.replace(/_SY\d+_|_SX\d+_\./g, '');

        // Extract author name from description metadata
        const authorMatch = doc.body.textContent.match(/author:\s*([^<]+)/i);
        const authorName = authorMatch ? authorMatch[1].trim() : '';

        return `
          <div class="col-md-3 col-sm-6 mb-4">
            <div class="card h-100 p-2 shadow-sm text-center">
              <a href="${book.link}" target="_blank" rel="noopener noreferrer">
                ${coverUrl 
                  ? `<img src="${coverUrl}" class="card-img-top mb-2" alt="${book.title}" style="max-height: 220px; object-fit: contain;">` 
                  : `<div class="p-4 bg-light text-muted small">No Cover Available</div>`}
              </a>
              <div class="card-body p-1 d-flex flex-column justify-content-between">
                <h6 class="card-title mb-1 small"><strong>${book.title}</strong></h6>
                ${authorName ? `<p class="card-text text-muted small mb-0">${authorName}</p>` : ''}
              </div>
            </div>
          </div>
        `;
      }).join('');
    })
    .catch(err => {
      console.error("Error fetching Goodreads feed:", err);
      document.getElementById("goodreads-recent").innerHTML = "<p class='text-muted small'>Failed to load book feed.</p>";
    });
</script>
