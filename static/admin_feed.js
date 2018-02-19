var $ = window.jQuery;

    function load_page(){
        var autorize = {'action': 'load_page'};

        var data = new FormData();
        data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/admin_feed',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                    var data = JSON.stringify(data);

                    data = JSON.parse(data);

                    for (i = 0; i < data.number; i++){
                        var div = document.createElement('div');

                        div.setAttribute('class', 'item');
                        div.setAttribute('id', 'post-' + String(i));

                        var keywords = '<p>' + data.summary[i].keywords.replace(/,/g , '</p><p>') + '</p>';

                        var child_div = '<div class="post-block"><h3><button id="hide-' + String(i) + '" onclick="hide(' + String(i) + ')"><i class="fa fa-times" aria-hidden="true"></i></button>' + data.summary[i].title + '</h3><div class="post-image"><img src="' + data.summary[i].photo + '" alt="Image"></div><div class="post-content"><p class="summ-text">' + data.summary[i].summary + '</p><div class="post-link"><a target="_blank" href="' + data.summary[i].link + '" id="link-' + String(i) + '">Link to post</a></div><div class="post-date">' + data.summary[i].date + '</div><div class="post-keywords">' + keywords + '</div></div></div></div>';


                        div.innerHTML = child_div;

                        main_div = document.getElementById("main_div");

                        main_div.appendChild(div);
                    }


             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });
         }

load_page()


    function hide(event){
       var link = document.getElementById('link-' + String(event)).href;

       var autorize = {'link': link,
                       'action':'hide'};

       var data = new FormData();
       data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/admin_feed',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                if(data.status == 'done'){
                    main_div = document.getElementById("main_div");
                    div = document.getElementById("post-" + String(event));

                    main_div.removeChild(div);
                }
             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });
    }