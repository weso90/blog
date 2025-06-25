import functools
from flask import render_template, request, redirect, url_for, flash, session
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm, LoginForm

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    return render_template("homepage.html", all_posts=all_posts)

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        flash('Musisz się zalogować, aby uzyskać dostęp do tej strony.', 'warning')
        return redirect(url_for('login', next=request.path)) # Przekazujemy 'next'
    return check_permissions

def entry_form_common(entry=None):
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        if entry is None:
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            flash('Wpis został pomyślnie dodany!', 'success')
        else:
            form.populate_obj(entry)
            flash('Wpis został pomyślnie zaktualizowany!', 'success')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("entry_form.html", form=form)

@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return entry_form_common()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return entry_form_common(entry=entry)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['logged_in'] = True
        session.permanent = True 
        flash('Zostałeś pomyślnie zalogowany.', 'success')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('index'))
    return render_template("login_form.html", form=form)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('Zostałeś pomyślnie wylogowany.', 'info')
    return redirect(url_for('index'))

@app.route("/drafts/")
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc()).all()
    return render_template("drafts.html", drafts=drafts)

@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Wpis został pomyślnie usunięty.', 'success')
    return redirect(url_for('index'))