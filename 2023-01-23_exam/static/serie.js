'use strict;'

/** serie.html  - Search ep by title and/or description inside the serie page **/
document.getElementById('titleEpFilter').addEventListener('keyup', e => {
    e.preventDefault();
  
    let filter = document.getElementById('titleEpFilter').value.toLowerCase();
    const episodes = document.querySelectorAll('.episode');
  
    for (let episode of episodes) {
      if (episode.querySelector('.episode-title').textContent.toLowerCase().includes(filter))
        episode.classList.remove('hide');
      else
        episode.classList.add('hide');
    }
  });
  
  document.getElementById('descriptionEpFilter').addEventListener('keyup', e => {
    e.preventDefault();
  
    let filter = document.getElementById('descriptionEpFilter').value.toLowerCase();
    const episodes = document.querySelectorAll('.episode');
  
    for (let episode of episodes) {
      if (episode.querySelector('.episode-description').textContent.toLowerCase().includes(filter))
        episode.classList.remove('hide')
      else
        episode.classList.add('hide')
    }
  });
  