var $ = window.jQuery;


    $('#sign_up').on('click', registration)

    function registration(){
        var email = document.getElementById('email2').value;
        var password = document.getElementById('password2').value;
        var name = document.getElementById('name').value;
        var surname = document.getElementById('surname').value;

        var autorize = {'email': email,
                        'password': password,
                        'action': 'registration'};

        var data = new FormData();
        data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/login',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                    if (data.action == 'redirect'){
                        window.location.replace('http://18.221.117.153:8000/user_feed');
                    }
                    else{
                        alert(data.action);
                    }


             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });
         }


    $('#log_in').on('click', login)

    function login(){
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;

        var autorize = {'email': email,
                        'password': password,
                        'action': 'login'};

        var data = new FormData();
        data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/login',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                    if (data.action == 'redirect_user'){
                        window.location.replace('http://18.221.117.153:8000/user_feed');
                    }
                    else if (data.action == 'redirect_admin'){
                        window.location.replace('http://18.221.117.153:8000/admin');
                    }
                    else if (data.action == 'Incorrect email or password'){
                        alert(data.action);
                    }


             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });
         }


    function forgot_password(){
        document.body.style.cursor='wait';

        var email = document.getElementById('forgot_email').value;

        var autorize = {'email': email,
                        'action': 'forgot_email'};

        var data = new FormData();
        data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/login',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                    if (data.action == 'Code sent'){
                        document.body.style.cursor='default';

                        document.getElementById('message').innerHTML = 'Code was sent on your email';

                        code_input = document.createElement('input');

                        code_input.setAttribute('type', 'text');
                        code_input.setAttribute('class', 'forgot');
                        code_input.setAttribute('placeholder', 'Enter code from email');
                        code_input.setAttribute('id', 'forgot_code');

                        new_pass = document.createElement('input');

                        new_pass.setAttribute('type', 'password');
                        new_pass.setAttribute('class', 'forgot');
                        new_pass.setAttribute('placeholder', 'Enter new password');
                        new_pass.setAttribute('id', 'new_pass');

                        confirm_pass = document.createElement('input');

                        confirm_pass.setAttribute('type', 'password');
                        confirm_pass.setAttribute('class', 'forgot');
                        confirm_pass.setAttribute('placeholder', 'Confirm password');
                        confirm_pass.setAttribute('id', 'confirm_pass');

                        forgot_div = document.getElementById('forgot_div');

                        forgot_div.insertBefore(code_input, forgot_div.children[2]);
                        forgot_div.insertBefore(new_pass, forgot_div.children[2]);
                        forgot_div.insertBefore(confirm_pass, forgot_div.children[2]);

                        document.getElementById('forgot_button').setAttribute('onclick', 'confirm_code()');
                        document.getElementById('forgot_button').value = 'Log in'
                    }
                    else if (data.action == 'Incorrect email'){
                        document.body.style.cursor='default';

                        alert(data.action);
                    }


             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });
         }


    function confirm_code(){
        document.body.style.cursor='wait';

        var email = document.getElementById('forgot_email').value;
        var code = document.getElementById('forgot_code').value;
        var new_pass = document.getElementById('new_pass').value;
        var confirm_pass = document.getElementById('confirm_pass').value;

        if((new_pass != confirm_pass) || (new_pass == '') || (confirm_pass == '')){
            document.body.style.cursor='default';

            alert('Comfirm password is incorrect');
        }
        else{
            var autorize = {'email': email,
                            'code': code,
                            'new_pass': new_pass,
                            'confirm_pass': confirm_pass,
                            'action': 'confirm_code'};

            var data = new FormData();
            data.append("data", JSON.stringify(autorize));

              $.ajax({
                 url: 'http://18.221.117.153:8000/login',
                 type: 'POST',
                 data: data,
                 cache: false,
                 dataType: 'json',
                 processData: false,
                 contentType: false,
                 success:function(data, status) {
                        document.body.style.cursor='default';

                        if (data.action == 'redirect_user'){
                        window.location.replace('http://18.221.117.153:8000/user_feed');
                    }
                        else if (data.action == 'redirect_admin'){
                        window.location.replace('http://18.221.117.153:8000/admin');
                    }
                        else {
                            alert(data.action);
                        }


                 },
                 error: function (XHR, status, error) {
                    console.log('Error: ', error);
                 }
              });
        }
    }


    function close_forgot(){
        document.getElementById('forgot_email').value = '';

        if(document.getElementById('forgot_div').contains(document.getElementById('forgot_code'))){
            document.getElementById('message').innerHTML = 'Enter Your e-mail for autorization';
            document.getElementById('forgot_code').remove();
            document.getElementById('new_pass').remove();
            document.getElementById('confirm_pass').remove();
            document.getElementById('forgot_button').setAttribute('onclick', 'forgot_password()');
            document.getElementById('forgot_button').value = 'Send me a code';
        }
    }