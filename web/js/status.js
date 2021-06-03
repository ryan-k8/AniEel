eel.status_link("return status")(status)
function status(s){
    document.getElementById("status-span").innerHTML = s;
}