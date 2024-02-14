var arr = []
var qty = []

if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
} else {
    ready();
}


function ready() {
    if ("ids" in localStorage) {
        var s = new Set(JSON.parse(localStorage.getItem("ids")));        
        arr = JSON.parse(localStorage.getItem("ids"));
        qty = JSON.parse(localStorage.getItem("qty"));
        var items = document.getElementsByClassName('item');
        for (var i = 0; i < items.length; i++) {
            var id = items[i].id;
            if (s.has(id)) {
                document.getElementById(id).disabled = true;
                document.getElementById(id).innerHTML = "Added";
            }
        }
    }
}



function addtoCart(id) {
    document.getElementById(id).disabled = true;
    document.getElementById(id).innerHTML = "Added";
    arr.push(id);
    qty.push(1);
}

function addtoStorage() {
    document.getElementById("iids").value = arr;
    localStorage.setItem('ids', JSON.stringify(arr));
    for (var i = 0; i < qty.length; i++) {
        qty[i] = 1;
    }
    localStorage.setItem('qty', JSON.stringify(qty));
}


function validateSearch() {
    var returnval = true;
    var s = document.forms['search']["q"].value;
    if (s.length == 0) {
        returnval = false;
    }
    s = s.trim()
    if (s.length == 0) {
        returnval = false;
    }
    return returnval;
}


function clearStorage() {
    localStorage.removeItem('ids');
    localStorage.removeItem('qty');
}






