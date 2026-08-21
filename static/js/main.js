console.log("NyumbaHunt JS loaded!");

const photoInput=document.getElementById("photoInput");
const preview=document.getElementById("preview");
if(photoInput){
  photoInput.addEventListener("change",()=>{
    const f=photoInput.files[0];
    if(f){
      preview.src=URL.createObjectURL(f);
      preview.style.display="block";
    }
  });
}
if(typeof io!== "undefined"){
  const socket=io();
  socket.on("new_house",(h)=>{
    const notif=document.createElement("div");
    notif.className="live-notif";
    notif.innerHTML=`🔴 LIVE: New ${h.beds} in ${h.location} for KES ${h.price}!`;
    document.body.appendChild(notif);
    setTimeout(()=>notif.remove(),5000);
  });
}
