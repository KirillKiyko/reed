    function google_auth(){
        console.log('google');

        $.ajax({
           url: 'http://localhost:8000/google_login',
           type: 'GET',
           success:function(data, status) {
                  console.log(data, status);
                  alert(data.message);
           },
           error: function (XHR, status, error) {
              console.log('Error: ', error);
           }
        });
    }


    function twitter_auth(){
        console.log('twitter');
        $.ajax({
           url: 'http://localhost:8000/twitter_login',
           type: 'GET',
           success:function(data, status) {
                  console.log(data, status);
           },
           error: function (XHR, status, error) {
              console.log('Error: ', error);
           }
        });
    }