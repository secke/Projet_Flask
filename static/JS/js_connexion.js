


function repererlogin(){
    log=document.querySelector("#log")
   
    return log
    
}
mylog=repererlogin()
function recupusername(event){
    parent=event.target.parentNode.querySelector("#username").innerText;
    const dict_username={parent};
    const fic_json=JSON.stringify(dict_username);
}

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
        motPass=document.getElementById("mp")
        motPass.value=rfinal;
        console.log(rfinal);
    
    
}

var choice_nbr_user = document.querySelector('.choice_user')

var btn_affiche = document.querySelector('.btn_affiche')

var choice_user = document.querySelector('.btn_choice_user')

// console.log(choice_user)

// choice_user.addEventListener('click', ()=>{
//     choice_nbr_user.style.display = 'none'
//     // alert("choix  effectue")
// })

// btn_affiche.addEventListener('click', ()=>{
//     // choice_nbr_user.style.display ='flex'
//     document.body.appendChild(choice_nbr_user)
//     choice_user.classList.toggle('btn_affiche_visible')
//     // alert('ça marche')
// })

// ################|||| Récupération des information du user après click ||||################

var article_user = document.querySelector('.div_article_user')

// console.log(article_user)


// bouttonValid.addEventListener('click',()=>{
    
// });



const eye = document.querySelector(".beut_ler");
const eyeoff = document.querySelector(".beut_lendem");
const passwordField=document.querySelector("input[type=password]");
console.log(eye)
eye.addEventListener("click", () => {
  eye.style.display = "none";
  eyeoff.style.display = "block";

  passwordField.type = "text";
});

eyeoff.addEventListener("click", () => {
  eyeoff.style.display = "none";
  eye.style.display = "block";

  passwordField.type = "password";
});
