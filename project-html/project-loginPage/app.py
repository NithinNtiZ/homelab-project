from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data (in a real application, this would be stored securely)
users = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        # Successful login
        # return f"Welcome, {username}!"
        return redirect("https://html.onlineviewer.net/")
    else:
        # Invalid credentials, redirect back to login page
        # return redirect(url_for('index'))
        return redirect(url_for('index'))
    
@app.route('/show', methods=['GET'])
def show():
    ...

if __name__ == '__main__':
    app.run(debug=True)
