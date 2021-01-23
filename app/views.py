from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="***",
    password="***",
    hostname="***",
    databasename="***",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

class Potion(db.Model):

    __table__ = db.Model.metadata.tables['potion']

class Spell(db.Model):

    __table__ = db.Model.metadata.tables['spell']

class Path(db.Model):
    __table__ = db.Model.metadata.tables['path_test']

class Ancestry(db.Model):
    __table__ = db.Model.metadata.tables['ancestry']

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/potions")
def potion():
    return render_template("public/potions.html", potions=Potion.query.all())

@app.route("/modal/<int:id>")
def modal(id):
    reqSpell = Spell.query.filter(Spell.id == id).one()
    modalhtml = '<div class="modal-dialog modal-lg"><div class="modal-content"><div class="modal-header"><h5 class="modal-title">' + reqSpell.name + '  ' + reqSpell.tradtion + '  ' + reqSpell.type + '  ' + reqSpell.rank + '</h5></div><div class="modal-body">'
    print(modalhtml)

    if reqSpell.req != "":
        modalhtml = modalhtml + '<p><b>Requirement </b>' + reqSpell.req + '</p>'
    if reqSpell.area != "":
        modalhtml = modalhtml + '<p><b>Area </b>' + reqSpell.area + '</p>'
    if reqSpell.target != "":
        modalhtml = modalhtml + '<p><b>Target </b>' + reqSpell.target + '</p>'
    if reqSpell.duration != "":
        modalhtml = modalhtml + '<p><b>Duration </b>' + reqSpell.duration + '</p>'

    modalhtml = modalhtml + '<hr><p>' + reqSpell.description + '</p>'

    if reqSpell.twentyplus != "":
        modalhtml = modalhtml + '<p><b>Attack Roll 20+ </b>' + reqSpell.twentyplus + '</p>'
    if reqSpell.triggered != "":
        modalhtml = modalhtml + '<p><b>Triggered </b>' + reqSpell.triggered + '</p>'
    if reqSpell.aftereffect != "":
        modalhtml = modalhtml + '<p><b>Aftereffect </b>' + reqSpell.aftereffect + '</p>'
    if reqSpell.sacrifice != "":
        modalhtml = modalhtml + '<p><b>Sacrifice </b>' + reqSpell.sacrifice + '</p>'
    if reqSpell.permanence != "":
        modalhtml = modalhtml + '<p><b>Permancence </b>' + reqSpell.permanence + '</p>'
    if reqSpell.special != "":
        modalhtml = modalhtml + '<p><b>Special </b>' + reqSpell.special + '</p>'

    modalhtml = modalhtml + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button></div></div></div>'
    print(modalhtml)
    return str(modalhtml);

@app.route("/spells/<int:page>")
def spelltest(page=1):
    per_page = 100
    potions = Spell.query.paginate(page,per_page,error_out=False)
    return render_template("public/spells.html", potions=potions.items)

@app.route("/spells")
def spell():
    return render_template("public/spells.html", potions=Spell.query.all())

@app.route("/paths")
def path():

    with open("/home/silverleaf/data/ancestries.txt", "r") as file:
        ancestries = file.readlines()
    file.close()

    with open("/home/silverleaf/data/novice.txt", "r") as file:
        novice = file.readlines()
    file.close()

    with open("/home/silverleaf/data/expert.txt", "r") as file:
        expert = file.readlines()
    file.close()

    with open("/home/silverleaf/data/master.txt", "r") as file:
        master = file.readlines()
    file.close()

    return render_template("public/paths.html", ancestries=ancestries, novice=novice, expert=expert, master=master)

@app.route("/paths/<some_path>")
def pathEntry(some_path):
    return render_template("public/path_page.html", pathData=Path.query.filter(Path.path_name == some_path))

@app.route("/ancestry/<anc>")
def ancEntry(anc):
    return render_template("public/anc_page.html", ancData=Ancestry.query.filter(Ancestry.anc == anc))