function clearErrors() {
    errors = document.getElementsByClassName('formerror');
    for (let item of errors) {
        item.innerHTML = "";
    }
}


function seterror(id, errormsg) {
    element = document.getElementById(id);
    element.getElementsByClassName('formerror')[0].innerHTML = errormsg;
}


function validateInput(name) {
    var returnval = true;
    clearErrors();
    var s = document.forms[name]["cname"].value;
    s = s.trim()
    if (s.length == 0) {
        seterror("cname", "<br>Name cannot be empty!");
        returnval = false;
    }
    return returnval;
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


function deleteItem() {
    if (confirm("Do you want to delete the item?") == true) {
        return true;
    }
    return false;
}
