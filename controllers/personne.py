
def pdf(pdf_nom: str, place: object):
    def f(d:str):
        if d[0] == "0":
            return d[1]
        return d
    from fpdf import FPDF
    import os
    import datetime
    pdf = FPDF()
    pdf.add_page()

    #pdf.set_font("Arial", size=15)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10,txt="Nom et Prénom : "+place.personne_id.nom +" "+place.personne_id.prenom, ln=1, align="C")
    pdf.cell(50, 12,txt="Film à suivre : "+place.affiche_id.film_id.titre, ln=1,align="L")
    pdf.cell(50, 13,txt="Durée du Film : "+place.affiche_id.film_id.duree, ln=1,align="L")
    pdf.cell(50, 14,txt="Date de sortie du Film : "+place.affiche_id.film_id.date_sortie.__str__(), ln=1,align="L")
    pdf.cell(50, 15,txt="Réalisateur du Film : "+place.affiche_id.film_id.realisateur, ln=1,align="L")
    pdf.cell(50, 16,txt="Nombre de place que vous avez réservés pour ce Film : "+str(place.nombre_place), ln=1,align="L")

    jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois_annee = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    dateComplet = str(place.affiche_id.date_heure_projection.__str__().split(" ")[0])
    heures = str(place.affiche_id.date_heure_projection.__str__().split(" ")[1])
    dateComplet = dateComplet.split("-")
    w = datetime.date(int(dateComplet[0]), int(f(dateComplet[1])), int(f(dateComplet[2]))).isocalendar()
    pdf.cell(200, 20,txt=jours_semaine[w[2] - 1] + ", le "+f(dateComplet[2]) + " " + mois_annee[int(f(dateComplet[1])) - 1] + " " + dateComplet[0] + ", "+heures, ln=1, align="R")

    ''' 
    .cell(w, h = 0, txt = '', border = 0, ln = 0, 
          align = '', fill = False, link = '')
     '''


    file_url = "./applications/ProjetCinema/static/"+ pdf_nom
    pdf.output(file_url)

def open_pdf(pdf_nom: str):
    import webbrowser
    path = 'http://127.0.0.1:8000/ProjetCinema/static/'+ pdf_nom
    webbrowser.open_new(path)
def open_pdf_url(url_pdf: str):
    import webbrowser
    path = url_pdf
    webbrowser.open_new(path)

@auth.requires_login()
def ajout_personne():
    pdf_name = ""
    if not session.pdf_url:
        session.pdf_url = None
    form = SQLFORM(db.personne)
    mode_reservation = False
    if request.vars.affiche_id:
        mode_reservation = True
        session.affiche_id = request.vars.affiche_id
        my_extra_element = TR(LABEL('Nombre de place à réserver : '),
                      INPUT(_name='nombre_place', _type='number', _required=True, _min=1))
        form[0].insert(-1, my_extra_element)

    nom = request.vars.nom
    prenom = request.vars.prenom
    message=T('')
    if form.process().accepted:
        response.flash = 'form accepted'
        for row in db().select(db.personne.ALL):
            count = 0
            for _row in db().select(db.personne.ALL):
                if row.nom == _row.nom and row.prenom == _row.prenom:
                    count += 1
                    if count >= 2:
                        try:
                            db(db.personne.id ==  _row.id).delete()
                        except Exception as e:
                            print("Une erreur s'est produit")
            count = 0
        person = db.personne(nom=nom, prenom=prenom)
        if session.affiche_id:
            import datetime
            d = datetime.datetime.now().__str__().split(" ")
            date_now_split = d[0] + "-" + d[1].split(":")[0] + "-" + d[1].split(":")[1] + "-" + d[1].split(":")[2].split(".")[0]
            
            place = db.place.insert(affiche_id=session.affiche_id, personne_id=person.id, nombre_place=request.vars.nombre_place)
            def transform(l: str):
                if len(l.split(" ")) > 1:
                    ll = l.split(" ")
                    l = ""
                    for i in ll:
                        l += i + "-"
                return l
            pdf_name = "upload/pdf/" + transform(nom) + "-" + transform(prenom) + date_now_split + '.pdf'
            pdf_url_enreg = db.pdf.insert(place_id=place.id, pdf_url=pdf_name)
            session.pdf_url = pdf_url_enreg.pdf_url

            #affiche = db.affiche(session.affiche_id) or redirect(URL('error'))

            pdf(pdf_name, place)
            session.affiche_id = 0
            message=T('Film réservé')
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form, message=message, mode_reservation=mode_reservation, pdf_url=session.pdf_url)

@auth.requires_login()
def list_personne():
    rows = db().select(db.personne.ALL)
    return dict(rows=rows, )

@auth.requires_login()
def supprimer_personne():
    db(db.personne.id ==  request.args(0)).delete()
        
    return dict(form=redirect(URL('list_personne')), message=T('Un enrégistrement d\'une personne a été supprimé'))

@auth.requires_login()
def modifier_personne():
    personne = db.personne(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.personne, personne)
    form.process(detect_record_change=True)
    if form.record_changed:
        response.flash = 'form changed'
        return dict(form=redirect(URL('list_personne')))
    elif form.accepted:
        response.flash = 'form accepted'
        return dict(form=redirect(URL('list_personne')))
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)

    