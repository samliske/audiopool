from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb+srv://Cluster80841:<JE8PDgdUx3S0Muse>@cluster0.5pbyoxd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)
print(os.environ.get('MONGO_DB_PASSWORD'))


try:
    if 'songs' not in mongo.db.list_collection_names():
        mongo.db.create_collection('songs')
        mongo.db.insert_one({"dummy": "data"})

except Exception as e:
    print("Failed to connect to MongoDB:", e)

@app.route('/')
def index():
    songs = mongo.db.songs.find()
    return render_template('index.html', songs=songs)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get song data from form
        title = request.form['title']
        artist = request.form['artist']
        audio_file = request.files['audio_file']

        # Save audio file to disk
        audio_filename = audio_file.filename
        audio_path = os.path.join('static/audio', audio_filename)
        audio_file.save(audio_path)

        # Save song data to MongoDB
        mongo.db.songs.insert_one({
            'title': title,
            'artist': artist,
            'audio_path': audio_path,
            'children': []
        })

        return redirect(url_for('index'))

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
