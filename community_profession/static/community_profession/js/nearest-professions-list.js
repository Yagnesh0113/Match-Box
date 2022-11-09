/* Start search list */
   function professionSearch() {
     var input, filter, ul, li, a, i;
     input = document.getElementById("profession-search");
     filter = input.value.toUpperCase();
     ul = document.getElementById("profession_id");
     li = ul.getElementsByTagName("li");
     for (i = 0; i < li.length; i++) {
       a = li[i].getElementsByTagName("a")[0];
       if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
         li[i].style.display = "";
       } else {
         li[i].style.display = "none";
       }
     }
   }
/* End search list */