

@auth.requires_login()
def ajout_place():
    form = SQLFORM(db.place)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def list_place():
    rows = db().select(db.place.ALL)
    rows_pdf = db().select(db.pdf.ALL)
    return dict(rows=rows, rows_pdf=rows_pdf)

@auth.requires_login()
def supprimer_place():
    db(db.place.id ==  request.args(0)).delete()
        
    return dict(form=redirect(URL('list_place')), message=T('Un enrégistrement d\'une place a été supprimé'))

@auth.requires_login()
def modifier_place():
    place = db.place(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.place, place)
    form.process(detect_record_change=True)
    if form.record_changed:
        response.flash = 'form changed'
        return dict(form=redirect(URL('list_place')))
    elif form.accepted:
        response.flash = 'form accepted'
        return dict(form=redirect(URL('list_place')))
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)




