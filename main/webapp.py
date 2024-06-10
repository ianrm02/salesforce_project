import os
from os import listdir, path
from os.path import isfile, join
from flask import Flask, render_template, request, flash, url_for
from ClassifierApp import ClassifierApp
import config
import json

clfApp = ClassifierApp()

# create instance of flask
clfApp = ClassifierApp()
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'salesforcebutthesecondtime'

conf_threshold = 4

country_dropdown_ids = clfApp.clf.iso_standard_df["alpha-2"].to_list()
state_dropdown_ids = config.COUNTRY_WITH_REQUIRED_STATES_ALL_STATES


def search(formdata):
    if(not ('sdropdown_form' in formdata and 'cdropdown_form' in formdata)):
        return "Error: Missing required fields"
    search_address = formdata['addsearch']
    search_state = formdata['sdropdown_form']
    search_country = formdata['cdropdown_form']
    results = clfApp.db_handler.search_db((search_address, search_state, search_country))
    if(len(results) == 0):
        return
    return results

# connect URL endpoints
@app.route("/", methods=('GET', 'POST'))
def home():
    # If the user has submitted db info
    if(request.method == 'POST'):
        dbname = request.form['dbname']
        username = request.form['username']
        password = request.form['password']
        host = request.form['host']
        if not (dbname and username and password and host):
            flash('Please fill out all fields')
        else:
            clfApp.load_db_from_payload((dbname, username, password, host))

    clfApp.run()

    return render_template('home.html')


@app.route("/country_approve", methods=('GET', 'POST')) # define path component
def country_approve():
    search_response = None
    if(request.method == 'POST'):
        search_response = search(request.form)
        if(isinstance(search_response, str)):
            flash(search_response)
        flash(search_response)
    

    #TODO loading screen to show it's in processing
    country_changes = [item for item in clfApp.db_handler.get_all_from_table("CountryChanges")]
    country_changes.sort(key=lambda x: x[3])
    country_changes.reverse()

    print(country_changes)

    #Sorted by confidence
    #Each address has [OldCo] [NewCo] [Freq] [Conf]

    affected_ccodes = list(set([code[2] for code in country_changes]))
    affected_ccodes.sort()

    country_change_ids = [['C'] + code[1:] for code in country_changes]

    return render_template('country_skeleton.html', conf_threshold = conf_threshold, aff_country_codes = affected_ccodes, cdropdown_ids = json.dumps(country_dropdown_ids), change_ids = json.dumps(country_change_ids), sdropdown_ids = json.dumps(state_dropdown_ids), search_response = search_response)


@app.route("/state_approve")
def state_approve():
    fetchresults = clfApp.db_handler.get_all_from_table("StateChanges")

    state_changes = [item for item in clfApp.db_handler.get_all_from_table("StateChanges")]
    state_changes.sort(key=lambda x: x[5]) 
    state_changes.reverse() #highest to lowest confidence

    #Each address has [ID] [NewCo] [OldSt] [NewSt] [Freq] [Conf]

    state_change_ids = list()

    #state_change_id format for the render_template() must be S, OldS, newS, freq, conf, newC

    for change in state_changes:
        change[3] = change[3].strip()
        state_change_ids.append(['S', change[2], change[3], change[4], change[5], change[1]])

    affected_ccodes = list(set([item[5] for item in state_change_ids]))
    affected_scodes = {country: [] for country in affected_ccodes}

    for item in state_change_ids: #for each change 
        if item[2] not in affected_scodes[item[5]]: #if current state isnt represented yet in its country bucket
            affected_scodes[item[5]].append(item[2]) #append the state to the country bucket

    for country, states in affected_scodes.items():
        tmp_states = sorted(states)
        affected_scodes[country] = tmp_states

    return render_template('state_skeleton.html', conf_threshold = conf_threshold, aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = json.dumps(country_dropdown_ids), sdropdown_ids = json.dumps(state_dropdown_ids), change_ids = json.dumps(state_change_ids))


@app.route("/address_approve")
def address_approve():
    #address_changes = [item for item in clfApp.db_handler.get_all_from_table("AddressChanges")]
    #address_changes.sort(key=lambda x: x[3])
    #Sorted by confidence

    #TODO logic to get from changes to the format needed bby the render_template()

    #affected_ccodes = list(set([code[1] for code in address_changes]))
    #affected_scodes = list(set([code[1] for code in address_changes]))

    affected_ccodes = []
    affected_scodes = []

    return render_template('address_skeleton.html', aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = config.COUNTRY_WITH_REQUIRED_STATES_ALL_STATES, cstate_ids = config.COUNTRY_WITH_REQUIRED_STATES_ALL_STATES, address_info = address_batch)


@app.route("/statistics")
def statistics():
    return render_template('statistics.html')


@app.route("/end")
def end():
    return render_template('endscreen.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


