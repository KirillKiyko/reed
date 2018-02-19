var $ = window.jQuery;

    function load_page(){
        var autorize = {'action': 'load_page'};

        var data = new FormData();
        data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/summary',
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

                        keywords = '<p>' + data.summary[i].keywords.replace(/,/g, '</p><p>') + '</p>'

                        var child_div = '<div class="post-block"><h3><button id="del-' + String(i) + '"onclick="del(' + String(i) + ')"><i class="fa fa-times" aria-hidden="true"></i></button>' + data.summary[i].title + '</h3><div class="post-image"><img src="' + data.summary[i].photo + '" alt="Image"></div><div class="post-content"><p class="summ-text">' + data.summary[i].summary + '</p><div class="post-link"><a target="_blank" href="' + data.summary[i].link + '" id="link-' + String(i) + '">Link to post</a></div><div class="post-date">' + data.summary[i].date + '</div><div class="post-keywords">' + keywords + '</div></div></div></div>';


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


   $('#get_url').on('click', get_url)


    function get_url(event) {
      document.body.style.cursor='wait';
      event.preventDefault();
      event.stopPropagation();

       var url = document.getElementById('url').value;
       if(document.getElementById('url').value!='') {document.getElementById('url').value=''};

       var autorize = {'url': url,
                       'action':'summary'};

       var data = new FormData();
       data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/summary',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                document.body.style.cursor='default';
                if(data.result == 'You have this result'){
                    alert(data.result);
                }
                else{
                    if (data.result == 'This language will be supported soon'){
                        alert('This language will be supported soon');
                    }
                    else if (data.result == 'This URL is unsummarizable'){
                        alert(data.result);
                    }
                    else{
                        var data = JSON.stringify(data);

                        data = JSON.parse(data);

                        var div = document.createElement('div');

                        div.setAttribute('class', 'item');
                        div.setAttribute('id', 'post-' + String(data.number));

                        var keywords = '<p>' + data.summary.keywords.replace(/,/g, "</p><p>") + '</p>';

                        child_div = '<div class="post-block"><h3><button id="del-' + String(data.number) + '" onclick="del(' + String(data.number) + ')"><i class="fa fa-times" aria-hidden="true"></i></button>' + data.summary.title + '</h3><div class="post-image"><img src="' + data.summary.photo + '" alt="Image"></div><div class="post-content"><p class="summ-text">' + data.summary.summary + '</p><div class="post-link"><a target="_blank" href="' + data.summary.link + '" id="link-' + String(data.number) + '">Link to post</a></div><div class="post-date">' + data.summary.date + '</div><div class="post-keywords">' + keywords + '</div></div></div></div>';


                        div.innerHTML = child_div;

                        main_div = document.getElementById("main_div");

                        main_div.insertBefore(div, main_div.children[0]);
                    }
                }
             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });


   }

    function del(event) {

       var link = document.getElementById('link-' + String(event)).href;

       var autorize = {'url': link,
                       'action':'delete'};

       var data = new FormData();
       data.append("data", JSON.stringify(autorize));

          $.ajax({
             url: 'http://18.221.117.153:8000/summary',
             type: 'POST',
             data: data,
             cache: false,
             dataType: 'json',
             processData: false,
             contentType: false,
             success:function(data, status) {
                if(data.result == 'done'){
                    main_div = document.getElementById("main_div");
                    div = document.getElementById("post-" + event);
                    console.log(div);

                    main_div.removeChild(div);
                }
             },
             error: function (XHR, status, error) {
                console.log('Error: ', error);
             }
          });


   }