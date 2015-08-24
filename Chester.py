import cPickle as pickle
import random
from flask import Flask, render_template, redirect
from flask_wtf import Form
from wtforms import SelectField, TextField, validators
from gtts import gTTS

people = ["PUT PEOPLE HERE",
        "JUST LIKE THIS"]

greetings = ["My Dearest {}",
        "Hello {}",
        "My Beloved {}",
        "Yo {}",
        "To {}, the brightest star in my sky",
        "Greetings {}",
        "Salutations {}",
        "My Darling {}",
        "Hey {} face",
        "{}, you crazy son of a bitch",
        "What up {}"]


signoff = ["Sincerely, {}",
        "With deep admiration, {}",
        "Yours for eternity, {}",
        "Because I love you, {}",
        "Thanks for all your hard work this summer, {}",
        "Goodbye forever, {}",
        "Ten thousand hugs and kisses, {}",
        "Hoping you feel like a hundred bucks {}",
        "Catch ya on the flippy-flop, {}",
        "With human emotion {}"]
       
try:
    # Too lazy for an actual database? Just stick a dictionary in a pickle!
    dbf = open("love.pdb")
    db = pickle.load(dbf)
except IOError:
    db = {}
    for s in people:
        db[s] = []
app = Flask(__name__)

class HumanLove(Form):
    to = SelectField('To')
    message = TextField('Message', validators = [validators.Length(min=3)])
    fro = TextField('From', validators = [validators.Length(min=2)])

@app.route("/", methods = ["GET", "POST"])
def main():
    form = HumanLove(name = "APPRECIATE")
    stp = []
    for (s, msgs) in db.iteritems():
        if msgs == []:
            # Let's make sure everyone gets at least one.
            stp.append(s)
    if stp == []:
        # Everyone has at least one message? Cool.
        stp = db.keys()
    form.to.choices = [(s, s) for s in set(stp)]
    if form.validate_on_submit():
        to = form.to.data
        fro = form.fro.data
        # Get a random greeting.
        greet = greetings[random.randrange(len(greetings))].format(to)
        # Get a random farewell
        farewell = signoff[random.randrange(len(signoff))].format(fro)
        full_message = "{} {} {}".format(greet, form.message.data, farewell)
        tts = gTTS(text = full_message)
        messages = db.get(to, [])
        if messages is None:
            messages = []
        db[to] = messages.append(full_message)
        tts.save("messages/message-to-{}-from-{}.mp3".format(to, fro))
        dbf = open("love.pdb", "a+")
        pickle.dump(db, dbf)
        dbf.close()
        return redirect("/")
    return render_template('index.html', form = form)

if __name__ == "__main__":
    app.secret_key = "SEKRIT"
    app.run(debug = True)
