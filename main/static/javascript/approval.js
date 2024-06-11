// Data from jinja
var cdropdown_ids = null;
var sdropdown_id_map = null;
var change_ids = null;
var conf_threshold = 4;

// Page elements
var emptyStateDropdown = null;

if(window.location.pathname == "/address_approve"){
  initAddressPage();
}
else{
  initOnPageLoad();
}

function initAddressPage(){
  clusters = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('clusters'));
  this.cdropdown_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('cdropdown_ids'));
  this.sdropdown_id_map = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('sdropdown_ids'));
  // Init additional page elements
  var addTable = document.getElementById("addtable");

  emptyStateDropdown = document.createElement("select");
  var emptyoption = document.createElement("option");
  emptyoption.text = "No states available";
  emptyStateDropdown.appendChild(emptyoption);
  emptyStateDropdown.setAttribute("id", "defaultempty");

  var cdropdown = document.createElement("select");
  for (var i = 0; i < cdropdown_ids.length; i++) {
    var opt = document.createElement("option");
    opt.text = cdropdown_ids[i];
    cdropdown.appendChild(opt);
  }
  for(var i = 0; i < clusters.length; i++){
    var curTable = document.createElement("table");
    var row = curTable.insertRow();
    var newCell = row.insertCell();
    newCell.innerText = "Address Field";
    newCell = row.insertCell();
    newCell.innerText = "Custom";
    for(var x = 0; x < clusters[i].length; x++){
      row = curTable.insertRow();
      newCell = row.insertCell();
      newCell.innerText = clusters[i][x];
      newCell = row.insertCell();

      var sdropdown = null;
      // If no states are available
      var dupEmpty = emptyStateDropdown.cloneNode(true);
      dupEmpty.setAttribute("id", "sdropdown" + clusters[i][x]);
      sdropdown = dupEmpty;
      newCell.appendChild(sdropdown);
    
      // Create Country dropdown
      var curcdropdown = cdropdown.cloneNode(true);
      curcdropdown.onchange = function () { repopulate_statedropdown(this.attributes["id"].value);};
      curcdropdown.setAttribute("id", "cdropdown" + clusters[i][x]);
      newCell.appendChild(curcdropdown);
    }
    addTable.appendChild(curTable);
  }
}

// initialize variables and call page load
function initOnPageLoad() {
  var fileName = location.href.split("/").slice(-1);

  this.change_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('change_ids'));
  this.cdropdown_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('cdropdown_ids'));
  this.sdropdown_id_map = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('sdropdown_ids'));

  // Init additional page elements
  emptyStateDropdown = document.createElement("select");
  var emptyoption = document.createElement("option");
  emptyoption.text = "No states available";
  emptyStateDropdown.appendChild(emptyoption);
  emptyStateDropdown.setAttribute("id", "defaultempty");

  activateAccordions();
  fillAllAccordions();
  
  displayRows();
  displayNotif();
  enableButton();
}

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
//id type | statechangeid | newcountry |   oldstate    | newstate | occurrences | confidence
//id type | countrychangeid |   oldcountry   | newcountry | occurrences | confidence
function fillAllAccordions(isCountry) {
  // Initialize country dropdown (only needed on page load)
  var cdropdown = document.createElement("select");
  for (var i = 0; i < cdropdown_ids.length; i++) {
    var opt = document.createElement("option");
    opt.text = cdropdown_ids[i];
    cdropdown.appendChild(opt)
  }
  var countryCode, stateCode, tableId, oldField, occurrences, confidence;
  // Fill accordions
  for (var i = 0; i < change_ids.length; i++) {
    change_id = change_ids[i]; // Get current id
    // change_id format may differ based on country or state
    if (change_id[0] == 'S') { // State
      countryCode = change_id[5];
      if (countryCode == null) {
        countryCode = "None";
      }
      stateCode = change_id[2];
      tableId = stateCode + countryCode; // id to find the table element
      oldField = change_id[1]; // Original field found in the db
      occurrences = change_id[3]; // Number of occurrences
      confidence = change_id[4]; // Conversion confidence
    }
    else if (change_id[0] == 'C') { // Country
      countryCode = change_id[2];
      tableId = countryCode;
      oldField = change_id[1];
      occurrences = change_id[3];
      confidence = change_id[4];
    }
    var curTable = document.getElementById(tableId);
    // Create and fill row for current change id
    var newRow = curTable.insertRow();
    var newCell = newRow.insertCell();
    newCell.innerText = oldField;
    newCell.name = tableId;
    newCell.ondblclick = function(){ fillSearchBar(this.innerText)}
    newCell = newRow.insertCell();
    newCell.innerText = occurrences;
    newCell = newRow.insertCell();
    newCell.innerText = confidence;
    newCell = newRow.insertCell();
    // Make checkbox
    //onchange="checkApproved(); enableButton(); displayNotif()"
    var checkbox = document.createElement("INPUT");
    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("id", "check" + tableId + oldField);
    checkbox.setAttribute("class", "check" + tableId);
    checkbox.onclick = function () { checkApproved(this.attributes["class"].value); enableButton(); displayNotif(); };
    if(countryCode == "None"){
      checkbox.disabled = true;
    }
    // Autoselect entries above the confidence threshold(don't select ones with invalid country)
    if (confidence >= conf_threshold && countryCode != "None") {
      checkbox.checked = true;
    }
    newCell.appendChild(checkbox);

    // Create country dropdown
    newCell = newRow.insertCell();
    // Create state dropdown (populated based on country)
    if (change_id[0] == 'S') {
      var sdropdown = null;
      // If no states are available
      if (countryCode == "None" || !(countryCode in sdropdown_id_map)) {
        var dupEmpty = emptyStateDropdown.cloneNode(true);
        dupEmpty.setAttribute("id", "sdropdown" + tableId + oldField);
        sdropdown = dupEmpty;
      }
      // Create and populate state dropdown
      else {
        sdropdown = document.createElement("select");
        sdropdown.setAttribute("id", "sdropdown" + tableId + oldField)
        for (var x = 0; x < sdropdown_id_map[countryCode].length; x++) {
          var newOption = document.createElement("option");
          newOption.text = sdropdown_id_map[countryCode][x];
          sdropdown.appendChild(newOption);
        }
        sdropdown.selectedIndex = sdropdown_id_map[countryCode].indexOf(stateCode); // Make selected state code match accordion title code
      }
      sdropdown.setAttribute("data-state", stateCode);
      sdropdown.setAttribute("data-country", countryCode);
      sdropdown.onchange = function(){moveToTable(this)};
      newCell.appendChild(sdropdown);
    }
    // Create Country dropdown
    var curcdropdown = cdropdown.cloneNode(true);
    curcdropdown.setAttribute("id", "cdropdown" + tableId + oldField);
    curcdropdown.selectedIndex = cdropdown_ids.indexOf(countryCode);
    curcdropdown.setAttribute("data-countrytable", countryCode);
    if (change_id[0] == 'S') {
      curcdropdown.onchange = function () { repopulate_statedropdown(this.attributes["id"].value);};
    }
    else{
      curcdropdown.onchange = function() { moveToTable(this); }
    }
    newCell.appendChild(curcdropdown);

    checkApproved("check" + tableId);
  }
}

// Takes input for the next page and makes the url. We don't have pages sorted into folders so using the root(/) allow us to make the url work
// More complex webapp would need to utilize url_for or something similar
function redirect(next_page) {
  window.location.href = "/" + next_page;
}
// Repopulates state dropdowns to match country selection
function repopulate_statedropdown(dropId){
  // Remove "sdropdown"
  dropId = dropId.substring(9);
  // Find matching dropdown using accordion country code and the associated string in the row
  var cdropdown = document.getElementById("cdropdown" + dropId);
  var nccode = cdropdown.options[cdropdown.selectedIndex].text; // The newly selected code
  var sdropdown = document.getElementById("sdropdown" + dropId);
  // Clear dropdown
  while (sdropdown.options.length > 0) {
    sdropdown.remove(0);
  }
  // Mark as empty if there are no associated states
  if (!(nccode in sdropdown_id_map)) {
    var emptyoption = document.createElement("option");
    emptyoption.text = "No states available";
    emptyoption.disabled = true;
    sdropdown.appendChild(emptyoption);
    return;
  }
  // Repopulate with new options matching new states
  for (var i = 0; i < sdropdown_id_map[nccode].length; i++) {
    var newOption = document.createElement("option");
    newOption.text = sdropdown_id_map[nccode][i];
    sdropdown.appendChild(newOption);
  }
}

// Allows for "Approve All" feature called by upper checkbox
// Should only apply to all in the accordion(matching table id (ccode) or (ccode+scode))
function selectAll(tableId) {
  //Auto select feature
  var newCheckVal = document.getElementById("approveall" + tableId).checked;
  var checks = document.getElementsByClassName("check" + tableId);
  for (var i = 0; i < checks.length; i++) {
    checks[i].checked = newCheckVal;
  }
}

// Check approve all button if all checkmarks in current table approved
function checkApproved(tableId) {
  tableId = tableId.substring(5); //remove "check" from the id
  var approveAllButton = document.getElementById("approveall" + tableId);
  // Get all checkboxes from the same table
  var checks = document.getElementsByClassName("check" + tableId);
  var setChecked = true;
  for (var j = 0; j < checks.length; j++) {
    if (!(checks[j].checked)) {
      setChecked = false;
      break;
    }
  }
  approveAllButton.checked = setChecked;
}

// Display notification if not all addresses approved
function displayNotif() {
  var tables = document.getElementsByTagName("table");
  var approveAllList = document.getElementsByClassName("approveall");
  var notifs = document.getElementsByClassName("notification");
  var displayNotif = "none";

  for (var i = 0; i < tables.length; i++) {
    var curid = tables[i].id;
    if(curid == "search_results_table"){
      continue;
    }
    var tab = document.getElementById("tab" + curid);
    var highlightTab = "";

    if (!(approveAllList[i].checked)) {
      displayNotif = "block";
      highlightTab = "#f24e6c";
      var countryCode = curid.substring(curid.length-2);
      if(countryCode == "ne"){ // Handle None case. Need better solution
        countryCode = "None";
      }
      var parentAcc = document.getElementById("tab" + countryCode);
      parentAcc.style.backgroundColor = highlightTab;
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
  var allApproved = true;

  for (var i = 0; i < allCheckedList.length; i++) {
    if (!allCheckedList[i].checked) {
      allApproved = false;
      break;
    }
  }
  nextButton.disabled = !allApproved;
}

// Display number of items in each table
function displayRows() {
  var tables = document.getElementsByTagName("table");

  for (var i = 0; i < tables.length; i++) {
    if(tables[i].id == "search_results_table"){ // May not exist at this time
      continue;
    }
    document.getElementById("itemNum" + tables[i].id).textContent = "Items: " + (tables[i].rows.length - 1);
  }
}

// Open and close import settings form
function openForm() {
  document.getElementById("settingsForm").style.display = "block";

}

function closeForm() {
  document.getElementById("settingsForm").style.display = "none";
}

// Download text file after export clicked
function exportSettings(file) {
  var exportFile = document.createElement('a');
  var text = "Settings exported"; // change this to get the changed dropdown values
  exportFile.setAttribute('href', 'data:text/plain;charset=utf-8, ' + encodeURIComponent(text));
  exportFile.setAttribute('download', file);
  document.body.appendChild(exportFile);
  exportFile.click();
  document.body.removeChild(exportFile);
}

function uploadSettings() {
  alert("File uploaded");
  // please implement settings reading here
}

function fillSearchBar(text){
  var searchBar;
  if(window.location.pathname == "/address_approve"){
    searchBar = document.getElementById("addsearch");
  }
  else if(window.location.pathname == "/state_approve"){
    searchBar = document.getElementById("statesearch");
  }
  else if(window.location.pathname == "/country_approve"){
    searchBar = document.getElementById("countrysearch");
  }
  searchBar.value = text;
}

function moveToTable(cell){
  // Should change this system to be based on custom attributes
  countryCode = "";
  stateCode = "";
  if(document.location.pathname == "/country_approve"){
    countryCode = cell[cell.selectedIndex].value;
  }
  else if(document.location.pathname == "/state_approve"){
    cdrop = document.getElementById("c" + cell.id.substring(1));
    countryCode = cdrop[cdrop.selectedIndex].value;
    stateCode = cell[cell.selectedIndex].value;
  }
  tableId = stateCode + countryCode;
  var row = cell.closest("tr");
  var nrow = row.cloneNode(true);
  row.remove();
  var ntable = document.getElementById(tableId);
  ntable.append(nrow);
}