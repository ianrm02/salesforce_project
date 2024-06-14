// Data from jinja
var cdropdown_ids = null;
var sdropdown_id_map = null;
var change_ids = null;
var conf_threshold = 4;

// Common page elements
var emptyStateDropdown = null;
var emptyAccordion = null;
var emptyAccPanel = null;
var cdropdown = null;

// Address Page elements
var clusterTable = null;
var clusterIndex = 0;
var clusterText = null;

if(window.location.pathname == "/address_approve"){
  initCommonElements();
  initAddressPage();
}
else if(window.location.pathname == "/country_approve" || window.location.pathname == "/state_approve"){
  initCommonElements();
  initOnPageLoad();
}

function initCommonElements(){
  // Data from Jinja(from flask)
  this.cdropdown_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('cdropdown_ids'));
  this.sdropdown_id_map = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('sdropdown_ids'));
  // State dropdown for countries with none listed
  emptyStateDropdown = document.createElement("select");
  var emptyoption = document.createElement("option");
  emptyoption.text = "No states available";
  emptyoption.disabled = true;
  emptyStateDropdown.appendChild(emptyoption);
  emptyStateDropdown.setAttribute("id", "defaultempty");
  // Country dropdown
  cdropdown = document.createElement("select");
  for (var i = 0; i < cdropdown_ids.length; i++) {
    var opt = document.createElement("option");
    opt.text = cdropdown_ids[i];
    cdropdown.appendChild(opt);
  }
}

function initAddressPage(){
  clusters = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('clusters'));
  // Init additional page elements
  emptyAccordion = (document.getElementById("tabCluster")).cloneNode(true); 
  emptyAccPanel = (document.getElementById("panelCluster")).cloneNode(true);;
  clusterText = document.getElementById("clusterText");
  clusterTable = document.getElementById("clusterTable");
  // Fill first two rows (label and affect all)
  var row = clusterTable.insertRow();
  var newCell = row.insertCell();
  newCell.innerText = "Address Field";
  newCell = row.insertCell();
  newCell.innerText = "Custom";
  row = clusterTable.insertRow();
  newCell = row.insertCell();
  newCell.innerText = "Affect all remaining";
  newCell = row.insertCell();
  // Create state dropdown
  sdropdown = emptyStateDropdown.cloneNode(true);
  sdropdown.setAttribute("id", "sdropdownAll");
  sdropdown.onchange = function() {clusterAffectAll();}
  newCell.appendChild(sdropdown);

  // Create Country dropdown
  var curcdropdown = cdropdown.cloneNode(true);
  curcdropdown.onchange = function () { repopulate_statedropdown(this.attributes["id"].value);};
  curcdropdown.setAttribute("id", "cdropdownAll");
  newCell.appendChild(curcdropdown);
  //Activate cluster accordion and load first cluster
  document.getElementById("tabCluster").addEventListener("click", function () {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
  loadCluster();
}

// initialize variables and call page load
function initOnPageLoad() {
  this.change_ids = JSON.parse(document.head.querySelector('meta[name="init_data"]').getAttribute('change_ids'));
  // Call init methods
  activateAccordions();
  fillAllAccordions();
  displayRecords();
  displayNotif();
  enableButton();
}

// Allows accordions to actually extend and function
function activateAccordions() {
  var acc = document.getElementsByClassName("accordion");
  // Store copy of empty accordion to make new ones later (AVOID COUNTRY ACC ON STATE PAGE)
  emptyAccordion = acc[1].cloneNode(true); 
  emptyAccPanel = (document.getElementsByClassName("panel")[1]).cloneNode(true);;
  // Activate all accordions
  for (var i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
      this.classList.toggle("active");
      var panel = this.nextElementSibling;
      if (panel.style.display === "block") {
        panel.style.display = "none";
      } else {
        panel.style.display = "block";
      }
    });
  }
}
// Populate all accordions with rows and values
function fillAllAccordions(isCountry) {
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
    // Field cell
    var newCell = newRow.insertCell();
    newCell.innerText = oldField;
    newCell.name = tableId;
    newCell.ondblclick = function(){ fillSearchBar(this.innerText)};
    // Occurrences cell
    newCell = newRow.insertCell();
    newCell.innerText = occurrences;
    // Confidence cell
    newCell = newRow.insertCell();
    newCell.innerText = confidence;
    // Checkbox cell
    newCell = newRow.insertCell();
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
  var nccode = cdropdown.options[cdropdown.selectedIndex].value; // The newly selected code
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
    if(curid == "search_results_table"){ // May be null at this time
      continue;
    }
    var tab = document.getElementById("tab" + curid);
    var highlightTab = "#0d9dda";
    // Update visuals if not all checked
    if (!(approveAllList[i].checked)) {
      displayNotif = "block";
      highlightTab = "";
      var countryCode = curid.substring(curid.length-2);
      if(countryCode == "ne"){ // Handle None case. Needs better solution
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

// Let user click next page button if all addresses are approved (admin next page bypasses this)
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

// Display number of records in each table
function displayRecords() {
  var tables = document.getElementsByTagName("table");
  var col = 1; // Occurrences column

  for (var i = 0; i < tables.length; i++) {
    var sum = 0;
    if (tables[i].id == "search_results_table") { // May be null at this time
      continue;
    }
    
    for (var row = 1; row < tables[i].rows.length; row++) {
      
      if (tables[i].rows[row].cells.length > col) {
        sum += parseInt(tables[i].rows[row].cells[col].innerText);
      }
    }
    // Update records display
    document.getElementById("itemNum" + tables[i].id).textContent = "Records: " + sum;
  }
}

// Open and close import settings form
function openForm(id) {
  document.getElementById(id).style.display = "block";

}
function closeForm(id) {
  document.getElementById(id).style.display = "none";
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

// Dummy function for user settings upload
function uploadSettings() {
  alert("File uploaded");
  // please implement settings reading here
}

// Autofill correct search bar on double click of field
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

// Moves row from one table to another
// Will create and delete accordions/tables as needed
function moveToTable(callingDropdown){
  countryCode = "";
  stateCode = "";
  // Handle retrieval based on page format
  if(document.location.pathname == "/country_approve"){
    countryCode = callingDropdown[callingDropdown.selectedIndex].value;
  }
  else if(document.location.pathname == "/state_approve"){
    cdrop = document.getElementById("c" + callingDropdown.id.substring(1));
    countryCode = cdrop[cdrop.selectedIndex].value;
    stateCode = callingDropdown[callingDropdown.selectedIndex].value;
  }
  // Clone row and delete from current table
  tableId = stateCode + countryCode;
  var oldTable = callingDropdown.closest("table");
  var row = callingDropdown.closest("tr");
  var nrow = row.cloneNode(true);
  row.innerHTML = "";
  row.remove();
  // Delete table if empty
  if(oldTable.querySelectorAll("tr").length == 1){
    var oldAcc = (oldTable.closest("div")).previousElementSibling;
    oldAcc.innerHTML = "";
    oldAcc.remove();
    oldTable = oldTable.closest("div");
    oldTable.innerHTML = "";
    oldTable.remove();
    
  }
  // Update all row values
  var fieldBox = nrow.querySelector("td");
  fieldBox.name = tableId;
  fieldBox.ondblclick = function(){ fillSearchBar(this.innerText)};
  var checkbox = nrow.querySelector("input");
  checkbox.setAttribute("id", "check" + tableId + fieldBox.innerText);
  checkbox.setAttribute("class", "check" + tableId);
  checkbox.onclick = function () { checkApproved(this.attributes["class"].value); enableButton(); displayNotif(); };
  // Country dropdown handling
  var dropdownList = nrow.querySelectorAll("select");
  var cdropdown = null;
  if (dropdownList.length == 2) {// State handling
    cdropdown = dropdownList[1];
    cdropdown.onchange = function () { repopulate_statedropdown(this.attributes["id"].value);};

    var sdropdown = dropdownList[0];
    // If no states are available
    if (!(countryCode in sdropdown_id_map)) {
      sdropdown = emptyStateDropdown.cloneNode(true);
      sdropdown.setAttribute("id", "sdropdown" + tableId + fieldBox.innerText);
    }
    // Create and populate state dropdown
    else {
      sdropdown = document.createElement("select");
      sdropdown.setAttribute("id", "sdropdown" + tableId + fieldBox.innerText);
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
  }
  else{
    cdropdown = dropdownList[0];
    cdropdown.onchange = function() { moveToTable(this); }
  }
  cdropdown.setAttribute("id", "cdropdown" + tableId + fieldBox.innerText);
  cdropdown.selectedIndex = cdropdown_ids.indexOf(countryCode);
  cdropdown.setAttribute("data-countrytable", countryCode);

  var ntable = document.getElementById(tableId);
  // If the accordion isn't made yet
  if(ntable == null){
    // Find/make country accordion and retrieve table
    var countryAcc = document.getElementById("tab" + countryCode);
    if(countryAcc == null){
      countryAcc = createAccordion(countryCode, countryCode, "accordiongroup");
    }
    ntable = (countryAcc.nextElementSibling).querySelector("table");
    // Make state accordion if applicable, country acc no longer needs table
    if(stateCode != ""){
      ntable.innerHTML = "";
      ntable.remove();
      stateAcc = createAccordion(tableId, stateCode, "panel" + countryCode);
      ntable = (stateAcc.nextElementSibling).querySelector("table");
    }
  }
  // Add and update visuals
  ntable.append(nrow);
  checkApproved("check" + tableId);
  displayRecords();
  displayNotif();
}

function insertAccordion(parentId, currentId, insAcc, insPanel){
  var parentObj = document.getElementById(parentId);
  var found = false;
  // Find spot alphabetically
  for(var i = 0; i < parentObj.childNodes.length; i++){
    if(parentObj.childNodes[i].id > "tab" + currentId){
      parentObj.insertBefore(insPanel, parentObj.childNodes[i]);
      parentObj.insertBefore(insAcc, insPanel);
      found = true;
      break;
    }
  }
  // Append if alphabetically at the end
  if(!found){
    parentObj.append(insAcc);
    parentObj.append(insPanel);
  }
}

function createAccordion(accId, accTitle, parentId){
  // Clone empty and adjust all ids/title
  newAcc = emptyAccordion.cloneNode(true);
  newAcc.id = "tab" + accId;
  newAccText = newAcc.childNodes[0];
  newAccText.textContent = accTitle;
  
  // Update panel ids and functions
  newAccPanel = emptyAccPanel.cloneNode(true);
  newAccPanel.id = "panel" + accId;
  var insTable = newAccPanel.querySelector("table");
  insTable.id = accId;
  if(window.location.pathname != "/address_approve"){
    newAccSpan = newAcc.querySelector('span');
    newAccSpan.id = "itemNum" + accId;
    var checkbox = insTable.querySelector("input");
    checkbox.id = "approveall" + accId;
    checkbox.onclick = function(){
      selectAll(this.id.substring(10));
      enableButton();
      displayNotif();
    }
  }
  
  // Activate accordion
  newAcc.addEventListener("click", function () {
    this.classList.toggle("active");
    var panel = this.nextElementSibling
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
  // Insert into page and pass back for table population
  insertAccordion(parentId, accId, newAcc, newAccPanel);
  return newAcc;
}

// Display current cluster to the user
function loadCluster(){
  clusterText.innerText = clusters.length - clusterIndex + " groups remaining";
  if(clusters.length-clusterIndex == 0){
    return;
  }
  for(var x = 0; x < clusters[clusterIndex].length; x++){
    row = clusterTable.insertRow();
    newCell = row.insertCell();
    newCell.innerText = clusters[clusterIndex][x];
    newCell = row.insertCell();

    // Create state dropdown
    sdropdown = emptyStateDropdown.cloneNode(true);
    sdropdown.setAttribute("id", "sdropdown" + clusters[clusterIndex][x]);
    sdropdown.onchange = function(){addressMoveToTable(this);}
    newCell.appendChild(sdropdown);
  
    // Create Country dropdown
    var curcdropdown = cdropdown.cloneNode(true);
    curcdropdown.onchange = function () { repopulate_statedropdown(this.attributes["id"].value);};
    curcdropdown.setAttribute("id", "cdropdown" + clusters[clusterIndex][x]);
    newCell.appendChild(curcdropdown);
  }
}
// Update all remaining values in current cluster table based on user input
function clusterAffectAll(){
  var rows = clusterTable.querySelectorAll("tr");
  // Extract selected dropdown values
  var dropdown = document.getElementById("sdropdownAll");
  var stateCode = dropdown[dropdown.selectedIndex].value;
  dropdown = document.getElementById("cdropdownAll");
  var countryCode = dropdown[dropdown.selectedIndex].value;

  for(var i = 2; i < rows.length; i++){
    var currentRow = rows[i];
    var dropCell = currentRow.childNodes[1];
    var dropdownList = dropCell.querySelectorAll("select");
    addressMoveToTable(dropdownList[0], stateCode, countryCode);
  }
  clusterIndex++;
  loadCluster();
}
// Handles moving on address page because of reduced item set
function addressMoveToTable(callingDropdown, stateCode, countryCode){
  var nrow = callingDropdown.closest("tr");
  var cell = callingDropdown.closest("td");
  var dropdownList = cell.querySelectorAll("select");
  if(stateCode == null){
    var stateCode = dropdownList[0][dropdownList[0].selectedIndex].value;
    var countryCode = dropdownList[1][dropdownList[1].selectedIndex].value;
  }
  else{
    dropdownList[1].selectedIndex = cdropdown_ids.indexOf(countryCode);
  }
  tableId = stateCode+countryCode;

  var ntable = document.getElementById(tableId);
  // If the accordion isn't made yet
  if(ntable == null){
    // Find/make country accordion and retrieve table
    var countryAcc = document.getElementById("tab" + countryCode);
    if(countryAcc == null){
      countryAcc = createAccordion(countryCode, countryCode, "accordiongroup");
    }
    ntable = (countryAcc.nextElementSibling).querySelector("table");
    // Make state accordion if applicable, country acc no longer needs table
    if(stateCode != ""){
      ntable.innerHTML = "";
      ntable.remove();
      stateAcc = createAccordion(tableId, stateCode, "panel" + countryCode);
      ntable = (stateAcc.nextElementSibling).querySelector("table");
    }
  }
  ntable.append(nrow);
  repopulate_statedropdown(dropdownList[1].id);
  if(stateCode == null){
    dropdownList[0].selectedIndex = sdropdown_id_map[countryCode].indexOf(stateCode);
  }
  if(clusterTable.querySelectorAll("tr").length == 2 && clusterIndex < clusters.length){
    clusterIndex++;
    loadCluster();
  }
}