
function repererlogin(){
    log=document.querySelector("#log")
   
    return log
    

}

mylog=repererlogin()

var evLien=document.querySelector('#lien_connex')

// evLien.addEventListener('click',()=>{
//     var us=document.querySelector('#username')
//     var log=document.querySelector('#log')
//     log.value=us.innerText
// })
function recupusername(){
   us=document.getElementById("username");
   return us.innerText;

   
}
// valeur_log=recupusername()
// console.log(valeur_log);








const mesFonctions= {special:function(){
    petite=function (x,y){
        x=Math.ceil(x)
        y=Math.floor(y)
        return Math.floor(Math.random()*(y-x))+x;};
    var valCaract= String.fromCharCode(petite(33,47))+String.fromCharCode(petite(58,64))
    +String.fromCharCode(petite(91,96))+String.fromCharCode(petite(123,126));
    n=Math.floor(Math.random()*valCaract.length)
    return valCaract[n]
},
nombre:function(){
    return Math.floor(Math.random()*10)
},
letMinus:function(){
    let valM="abcdefghijklmnopqrstuvwxyz"
    return valM[Math.floor(Math.random()*valM.length)]
},
letMaj:function(){
    let v00="abcdefghijklmnopqrstuvwxyz"
    let v01=v00.toUpperCase()
    return v01[Math.floor(Math.random()*v01.length)]
}};


function valider(){
    var rt='';
    var r01='',r02='',r03='',r04='';
    for(let i=0;i<15;i++){
        r01+=mesFonctions.letMaj()
        r02+=mesFonctions.letMinus()
        r03+=mesFonctions.nombre()
        r04+=mesFonctions.special()}
    rt=r01+r02+r03+r04;
    var rfinal='';
    for(let i=0;i<15;i++){
        rfinal+=rt[Math.floor(Math.random()*rt.length)]
                }
        motPass.value=rfinal;
    
    
}


// bouttonValid.addEventListener('click',()=>{
    
// });
