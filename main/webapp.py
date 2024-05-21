from flask import Flask
from flask import request

# create instance of flask
app = Flask(__name__)

# connect URL endpoints
@app.route("/") # define path component
def index():
    return """<!DOCTYPE html>
              <html>
              <head>
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <style>
              body {font-family: "Lato", sans-serif;}
              
              p {font-family: "Lato", sans-serif;}
              
              table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
              }

              td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
              }

              tr:nth-child(even) {
                background-color: #dddddd;
              }
              
              .accordion {
                background-color: #eee;
                color: #444;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 15px;
                transition: 0.4s;
              }

              .active, .accordion:hover {
                background-color: #ccc; 
              }

              .panel {
                padding: 0 18px;
                display: none;
                background-color: white;
                overflow: hidden;
              }
              </style>
              </head>
              <body>

              <h2>Approve address entries</h2>

              <button class="accordion">AR</button>
              <div class="panel">    
                <button class="accordion">Invalid State</button>
                <div class="panel">
                </div>
              </div>

              <button class="accordion">US</button>
              <div class="panel">
                <table>
                    <tr>
                      <th>Address</th>
                      <th>Confidence</th>
                      <th>Country</th>
                      <th>State</th>
                    </tr>
                    <tr>
                      <td>123 Argument ln.</td>
                      <td>60%</td>
                      <td>
                        <form action="" method="get">
                          <select name="countries" id="countries">
                            <option value="US">US</option>
                            <option value="CN">CN</option>
                            <option value="CA">CA</option>
                          </select>
                          <input type="submit" value="Confirm">
                        </form>
                      </td>
                      <td>
                        <form action="" method="get">
                          <select name="states" id="states">
                            <option value="CO">CO</option>
                            <option value="CA">CA</option>
                            <option value="TX">TX</option>
                          </select>
                          <input type="submit" value="Confirm">
                        </form>
                      </td>
                    </tr>
                  </table>
                  <input type="text" name="country">
                  <input type="submit" value="Convert">
                  <br>
                  <br>
              </div>

              <button class="accordion">CA</button>
              <div class="panel">
                
              </div>

              <script>
              var acc = document.getElementsByClassName("accordion");
              var i;

              for (i = 0; i < acc.length; i++) {
                acc[i].addEventListener("click", function() {
                  this.classList.toggle("active");
                  var panel = this.nextElementSibling;
                  if (panel.style.display === "block") {
                    panel.style.display = "none";
                  } else {
                    panel.style.display = "block";
                  }
                });
              }
              </script>

              </body>
              </html>
              """

if __name__ == "__main__":
    # country_input = input("Country: ")
    # print("Input: ", country_input)
    app.run(host="127.0.0.1", port=8080, debug=True)