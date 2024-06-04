import os
from os import listdir, path
from os.path import isfile, join
from flask import Flask, render_template, request, flash, url_for
from ClassifierApp import ClassifierApp
import config
import common_state_alternates

# create instance of flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'salesforcebutthesecondtime'
clfApp = ClassifierApp()

conf_threshold = 90

country_dropdown_ids = clfApp.clf.iso_standard_df["alpha-2"]
state_dropdown_ids = {'AR':['ER'], 'US':['CO', 'DE', 'TX']} #TODO

address_batch = [['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '12 ARROZ CT', 80], ['US', 'CO', '4 Littleton Dr', 12], ['US', 'CO', '400 Colo St.', 20], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', '123 Arentin Ln.', 50], ['AR', 'ER', 'DO NOT DISPLAY', 50]]
# LIST MUST BE SORTED BY CONFIDENCE BEFORE PASSED TO PAGE

# 0=Type 1=New 2=Occurences 3=Confidence
# Change Type: C|A|S
change_ids = [['C', 'Arroz', 'AR', 1200, 10], ['C', 'ArGE', 'AR', 30, 10], ['C', 'United States', 'US', 100000, 100], ['S', 'Colorado', 'CO', 10000, 100, 'US'], ['S', 'Entree Reo', 'ER', 12500, 80, 'AR'], ['S', 'Entre Rios', 'ER', 10000, 100, 'AR']]

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

    return render_template('home.html')


@app.route("/country_approve") # define path component
def country_approve():
    #TODO loading screen to show it's in processing
    country_changes = [item for item in clfApp.db_handler.get_all_from_table("CountryChanges")]
    country_changes.sort(key=lambda x: x[3])
    country_changes.reverse()

    print(country_changes)


    #Sorted by confidence
    #Each address has [OldCo] [NewCo] [Freq] [Conf]

    affected_ccodes = list(set([code[1] for code in country_changes]))
    affected_ccodes.sort()

    print(affected_ccodes)

    country_change_ids = [['C'] + code for code in country_changes]

    return render_template('country_skeleton.html', conf_threshold = conf_threshold, aff_country_codes = affected_ccodes, dropdown_ids = country_dropdown_ids, change_ids = country_change_ids)


@app.route("/state_approve")
def state_approve():
    fetchresults = clfApp.db_handler.get_all_from_table("StateChanges")

    for res in fetchresults:
        print(res)

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
        print(affected_scodes)

    return render_template('state_skeleton.html', conf_threshold = conf_threshold, aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = state_dropdown_ids, change_ids = state_change_ids)


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

    return render_template('address_skeleton.html', aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = state_dropdown_ids, cstate_ids = state_dropdown_ids, address_info = address_batch)


@app.route("/statistics")
def statistics():
    return render_template('statistics.html')


@app.route("/end")
def end():
    return render_template('endscreen.html')





if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


