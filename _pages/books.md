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
  const MAX_AGE_DAYS = 360;
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
        const htmlContent = doc.body.innerHTML;

        // Extract and clean up cover image for maximum resolution
        const imgTag = doc.querySelector('img');
        let coverUrl = imgTag ? imgTag.src : (book.thumbnail || '');
        coverUrl = coverUrl
          .replace(/\._S[YX]\d+_\./g, '.')
          .replace(/\._S[YX]\d+_/g, '')
          .replace(/\._U[XY]\d+_/g, '');
        const isNoPhoto = !coverUrl || coverUrl.includes('nophoto');

        // Extract individual fields using exact regex matching on HTML string
        const parseField = (regex) => {
          const match = htmlContent.match(regex);
          return (match && match[1] && match[1].trim() !== '') ? match[1].trim() : null;
        };

        const author = parseField(/author:\s*([^<]+)/i) || book.author || 'Unknown Author';
        const published = parseField(/book published:\s*([^<]+)/i);
        const avgRating = parseField(/average rating:\s*([\d\.]+)/i);
        const myRatingVal = parseField(/rating:\s*(\d+)/i);
        const dateAdded = parseField(/date added:\s*([^<]+)/i);

        // Format star rating
        let myRatingHtml = '<span class="text-muted">Not rated</span>';
        if (myRatingVal && parseInt(myRatingVal) > 0) {
          const stars = parseInt(myRatingVal);
          myRatingHtml = `<span class="text-warning">${'★'.repeat(stars)}</span><span class="text-muted">${'☆'.repeat(5 - stars)}</span>`;
        }

        return `
          <div class="col-md-4 col-sm-6 mb-4">
            <div class="card h-100 shadow-sm border p-3">
              <a href="${book.link}" target="_blank" rel="noopener noreferrer" class="text-center mb-3 d-block">
                ${!isNoPhoto 
                  ? `<img src="${coverUrl}" class="card-img-top rounded" alt="${book.title}" style="max-height: 250px; object-fit: contain;">` 
                  : `<div class="p-4 bg-light rounded text-muted small border">No Cover Available</div>`}
              </a>
              <div class="card-body p-0 d-flex flex-column justify-content-between">
                <div>
                  <h6 class="card-title font-weight-bold mb-1">${book.title}</h6>
                  <p class="text-secondary small mb-3">by <strong>${author}</strong></p>
                </div>

                <ul class="list-unstyled small border-top pt-2 mb-0">
                  ${published ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Published:</span> <strong>${published}</strong></li>` : ''}
                  ${avgRating ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Avg Rating:</span> <strong>${avgRating} / 5</strong></li>` : ''}
                  ${dateAdded ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Date Added:</span> <strong>${dateAdded}</strong></li>` : ''}
                  <li class="d-flex justify-content-between py-1"><span class="text-muted">My Rating:</span> <span>${myRatingHtml}</span></li>
                </ul>
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
