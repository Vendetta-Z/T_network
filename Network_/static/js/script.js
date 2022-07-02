function new_post_popup(){
    x = 1;
    div_create_post = document.getElementsByClassName('create_new_post_main_div');
    div_cover = document.getElementsByClassName('new_post_button_background_cover')
    
    if (x === 1){
        $('.create_new_post_main_div').css('display','block');
        $('.new_post_button_background_cover').css('display','block');
        x = 0;
    }
    else{
        console.log('что-то с функцией открытия popup создание нового поста')
    }
}


function close_popup(){
    $('.create_new_post_main_div').css('display','none');
    $('.new_post_button_background_cover').css('display','none');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function send_data_for_create_new_post(){
    postImage = document.getElementById('post_image').files[0]
    postDescription = document.getElementById('description_textarea_for_new_post').value

    var formdata = new FormData()
    formdata.append('postImage', postImage); 
    formdata.append('postDescription', postDescription);

    $.ajax({
        url:'/create_new_post',
        method: "POST",
        processData: false,
        contentType: false,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data:formdata,
        success: function(data){
            
            $('.create_new_post_main_div').css('display','none');
            $('.new_post_button_background_cover').css('display','none');

            $('.notification_popup_main_div').css('display', 'block')
            $('.notification_popup_paragraph').text('fuck')
            setInterval(function(){
                $('.notification_popup_main_div').css('display', 'none')
            }, 2000);

            var posts = JSON.parse(data)
            console.log(posts)
            var post = '<div class="block_with_posts" onclick="view_more_about_post(' + posts[0]['pk'] + ')">'
                            +'<img src="'+ posts[0]['fields']['image'] +'">'
                            +'<h4>'+ posts[0]['fields']['description'] +'</h4>'
                        +'</div>'
            $('.posts').prepend(post)

        }
    })
}   



function view_more_about_post(post_id){
    $('.popup_for_more_about_post').css('display', 'block')

    $.ajax({
        url:'get_post',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data:{'post_id':post_id},
        method:'GET',
        success: function(data){
            post = JSON.parse(data['post'])
            likes_len = data['Likes']
            $('.more_info_about_post_block__img').attr('src', post[0]['fields']['image'])
            $('.like_btn_in_post_more_info_popup').attr('onclick', 'adding_like_for_post(' + post[0]['pk'] + ')')
            $('.like_btn_in_post_more_info_popup').html(likes_len + '<img src="'+ data['like_icon'] +'"></img>')
            $('.more_info_about_post__description').text(post[0]['fields']['description'])
            $('.add_comment_btn').attr('onclick', 'add_comment('+ post[0]['pk'] +')')
            $('.publiation_author_link').attr('href', 'get_user_profile/' + post[0]['fields']['author'])
            $('.publiation_author_link').text( data['author'])

            $('.comments_div_in_popup_for_more_info').html('')
            comments = data['comments']
            for (var comm in comments){
                $('.comments_div_in_popup_for_more_info').append(`
                <div>
                    <p>Автор:  ` + comments[comm]['author'] + `</p>
                    <a>Текст комментария: ` + comments[comm]['text'] + `</a>
                    <p>--------------------------------</p>
                </div> `
                )
            }
        }   
    })
}


// Закрытие окна с информацией о посте 
$('#close_post_more_info_popup_').click(function(){
    $('.popup_for_more_about_post').css('display', 'none')
})







$('.submenu_btn_in_post_more_info_popup').click(function(){
    let a = 0
    if(a === 0){
        $('.publication_submenu_block').css('display', 'none')
        a = 1
    }
    if(a === 1){
        $('.publication_submenu_block').css('display', 'block')
        a = 0
    }
})

function adding_like_for_post(post_id){
    $.ajax({
        url:'Like/add_like',
        data:{'post_id': post_id},
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        method:'POST',
        success:function(data){
            if(data['method'] === 'A'){
                $('.like_btn_in_post_more_info_popup').html((data['Likes_count'] + '<img src="'+ data['like_icon'] +'"></img>'))
            }
            else if(data['method'] === 'R'){
                $('.like_btn_in_post_more_info_popup').html((data['Likes_count'] + '<img src="'+ data['like_icon'] +'"></img>'))
            }
        }
    })
}

function add_comment(post_id){
    text = $('.comment_text_input').val()
    $.ajax({
        url:'Comments/new_comment',
        data:{'post_id': post_id, 'comm_text': text},
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        method:'POST',
        success:function(data){
            console.log(data)
            $('.comments_div_in_popup_for_more_info').append(`
            <div>
                <p>` + data['author'] + `</p>
                <a>` + data['text'] + `</a>
                <p>--------------------------------</p>
            </div>
            `)
        }
    })
}    
