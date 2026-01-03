// creatin function  to run functions from backend
async  function Run_Back_Function(func, dat){
    // a function to run functions from backend
    // write the backend function \ command to console 
    console.log(`pywebview.api.${func}("${dat}")`);
    // executing the function dynamically via pywebview API
    var resp = await window.pywebview.api[func](dat);
    return resp
    }


class Logger{
    constructor(){}

    getCallerInfo() {

        // uses an error to get the stack and get the info from within 
        // when creatin the error object it does not rain an error (as it need to be raised to actually happend)
        const err = new Error();
        const stackLines = err.stack.split("\n");
        
        // removing eel background stack
        // stackLines.pop()
        
        const callerLine = stackLines[3]; // Index 2 is the calling function
        const match = callerLine.match(/at (\S+) \((.*):(\d+):(\d+)\)/) || callerLine.match(/at (.*):(\d+):(\d+)/);
        
        if (match) {
            return {
                functionName: match[1] || "anonymous",
                fileName: match[2].split("/").pop() || "unknown",
                line: match[3],
                column: match[4],
                a: callerLine
            };
        }
    
        return { functionName: "unknown", fileName: "unknown", line: "?", column: "?" };
    }

    Extra_Log(input_str, level="debug"){

        input_str = input_str.toString()
        let a = this.getCallerInfo()

        let trace = `${a.functionName}.${a.fileName}:${a.line}`
        // send to backend logger via pywebview API (fire-and-forget)
        if (window.pywebview && window.pywebview.api && window.pywebview.api.Front_Log) {
            window.pywebview.api.Front_Log(input_str, trace, level).catch(() => {});
        }
        console.log(input_str)
        // return a

    }
}

window.logger = new Logger()

function getCallerInfo() {

    // uses an error to get the stack and get the info from within 
    // when creatin the error object it does not rain an error (as it need to be raised to actually happend)
    const err = new Error();
    const stackLines = err.stack.split("\n");
    
    // removing eel background stack
    stackLines.pop()
    
    const callerLine = stackLines[1]; // Index 2 is the calling function
    const match = callerLine.match(/at (\S+) \((.*):(\d+):(\d+)\)/) || callerLine.match(/at (.*):(\d+):(\d+)/);

    if (match) {
        return {
            functionName: match[1] || "anonymous",
            fileName: match[2].split("/").pop() || "unknown",
            line: match[3],
            column: match[4]
        };
    }

    return { functionName: "unknown", fileName: "unknown", line: "?", column: "?" };
}





// ---------------------------------------------------------------------- //
// ------------------------Display Classes ------------------------------ // 
// ====================================================================== //

class Display{
    constructor(disp){
        this.startTime;
        this.stopwatchInterval;
        this.update_state = false;
        this.elapsedPausedTime = 0;
        this.disp = disp
   }

    Start() {
        if (!this.stopwatchInterval) {
        this.startTime = new Date().getTime() - this.elapsedPausedTime; // get the starting time by subtracting the elapsed paused time from the current time
        this.stopwatchInterval = setInterval(this.Update, 10); // update every second
        }
    }

    Stop() {
        clearInterval(this.stopwatchInterval); // stop the interval
        this.elapsedPausedTime = new Date().getTime() - this.startTime; // calculate elapsed paused time
        this.stopwatchInterval = null; // reset the interval variable
      }
      
    Reset() {
        this.Stop(); // stop the interval
        this.elapsedPausedTime = 0; // reset the elapsed paused time variable
        disp.innerHTML = "00:00:00:00"; // reset the display
      }

    Pad(number) {
        // add a leading zero if the number is less than 10
        return (number < 10 ? "0" : "") + number;
    }
    //  the methood is an arrow function so that the scope will stay relevant for in class object because of how setInterval(which calls this methood) works 
    // it is runs in the windows scope so it will be able to foolow time count more details here: https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval#explanation
   Update= () =>  {
        var currentTime = new Date().getTime(); // get current time in milliseconds
        var elapsedTime = currentTime - this.startTime; // calculate elapsed time in milliseconds
        var centiSeconds = Math.floor(elapsedTime / 10) % 100; // calculate centiseconds
        var seconds = Math.floor(elapsedTime / 1000) % 60; // calculate seconds
        var minutes = Math.floor(elapsedTime / 1000 / 60) % 60; // calculate minutes
        var hours = Math.floor(elapsedTime / 1000 / 60 / 60); // calculate hours
        var displayTime = this.Pad(hours) + ":" + this.Pad(minutes) + ":" + this.Pad(seconds) + ":" + this.Pad(centiSeconds); // format display time
        this.disp.innerHTML = displayTime; // update the display
        
    }

    async Display_Tape(){
        try {
            let n = await window.pywebview.api.Tape_Command("Timer_Return");
            document.querySelector(".display").innerHTML = n;
        } catch (e) { console.error(e); }
    }

    Tape_start = () => {
        if(this.update_state == true){return}
        this.stopwatchInterval = setInterval(this.Display_Tape, 500);
        this.update_state = true;
        let reel_svg = document.querySelector(".Reel_SVG");
        
        if(reel_svg.getAttribute("animation_running") == "false"){
            // activating reel animation
            reel_svg.dispatchEvent(new MouseEvent("click"));
            reel_svg.setAttribute("animation_running","true");
        }
    }
    
    Tape_stop = async () =>{
        await clearInterval(this.stopwatchInterval);
        await this.Display_Tape()
        this.update_state = false;

        let reel_svg = document.querySelector(".Reel_SVG");
        if(reel_svg.getAttribute("animation_running") != "false"){
            // activating reel animation
            reel_svg.dispatchEvent(new MouseEvent("click"));
            reel_svg.setAttribute("animation_running","false");
        }
    }



}

// --------------------------------------------------------------------------- //
// ------------------------LOC Button's Classes ------------------------------ // 
// =========================================================================== //


class Loc_Button{
    constructor(){
        this.button_count = document.querySelectorAll(".btn_loc").length;
        this.section = document.querySelector(".loc_batton_div");
        this.loc_button_Interval;
        this.interval_status = "Stopped";
        }

   async Get_TimeStamp(current= false){
        // methood to get formated timestamp 
        
        ///////////////////////////////////////////////////////////////////////////////////////////////////////
        // made function asynce for getting the time from tape before entering to loc object becouse without //
        // making the function asynce the only way to get promise output is by using that output on the spot //
        // by awaiting to the tape command (command that go backward using eel) you arer making              //
        // the code "syncronus"and waiting to the response before continuing  and why i changed              //
        // almost all the functions in the create loc button stack to async                                  //
        ///////////////////////////////////////////////////////////////////////////////////////////////////////

        if(current == true){
            // return Run_Back_Function("Timer_Return")
            let timestamp = await window.pywebview.api.Tape_Command("Timer_Return");
            let [loc_h, loc_m, loc_s] = document.querySelectorAll(".time_field");
            console.log(`first - ${timestamp}`);
                // timestamp = timestamp.split(":");
                // let ind = 0
                // loc_h.value = timestamp[0];
                // loc_m.value = timestamp[1];
                // loc_s.value = timestamp[2];
                // window.loc_timestamp = timestamp;
                return timestamp
                

            }
        
        let [loc_h, loc_m, loc_s] = document.querySelectorAll(".time_field");
        [loc_h, loc_m, loc_s].forEach(
            t => {if(t.value == ""){t.value = "00"}}
            )

        let loc_time = loc_h.value + ":" + loc_m.value + ":" + loc_s.value;
        // window.loc_timestamp = timestamp;
        return loc_time
            
   }
   

//  Creating Buttons
// -------------------------------------------
   Create_Loc_Del_btn(btn_loc){
        // creating empty button
        let btn_delete = document.createElement('button');
        let svg = '<svg viewBox="0,0,256,256" width="12px" height="12px" fill-rule="nonzero"><g fill="#ffffff" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><g transform="scale(10.66667,10.66667)"><path d="M10,2l-1,1h-6v2h1.10938l1.7832,15.25586v0.00781c0.13102,0.98666 0.98774,1.73633 1.98242,1.73633h8.24805c0.99468,0 1.8514,-0.74968 1.98242,-1.73633l0.00195,-0.00781l1.7832,-15.25586h1.10938v-2h-6l-1,-1zM6.125,5h11.75l-1.75195,15h-8.24805z"></path></g></g></svg>'
        btn_delete.innerHTML = svg ;  // Delete icons created by Kiranshastry
        // btn_delete.id = "btn_del" + ;
        btn_delete.className = "button btn_loc btn_del";
        btn_delete.btn_loc = btn_loc;
        btn_delete.addEventListener("click", this.Delete_Loc);
        return btn_delete
   }

    Create_Loc_Edit_btn(btn_loc){

        let btn_edit = document.createElement('button');
        
        // adding property to button loc 
        btn_edit.className = "button btn_loc btn_edit";
        btn_edit.btn_loc = btn_loc;
        btn_edit.in_edit_mode = false;
        let svg = '<svg  x="0px" y="0px" width="12" height="12" viewBox="0,0,256,256"><g fill="#ffffff" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><g transform="scale(10.66667,10.66667)"><path d="M18.41406,2c-0.256,0 -0.51203,0.09797 -0.70703,0.29297l-2,2l-1.41406,1.41406l-11.29297,11.29297v4h4l14.70703,-14.70703c0.391,-0.391 0.391,-1.02406 0,-1.41406l-2.58594,-2.58594c-0.195,-0.195 -0.45103,-0.29297 -0.70703,-0.29297zM18.41406,4.41406l1.17188,1.17188l-1.29297,1.29297l-1.17187,-1.17187zM15.70703,7.12109l1.17188,1.17188l-10.70703,10.70703h-1.17187v-1.17187z"></path></g></g></svg>'
        btn_edit.innerHTML = svg;
        btn_edit.edit_state = false;
        btn_edit.addEventListener("click",this.Edit_Loc);
        return btn_edit
        }


    async Create_Loc_Div(current= false){
        // creating empty div
        let div_btn = document.createElement('div');
        
        div_btn.class = "button btn_loc"

        let btn_loc = await this.Create_Loc_btn(current);
        let btn_edit = this.Create_Loc_Edit_btn(btn_loc);
        let btn_delete = this.Create_Loc_Del_btn(btn_loc);
        
        div_btn.append(btn_loc)
        div_btn.append(btn_edit)
        div_btn.append(btn_delete)
        return div_btn

    }


    async Create_Loc_btn(current= false){
        // creating empty button & getting timestamp
        let loc_time = await this.Get_TimeStamp(current);
        console.log(`secound - ${loc_time}`);
        // loc_time = window.loc_timestamp;
        let btn_loc = document.createElement('button');
        let btn_num = document.querySelector(".loc_batton_list_div").childElementCount -1;
        
        // adding property to button loc 
        btn_loc.innerHTML = `<sapn>Loc ${String(btn_num)} - ${loc_time}</span>`;
        btn_loc.id = "btn_loc" + String(btn_num);
        btn_loc.className = "button btn_loc";
        btn_loc.TimeStamp = loc_time;
        // btn_loc.state = btn_loc.state_enum.DEFAULT
        btn_loc.addEventListener("click", this.Tape_Loc);
        return btn_loc
        }

//  Adding to View 
// ----------------------------------------------

    async Add_Loc_Time_btn(current= false){
    //    getting values and creating blank button
        let section = document.querySelector(".loc_batton_list_div");

        let div_btn = await this.Create_Loc_Div(current);

        // adding button to div
        section.appendChild(div_btn);
        
        // btn can be diable with btn.disabled = true
        return div_btn;
    }

//  CLicks Funfctions
// ---------------------------------------------

    async Tape_Loc(event){
        
        //  Make Sure that the event wont happend if editing button text
        if(event.currentTarget.contentEditable == "true"){return};

        // getting time and fromating
        let loc_time = event.currentTarget.TimeStamp;
        loc_time = `"${loc_time}"`
        //  if to make sure that the interval will be reactiveted only when it fininshed
        if(Loc_Object.interval_status == "Stopped"){
            
            Loc_Object.interval_status = "Running";
            
                if(display.update_state == true){
                await window.pywebview.api.Tape_Command("LOC",loc_time);
                Loc_Object.loc_button_Interval = setInterval(Loc_Object.Tape_Loc_Response_stat, 500);
                }
        
            else{
                display.Tape_start();
                Loc_Object.loc_button_Interval = setInterval(Loc_Object.Tape_Loc_Response_stat, 500);
                await eel.Tape_Command("LOC",loc_time)();
            }

            // unsetting the glowing buttons
            let clicked_btn = document.querySelectorAll(".button.clicked")
            clicked_btn.forEach(btn => {btn.classList.remove("clicked")})
        
        }
        else{console.log("repeted_click")}
    
            // ST? = 10 for wind location
        
    }

    async Tape_Loc_Response_stat(){
           let response = await window.pywebview.api.Tape_Command("Get_Status");
        console.info(response);
        if (response == "locate wind"){
            console.info("loc in wine mode")
        }
        else{
            console.info("loc stoped Winding");
            clearInterval(Loc_Object.loc_button_Interval);
            display.Tape_stop()
            Loc_Object.interval_status = "Stopped";
        }
    }

    Delete_Loc(event){
        
        // btn_loc = event.target.btn_loc;
        let btn_div = event.currentTarget.parentElement;
        let conf = confirm("Are you sure you want to remove location?");
        if(conf){
            btn_div.remove()
            return "deleted"
        }

        else{
            return "false alarm"
        }
    }

    
    Edit_Loc(event){

        let btn_loc = event.currentTarget.btn_loc;
        let btn_edit = event.currentTarget
        let state = event.currentTarget.edit_state;
        // let enter_func = (n) => {if(n.code == "Enter"){ fake_n = {"currentTarget":};Loc_Object.Edit_Loc(n)}};
        //  if in edit
        if(state){
            // stoping button from performing as button
            btn_loc.disabled = false;
            // btn_loc.contentEditable = false;
            btn_loc.firstChild.contentEditable = false;
            btn_loc.removeEventListener("keypress", Loc_Object.Edit_Loc_Enter);
            
            // updating id base on button name
                // cleaning the timestamp 
            let temp_id= btn_loc.firstChild.innerHTML.replace(/-.\d+:.\d+:.\d+/, "").trim();
            temp_id = temp_id.replace(/\d+:.\d+:.\d+/, "").trim();
            temp_id = temp_id.replaceAll(" ", "_");
            btn_loc.id  = `btn_loc_${temp_id}`;

            btn_edit.classList.remove("clicked");
            btn_edit.edit_state = false
        }
        else{
            // making button perform as button
            btn_loc.disabled = true;
            // btn_loc.contentEditable = true;
            btn_loc.firstChild.contentEditable = true;
            btn_loc.addEventListener("keydown",Loc_Object.Edit_Loc_Enter);


            btn_edit.classList.add("clicked");
            btn_edit.edit_state = true;
        }

    }

    Edit_Loc_Enter(event){
        // console.log(event.currentTarget)
        // let fake_event = {"currentTarget": document.querySelector(".button.btn_loc.btn_edit")};
        let fake_event = {"currentTarget": event.currentTarget.nextElementSibling};
        if(event.code == "Enter"){
            Loc_Object.Edit_Loc(fake_event)}
    }
}
// export * from "Logic_Classes.js"