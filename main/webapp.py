from flask import Flask, render_template, request, flash

# create instance of flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'salesforcebutthesecondtime'

country_dropdown_ids = ['AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'CV', 'KH', 'CM', 'CA', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'SZ', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MK', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW']
state_dropdown_ids = {'AR':['ER'], 'US':['CO', 'DE', 'TX']}
affected_ccodes = ['AR', 'US']
affected_scodes = {'AR':['ER'], 'US':['CO']}
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
    return render_template('home.html')

@app.route("/country_approve") # define path component
def country_approve():
    return render_template('country_skeleton.html', aff_country_codes = affected_ccodes, dropdown_ids = country_dropdown_ids, change_ids = change_ids)

@app.route("/state_approve")
def state_approve():
    return render_template('state_skeleton.html', aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = state_dropdown_ids, cstate_ids = state_dropdown_ids, change_ids = change_ids)

@app.route("/address_approve")
def address_approve():
    return render_template('address_skeleton.html', aff_country_codes = affected_ccodes, aff_state_codes = affected_scodes, cdropdown_ids = country_dropdown_ids, sdropdown_ids = state_dropdown_ids, cstate_ids = state_dropdown_ids, address_info = address_batch)

@app.route("/statistics")
def statistics():
    return render_template('statistics.html')

@app.route("/end")
def end():
    return render_template('endscreen.html')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)