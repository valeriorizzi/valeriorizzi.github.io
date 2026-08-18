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
  const PROXY_URL = "https://api.allorigins.win/get?url=" + encodeURIComponent(GOODREADS_RSS);
  const MAX_AGE_DAYS = 180;
  const MAX_BOOKS = 20;

  fetch(PROXY_URL)
    .then(res => {
      if (!res.ok) throw new Error("Network response failed");
      return res.json();
    })
    .then(data => {
      const container = document.getElementById("goodreads-recent");
      if (!data || !data.contents) {
        container.innerHTML = "<p class='text-muted small'>Unable to fetch feed data.</p>";
        return;
      }

      const rawXml = data.contents;
      const itemMatches = rawXml.match(/<item>[\s\S]*?<\/item>/gi) || [];

      if (itemMatches.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books found in feed.</p>";
        return;
      }

      const getTag = (xmlStr, tag) => {
        const re = new RegExp(`<${tag}[^>]*>(.*?)</${tag}>`, 'si');
        const m = xmlStr.match(re);
        if (!m || !m[1]) return null;
        return m[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/gi, '$1').trim();
      };

      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - MAX_AGE_DAYS);

      const parsedBooks = [];

      for (const itemXml of itemMatches) {
        const dateStr = getTag(itemXml, "user_date_added") || getTag(itemXml, "pubDate");
        if (dateStr) {
          const bookDate = new Date(dateStr);
          if (!isNaN(bookDate.getTime()) && bookDate < cutoffDate) {
            continue;
          }
        }

        const title = getTag(itemXml, "title") || "Untitled";
        const link = getTag(itemXml, "link") || "#";
        const author = getTag(itemXml, "author_name") || "Unknown Author";
        const published = getTag(itemXml, "book_published");
        const avgRating = getTag(itemXml, "average_rating");
        const myRatingVal = getTag(itemXml, "user_rating");
        const dateAdded = getTag(itemXml, "user_date_added") || getTag(itemXml, "pubDate");

        let coverUrl = getTag(itemXml, "book_large_image_url") 
                    || getTag(itemXml, "book_medium_image_url") 
                    || getTag(itemXml, "book_image_url") 
                    || "";
        
        coverUrl = coverUrl.replace(/\._S[YX]\d+_\./g, '.').replace(/\._S[YX]\d+_/g, '');
        const isNoPhoto = !coverUrl || coverUrl.includes("nophoto");

        let formattedDate = dateAdded;
        if (dateAdded) {
          const d = new Date(dateAdded);
          if (!isNaN(d.getTime())) {
            formattedDate = d.toLocaleDateString('en-GB', { year: 'numeric', month: '2-digit', day: '2-digit' });
          }
        }

        parsedBooks.push({
          title, link, author, published, avgRating, myRatingVal, formattedDate, coverUrl, isNoPhoto
        });

        if (parsedBooks.length >= MAX_BOOKS) break;
      }

      if (parsedBooks.length === 0) {
        container.innerHTML = "<p class='text-muted small'>No books added in the last 180 days.</p>";
        return;
      }

      container.innerHTML = parsedBooks.map(book => {
        let myRatingHtml = '<span class="text-muted">Not rated</span>';
        const stars = parseInt(book.myRatingVal, 10);
        if (!isNaN(stars) && stars > 0) {
          myRatingHtml = `<span class="text-warning">${'★'.repeat(stars)}</span><span class="text-muted">${'☆'.repeat(5 - stars)}</span>`;
        }

        return `
          <div class="col-md-4 col-sm-6 mb-4">
            <div class="card h-100 shadow-sm border p-3">
              <a href="${book.link}" target="_blank" rel="noopener noreferrer" class="text-center mb-3 d-block">
                ${!book.isNoPhoto 
                  ? `<img src="${book.coverUrl}" class="card-img-top rounded" alt="${book.title}" style="max-height: 250px; object-fit: contain;">` 
                  : `<div class="p-4 bg-light rounded text-muted small border">No Cover Available</div>`}
              </a>
              <div class="card-body p-0 d-flex flex-column justify-content-between">
                <div>
                  <h6 class="card-title font-weight-bold mb-1">${book.title}</h6>
                  <p class="text-secondary small mb-3">by <strong>${book.author}</strong></p>
                </div>

                <ul class="list-unstyled small border-top pt-2 mb-0">
                  ${book.published ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Published:</span> <strong>${book.published}</strong></li>` : ''}
                  ${book.avgRating ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Avg Rating:</span> <strong>${book.avgRating} / 5</strong></li>` : ''}
                  ${book.formattedDate ? `<li class="d-flex justify-content-between py-1"><span class="text-muted">Added:</span> <strong>${book.formattedDate}</strong></li>` : ''}
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
