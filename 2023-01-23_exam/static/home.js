'use strict;'


/** home.html --> Category managment, use the category_id that are saved inside the value to add or remove the '.hide' class **/
document.querySelectorAll('#filter-category > li > a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();

    const filter = link.getAttribute('data-value');
    const podcasts = document.querySelectorAll('.podcast');

    if (filter == -1) {  // -1 mean all
      for (let podcast of podcasts)
        podcast.classList.remove('hide')
    }
    else
      for (let podcast of podcasts) {
        if (podcast.getAttribute('data-value') == filter)
          podcast.classList.remove('hide')
        else
          podcast.classList.add('hide')
      }
  });
});


/** home.html  - Search serie by title in homepage **/
document.getElementById('titleFilter').addEventListener('keyup', e => {
  e.preventDefault();

  let filter = document.getElementById('titleFilter').value.toLowerCase();
  const podcasts = document.querySelectorAll('.podcast');

  for (let podcast of podcasts) {
    if (podcast.querySelector('.card-title').textContent.toLowerCase().includes(filter))
      podcast.classList.remove('hide');
    else
      podcast.classList.add('hide');
  }
});