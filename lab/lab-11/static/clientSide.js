'use strict;'

document.querySelectorAll('#filter-day-ul > li > a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
        
    const filter = link.text;

    let minDate, maxDate;

    if(filter == "Oggi"){
        minDate= dayjs();
        maxDate= minDate;
    }
    else if (filter == "Questa settimana"){
        //minDate = dayjs().startOf('week');    --> Da inizio settimana ad oggi (es, oggi mercoledi <=> lun,mart,merc)
        maxDate = dayjs();
        minDate = maxDate.subtract(7, 'day')
    }
    else if (filter == "Questo mese"){
      minDate = dayjs().startOf('month');
      maxDate = dayjs().endOf('month');
    }
    else
        console.log("Errore nel filtro..");

    console.log(minDate.format('DD/MM/YYYY'));
    console.log(maxDate.format('DD/MM/YYYY'));
    
    // aggiungi classe 'hide' con display: none in style.css e modifica codice qui sotto per rimuovere l'articolo

    const articles = document.querySelectorAll('article');
    for (let article of articles) {
      
      let dateArticle = dayjs(article.querySelector('.flex-grow-1 > p').innerText);
      console.log(article);
      console.log(dateArticle.format('DD/MM/YYYY'));

      if( dateArticle.isBefore(minDate, 'day') || dateArticle.isAfter(maxDate, 'day'))
        article.classList.add('hide');
      else
        article.classList.remove('hide');
    }
  });
});



document.querySelectorAll('#order-ul > li > a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
        
    const filter = link.text;

    let m = document.getElementById('main-mylist');

    if(filter == "Dal più recente"){
      Array.prototype.slice.call(m.children)
      .map(function (x) { return m.removeChild(x); })
      .sort(function (x, y) {
        return dayjs(x.querySelector('.flex-grow-1 > p').innerText)
                      .isBefore(dayjs(y.querySelector('.flex-grow-1 > p').innerText));
      })
      .forEach(function (x) { m.appendChild(x); });
    }
    else if (filter == "Dal meno recente"){
      Array.prototype.slice.call(m.children)
      .map(function (x) { return m.removeChild(x); })
      .sort(function (x, y) {
        return dayjs(x.querySelector('.flex-grow-1 > p').innerText)
                      .isAfter(dayjs(y.querySelector('.flex-grow-1 > p').innerText));
      })
      .forEach(function (x) { m.appendChild(x); });
    }
    else
      console.log("Problema nel reorder di tutto");
  
  });
});