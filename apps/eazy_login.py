# an eazy app for login

from flask import request, session, url_for, escape, redirect

def register(app):


    @app.route('/')
    def index():
        if 'username' in session:
            return '''
                <p>Logged in as %s</p>
                <a href="http://localhost:5000/logout">logout</a>
            ''' % escape(session['username'])
        return '''
            <p>You are not logged in</p>
            <a href="http://localhost:5000/login">login</a>
        '''

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''

    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        session.pop('username', None)
        return redirect(url_for('index'))







