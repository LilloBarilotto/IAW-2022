let books = [
    {
        id : 1,
        title : "Idk really",
        author : "rt",
        date : dayjs("2000-11-02"),
        review : 3
    },
    {
        id : 2,
        title : "Bello",
        author : "impossibile",
        date : dayjs("2022-01-10")
    }
];

const addBook = function(x, books){

    if(!x.id || !x.author || !x.title){
        console.log("Il libro " + x + "non è stato inserito in array non avendo tutte le prop obbligatorie");
        return undefined;
    }
    
    for (const book of books)
        if(book.id === x.id){
            console.log("Id del libro " + x + "è gia' presente tra i vari libri!");
            return undefined;
        }

    return books.push(x);
}

const removeBook = function(x, books){

    const index = books.findIndex(book => book.id === x.id);
    books.splice(index, index >= 0 ? 1 : 0);
}

const avgBooks = function (books){
    let tmp=0, count=0;

    for(const book in books)
        if(book.review){
            tmp+=book.review;
            count++;
        }
    
    if(count===0)
        return NaN;
    
    return Math.round(tmp/count);
}

const delayRelease = function(n, books){

    for(let book in books)
        book.date = book.date.add(n,'day');
}

let libropresente = {
        id : 1,
        title : "Idk really with diff title but same id",
        author : "rt",
        date : dayjs("2000-02-11"),
        review : 3
}

let libronuovo = {
    id : 4,
    title : "Sono nuovo",
    author : "rt",
    date : dayjs("2000-02-11"),
    review: 5
}

console.log("Exercise 2:");
console.log("Stampa data di books[1] per sicurezza: "+books[1].date.format('DD/MM/YYYY'));

console.log("Aggiunta libro che darà errore");
addBook(libropresente, books);
console.log(books);

console.log("Aggiunta libro OK");
addBook(libronuovo, books);
console.log(books);

console.log("Rimuovi quest'ultimo libro");
removeBook(libronuovo, books);
console.log(books);

console.log("Media recensioni: "+ avgBooks(books));

console.log("Date rispetto a prima spostate di 7 giorni");
delayRelease(7, books);
console.log(books);
