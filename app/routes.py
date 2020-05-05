from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import NewListForm, NewItemForm, EditListForm, EditItemForm, LoginForm
from app.models import List, Item, User
from mongoengine.errors import NotUniqueError


API_TOKEN = app.config['API_TOKEN']

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = NewListForm()
    if form.validate_on_submit():
        name = form.name.data
        checklist = form.checklist.data
        private = form.private.data
        l = List(name=name, checklist=checklist, private=private)
        l.save()
        return redirect(url_for('index'))
    lists = List.objects
    return render_template("index.html", form=form, lists=lists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(name=form.name.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid name or password')
            return redirect(url_for('login'))
        login_user(user, remember=False)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/list/<id>', methods=['GET', 'POST'])
def list(id):
    if not current_user.is_authenticated:
        if request.method == 'POST' and request.headers['api-token'] == API_TOKEN:
            name = request.values['name']
            list = List.objects.get(id=id)
            i = Item(name=name, list=list)
            i.save()
            return i.name
        else:
            return redirect(url_for('login'))
    list = List.objects.get(id=id)
    form = NewItemForm()
    if form.validate_on_submit():
        name = form.name.data
        i = Item(name=name, list=list)
        i.save()
        return redirect(url_for('list', id=id))
    items = Item.objects(list=list)
    return render_template("list.html", form=form, list=list, items=items)


@app.route('/list/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_list(id):
    list = List.objects.get(id=id)
    form = EditListForm(list.name)
    if form.validate_on_submit():
        name = form.name.data
        checklist = form.checklist.data
        private = form.private.data
        try:
            list.modify(name=name, checklist=checklist, private=private)
        except NotUniqueError:
            return redirect(url_for('edit_list', id=id))
        return redirect(url_for('list', id=id))
    elif request.method == 'GET':
        form.name.data = list.name
    return render_template('edit_list.html', form=form, list=list)


@app.route('/list/<id>/delete')
@login_required
def del_list(id):
    list = List.objects.get(id=id)
    list.delete()
    return redirect(url_for('index'))


@app.route('/list/<list_id>/item/<item_id>')
@login_required
def item(list_id, item_id):
    list = List.objects.get(id=list_id)
    item = Item.objects.get(id=item_id)
    return item.name


@app.route('/list/<list_id>/item/<item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(list_id, item_id):
    list = List.objects.get(id=list_id)
    item = Item.objects.get(id=item_id)
    form = EditItemForm()
    if form.validate_on_submit():
        name = form.name.data
        item.modify(name=name)
        return redirect(url_for('list', id=list_id))
    elif request.method == 'GET':
        form.name.data = item.name
    return render_template('edit_item.html', form=form, item=item, list=list)


@app.route('/list/<list_id>/item/<item_id>/complete', methods=['GET','POST'])
@login_required
def complete(list_id, item_id):
    item = Item.objects.get(id=item_id)
    item.complete()
    return "done"


@app.route('/list/<list_id>/item/<item_id>/uncomplete', methods=['GET','POST'])
@login_required
def uncomplete(list_id, item_id):
    item = Item.objects.get(id=item_id)
    item.uncomplete()
    return "un-done"


@app.route('/list/<list_id>/item/<item_id>/delete')
@login_required
def del_item(list_id, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect(url_for('list', id=list_id))


@app.route('/ifttt-grocery', methods=['POST'])
def ifttt_grocery():
    item_name = request.form['item'].capitalize()
    list = List.objects.get(name='Grocery')
    item = Item(name=item_name, list=list)
    item.save()
    return item.name


@app.route('/test')
def test():
    return render_template('test.html')
