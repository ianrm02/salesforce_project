from flask import Flask, render_template
from flask import request

# create instance of flask
app = Flask(__name__)

# connect URL endpoints
@app.route("/") # define path component
def index():
    return render_template('test.html')

if __name__ == "__main__":
    # country_input = input("Country: ")
    # print("Input: ", country_input)
    app.run(host="127.0.0.1", port=8080, debug=True)