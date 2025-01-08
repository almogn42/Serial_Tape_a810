async  function Run_Back_Function(func, dat){
    // a function to run functions from backend
    // write the backend function \ command to console 
    console.log(`eel.${func}("${dat}")`);
    // executing the function dynamaclly
    return await eel[func](dat);
    }

eel.expose(go_to_page)
function go_to_page(url) {window.location.replace(url);};


function conn_check(ret){
    console.log(ret);
}

function connection_selection(event){
    port = this.id;
    eel.connecting_serial(port)(n => {console.log(n)});
}

function create_buttons(btn_list){
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



eel.connecting_serial()(create_buttons);