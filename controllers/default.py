# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

#Function return 

def f(d:str):
    if d[0] == "0":
        return d[1]
    return d

    
# ---- example index page ----

def index():
    import datetime
    date_now_split = datetime.datetime.now().__str__().split(" ")[0].split("-")
    isocalendar = datetime.date(int(date_now_split[0]), int(date_now_split[1]), int(date_now_split[2])).isocalendar()
    semaine_number_auto =  isocalendar[1]
    day_number_auto =  isocalendar[2]
    

    rows = db().select(db.affiche.ALL)

    myorder = db.affiche.date_heure_projection.upper() | db.affiche.id
    rows5 = db().select(db.affiche.ALL, orderby=~myorder)
    rows5 = [rows5[count] for count in range(len(rows5)) if count < 5]
    
    lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche = [], [], [], [], [], [], []

    for row in rows:
        dateComplet = str(row.date_heure_projection.__str__().split(" ")[0])
        dateComplet = dateComplet.split("-")
        w = datetime.date(int(dateComplet[0]), int(f(dateComplet[1])), int(f(dateComplet[2]))).isocalendar()
        weekNumber: int = w[1]
        if semaine_number_auto == weekNumber:
            weekdayNumber: int = w[2]
            if weekdayNumber == 7:
                dimanche.append(row)
            elif weekdayNumber == 1:
                lundi.append(row)
            elif weekdayNumber == 2:
                mardi.append(row)
            elif weekdayNumber == 3:
                mercredi.append(row)
            elif weekdayNumber == 4:
                jeudi.append(row)
            elif weekdayNumber == 5:
                vendredi.append(row)
            else:
                samedi.append(row)

    #response.flash = T("Hello World")message=T('Welcome to web2py!')
    return dict(rows5=rows5, lundi=lundi, mardi=mardi,
        mercredi=mercredi, jeudi=jeudi, vendredi=vendredi,
        samedi=samedi, dimanche=dimanche, day_number_auto=day_number_auto)

def nouveau_a_venir():
    import datetime
    date_now_split = datetime.datetime.now().__str__().split(" ")[0].split("-")
    isocalendar = datetime.date(int(date_now_split[0]), int(date_now_split[1]), int(date_now_split[2])).isocalendar()

    semaine_number_auto =  isocalendar[1] + 1
    fevr = 28
    if int(date_now_split[0])%4 == 0:
        fevr = 29
    mois_number = [31, fevr, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    lundi_samaine_day = int(date_now_split[2]) + 7
    if lundi_samaine_day > mois_number[int(date_now_split[1]) - 1]:
        lundi_samaine_day = (lundi_samaine_day)%mois_number[int(date_now_split[1]) - 1]
        
    if isocalendar[2] == 2:
        lundi_samaine_day -= 1
    elif isocalendar[2] == 3:
        lundi_samaine_day -= 2
    elif isocalendar[2] == 4:
        lundi_samaine_day -= 3
    elif isocalendar[2] == 5:
        lundi_samaine_day -= 4
    elif isocalendar[2] == 6:
        lundi_samaine_day -= 5
    elif isocalendar[2] == 7:
        lundi_samaine_day -= 6

    rows = db().select(db.affiche.ALL)
    lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche = [], [], [], [], [], [], []
    for row in rows:
        dateComplet = str(row.date_heure_projection.__str__().split(" ")[0])
        dateComplet = dateComplet.split("-")
        w = datetime.date(int(dateComplet[0]), int(f(dateComplet[1])), int(f(dateComplet[2]))).isocalendar()
        weekNumber: int = w[1]
        if semaine_number_auto == weekNumber:
            weekdayNumber: int = w[2]
            if weekdayNumber == 7:
                dimanche.append(row)
            elif weekdayNumber == 1:
                lundi.append(row)
            elif weekdayNumber == 2:
                mardi.append(row)
            elif weekdayNumber == 3:
                mercredi.append(row)
            elif weekdayNumber == 4:
                jeudi.append(row)
            elif weekdayNumber == 5:
                vendredi.append(row)
            else:
                samedi.append(row)

    #response.flash = T("Hello World")message=T('Welcome to web2py!')
    return dict(lundi=lundi, mardi=mardi, rows=rows,
        mercredi=mercredi, jeudi=jeudi, vendredi=vendredi,
        samedi=samedi, dimanche=dimanche, lundi_samaine_day=lundi_samaine_day)
        
def index1():
    rows = db().select(db.affiche.ALL)
    #response.flash = T("Hello World")message=T('Welcome to web2py!')
    return dict(rows=rows)
def contact():
    return dict()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
