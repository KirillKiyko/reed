var $ = window.jQuery;

    function load_page($){
        var autorize = {'action': 'load_page'};

        var data = new FormData();
        data.append("data", JSON.stringify(autorize));

        $.ajax({
             url: 'http://18.221.117.153:8000/admin',
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

                        var keywords = '<p>' + data.summary[i].keywords.replace(/,/g , '</p><p>') + '</p>'

                        var child_div = '<div class="post-block"><h3>' + data.summary[i].title + '</h3><div class="post-image"><img src="' + data.summary[i].photo + '" alt="Image"></div><div class="post-content"><p class="summ-text">' + data.summary[i].summary + '</p><div class="post-link"><a target="_blank" href="' + data.summary[i].link + '" id="link-' + String(i) + '">Link to post</a></div><div class="post-date">' + data.summary[i].date + '</div><div class="post-keywords">' + keywords + '</div></div></div><div class="post-control"><button class="like" onclick="like(' + String(i) + ')"><i class="fa fa-thumbs-up" aria-hidden="true"></i></button><button class="dislike" onclick="dislike(' + String(i) + ')"><i class="fa fa-thumbs-up" aria-hidden="true"></i></button></div></div>';


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

load_page($)

   function like(event) {
       var action = 'publish';
       var link = document.getElementById('link-' + event).href;

       var autorize = {'link': link,
                       'action': action};

       var data = new FormData();
       data.append("data", JSON.stringify(autorize));

         $.ajax({
             url: 'http://18.221.117.153:8000/admin',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                 if (data.status == 'done'){
                    main_div = document.getElementById("main_div");
                    div = document.getElementById("post-" + event);

                    main_div.removeChild(div);
                 }
             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }

          });


   }



   function dislike(event) {
       var action = 'private';
       var link = document.getElementById('link-' + event).href;

       var autorize = {'link': link,
                       'action': action};

       var data = new FormData();
       data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/admin',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                 if (data.status == 'done'){
                    main_div = document.getElementById("main_div");
                    div = document.getElementById("post-" + event);

                    main_div.removeChild(div);
                 }
             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }

          });


   }




