from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


@app.route('/')
def home():
    image_folder = r"C:\Users\pierrontl\Documents\GitHub\Fraude\API\static"
    image_files = []
    
    for parent, dnames, fnames in os.walk(image_folder):
        for fname in fnames:
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Vérifiez l'extension de fichier pour vous assurer qu'il s'agit d'une image
                image_files.append(fname)

    return render_template('home.html', image_files=image_files)

if __name__ == '__main__':
    app.run(debug=True)
