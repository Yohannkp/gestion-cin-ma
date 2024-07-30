@auth.requires_login()
def ajout_affiche():
    form = SQLFORM(db.affiche)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

@auth.requires_login()
def list_affiche():
    rows = db().select(db.affiche.ALL)
    return dict(rows=rows, test78="test78.pdf")

@auth.requires_login()
def supprimer_affiche():
    db(db.affiche.id ==  request.args(0)).delete()
        
    return dict(form=redirect(URL('list_affiche')), message=T('Un enrégistrement d\'une affiche a été supprimée'))

@auth.requires_login()
def modifier_affiche():
    affiche = db.affiche(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.affiche, affiche)
    form.process(detect_record_change=True)
    if form.record_changed:
        response.flash = 'form changed'
        return dict(form=redirect(URL('list_affiche')))
    elif form.accepted:
        response.flash = 'form accepted'
        return dict(form=redirect(URL('list_affiche')))
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

def detail():
    import datetime
    def f(d:str):
        if d[0] == "0":
            return d[1]
        return d
    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    affiche = db.affiche(request.args(0)) or redirect(URL('error'))

    dateComplet = str(affiche.date_heure_projection.__str__().split(" ")[0])
    dateComplet = dateComplet.split("-")
    w = datetime.date(int(dateComplet[0]), int(f(dateComplet[1])), int(f(dateComplet[2]))).isocalendar()
    week_day: str = jours_semaine[w[2] - 1]

    return dict(affiche=affiche, week_day=week_day)