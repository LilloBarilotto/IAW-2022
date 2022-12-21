// definizioni tre array, copie shallow
let voto = [26, 21 ,24, 22, 30, 22, 30, 27, 27, 30, 28, 29, 22, 29, 28, 28, 27];
let voto_del = Array.from(voto);
let voto_add = Array.from(voto);
let avg_voto;



//funzione utili per la prima parte
const avg = function(x) {
    let res, i;
    for(i=0, res=0; i< x.length; i++){
        res+=x[i];
    }

    return Math.round(res/x.length);
}

const remove_min = function(x){
    let min, index_min, i;

    if(x.length<0)
        return undefined;

    for(i=1, min=x[0], index_min=0; i<x.length; i++)
        if(x[i]<min){
            min=x[i];
            index_min=i;
        }
    
    x.splice(index_min,1)
    return undefined;
}

const remove_max = function(x){
    let max, index_max, i;

    if(x.length<0)
        return undefined;

    for(i=1, max=x[0], index_max=0; i<x.length; i++)
        if(x[i]>max){
            max=x[i];
            index_max=i;
        }
    
    x.splice(index_max,1);
    return undefined;
}

// pt.1 rimozione min e max da copia array
    remove_min(voto_del);
    remove_max(voto_del);

// pt.2 aggiunta media 
    avg_voto = avg(voto);
    voto_add.unshift(avg_voto);
    voto_add.unshift(avg_voto);

// pt.3 stampa

    console.log(voto);
    console.log(voto_del);
    console.log(voto_add);