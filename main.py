#Flask
from flask import Flask, request, render_template
from flask import Response

#mongoMethods Dependencies
import pymongo
import tellurium
import dns
import oscillatorDB.mongoMethods as mm

#Miscellaneous Packages
from zipfile import ZipFile
import os

#Initializing Flask app and mongoMethods Startup
app = Flask(__name__)
mm.startup()



#Index Page
@app.route("/")
def index():
    num_nodes = request.args.get("num_nodes", "")
    num_reactions = request.args.get("num_reactions", "")
    oscillator = request.args.get("oscillator", "")
    mass_conserved = request.args.get("mass_conserved", "")

    oscillatorDB(num_nodes, num_reactions, oscillator, mass_conserved)

    return render_template('index.html')




@app.route("/download/<path:filename>", methods = ['GET'])
def download_zipfile(filename):
  # return render_template('download.html', value=filename)
  # if '/' in filename or '\\' in filename:
    # abort(404)
  return send_from_directory("downloads", filename, as_attachment=True)




#Function to process parameters and create download.zip
def oscillatorDB(num_nodes, num_reactions, oscillator, mass_conserved):

  def createToZipFile(zipfilename, filename, antimony_model):
    subdir = "downloads"
    filepath = os.path.join(subdir, zipfilename)

    with ZipFile(filepath, "a") as zip_file:
      zip_file.writestr(filename, antimony_model)

  try:
    num_nodes = int(num_nodes)
    num_reactions = int(num_reactions)

    if oscillator == "osc_yes":
      oscillator_status = True
    elif oscillator == "osc_no":
      oscillator_status = False

    if mass_conserved == "conserved_yes":
      conserved = True
    elif mass_conserved == "conserved_no":
      conserved = False

    query = { "num_nodes" : num_nodes, "num_reactions" : num_reactions, "oscillator" : oscillator_status, "mass_conserved" : conserved }
    model_IDS = mm.get_ids(query)

    # createZipFile("download.zip")

    if model_IDS:
      for ID in model_IDS:
        ant = mm.get_antimony({ "ID" : ID })
        filename = str(ID) + ".txt"
        createToZipFile("download.zip", filename, ant)
    else:
      print("No entries found.")
  except ValueError:
    return "Invalid Input"



  #Functions to create text files and save to zip file
  # def saveToTextFile(filename, antimony_model):

  #   subdir = "downloads"
  #   filepath = os.path.join(subdir, filename)

  #   with open(filepath, "w") as text_file:
  #     text_file.write(antimony_model)

  # def createZipFile(zipfilename):

  #   subdir = "downloads"
  #   filepath = os.path.join(subdir, zipfilename)

  #   ZipFile(filepath, "w")

  # def addToZipFile(zipfilename, file):

  #   subdir = "downloads"
  #   filepath = os.path.join(subdir, file)

  #   with ZipFile(filepath, "a") as zip_file:
  #     zip_file.write(file)
  #   os.remove(file)


#Flask Development Server
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
