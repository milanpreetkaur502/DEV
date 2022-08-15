const STATE={
    activeModalBtnName : "device",
    activeModalBtn : document.getElementById("modalSidePanelDeviceBtn").classList,
    prevConfigCard : document.getElementById("configCardsForDevice").classList,
    addJobBtn : document.getElementById("addJobBtn"),
    addJobBtnHolder : document.getElementById("addJobBtnHolder"),
    jobCardsDisplayer : document.getElementById("jobCardsDisplayer"),
    timerForAutoRefresh : null,
}

const job={
    deviceId:null,
    from : "client",
    device:new Map(),
    cloud:new Map(),
    camera:new Map(),
    getLogs:new Map(),
}

function sendHandler(){
    job.device=Object.fromEntries(job.device);
    job.cloud=Object.fromEntries(job.cloud);
    job.camera=Object.fromEntries(job.camera);
    job.getLogs=Object.fromEntries(job.getLogs);
    let jsonData = JSON.stringify(job);
    // alert(jsonData)
    // return
    let spinner=document.getElementById("msgDisplayerRecievedFromJob");
    spinner.style.display='block';
    const url = "https://aaxsxrwma8.execute-api.us-east-1.amazonaws.com/sendJob"
    let fetchData = {
        method:'POST',
        body : jsonData,

    }
    
    fetch(url,fetchData)
    .then(
        (response)=>{
            response.json()
            .then((data)=>{
                spinner.style.display='none';
                if (response.status==200){
                    flashMsg(data,"w3-green");
                }else{
                    flashMsg(data,"w3-red");
                }
            });    
        })
    
    
}

function addJobHandler(element){
    let div = element.parentElement;
    let inp = element.previousSibling.previousSibling.previousSibling.previousSibling;
    let value = inp.value;
    let key = inp.name;
    // console.log(div)
    // console.log(inp)
    if (value==""){
        return null;
    }
    if(STATE.activeModalBtnName=="device"){
        if (key=="Device-Test-Flag"){
            job.device.set(key,'True');
            key="Device-Test-Duration"    ;
        }
        if (div.getAttribute("data-timeZone")=="True"){
            let val = document.getElementById("time_zone").value;
            key="Time-Zone";
            value=val;
        }
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
    bootStatus=btnElement.getAttribute("data-devicebooted");
    if (bootStatus=="False"){
        flashMsg("Device has not booted yet","w3-red");
        return 
    }
    let modal = document.getElementById("modalForConfig");
    modal.style.display='block';
    let modalHeader = document.getElementById('modalHeader');
    modalHeader.innerText="You are managing device "+btnElement.value;
    job.deviceId=btnElement.value;
}
function closeConfigModel(){
    document.getElementById('modalForConfig').style.display='none';
    location.reload();
}

function unhideForm(name){
    let form=document.getElementById(name);
    form.style.display='block';
}
function hideForm(name){
    let form=document.getElementById(name);
    form.style.display='none';
}

function flashMsg(msg,color="w3-red"){
    document.getElementById("flashMsg").innerText=msg;
    let elmnt = document.getElementById("flashCard");
    elmnt.classList.remove("w3-red")
    elmnt.classList.add(color);
    elmnt.style.display="block";
}

function autoRefreshJobLogs(btn){
    if(STATE.timerForAutoRefresh==null){
        STATE.timerForAutoRefresh = window.setInterval(getJobLogs,5000)
        let temp = document.getElementById("refreshJobLogs-btn");
        temp.classList.add("w3-disabled")
        btn.innerText="Stop Auto Refresh"
        btn.classList.remove("w3-teal")
        btn.classList.add("w3-red")
    }else{
        window.clearInterval(STATE.timerForAutoRefresh);
        document.getElementById("refreshJobLogs-btn").classList.remove("w3-disabled");
        btn.innerText="Auto Refresh"
        btn.classList.remove("w3-red")
        btn.classList.add("w3-teal")
        STATE.timerForAutoRefresh=null
    }
   
}

function getJobLogs(){
    const url = "http://digi.webzinny.in/getJobLogs?deviceId="+job.deviceId
    fetch(url)
    .then(
        (response)=>{
            response.json()
            .then((data)=>{
                if (response.status==200){
                    console.log(data)
                    const tBody = document.getElementById("tbodyForJobLogs");
                    while (tBody.hasChildNodes()) {
                        tBody.removeChild(tBody.firstChild);
                    }
                    data.Items.forEach(function(obj,ind) {
                        var row = document.createElement('tr');
                        arr = []
                        for(let i=0;i<4;i++){
                            arr.push(document.createElement('td'))
                        }
                        arr[0].appendChild(document.createTextNode(ind+1))
                        arr[1].appendChild(document.createTextNode(obj.JobId))
                        arr[2].appendChild(document.createTextNode(obj.JobStatus))
                        arr[3].appendChild(document.createTextNode(obj.Timestamp))
                        arr.forEach(function(elmnt){
                            row.appendChild(elmnt)
                        })
                        tBody.appendChild(row);
                    });
                }else{
                    flashMsg("Something went wrong with Job Logs","w3-red");
                }
            });    
        })
}