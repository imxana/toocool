# the flaskr app

from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash

def register(app):


    @app.route('/')
    def show_entries():
        cur = g.Post.query.all()
        entries = [dict(title=row.title, text=row.body) for row in cur]
        return render_template('flaskr/show_entries.html', entries=entries)


    @app.route('/add', methods=['POST'])
    def add_entry():
        if not session.get('logged_in'):
            abort(401)
        entry = g.Post(request.form['title'], request.form['text'], g.Category.query.filter_by(name='Python').first())
        g.db.session.add(entry)
        g.db.session.commit()    
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            user = g.User.query.filter_by(username=request.form['username']).first()
            if not bool(user):
                error = 'Invalid username'
            elif request.form['password'] != user.password:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        return render_template('flaskr/login.html', error=error)



    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))



