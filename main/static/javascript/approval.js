
var sdropdown_ids = {"US":["TX", "DE"], "AR":["ER"]};
var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/');
document.head.appendChild(jQueryScript);
activateAccordions();

// Allows accordions to actually extend and function
function activateAccordions(){
  var acc = document.getElementsByClassName("accordion");
  for (var i = 0; i < acc.length; i++) {
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
}

// Takes input for the next page and makes the url. We don't have pages sorted into folders so using the root(/) allow us to make the url work
// More complex webapp would need to utilize url_for or something similar
function redirect(next_page) {
  window.location.href = "/"+next_page;
}
// Repopulates state dropdowns to match country selection
function repopulate_statedropdown(ccode, fieldstring){
  // Find matching dropdown using accordion country code and the associated string in the row
  var cdropdown = document.getElementById("cdropdown" + ccode + fieldstring);
  var nccode = cdropdown.options[cdropdown.selectedIndex].text; // The newly selected code
  var sdropdown = document.getElementById("sdropdown" + ccode + fieldstring);
  // Clear dropdown
  while(sdropdown.options.length > 0){
    sdropdown.remove(0);
  }
  // Mark as empty if there are no associated states
  if(!(nccode in sdropdown_ids)){
    var emptyoption = document.createElement("option");
    emptyoption.text = "No states available";
    sdropdown.appendChild(emptyoption);
    return;
  }
  // Repopulate with new options matching new states
  for(var i = 0; i < sdropdown_ids[nccode].length; i++){
    var newOption = document.createElement("option");
    newOption.text = sdropdown_ids[nccode][i];
    sdropdown.appendChild(newOption);
  }
}

// Allows for "Approve All" feature called by upper checkbox
// Should only apply to all in the accordion(matching country code in the tag)
function selectAll(ccode){
  //Auto select feature
  var newCheckVal = document.getElementById("approveall"+ccode).checked;
  var checks = document.getElementsByName("check"+ccode);

  for(var i = 0; i < checks.length; i++){
    checks[i].checked = newCheckVal;
  }
}

// function checkApproved(){
//   var tables = document.getElementsByTagName("approveall"+ccode).checked;
//   var checks = document.getElementsByName("check"+ccode);

//   for(var i = 0; i < checks.length; i++){
//     checks[i].checked = newCheckVal;
//   }
// }