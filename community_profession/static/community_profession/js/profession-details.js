/* Start profession profile Restriction */
let fileInput = document.getElementById("file_id");
   let fileSubmit = document.getElementById("file-submit");

   fileInput.addEventListener("change", function(){
      if (fileInput.files.length > 0){
         const fileSize=fileInput.files.item(0).size;
         const fileMb=fileSize/1024**2;
         if (fileMb >= 2){
            alert("Please select a file less than 2MB.")
            fileInput.value = "";
            fileSubmit.disabled = true;
         } else {
            fileSubmit.disabled = false;
         }

      }
   });
/* End profession profile Restriction */

/* Start profession Image Add Restriction */
let fileInput1 = document.getElementById("file_id1");
   let fileSubmit1 = document.getElementById("file-submit1");

   fileInput1.addEventListener("change", function(){
      if (fileInput1.files.length > 0){
         const fileSize1=fileInput1.files.item(0).size;
         const fileMb1=fileSize1/1024**2;
         if (fileMb1 >= 2){
            alert("Please select a file less than 2MB.")
            fileInput1.value = "";
            fileSubmit1.disabled = true;
         } else {
            fileSubmit1.disabled = false;
         }

      }
   });
/* End profession Image Add Restriction */

/* Start profession Video Add Restriction */
let fileInput2 = document.getElementById("file_id2");
   let fileSubmit2 = document.getElementById("file-submit2");

   fileInput2.addEventListener("change", function(){
      if (fileInput2.files.length > 0){
         const fileSize2=fileInput2.files.item(0).size;
         const fileMb2=fileSize2/1024**2;
         if (fileMb2 >= 2){
            alert("Please select a file less than 2MB.")
            fileInput2.value = "";
            fileSubmit2.disabled = true;
         } else {
            fileSubmit2.disabled = false;
         }

      }
   });
/* End profession Video Add Restriction */

/* Start edit service */
function data(id,val1,val2){
      document.getElementById('serviceedit').action ='/edit_service/'+id;
      document.getElementById("demo1").value = val1;
      document.getElementById("demo2").value = val2;
   }
/* End edit service */