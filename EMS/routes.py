from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from server import app, ems
import datetime
import time
from src.event import *
from src.errors import *


@app.route('/')
def home():
    return redirect('login')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))   

#index page
@app.route('/index')
@login_required
def index():
    return render_template('index.html', ems = ems)

#404
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        zid = request.form['zID']
        password = request.form['password']

        user = ems.validate_login(zid, password)
        if user is not None:
            login_user(user)
            return redirect(url_for('index', next=None))
        else:
            return render_template('login.html', errorM='zID and password does not match', status='False')
    return render_template('login.html')
'''
#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = ems.check_login(email, password)
            if user == None:
                return render_template('login.html', msg='Invalid user')
            else :
                login_user(user)
                temp = request.args.get('next')
                return redirect(temp or url_for('index'))

    return render_template('login.html')


#add the guest_user
@app.route('/guest_register', methods=['GET', 'POST'])
def guest_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        ems.user_manager.add_guest(name, email, password)
    return render_template('guest_register.html')

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        if 'create_seminar' in request.form:
            return render_template('create_event.html', type='Seminar', form='POST')
        if 'create_course' in request.form:
            return render_template('create_event.html', type='Course', form='POST')

        event_type = request.form['type']
        name = request.form['name']
        convener = ems.check_email(current_user.email)
        details = request.form['description']
        loc = request.form['venue']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        due_date = request.form['register_due_date']
        early_bird= request.form['early_bird_date']
        fee = request.form['registration_fee']
        end_date = request.form['end_date']
        due_date = request.form['register_due_date']
        if event_type == 'Seminar':
            event_id = ems.create_seminar(name, convener, details, loc, start_date, end_date,register_due_date, early_bird, fee)
        if event_type == 'Course':
            attendee_capacity = request.form['attendee_capacity']
            event_id = ems.create_course(name, convener, details, loc, start_date, end_date, due_date, early_bird, attendee_capacity, fee)
        return redirect(url_for('event_details', event_id=event_id))

    return render_template('create_event.html', type='', form='POST')



@app.route('/<event_id>/inner_page', methods=["GET", "POST"])
@login_required
def event_details(event_id):
    event = ems.event_manager.get_event(event_id)
    if event is None:
        return redirect(url_for('page_not_found'))
        #no event found
    user = ems.check_email(current_user.email)
    if request.method == 'POST':
        try:
            if 'Cancel' in request.form:
                ems.cancel_event(user, event)
        except StatusChangingError as sce:
            return render_template('event_details.html', event=event, errors=sce.errors, form='POST')

        try:
            if 'Close' in request.form:
                ems.close_event(user, event)
        except StatusChangingError as sce:
            return render_template('event_details.html', event=event, errors=sce.errors, form='POST')
        try:
            if 'Purchase' in request.form:
                ems.purchase_event(user, event)
                fee = ems.event_price(event, user)
                purchase_msg = "This is free.".format(fee)
                return render_template('event_details.html', event=event, form='POST', purchase_msg=purchase_msg)
        except PurchasingError as pe:
            return render_template('event_details.html', event=event, errors=pe.errors, form='POST')

        try:
            if 'Register' in request.form:
                ems.register_course(user, event)
        except RegisterError as re:
            return render_template('event_details.html', event=event, errors=re.errors, form='POST')

        try:
            if 'Unregister' in request.form:
                ems.unregister_course(user, event)
        except RegisterError as re:
            return render_template('event_details.html', event=event, errors=re.errors, form='POST')

        if 'Cancel_creating' in request.form:
            return render_template('event_details.html', event=event, form='POST')

        if 'Add_session' in request.form:
            return render_template('event_details.html', event=event, creating=True, form='POST')
            
        #if 'Close_session' in request.form:
        #     return render_template('event_details.html', event=event,  form='POST')
        try:
            if 'Creating_confirm' in request.form:
                name = request.form['name']
                detail = request.form['detail']
                speaker = ems.check_email(request.form['email'])
                attendee_capacity = request.form['attendee_capacity']
                ems.create_session(event, name, detail, speaker, attendee_capacity)
                return redirect(url_for('event_details', event_id=event_id))
        except EventCreatingError as ece:
            return render_template('event_details.html', event=event, creating=True, form='POST', errors = ece.errors)
    return render_template('event_details.html', event=event, form='POST')


@app.route('/<session_id>/<event_id>/register', methods=["GET", "POST"])
@login_required
def session_register_inner_page(event_id, session_id):
    event = ems.event_manager.get_event(event_id)
    if event is None:
        return redirect(url_for('page_not_found'))
    user = ems.check_email(current_user.email)
    try:
        ems.register_s(user, event, session_id)
    except RegisterError as re:
        render_template('event_details.html', event=event, method='POST', errors=re.errors)
    return redirect(url_for('event_details', event_id=event.id))


@app.route('/<session_id>/<event_id>/ unregister', methods=["GET", "POST"])
@login_required
def session_unregister_inner_page(event_id, session_id):
    event = ems.event_manager.get_event(event_id)
    if event is None:
        return redirect(url_for('page_not_found'))
    user = ems.check_email(current_user.email)
    
    try:
        ems.unregister_s(user, event, session_id)
    except RegisterError as re:

        render_template('event_details.html', event=event, method='POST', errors=re.errors)
    return redirect(url_for('event_details', event_id=event.id))


@app.route('/<event_id>/<session_id>/register_index', methods=["GET", "POST"])
@login_required
def session_register_index(event_id, session_id):
    event = ems.event_manager.get_event(event_id)
    if event is None:
        return redirect(url_for('page_not_found'))
    user = ems.check_email(current_user.email)
    try:
        ems.register_session(user, event, session_id)
    except RegisterError as re:
        render_template('index.html', ems=ems, method='POST', errors=re.errors)
    return redirect(url_for('index', ems=ems))



@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        date_format = "%Y-%m-%dT%H:%M"
        # (name, convener, description, attendee_capacity, venue, start_date, end_date, register_due_date):
        name = request.form['name']
        convener = current_user
        description = request.form['description']
        attendee_capacity = request.form['attendee_capacity']
        venue = request.form['venue']
        start_date = datetime.strptime(request.form['start_date'], date_format)
        end_date = datetime.strptime(request.form['end_date'], date_format)
        register_due_date = datetime.strptime(request.form['register_due_date'], date_format)
        type = request.form['type']
        if type == 'Seminar':
            event = Seminar(name, convener, description, attendee_capacity, venue,
                            start_date, end_date, register_due_date)
        else:
            event = Course(name, convener, description, attendee_capacity, venue,
                           start_date, end_date, register_due_date)
        ems.create_event(current_user, event)
        return redirect(url_for('dashboard', next=None))
    return render_template('add_event.html', form = 'POST')



@app.route('/<event_id>/<session_id>/unregister_index', methods=["GET", "POST"])
@login_required
def session_unregister_index(event_id, session_id):
    event = ems.event_manager.get_event(event_id)
    if event is None:
        return redirect(url_for('page_not_found'))
    user = ems.check_email(current_user.email)
    try:
        ems.unregister_s(user, event, session_id)
    except RegisterError as re:
        render_template('index.html', ems=ems, method='POST', errors=re.errors)
    return redirect(url_for('index', ems=ems))
    
''' 
@app.route('/index')
@login_required
def index():
    return render_template('index.html',
                           all_open_seminars=ems.get_all_open_seminars(),
                           all_open_courses=ems.get_all_open_courses()
                           )
'''
