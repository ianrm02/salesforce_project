var acc = document.getElementsByClassName("accordion");
var sdropdown_ids = {"US":["TX", "DE"], "AR":["ER"]};
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function () {
  this.classList.toggle("active");
  var panel = this.nextElementSibling
  if (panel.style.display === "block") {
    panel.style.display = "none";
  } else {
    panel.style.display = "block";
  }
  });
}
// Takes input for the next page and makes the url. We don't have pages sorted into folders so using the root(/) allow us to make the url work
// More complex webapp would need to utilize url_for or something similar
function redirect(next_page) {
  window.location.href = "/"+next_page;
}

function selectAll(table, bx) {
  for (var bxs = table.getElementsByTagName('input'), j = bxs.length; j--;) {
    if (bxs[j].type == "checkbox") {
      bxs[j].checked = bx.checked;
    }
  }
}

function repopulate_statedropdown(ccode, fieldstring){
  var cdropdown = document.getElementById("cdropdown" + ccode + fieldstring);
  var nccode = cdropdown.options[cdropdown.selectedIndex].text;
  var sdropdown = document.getElementById("sdropdown" + ccode + fieldstring);
      
  while(sdropdown.options.length > 0){
    sdropdown.remove(0);
  }
  if(!(nccode in sdropdown_ids)){
    var emptyoption = document.createElement("option");
    emptyoption.text = "No states available";
    sdropdown.appendChild(emptyoption);
    return;
  }
  for(var i = 0; i < sdropdown_ids[nccode].length; i++){
    var newOption = document.createElement("option");
    newOption.text = sdropdown_ids[nccode][i];
    sdropdown.appendChild(newOption);
  }
}
    // Auto select feature
    // $(document).ready(function(){
    //   $('[type="checkbox"]').each(function(){
    //     if ($(this).attr('value')==='100') {
    //       $(this).attr("checked","checked");
    //     }
    //   })
    // })