var email = document.getElementById("email");
var email2 = document.getElementById("email2");
    
function ValidateEmail(inputText)
{
var mailformat = /^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i;
if(inputText.value.match(mailformat))
{
document.getElementById("email").style.outline = "none"
return true;
}
else
{
document.getElementById("email").style.outline = "1px solid red"

return false;
}
}

function ValidateEmail2(inputText)
{
var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
if(inputText.value.match(mailformat))
{
document.getElementById("email2").style.outline = "none"
return true;
}
else
{
document.getElementById("email2").style.outline = "1px solid red"

return false;
}
}

function ValidatePassword(){
        if(document.loginform.password.value == ''){
        document.getElementById("password").style.outline = "1px solid red"
        return false;
    }else{
        document.getElementById("password").style.outline = "none"
    }
    
}

function ValidatePassword2(){
        if(document.signupform.password2.value == ''){
        document.getElementById("password2").style.outline = "1px solid red"
        return false;
    }else{
        document.getElementById("password2").style.outline = "none"
    }
    
}

function ValidateName(){
        if(document.signupform.name.value == ''){
        document.getElementById("name").style.outline = "1px solid red"
        return false;
    }else{
        document.getElementById("name").style.outline = "none"
    }
    
}

function ValidateSurname(){
        if(document.signupform.surname.value == ''){
        document.getElementById("surname").style.outline = "1px solid red"
        return false;
    }else{
        document.getElementById("surname").style.outline = "none"
    }
    
}

function ValidateSearch(){
        if(document.searchform.url.value == ''){
        document.getElementById("url").style.outline = "1px solid red"
        return false;
    }else{
        document.getElementById("url").style.outline = "none"
    }
    
}

function ClearUrl(){
    if(document.searchform.url.value != ''){
        document.searchform.url.value = ''
    }
}