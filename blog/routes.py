from flask import render_template, request, redirect, url_for, flash
from blog import app, db
from blog.models import Entry
from blog.forms import EntryForm

@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc()).all()
    return render_template("homepage.html", all_posts=all_posts)

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
def create_entry():
    return entry_form_common()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return entry_form_common(entry=entry)