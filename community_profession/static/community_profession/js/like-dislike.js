$('.like-form').submit(function(e){
      e.preventDefault()
      //console.log('works')
      const post_id = $(this).attr('id')
      //console.log(post_id)
      const liketext = $(`.like-btn${post_id}`).html()
      //console.log(liketext)
      const trim = $.trim(liketext)
      //console.log(trim)
      const url = $(this).attr('action')
      //console.log(url)
      let res;
      const likes = $(`.like-count${post_id}`).text()
      //console.log(likes + 1)
      const trimCount = parseInt(likes)
      //console.log(trimCount + 1)

      $.ajax(
         {
         type : "POST",
         url : url,
         data : {
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
            'post_id':post_id,
         },
         success: function(response){
            //console.log('success', response)
            if(trim === '<i class="fa-solid fa-thumbs-down"></i>') {
               $(`.like-btn${post_id}`).html('<i class="fa-solid fa-thumbs-up"></i>')
               res = trimCount - 1
            } else {
               $(`.like-btn${post_id}`).html('<i class="fa-solid fa-thumbs-down"></i>')
               res = trimCount + 1
            }

           $(`.like-count${post_id}`).text(res)
         },
         error: function(response) {
            console.log('error', response)
        }
      }
      )

   })