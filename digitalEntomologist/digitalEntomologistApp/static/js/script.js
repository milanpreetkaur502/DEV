const STATE={
    activeModalBtnName:"device",
    activeModalBtn:document.getElementById("modalSidePanelDeviceBtn").classList,
    prevConfigCard:document.getElementById("configCardsForDevice").classList,
    addJobBtn:document.getElementById("addJobBtn"),
    addJobBtnHolder:document.getElementById("addJobBtnHolder"),
    jobCardsDisplayer:document.getElementById("jobCardsDisplayer"),
}

const job={
    deviceId:null,
    device:new Map(),
    cloud:new Map(),
    camera:new Map(),
    getLogs:new Map(),
    getData:new Map()
}

function sendHandler(){
    job.device=Object.fromEntries(job.device);
    job.cloud=Object.fromEntries(job.cloud);
    job.camera=Object.fromEntries(job.camera);
    job.getLogs=Object.fromEntries(job.getLogs);
    job.getData=Object.fromEntries(job.getData);
    let jsonData = JSON.stringify(job);

    const url = "https://aaxsxrwma8.execute-api.us-east-1.amazonaws.com/sendJob"
    let fetchData = {
        method:'POST',
        body : jsonData,

    }

    fetch(url,fetchData)
    .then(
        (response)=>{
            response.json()
            .then((data)=>{console.log(data);
                                            
            });
        })
    
}

function addJobHandler(element){
    let div = element.parentElement;
    let inp = element.previousSibling.previousSibling;
    let value = inp.value;
    let key = inp.name;
    if (value==""){
        return null;
    }
    if(STATE.activeModalBtnName=="device"){
        job.device.set(key,value);
    }else if(STATE.activeModalBtnName=="cloud"){
        job.cloud.set(key,value);
    }else if(STATE.activeModalBtnName=="camera"){
        job.camera.set(key,value)
    }else if(STATE.activeModalBtnName=="getLogs"){
        job.getLogs.set(key,value);
    }else if(STATE.activeModalBtnName=="getData"){
        job.getData.set(key,value);
    }else{
        return null
    }
    STATE.addJobBtnHolder.appendChild(STATE.addJobBtn);
    div.remove();
    let newJobCard=document.createElement("div");
    newJobCard.classList=["w3-container w3-card w3-white w3-round w3-large w3-padding"]
    newJobCard.style.marginBottom="5px";
    newJobCard.innerText = key+" : "+value;
    STATE.jobCardsDisplayer.appendChild(newJobCard);
}

function configCardClickHandler(cardElement){
    cardElement.appendChild(STATE.addJobBtn);
}

function modalSidePanelBtnHandler(btnElement){
    let classArray = btnElement.classList;
    if(classArray==STATE.activeModalBtn){
        return;
    }

    classArray.remove("w3-text-white");classArray.remove("w3-transparent");
    classArray.add("activeBtnInModal");

    let prevClassArray=STATE.activeModalBtn;
    prevClassArray.remove("activeBtnInModal");
    prevClassArray.add("w3-text-white");prevClassArray.add("w3-transparent");
    
    STATE.prevConfigCard.remove("w3-visible");
    STATE.prevConfigCard.add("w3-hide");

    let upcomingCard = document.getElementById(btnElement.getAttribute("data-btnBindedToCard")).classList;
    upcomingCard.remove("w3-hide");
    upcomingCard.add("w3-visible");

    STATE.activeModalBtn=classArray;
    STATE.prevConfigCard=upcomingCard;
    STATE.activeModalBtnName=btnElement.value;
}

function openConfigModel(btnElement){
    let modal = document.getElementById("modalForConfig");
    modal.style.display='block';
    let modalHeader = document.getElementById('modalHeader');
    modalHeader.innerText="You are sending job to device "+btnElement.value;
    job.deviceId=btnElement.value;
}

function deviceRegistrationFormToggler(){
    let form=document.getElementById('deviceRegistrationForm');
    form.style.display='block';
}
function cancelRegistrationHandler(){
    let form=document.getElementById('deviceRegistrationForm');
    form.style.display='none';
}
