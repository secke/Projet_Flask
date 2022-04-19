const bouttonValid=document.querySelector('.boutValid')
const motPass=document.querySelector('#mp')


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




bouttonValid.addEventListener('click',()=>{
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
});