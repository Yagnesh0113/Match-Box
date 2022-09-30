/* Start  Community - Post Image and video Restriction */
let fileInput = document.getElementById("file_id");
   let fileSubmit = document.getElementById("file-submit");

   fileInput.addEventListener("change", function(){
      if (fileInput.files.length > 0){
         const fileSize=fileInput.files.item(0).size;
         const fileMb=fileSize/1024**2;
         if (fileMb >= 2){
            alert("Please select a file less than 2MB.")
            fileInput.value="";
            fileSubmit.disabled = true;
         } else {
            fileSubmit.disabled = false;
         }

      }
   });
/* End  Community - Post Image and video Restriction */

/* Start Create Community - Restriction for - profile and Cover image */
 function community_check1()
{
   var file1 = document.getElementById("file_1");
   var max_id = document.getElementById("max_obj").value;

   if (file1.files[0].size > max_id)
   {
      alert("Please select a file less than 2MB.");
      file1.value = "";
   }
};

function community_check2()
{
   var file2 = document.getElementById("file_2");
   var max2 = document.getElementById("max_obj1").value;

   if (file2.files[0].size > max2)
   {
      alert("Please select a file less than 2MB.");
      file2.value = "";
   }
};
/* End Create Community - restriction for - profile and Cover image */

/* Start Ask and post js */
document.getElementsByClassName("tablink")[0].click();

function openCity(evt, cityName) {
 var i, x, tablinks;
 x = document.getElementsByClassName("city");
 for (i = 0; i < x.length; i++) {
   x[i].style.display = "none";
 }
 tablinks = document.getElementsByClassName("tablink");
 for (i = 0; i < x.length; i++) {
   tablinks[i].classList.remove("w3-light-grey");
 }
 document.getElementById(cityName).style.display = "block";
 evt.currentTarget.classList.add("w3-light-grey");
}
/* End Ask and post js */

/* Start navigation drop down script */
(function($){
      $('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
      if (!$(this).next().hasClass('show')) {
      $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
      }
      var $subMenu = $(this).next(".dropdown-menu");
      $subMenu.toggleClass('show');

      $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
      $('.dropdown-submenu .show').removeClass("show");
      });

      return false;
      });
      })(jQuery)
/* End navigation drop down script */

/* Start the report-post script */
function Reportpost(id){
      document.getElementById('report-post').action ='';
      document.getElementById("demo1").value = id;
   }
/* End the report-post script */

/* Start the report-question script */
 function Reportquestion(id){
      document.getElementById('report-question').action ='';
      document.getElementById("demo2").value = id;
   }
/* End the report-question script */