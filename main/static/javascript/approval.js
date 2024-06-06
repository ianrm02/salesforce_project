var sdropdown_ids = { "US": ["TX", "DE"], "AR": ["ER"] };
var jQueryScript = document.createElement('script');
jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/');
document.head.appendChild(jQueryScript);
activateAccordions();
checkApproved();
displayRows();
displayNotif();

// Allows accordions to actually extend and function
function activateAccordions() {
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
  window.location.href = "/" + next_page;
}
// Repopulates state dropdowns to match country selection
function repopulate_statedropdown(ccode, fieldstring) {
  // Find matching dropdown using accordion country code and the associated string in the row
  var cdropdown = document.getElementById("cdropdown" + ccode + fieldstring);
  var nccode = cdropdown.options[cdropdown.selectedIndex].text; // The newly selected code
  var sdropdown = document.getElementById("sdropdown" + ccode + fieldstring);
  // Clear dropdown
  while (sdropdown.options.length > 0) {
    sdropdown.remove(0);
  }
  // Mark as empty if there are no associated states
  if (!(nccode in sdropdown_ids)) {
    var emptyoption = document.createElement("option");
    emptyoption.text = "No states available";
    sdropdown.appendChild(emptyoption);
    return;
  }
  // Repopulate with new options matching new states
  for (var i = 0; i < sdropdown_ids[nccode].length; i++) {
    var newOption = document.createElement("option");
    newOption.text = sdropdown_ids[nccode][i];
    sdropdown.appendChild(newOption);
  }
}

// Allows for "Approve All" feature called by upper checkbox
// Should only apply to all in the accordion(matching country code in the tag)
function selectAll(code) {
  //Auto select feature
  var newCheckVal = document.getElementById("approveall" + code).checked;
  var checks = document.getElementsByName("check" + code);

  for (var i = 0; i < checks.length; i++) {
    checks[i].checked = newCheckVal;
  }
}

// Check approve all button if all checkmarks in table approved
function checkApproved() {
  var tables = document.getElementsByTagName("table");

  for (var i = 0; i < tables.length; i++) {
    var approveAllButton = document.getElementById("approveall" + tables[i].id);
    var checks = document.getElementsByName("check" + tables[i].id);
    var setChecked = true;

    for (var j = 0; j < checks.length; j++) {
      if (!(checks[j].checked)) {
        setChecked = false;
        break;
      }
    }

    approveAllButton.checked = setChecked;
  }
}

// Display notification if not all addresses approved
function displayNotif() {
  var tables = document.getElementsByTagName("table");
  var approveAllList = document.getElementsByClassName("approveall");
  var notifs = document.getElementsByClassName("notification");
  var displayNotif = "none";

  for (var i = 0; i < tables.length; i++) {
    var tab = document.getElementById("tab" + tables[i].id);
    var highlightTab = "";

    if (!(approveAllList[i].checked)) {
      displayNotif = "block";
      highlightTab = "#f24e6c";
    } 
    tab.style.backgroundColor = highlightTab;
  }

  for (var i = 0; i < notifs.length; i++) {
    notifs[i].style.display = displayNotif;
  }
}

// Let user click button if all addresses are approved
function enableButton() {
  var allCheckedList = document.getElementsByClassName("approveall");
  var nextButton = document.getElementById("nextPage");
  var numChecked = 0;

  for (var i = 0; i < allCheckedList.length; i++) {
    if (allCheckedList[i].checked) {
      numChecked++;
      if (numChecked == allCheckedList.length) {
        nextButton.disabled = false;
      }
    } else {
      numChecked--;
      if (numChecked != allCheckedList.length) {
        nextButton.disabled = true;
      }
    }
  }
}

// Display number of items in each table
function displayRows() {
  var tables = document.getElementsByTagName("table");
  
  for (var i = 0; i < tables.length; i++) {
    document.getElementById("itemNum" + tables[i].id).textContent = "Items: " + tables[i].rows.length;
  }
}

// Open and close import settings form
function openForm() {
  document.getElementById("settingsForm").style.display = "block";
}

function closeForm() {
  document.getElementById("settingsForm").style.display = "none";
}