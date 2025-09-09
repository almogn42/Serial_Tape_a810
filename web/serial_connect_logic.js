async  function Run_Back_Function(func, dat){
    // a function to run functions from backend
    // write the backend function \ command to console 
    logger.Extra_Log(`eel.${func}("${dat}")`);
    // executing the function dynamaclly
    return await eel[func](dat);
    }

eel.expose(go_to_page)
function go_to_page(url) {window.location.replace(url);};


function conn_check(ret){
    logger.Extra_Log(ret);
    // console.trace("trace is ")
    // stack = new Error("test").stack
    // a = new Error()
    // b = a.prototype.toString()
    // console.log(b)
    return logger.Extra_Log("sss")

}

//  when cliking the button a function to send to tape creation the correct port
async function connection_selection(event){
    port = this.id;
    await eel.connecting_serial(port)(n => {logger.Extra_Log(n)});
    let diag = document.querySelector("dialog");
    diag.showModal();
}

// when cliking the button a function to send to tape creation the correct machine type
async function mechine_selection(event){
    mechine = this.id;
    await eel.Create_Tape_object(mechine)()
    go_to_page("tape_interface3.html")
    
}


function create_buttons(btn_list){
    // creting a case for when there is no serial device
    if(typeof(btn_list) == "string"){
        let main_text = document.querySelector("h3")
        main_text.innerHTML = "There seem to be No serial device connected <br>Please make sure the serial device is connected well and press f5"
        return "no device found"
    }
    // Creting Buttons
    center = document.querySelector(".controls-left")
    btn_list.forEach(b => {
        let btn = document.createElement('button');
        btn.id = b.id;
        btn.innerHTML = b.description;
        btn.className = "button";
        center.appendChild(btn);
        btn.addEventListener("click", connection_selection)
    });
}
function create_mechine_select_buttons (mech_list){
    let diag_div = document.querySelector("#dialog_div");
    // let mech_list = await eel.Get_Supported_Tapes()();
    mech_list.forEach(mechine => {
        let btn = document.createElement('button');
        btn.id = mechine.split(" ").pop();
        btn.innerHTML = mechine;
        btn.className = "button";
        diag_div.appendChild(btn);
        btn.addEventListener("click", mechine_selection)        
    })
    }

// Creating the buttons 
eel.connecting_serial()(create_buttons);
eel.Get_Supported_Tapes()(create_mechine_select_buttons);