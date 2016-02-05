from flask import Flask, render_template
from flask import request, Response, stream_with_context
from flask_wtf import Form
from flask import send_from_directory
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Regexp
import re
import os

from TwitterStrings_stream import run_kmp, set_context


class KMPForm(Form):
    #  class variables
    pattern = StringField(label='pattern', default='attack',
                          validators=[InputRequired("input"),
                                      Regexp(regex=re.compile(
                                             r'[\w\W\b\B\d\D\s\S]+'),
                                             flags=re.ASCII)])
    follow = StringField(label='follow_list', default="30313925, 76067316")
    track = StringField(label='track', default="terrorism, weapons")
    language = StringField(label='language', default='en')
    # locations = StringField(label='locations', default='-74, 40, -73, 41')
    submit = SubmitField(label='Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret development key!'
#  load from environment var
#  app.config.from_envvar('APPLICATION_SETTINGS')


@app.route('/', methods=['GET'])
def welcome():
    form = KMPForm(request.form, csrf_enabled=True)
    return render_template("filter_tweets_form.html", form=form)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/next_match/', methods=['POST'])
def next_match():
    """
    HTTP web server receives data in a form
    TWITTER issues API response
    """
    #  form = KMPForm(request.POST)
    form = KMPForm(request.form, csrf_enabled=True)
    #  if request.method == 'POST' and form.validate():
    #  if request.POST and form.validate():
    if form.validate_on_submit():
        language = form.language.data
        follow = form.follow.data
        track = form.track.data
        # locations = form.locations.data
        pattern_to_search_for = form.pattern.data
        iterator = set_context(language, follow, track)
        #  yields tweet
        return Response(stream_with_context(run_kmp(pattern_to_search_for, iterator)))

##########################
if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=8000, debug=True)
