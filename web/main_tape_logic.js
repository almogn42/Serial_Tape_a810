// // creatin function  to run functions from backend
// async  function Run_Back_Function(func, dat){
//     // a function to run functions from backend
//     // write the backend function \ command to console 
//     logger.Extra_Log(`eel.${func}("${dat}")`);
//     // executing the function dynamaclly
//     return await eel[func](dat)();
//     }

    async  function Run_Back_Function(func, dat){
        // a function to run functions from backend
        // write the backend function \ command to console 
        logger.Extra_Log(`pywebview.api.${func}("${dat}")`);
        // executing the function dynamaclly
        let resp = await pywebview.api[func](dat);
        return resp
        }

async function Timer_run(){
    // let screen = document.querySelector(".display");
    display.Tape_start();
    return "running Counter"

}


function Tape_Play(event){
    // running command
    let btn = document.querySelector("#play_btn");
    pywebview.api.Tape_Command("Play");

    // running the display timer 
    Timer_run();

    // managing glow (like light behind button)
    if(btn.classList.length > 1){
        btn.classList.remove("clicked");
        }
    else{
        btn.classList.add("clicked");
    }
}

function Tape_Stop(event){
    // running the command
    pywebview.api.Tape_Command("Stop");
    // running the display timer 
    // display.Tape_stop();
    window.stop_button_Interval = setInterval(Tape_Stop_Response_stat, 500);    
    window.stop_button_Interval_status = "Stopped";
    
    // unsetting the glowing buttons
    let clicked_btn = document.querySelectorAll(".button.clicked")
    clicked_btn.forEach(btn => {btn.classList.remove("clicked")})

}

async function Tape_Stop_Response_stat(){
    let response = await pywebview.api.Tape_Command("Get_Status");
    logger.Extra_Log(response, level="info");
    if (response == "stop achieved"){
        logger.Extra_Log("Stop Achived", level="info");
        clearInterval(window.stop_button_Interval);
        display.Tape_stop()
        window.stop_button_Interval_status = "Stopped";
    }
}

function Tape_Record(event){
    let btn = document.querySelector("#rec_btn");
    pywebview.api.Tape_Command("Record");
    logger.Extra_Log(event)

    // running the display timer 
    Timer_run();

    // managing glow (like light behind button)
    if(btn.classList.length > 1){
    btn.classList.remove("clicked");
        }
    else{
        btn.classList.add("clicked");
    }
}

function Tape_FF(event){
    let btn = document.querySelector("#FastForward_btn");
    pywebview.api.Tape_Command("Foreword");
    // running the display timer 
    Timer_run();
    
    // managing glow (like light behind button)
    if(btn.classList.length > 1){
        btn.classList.remove("clicked");
        }
    else{
        btn.classList.add("clicked");
    }
}

function Tape_FB(event){
    let btn = document.querySelector("#FastBackward_btn");
    pywebview.api.Tape_Command("Back");
    // running the display timer 
    Timer_run();
    
    // managing glow (like light behind button)
    if(btn.classList.length > 1){
        btn.classList.remove("clicked");
        }
    else{
        btn.classList.add("clicked");
    }
}

function Tape_Chanl_State(event){
    //  getting the button oject
    let btn = event.currentTarget;
    let channel = btn.getAttribute("channel");
    let linked_status = btn.getAttribute("linked");

    // splited for when in linke mode or not
    if(linked_status == "true"){
        let btn = document.querySelectorAll('.button.chl_ready_state');
        btn.forEach(btn => {
            let channel = btn.getAttribute("channel");

            // managing glow and state (like light behind button)
            if(btn.classList.length > 2){
                btn.classList.remove("clicked");
                pywebview.api.Tape_Command("Channel_Safe", channel);
                btn.innerHTML = "SAFE";
                }
            else{
                btn.classList.add("clicked");
                pywebview.api.Tape_Command("Channel_Ready", channel);
                btn.innerHTML = "READY";
            }
        })}
    
    else{
        // managing glow and state (like light behind button)
        if(btn.classList.length > 2){
            btn.classList.remove("clicked");
            pywebview.api.Tape_Command("Channel_Safe", channel);
            btn.innerHTML = "SAFE";
            }
        else{
            btn.classList.add("clicked");
            pywebview.api.Tape_Command("Channel_Ready", channel);
            btn.innerHTML = "READY";
        }      
    } 
  
}


function Tape_Chanl_Mute(event){
    //  getting the button oject
    let btn = event.currentTarget;
    let channel = btn.getAttribute("channel");
    let linked_status = btn.getAttribute("linked");

    // splited for when in linke mode or not
    if(linked_status == "true"){
        let btn = document.querySelectorAll('.button.chl_mute_state');
        btn.forEach(btn => {
            let channel = btn.getAttribute("channel");

            // managing glow and state (like light behind button)
            if(btn.classList.length > 2){
                btn.classList.remove("clicked");
                pywebview.api.Tape_Command("Channel_Mute_Off", channel);
                // btn.innerHTML = "SAFE";
                }
            else{
                btn.classList.add("clicked");
                pywebview.api.Tape_Command("Channel_Mute", channel);
                // btn.innerHTML = "READY";
            }
        })}


    else{
        // managing glow and state (like light behind button)
        if(btn.classList.length > 2){
            btn.classList.remove("clicked");
            pywebview.api.Tape_Command("Channel_Mute_Off", channel);
            // btn.innerHTML = "SAFE";
            }
        else{
            btn.classList.add("clicked");
            pywebview.api.Tape_Command("Channel_Mute", channel);
            // btn.innerHTML = "READY";
        }
    }
}

function Tape_Chanl_input_State(event){
    //  Getting all the valueses/ elements needed
    let DropDown = event.currentTarget;
    let val = DropDown.value;
    let channel = DropDown.getAttribute("channel");
    let selected_ind = DropDown.selectedIndex; 

    // creating an enum so that only the correct command could run 
    // & so the users cant forcibly enter rendom commands through html edit in develeper mode(entering command to value)
    const INPUT_OPTIONS  = {
        "INPUT": "Channel_Input",
        "SYNC": "Channel_Sync",
        "REPRO": "Channel_Repro"
    }


    let linked_status = DropDown.getAttribute("linked");
    // splited for when in linke mode or not
    if(linked_status == "true"){
        let DropDown = document.querySelectorAll('select.Channel_option');
        
        DropDown.forEach(DropDown => {
            logger.Extra_Log("test")
            let channel = DropDown.getAttribute("channel");
            DropDown.selectedIndex = selected_ind;
            // the HOLY CHECK ITSELEF IN THE NAME OF MOTEHRFU!@#                            
            if(INPUT_OPTIONS[val] != undefined){pywebview.api.Tape_Command(INPUT_OPTIONS[val], channel);}
            })}
    
    else{
        // the HOLY CHECK ITSELEF IN THE NAME OF MOTEHRFU!@#                            
        if(INPUT_OPTIONS[val] != undefined){pywebview.api.Tape_Command(INPUT_OPTIONS[val], channel);}
        }
    
}

function Tape_Chanl_input_join(event){
    // Getting all elements for use
    let btn = event.currentTarget;
    let DropDown = document.querySelectorAll('.Channel_option');
    let mute = document.querySelectorAll('.button.chl_mute_state');
    let ready = document.querySelectorAll('.button.chl_ready_state');


    if(btn.classList.length > 1){
        btn.classList.remove("clicked");
        // turning elements to not linked using the html attribute
        DropDown.forEach(Obj =>{Obj.setAttribute("linked","false")});
        mute.forEach(Obj =>{Obj.setAttribute("linked","false")});
        ready.forEach(Obj =>{Obj.setAttribute("linked","false")});
        // btn.innerHTML = "SAFE";
        }
    else{
        btn.classList.add("clicked");
        // turning elements to linked using the html attribute
        DropDown.forEach(Obj =>{Obj.setAttribute("linked","true")});
        mute.forEach(Obj =>{Obj.setAttribute("linked","true")});
        ready.forEach(Obj =>{Obj.setAttribute("linked","true")});
    }
        

}

function Tape_Zero_loc(event){
    let btn = event.currentTarget
    btn.TimeStamp = "00:00:00"
    // eel.Tape_Command("LOC", '"00:00:00"')(n => {logger.Extra_Log(n)});
    Loc_Object.Tape_Loc(event);

}

async function Set_Timer(){
    
    // poping for user to a choise to decide if to delete or not
    let conf = confirm("Are you sure you want to reset the timer? \nThis will set the tape timer to whatever number is on the Add Loc time display!");
        if(conf){
            let TimeStamp = `"${ await Loc_Object.Get_TimeStamp()}"`;
            pywebview.api.Tape_Command("Set_Timer", TimeStamp);
            display.disp.innerHTML = TimeStamp.replaceAll('"','');
        }
        else{return "ya pussy"}
    

}

async function Add_Loc_Time_btn(current= false){
    // initiating 
    loc_btn = await Loc_Object.Add_Loc_Time_btn(current)
    logger.Extra_Log("---------------------------------------")
    return loc_btn;
}


function validateNumber(event,field) {
    //  A fUNCTION TO RESTRICT NONnumber inbputs
    let pattern;
    if(field == "H"){pattern= /[-\d]+/}
    else{pattern = /[\d]+/}

    return pattern.test(event.key )
}

function Tape_get_ips(){
    let field = document.querySelector("#ips_value");
    pywebview.api.Tape_Command("Get_Ips").then(ips => {
        if(["3.75","7.5","15","30" ].includes(ips)){field.innerHTML = ips}
        else{alert(ips)}
    })
}

function Tape_Help_btn(){
    text =(
`Coded for Rafsoda Studios By Almog Nachmany
If you enjoyed this endeavor please considering buying me a coffee!
Links:
    https://buymeacoffee.com/kvothe42
    https://github.com/almogn42/Serial_Tape_a810
    https://gitlab.com/kvothe42-public/serial_tape_a810
         
        
Clarifications:
-   Quick Loc: creates a quick location button at the current time. 
    Works during play, record and fw/rw as well. Location names are editable.
        
-   Zero Loc: winds back the reel to the tape's predefined Zero Location

-   Link CH: links the left and right channels status' together. 
    Applicable to SAFE, READY, INPUT, SYNC and REPRO. 

-   Digital Counter: in addition to your machine's counter which is synced with
    the app's counter you have a digital counter,
    used to insert custom locations or to re-set your machine's counter
    using the Set Timer button.
    Please note: the app's digital counter can ONLY accept full timestamps.
    For Example: [-06:00:05], [08:59:42], [00:00:00]

the current Version is 1.2
`)
    let pre = document.querySelector("pre");
    pre.innerHTML =text
    let diag = document.querySelector("dialog");
    diag.showModal();
}

function diag_close(){
    let diag = document.querySelector("dialog");
    diag.close()
}

function On_Load_Init(){
    // a function to run all the things that need to run at the start of the page but dependant on dom :-)

    console.log("DOM Loaded - Initializing Variables");
    // Display Object init
    window.display = new Display(document.querySelector(".display"));
    //  for having loc methood later on
    window.Loc_Object = new Loc_Button()


    // filling fields
    Tape_get_ips();
    display.Display_Tape();


    

    // adding event listening to buttons
    document.querySelector("#play_btn").addEventListener("click", Tape_Play);
    document.querySelector("#stop_btn").addEventListener("click", Tape_Stop);
    document.querySelector("#rec_btn").addEventListener("click", Tape_Record);
    document.querySelector("#FastForward_btn").addEventListener("click", Tape_FF);
    document.querySelector("#FastBackward_btn").addEventListener("click", Tape_FB);
    document.querySelector("#add_loc_btn").addEventListener("click", Add_Loc_Time_btn);
    document.querySelector("#quick_loc_btn").addEventListener("click",n =>{Add_Loc_Time_btn(current = true)});
    document.querySelector("#zero_loc_btn").addEventListener("click",Tape_Zero_loc);
    document.querySelector("#ips_value").addEventListener("click",Tape_get_ips);
    document.querySelector("#set_timer_btn").addEventListener("click",Set_Timer);
    document.querySelectorAll(".chl_ready_state").forEach(btn => {btn.addEventListener("click",Tape_Chanl_State)});
    document.querySelectorAll(".chl_mute_state").forEach(btn => {btn.addEventListener("click",Tape_Chanl_Mute)});
    document.querySelectorAll(".Channel_option").forEach(btn => {btn.addEventListener("change" ,Tape_Chanl_input_State)});
    document.querySelector("#link_chnl_btn").addEventListener("click",Tape_Chanl_input_join);
    document.querySelector("#help_btn").addEventListener("click",Tape_Help_btn);
    document.querySelector("#diag_btn").addEventListener("click",diag_close);

    

}

function On_Load_Api_Obj(){
    // a function to run all the things that need to run at the start of the page but dependant on Api object of pywebview 
    // pywebview create the object a bit after dom apperently  
    
    console.log("running On_Load_Api_Obj");
    // setting the channels to safe
    pywebview.api.Tape_Command("Channel_Safe", 1);
    pywebview.api.Tape_Command("Channel_Safe", 2);

    // adding event listener to create variables on the finish of dom load only after api object creation
    if (document.readyState === "loading"){
        document.addEventListener("DOMContentLoaded", On_Load_Init);
        }
    else{
        On_Load_Init();
    }
    
}


window.addEventListener("pywebviewready", On_Load_Api_Obj);

