@auth.requires_login()
def ajout_film():
    form = SQLFORM(db.film)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def list_film1():
    #rows = db().select(db.personne.ALL), deletable=True, editable=True, csv=False
    rows = SQLFORM.grid(db.film)
    return dict(rows=rows)

@auth.requires_login()
def list_film():
    rows = db().select(db.film.ALL)
    return dict(rows=rows)

@auth.requires_login()
def supprimer_film():
    db(db.film.id ==  request.args(0)).delete()
        
    return dict(form=redirect(URL('list_film')), message=T('Un enrégistrement d\'un film a été supprimé'))

@auth.requires_login()
def modifier_film():
    film = db.film(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.film, film)
    form.process(detect_record_change=True)
    if form.record_changed:
        response.flash = 'form changed'
        return dict(form=redirect(URL('list_film')))
    elif form.accepted:
        response.flash = 'form accepted'
        return dict(form=redirect(URL('list_film')))
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, film=film)

def detail():
    film = db.film(request.args(0)) or redirect(URL('error'))

    return dict(film=film)