from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

if __name__ == '__main__':
    app.run(debug=True)
