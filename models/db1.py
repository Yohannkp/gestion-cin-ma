db = DAL('sqlite://gestion_cinema.sqlite')
#db = DAL('mysql://adaboubvincent:PaUl@_ADA20100@adaboubvincent.mysql.pythonanywhere-services.com/gestioncinema')

Film = db.define_table('film',
    Field('image', 'upload'),
    Field('resume_video', 'string'),
    Field('titre', 'string'),
    Field('date_sortie', 'date'),
    Field('duree', 'string'),
    Field('realisateur', 'string'),
    Field('description', 'text'),
    format = "%(titre)s")

Affiche = db.define_table('affiche',
    Field('numero_affiche', 'string'),
    Field('date_heure_projection', 'datetime'),
    Field('film_id', 'reference film', label=T('Film ')),
    format = "%(numero_affiche)s %(date_heure_projection)s")

Personne = db.define_table('personne',
    Field('nom', 'string'),
    Field('prenom', 'string'),
    format = "%(nom)s %(prenom)s")

Place = db.define_table('place',
    Field('affiche_id', 'reference affiche', label=T('Affiche ')),
    Field('personne_id', 'reference personne', label=T('Personne ')),
    Field('nombre_place', 'integer'))

PDF = db.define_table('pdf',
    Field('place_id', 'reference place', label=T('Place ')),
    Field('pdf_url', 'string'))
