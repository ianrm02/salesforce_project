import os
from os import listdir, path
from os.path import isfile, join
from flask import Flask, render_template, request, flash, url_for
from ClassifierApp import ClassifierApp
import config

# create instance of flask
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'salesforcebutthesecondtime'
clfApp = ClassifierApp()

country_dropdown_ids = clfApp.clf.iso_standard_df["alpha-2"]
state_dropdown_ids = {'AR':['ER'], 'US':['CO', 'DE', 'TX']} #TODO
affected_scodes = {'AR':['ER'], 'US':['CO']} #TODO
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
    #Sorted by confidence
    #Each address has [OldCo] [NewCo] [Freq] [Conf]

    print(country_changes)

    affected_ccodes = list(set([code[1] for code in country_changes]))
    affected_ccodes.sort()

    country_change_ids = [['C'] + code for code in country_changes]

    return render_template('country_skeleton.html', aff_country_codes = affected_ccodes, dropdown_ids = country_dropdown_ids, change_ids = country_change_ids)


@app.route("/state_approve")
def state_approve():
    state_changes = [item for item in clfApp.db_handler.get_all_from_table("StateChanges")]
    state_changes.sort(key=lambda x: x[3])
    #Sorted by confidence
    #Each address has [Old] [New] [Freq] [Conf]

    #TODO logic to get from changes to the format needed bby the render_template()

    print(state_changes)

    return render_template('state_skeleton.html', aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = state_dropdown_ids, cstate_ids = state_dropdown_ids, change_ids = change_ids)


@app.route("/address_approve")
def address_approve():
    address_changes = [item for item in clfApp.db_handler.get_all_from_table("AddressChanges")]
    address_changes.sort(key=lambda x: x[3])
    #Sorted by confidence

    #TODO logic to get from changes to the format needed bby the render_template()

    return render_template('address_skeleton.html', aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = state_dropdown_ids, cstate_ids = state_dropdown_ids, address_info = address_batch)


@app.route("/statistics")
def statistics():
    return render_template('statistics.html')


@app.route("/end")
def end():
    return render_template('endscreen.html')





if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


