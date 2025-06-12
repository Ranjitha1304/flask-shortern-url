from flask import Flask, render_template, request, redirect, url_for, flash
import string
import random
import validators

app = Flask(__name__)
app.secret_key = "your_secret_key"  # needed for flash messages

# In-memory store for demo purposes: short_id -> original_url
url_map = {}

def generate_short_id(num_chars=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(num_chars))
        if short_id not in url_map:
            return short_id

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('long_url', '').strip()

        # Validate URL
        if not validators.url(long_url):
            flash("Please enter a valid URL.", "error")
        else:
            # Generate short ID and store
            short_id = generate_short_id()
            url_map[short_id] = long_url

            # Construct short URL to show on page
            short_url = request.host_url + short_id

    return render_template('index.html', short_url=short_url)

@app.route('/<short_id>')
def redirect_short_url(short_id):
    long_url = url_map.get(short_id)
    if long_url:
        return redirect(long_url)
    else:
        return "Invalid URL", 404

if __name__ == '__main__':
    app.run(debug=True)
