from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    svg_filename = 'system_usage.svg'  # nom du fichier dans /static
    return render_template('template/index.html', system_usage=svg_filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
