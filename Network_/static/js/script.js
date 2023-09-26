const Scroll_Controler = {
    DisableScrool(){
        document.body.style.cssText = `
        overflow:hidden;
    `
    },
    EnableScrool(){
        document.body.style.cssText = ''
    }
}

$('#close_post_more_info_popup_').click(function(){
    document.body.style.cssText = '';
    $('.popup_for_more_about_post').css('display', 'none')
    
})


function new_post_popup(header='Новый пост',description_text, post_image, url_to_send_data='send_data_for_create_new_post()', author){
    Scroll_Controler.DisableScrool();
    $('.create_new_post_main_div').css('display','block');
    
    $('.post_author').text(author)
    $('.post_author').css('display','none')
    
    $('.new_post_popup_header').text(header);
    $('.new_post_popup_textarea').val(description_text);
    $('.send_data_btn_new_post_popup').attr('onclick', url_to_send_data);
    $('.post_image_in_new_post_popup').attr('value', post_image);
}


function delete_post_in_favorite(post_id){

}


function close_popup(){
    $('.create_new_post_main_div').css('display','none');
    Scroll_Controler.EnableScrool();
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
    postImage = document.getElementById('post_image_in_new_post_popup_id').files[0]
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

            var post = JSON.parse(data)
            console.log(post)
            var div_block_with_new_post = `
            <div class="gallery-item post_id_` + post[0]['pk'] +`" tabindex="0" onclick="view_more_about_post_in_profile('`+ post[0]['pk'] +`')">
                <img src="` + post[0]['fields']['image']  + `" class="gallery-image" alt="">
                <div class="gallery-item-info">
                    <ul>
                        <li class="gallery-item-likes"><span class="visually-hidden">Likes:</span><i class="fas fa-heart" aria-hidden="true"></i></li>
                        <li class="gallery-item-comments"><span class="visually-hidden">Comments:</span><i class="fas fa-comment" aria-hidden="true"></i> </li>
                    </ul>
                </div>
            </div>`
            $('.gallery').prepend(div_block_with_new_post)

        }
    })
}


function subscribe_to_user(user_id){
    $.ajax({
        url:'subscribe',
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data:{'user_id': user_id},
        success: (data) => {
            $('#sub_unsub_to_user_btn').text('Отписаться');
            $('#sub_unsub_to_user_btn').attr('onclick', 'unsubscribe_user('+ user_id +')');
        }
    })
}


function  open_popup_for_post(post_id, open_in_to){   
    $.ajax({
        url:'/get_post',
        headers: { "X-CSRFToken": getCookie("csrf_token")},
        data:{'post_id': post_id},
        method:'GET',
        contentType: 'application/json',
        dataType:'json',
        success: function(data){
        
            
        var comments = data['comments']
        var post = JSON.parse(data['post'])
        

        Scroll_Controler.DisableScrool();
        $('.popup_for_more_about_post').css('display', 'block')

        $('.more_info_about_post_block__img').attr('src', '/'+ post[0]['fields']['image']),
        $('.more_info_about_post__description').text(post[0]['fields']['description']),
        $('.like_btn_in_post_more_info_popup').attr('onclick', 'adding_like_for_post(' + post[0]['pk'] + ')'),
        $('.like_btn_in_post_more_info_popup').html(data['Likes'] + '<img src="'+ data['like_icon'] +'"></img>'),
        $('.add_comment_btn').attr('onclick', 'add_comment('+ post[0]['pk'] +')'),
        $('.publication_author_link').attr('href', 'get_user_profile/' + post[0]['fields']['author']),
        $('.publication_author_link').text( data['author']),
        $('.save_btn_in_post_more_info_popup').attr('onclick', 'save_post_to_favorite('+ post[0]['pk']+')'),
        $('.change_publication_data_btn').attr('onclick', 'change_post_data('+ post[0]['pk'] +')'),
        $('.comments_div_in_popup_for_more_info').html('')  
        $('.delete_publication_btn').attr('onclick', 'send_data_to_del_pub_('+ post[0]['pk'] +')')
    
        for (var comm in comments){
            $('.comments_div_in_popup_for_more_info').append(`
            <div class="comment_div_in_publication_feed_post">
                <p>Автор:  ` + comments[comm]['author'] + `</p>
                <a class="comment_in_publication_feed_post">Текст комментария:<br/> ` + comments[comm]['text'] + `</a>
                <p>--------------------------------</p>
            </div> `
            )
        }

        if(open_in_to === 'Pub_feed'){
            // data_to_open_popup.push("$('#sub_unsub_to_user_btn').remove();")

            if (data['self_user_follow_author'] === 0){
                $('.sub_unsub_user_btn').attr('onclick' ,'subscribe_to_user('+ post[0]['fields']['author'] +')')
                $('.sub_unsub_user_btn').text('Подписаться')
            }
            else{
                $('.sub_unsub_user_btn').attr('onclick' ,'unsubscribe_user('+ post[0]['fields']['author'] +')')
                $('.sub_unsub_user_btn').text('Отписаться')

            }
            
        }
        else if(open_in_to === 'pub_feed'){
                $()
                $('.submenu_btn_in_post_more_info_popup').remove();
                $('.delete_publication_btn'),attr('onclick', 'remove_post_on_favorites');

        }


}
})

}


// Закрытие окна с информацией о посте
function close_popup_post(){
    $('.popup_for_more_about_post').css('display', 'none');
    $('.publication_submenu_block').css('display', 'none');
    Scroll_Controler.EnableScrool();
}


function unsubscribe_user(post_author){
    $.ajax({
        url:'unsubscribe',
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data:{'following_user_id': post_author},
        success: (data) => {
            $('#sub_unsub_to_user_btn').text('Подписаться');
            $('#sub_unsub_to_user_btn').attr('onclick', 'subscribe_to_user( '+ post_author +' )');
        }
    })
}

function send_data_to_del_pub_(publication_id){
    $.ajax({
        url:'delete_post',
        type: 'POST',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data:{'post_id': publication_id},
        success: (data) => {
            $('#user_publication_id_'+publication_id).remove();
            $('.popup_for_more_about_post').css('display', 'none');
            $('.publication_submenu_block').css('display', 'none');
            $('.post_id_'+ publication_id).remove()
        }
    })
}


// $('.submenu_btn_in_post_more_info_popup').click(function(){
//     console.log('f')
//     let a = 0
//     if(a === 1){
//         $('.publication_submenu_block').css('display', 'none');
//         a = 0;
//     }
//     else{
//         $('.publication_submenu_block').css('display', 'block');
//         a = 1
//     }
// })

function adding_like_for_post(post_id){
    $.ajax({
        url:'/Like/add_like',
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
            $('.comment_div_in_publication_feed_post').append(`
            <div class="comment_in_publication_feed_post">
                <p>Автор:  ` + data['author'] + `</p>
                <a class="comment_in_publication_feed_post"> Текст комментария:<br/> ` + data['text'] + `</a>
                <p>--------------------------------</p>
            </div>
            `)
        }
    })
}

function save_post_to_favorite(post_id){
    $.ajax({
        url:'/Post/save_post',
        data:{'saved_post_id': post_id},
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        method:'POST',
        success:function(data){
            console.log(data)
            if(data['post_status'] === 'removed'){
                $('.saved_post_id_'+ post_id).remove();
            }
        }
    })
}

var sub_menu_popup_count = 0;
function open_sub_mune_in_post(open_in){

    if(sub_menu_popup_count === 0){

        $('.publication_submenu_block').css('display', 'block');
        sub_menu_popup_count ++;
    }
    else{
        sub_menu_popup_count --;
        $('.publication_submenu_block').css('display', 'none');
    }
}

//изменение данных поста
function change_post_data(post_id){
    close_popup_post();//для закрытия popup'a с информацией о посте  
    open_sub_mune_in_post();//для закрытия под-меню
    $.ajax({
        url:'get_post',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data:{'post_id':post_id},
        method:'GET',
        success: function(data){
            post_data = JSON.parse(data['post']);

            new_post_popup(
                header='Изменение поста' + post_data[0]['pk'],
                description_text = post_data[0]['fields']['description'],
                post_image = post_data[0]['fields']['image'],
                url_to_send_data = 'send_changed_data_to_back('+ post_data[0]['pk'] +')',
                author = post_data[0]['fields']['author']
                );

        }
    })
}

function load_user_posts(author){

    $.ajax({
        url:'get_user_posts',
        type: 'GET',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        data:{'post_author': author},
        success: (data) => {
            close_popup();
        }
    })

}

function refresh_changed_pub_in_profile(post_id){
    publication_by_id = $('#user_publication_id_'+post_id)
    pub_img = $('#image_for_post_id_'+post_id)
    pub_text = $('#description_for_post_id_'+post_id)

    $.ajax({
        url:'get_post',
        method: 'GET',
        data: {'post_id': post_id},
        enctype: 'multipart/form-data',
        headers: { "X-CSRFToken": getCookie("csrftoken")},
        success: (data) => {
            post_data = JSON.parse(data['post'])
            close_popup();
            pub_img.attr('src', post_data[0]['fields']['image'])
            pub_text.text(post_data[0]['fields']['description'])

        }
    })

}

function send_changed_data_to_back(post_id){
    post_description = $('.new_post_popup_textarea').val();
    post_image = $('.post_image_in_new_post_popup')[0].files[0];

    
    var formData = new FormData();
    formData.append('post_id',post_id);
    formData.append('post_description',post_description);
    formData.append('post_image', post_image);

    $.ajax({
        url:'change_post_data',
        method: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        headers: { "X-CSRFToken": getCookie("csrftoken")},

        success: function(data){
            refresh_changed_pub_in_profile(post_id);
        }
    })
}