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