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



function validateEmail(name) {
    var returnval = true;

    var email = document.forms[name]["femail"].value;
    if (email.length > 30) {
        if (name == 'form') {
            seterror("email", "*Email length is too long<br>");
        }
        else {
            seterror("email2", "*Email length is too long<br>");
        }
        returnval = false;
    }
    return returnval;
}

function validatePassword(name) {
    var returnval = true;
    var password = document.forms[name]["fpass"].value;
    if (password.length < 8) {
        if (name == 'form') {
            seterror("pass", "*Password should be atleast 8 characters long!<br>");
        }
        else {
            seterror("pass2", "*Password should be atleast 8 characters long!<br>");
        }
        returnval = false;
    }
    else if (password.length > 15) {
        if (name == 'form') {
            seterror("pass", "*Password should be atmost 15 characters long!<br>");
        }
        else {
            seterror("pass2", "*Password should be atmost 15 characters long!<br>");
        }
        returnval = false;
    }
    else {
        if (!password.match(/[a-z]/g) || !password.match(/[A-Z]/g)
            || !password.match(/[0-9]/g) || !password.match(/[^a-zA-Z\d]/g)) {
            if (name == 'form') {
                seterror("pass", "*Passsword must contain atleast 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character!<br>");
            }
            else {
                seterror("pass2", "*Passsword must contain atleast 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character!<br>");
            }
            returnval = false;
        }
    }

    return returnval;
}

function validateConfirmPassword(name) {
    var returnval = true;
    var p = document.forms[name]["fpass"].value;
    var cp = document.forms[name]["fcpass"].value;
    if (p != cp) {
        seterror("fcpass", "*Password and Confirm Password must be same!<br>");
        returnval = false;
    }

    return returnval;
}

function validateUsername(name) {
    var returnval = true;
    var uname = document.forms[name]["uname"].value;
    if (uname.length < 6 || uname.length > 10) {
        seterror("uname", "*Username should be at least 6 and at most 10 characters long!<br>");
        returnval = false;
    }
    if (uname.match(/[^a-zA-Z\d]/g)) {
        seterror("uname", "*Username should not contain any special character!<br>");
        returnval = false;
    }
    return returnval;
}

function validateMobile(name) {
    var returnval = true;
    var mobile = document.forms[name]["mobile"].value;
    if (mobile.length != 10) {
        seterror("mobile", "*Mobile number should be 10 characters long!<br>");
        returnval = false;
    }
    return returnval;
}

function validateDOB(name) {
    var returnval = true;

    var dateString = document.forms[name]["dob"].value;
    var parts = dateString.split("-");
    var dtDOB = new Date(parts[1] + "/" + parts[2] + "/" + parts[0]);
    var dtCurrent = new Date();

    if (dtCurrent.getFullYear() - dtDOB.getFullYear() < 18) {
        seterror("dob", "*Eligibility 18 years ONLY!<br>");
        returnval = false;
    }

    if (dtCurrent.getFullYear() - dtDOB.getFullYear() == 18) {
        if (dtCurrent.getMonth() < dtDOB.getMonth()) {
            seterror("dob", "*Eligibility 18 years ONLY!<br>");
            returnval = false;
        }
        if (dtCurrent.getMonth() == dtDOB.getMonth()) {
            if (dtCurrent.getDate() < dtDOB.getDate()) {
                seterror("dob", "*Eligibility 18 years ONLY!<br>");
                returnval = false;
            }
        }
    }
    return returnval;
} 


function validateInput(name) {
    var returnval = true;
    var s = document.forms[name]["iname"].value;
    s = s.trim()
    if (s.length == 0) {
        seterror("iname", "Name cannot be empty!");
        returnval = false;
    }
    var s = document.forms[name]["unit"].value;
    s = s.trim()
    if (s.length == 0) {
        seterror("unit", "Unit cannot be empty!");
        returnval = false;
    }
    return returnval;
}


function validateExpDate(name) {
    var returnval = true;
    var d1 = document.forms[name]["mfg"].value;
    var d2 = document.forms[name]["exp"].value;
    if (d1 > d2) {
        seterror("date", "Exp date cannot be less than Mfg date!");
        returnval = false;
    }
    return returnval;
}


function validateForm(name) {
    var returnval = true;
    clearErrors();
    returnval = validateEmail(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validatePassword(name);
    return returnval;
}


function validateForm2(name) {
    var returnval = true;
    clearErrors();
    returnval = validateUsername(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validateDOB(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validateMobile(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validateEmail(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validatePassword(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validateConfirmPassword(name);
    return returnval;
}


function validateForm3(name) {
    var returnval = true;
    clearErrors();
    returnval = validateInput(name);
    if (returnval == false) {
        return returnval;
    }
    returnval = validateExpDate(name);

    return returnval;
}


function clearStorage() {
    localStorage.removeItem('ids');
    localStorage.removeItem('qty');
}