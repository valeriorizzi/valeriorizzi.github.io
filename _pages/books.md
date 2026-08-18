---
layout: book-shelf
title: bookshelf
permalink: /books/
nav: true
collection: books
---

<div id="goodreads-recent" class="row mt-3"></div>

<script>
  // Replace YOUR_USER_ID with your actual Goodreads ID number
  const GOODREADS_RSS = "https://www.goodreads.com/review/list_rss/28031214-valerio?shelf=read";
  const MAX_AGE_DAYS = 180; // Filter out books added older than 60 days ago
  const MAX_BOOKS = 20;      // Maximum number of recent books to display

  fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(GOODREADS_RSS)}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("goodreads-recent");
      if (!data.items) return;

      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - MAX_AGE_DAYS);

      // Filter by date added and slice to get only the latest entries
      const recentBooks = data.items
        .filter(item => new Date(item.pubDate) >= cutoffDate)
        .slice(0, MAX_BOOKS);

      if (recentBooks.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books added in the last 60 days.</p>";
        return;
      }

      container.innerHTML = recentBooks.map(book => `
        <div class="col-md-4 col-sm-6 mb-3">
          <div class="card h-100 p-2 shadow-sm text-center">
            <a href="${book.link}" target="_blank" rel="noopener noreferrer">
              <img src="${book.thumbnail}" class="card-img-top mb-2" alt="${book.title}" style="max-height: 180px; object-fit: contain;">
            </a>
            <div class="card-body p-1">
              <h6 class="card-title mb-1 small"><strong>${book.title}</strong></h6>
              <p class="card-text text-muted small">${book.author}</p>
            </div>
          </div>
        </div>
      `).join('');
    })
    .catch(err => console.error("Error fetching Goodreads feed:", err));
</script>

