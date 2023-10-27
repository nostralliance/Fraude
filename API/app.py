'''
explication  code :
1. on définit une liste dans la qu'elle sera stocker le nom du fichier
2. une boucle qui permet de recuperer le répertoire parent le directory et l'image grace a os.walk
3. et pour chaque images on join l'image a dnames ou au parent 
4. puis on ajoute a la liste 



'''


from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
  liste = []
  for parent, dnames, fnames in os.walk(r"C:\Users\pierrontl\Documents\code_python\API\static"):
     return jsonify(fnames)
  #   print("fnames : ", fnames)
  #   for fname in fnames:
  #     print("fname avant :", fname)
  #     filename = os.path.join(fname)
  #     print("apres os.path.join de fnam", filename)
  #     liste.append(filename)
  # return jsonify(liste)

if __name__ == '__main__':
    app.run(debug=True)

