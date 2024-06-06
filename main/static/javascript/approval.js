// Initialize JQuery
// var jQueryScript = document.createElement('script');
// jQueryScript.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/');
// document.head.appendChild(jQueryScript);

// Data from jinja
var cdropdown_ids = null;
var sdropdown_id_map = null;
var change_ids = null;
var conf_threshold = 90;

// Page elements
var emptyStateDropdown = null;

initOnPageLoad();
// initialize variables and call page load
function initOnPageLoad(){
  this.change_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('data-change_ids'));
  this.cdropdown_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('data-cdropdown_ids'));
  //this.sdropdown_id_map = sdropdown_ids;

  // Init additional page elements
  emptyStateDropdown = document.createElement("select");
  var emptyoption = document.createElement("option");
  emptyoption.text = "No states available";
  emptyStateDropdown.appendChild(emptyoption);

  activateAccordions();
  fillAllAccordions();
  checkApproved();
  displayRows();
  displayNotif();
}
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
//id type | statechangeid | newcountry |   oldstate    | newstate | occurrences | confidence
//id type | countrychangeid |   oldcountry   | newcountry | occurrences | confidence
function fillAllAccordions(isCountry){
  // Initialize country dropdown (only needed on page load)
  var cdropdown = document.createElement("select");
  for(var i = 0; i < cdropdown_ids.length; i++){
    var opt = document.createElement("option");
    opt.text = cdropdown_ids[i];
    cdropdown.appendChild(opt)
  }
  var countryCode, stateCode, tableId, oldField, occurrences, confidence;
  // Fill accordions
  for(var i = 0; i < change_ids.length; i++){
    change_id = change_ids[i]; // Get current id
    if(change_id[0] == 'S'){
      countryCode = change_id[2];
      stateCode = change_id[4];
      tableId =  stateCode + countryCode; // id to find the table element
      oldField = change_id[3]; // Original field found in the db
      occurrences = change_id[5]; // Number of occurrences
      confidence = change_id[6]; // Conversion confidence
    }
    else if(change_id[0] == 'C'){
      countryCode = change_id[2];
      tableId = countryCode;
      oldField = change_id[1];
      occurrences = change_id[3];
      confidence = change_id[4];
    }
    var curTable = document.getElementById(tableId);
    if(curTable == null){
      document.write(tableId);
    }
    // Create and fill row for current change id
    var newRow = curTable.insertRow();
    var newCell = newRow.insertCell();
    newCell.innerText = oldField;
    newCell = newRow.insertCell();
    newCell.innerText = occurrences; 
    newCell = newRow.insertCell();
    newCell.innerText = confidence;
    newCell = newRow.insertCell();
    // Make checkbox
    //onchange="checkApproved(); enableButton(); displayNotif()"
    var checkbox = document.createElement("INPUT");
    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("id", "checkbox"+countryCode+oldField);
    checkbox.setAttribute("onchange", "checkApproved(); enableButton(); displayNotif()");
    // Autoselect entries above the confidence threshold
    if(confidence >= conf_threshold){
      checkbox.checked = true;
    }
    newCell.appendChild(checkbox);
    // Create country dropdown
    newCell = newRow.insertCell();
    var curcdropdown = cdropdown.cloneNode(true);
    curcdropdown.setAttribute("id", "cdropdown" + countryCode + oldField);
    curcdropdown.selectedIndex = cdropdown_ids.indexOf(countryCode);
    newCell.appendChild(curcdropdown);
    // Create state dropdown
    if(change_id[0] == 'S'){
      // If no states are available
      if(!(countryCode in sdropdown_id_map)){
        newCell.appendChild(emptyStateDropdown);
      }
      // Create and populate state dropdown
      else{
        var sdropdown = document.createElement("select");
        for(var i = 0; i < sdropdown_id_map[countryCode].length; i++){
          var newOption = document.createElement("option");
          newOption.text = sdropdown_id_map[countryCode][i];
          sdropdown.appendChild(newOption);
        }
        sdropdown.selectedIndex = sdropdown_id_map[countryCode].findIndex(stateCode); // Make selected state code match accordion title code
        newCell.appendChild(sdropdown);
      }
    }

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
  if(!(nccode in sdropdown_id_map)){
    var emptyoption = document.createElement("option");
    emptyoption.text = "No states available";
    sdropdown.appendChild(emptyoption);
    return;
  }
  // Repopulate with new options matching new states
  for(var i = 0; i < sdropdown_id_map[nccode].length; i++){
    var newOption = document.createElement("option");
    newOption.text = sdropdown_id_map[nccode][i];
    sdropdown.appendChild(newOption);
  }
}

// Allows for "Approve All" feature called by upper checkbox
// Should only apply to all in the accordion(matching country code in the tag)
function selectAll(ccode){
  //Auto select feature
  var newCheckVal = document.getElementById("approveall"+ccode).checked;
  var checks = document.getElementsByTagName("check"+ccode);
  for(var i = 0; i < checks.length; i++){
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
    document.getElementById("itemNum" + tables[i].id).textContent = "Items: " + (tables[i].rows.length-1);
  }
}

// Open and close import settings form
function openForm() {
  document.getElementById("settingsForm").style.display = "block";
}

function closeForm() {
  document.getElementById("settingsForm").style.display = "none";
}
