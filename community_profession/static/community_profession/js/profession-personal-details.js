/* Start - Star rating */
function replace_stars(value){
   	var html="\n";
   	var i;
   	for(i=1;i<=5;i++){
   		html+=" <input class='star' type='radio' name='rating' value='"+i+"' "+(value==i?"checked='checked'":"")+" />\n";
   	}
   	html+="<script type='text/javascript'>\n";
   	html+="  $('#container').find('.star').rating({\n";
   	html+="    callback: function(){ this.form.onsubmit() && this.form.submit(); }\n"
   	html+="  });\n";
   	html+="</"+"script>\n";
   	$("#code").val(html);
   	$("#container").html(html);
   }
   $(document).ready(function(){
    replace_stars(1);
   });
/* End - Star rating */

/* Start - Update Review - using modal */
function data(id,val1){
      document.getElementById('EditReview').action ='/edit_review/'+id;
      document.getElementById("demo1").value = val1;
   }
/* End - Update Review - using modal */


