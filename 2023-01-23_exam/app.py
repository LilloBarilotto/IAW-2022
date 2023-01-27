# import module
from flask import Flask, render_template, request, session, redirect, flash, url_for
from datetime import datetime, date
from flask_session import Session
import dao

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from PIL import Image

import os

# create the application
app = Flask(__name__)
app.secret_key = '9OLWxND4o83j4K4qwe213eqeiQWEWQDmO'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

PROFILE_IMG_HEIGHT = 130


@app.route('/', methods=['GET', 'POST'])
def home():
    series = dao.get_series()
    categories = dao.get_categories()

    if current_user.is_authenticated:
        fav_series = dao.get_fav_series_by_user(current_user.id)
    else:
        fav_series = {}

    return render_template('home.html', series=series, fav_series=fav_series, categories=categories)


@login_manager.user_loader
def load_user(user_id):
    utente = dao.get_user(user_id)
    if utente is not None:
        return User(id=utente['id'], username=utente['username'], password=utente['password'],
                    img_path=utente['img_path'], is_creator=utente['is_creator'], email=utente['email'],
                    firstname=utente['firstname'], surname=utente['surname'])

    return None


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = dao.get_user_by_email(email)

    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))

    new = User(id=user['id'], username=user['username'], password=user['password'],
               img_path=user['img_path'], is_creator=user['is_creator'], email=user['email'],
               firstname=user['firstname'], surname=user['surname'])

    login_user(new, True)
    return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    series  = dao.get_series()
    fav_series = dao.get_fav_series_by_user(current_user.id)

    return render_template('account.html', series=series, fav_series=fav_series)

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    is_creator = int(request.form.get('isCreator'))
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    surname = request.form.get('surname')


    if len(username) < 5 or len(username) > 20:
        flash('Vincolo username len non rispettato', 'danger')
        return redirect(url_for('signup'))

    if len(password) < 5 or len(password) > 20:
        flash('Vincolo password len non rispettato', 'danger')
        return redirect(url_for('signup'))

    if is_creator != 1 and is_creator != 0:
        flash('Vincolo valore checkbox non rispettato (non manipolare in modo strano i dati)', 'danger')
        return redirect(url_for('signup'))

    if dao.get_user_by_username(username):
        flash('Username già in uso, scegline un altro!', 'danger')
        return redirect(url_for('signup'))

    if dao.get_user_by_email(email):
        flash('C\'è già un utente registrato con questa mail', 'danger')
        return redirect(url_for('signup'))

    usr_image = request.files['img_profile']
    if not usr_image:
        flash('Immagine obbligatoria, assicurati di averne inserita una', 'danger')
        return redirect(url_for('signup'))

    img = Image.open(usr_image)

    width, height = img.size
    new_width = PROFILE_IMG_HEIGHT * width / height
    size = new_width, PROFILE_IMG_HEIGHT
    img.thumbnail(size, Image.ANTIALIAS)

    left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
    top = 0
    right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
    bottom = PROFILE_IMG_HEIGHT

    img = img.crop((left, top, right, bottom))
    ext = usr_image.filename.split('.')[1]
    img_path = username.lower() + '.' + ext
    img.save('static/user/' + img_path)

    new_user = {
        "username": username,
        "password": generate_password_hash(password, method='sha256'),
        "img_path": img_path,
        "is_creator": is_creator,
        "firstname": firstname,
        "surname": surname,
        "email": email
    }

    if dao.put_user(new_user):
        flash('Utente creato correttamente', 'success')
        return redirect(url_for('home'))

    # remove user_img that we stored before the store of the user in the db
    os.remove('static/user/' + img_path)

    flash('Errore nella creazione del utente: riprova!', 'danger')
    return redirect(url_for('signup'))



# define SERIE page and function
@app.route('/serie/<int:serie_id>')
def single_serie(serie_id):
    serie = dao.get_serie(serie_id)

    if serie is None:
        return render_template('404.html'), 404

    episodes = dao.get_episodes(serie_id)   
    datetoday = datetime.today().strftime("%Y-%m-%d, %H:%M:%S")

    return render_template('serie.html', serie=serie, episodes=episodes, datetoday=datetoday)


@app.route('/serie/new', methods=['POST'])
@login_required
def put_serie():
    title = request.form.get('title')
    description = request.form.get('description')
    created_at = datetime.today().strftime("%Y-%m-%d, %H:%M:%S")
    category_id = int(request.form.get('category'))
    user_id = current_user.id

    if not current_user.is_creator:
        flash('Funzione disponibile solo ad acccount creator, crea nuovo account', 'danger')
        return redirect(url_for('home'))

    if len(title) < 5 or len(title) > 60:
        flash('Vincolo title len non rispettato', 'danger')
        return redirect(url_for('home'))    

    if len(description) < 30 or len(description) > 300:
        flash('Vincolo title len non rispettato', 'danger')
        return redirect(url_for('home'))

    if dao.get_category(category_id) is None:
        flash('Errore gestione categoria, riprova', 'danger')
        return redirect(url_for('home'))

    serie_image = request.files['img_serie']
    if not serie_image:
        flash('Immagine obbligatoria, assicurati di averne inserita una', 'danger')
        return redirect(url_for('home'))

    test_image = Image.open(serie_image)
    new_image = make_square(test_image)

    ext = serie_image.filename.split('.')[1]

    if ("jpg" not in ext) and ("png" not in ext) and ("webp" not in ext):
        flash('Accettati formati immagine solo jpg, png, webp', 'danger')
        return redirect(url_for('home'))

    img_path = str(int(dao.get_max_id_serie()['max_id']) + 1) + '.' + ext
    new_image.save('static/serie/' + img_path)

    new_serie = {
        'title': title,
        'description':  description,
        'created_at':   created_at,
        'category_id':  category_id,
        'user_id':      user_id,
        'img_path':     img_path
    }

    if dao.put_serie(new_serie):
        flash('Podcast creato correttamente', 'success')
    else:
        flash('Errore nella creazione del podcast: riprova!', 'danger')

    return redirect(url_for('home'))


@app.route('/serie/del', methods=['POST'])
@login_required
def del_serie():
    if current_user.is_creator:

        serie = dao.get_serie(request.form.get('serie_id'))
        episodes = dao.get_episodes(serie['id'])

        if current_user.id == serie['user_id'] and dao.del_serie(serie['id']):

            # delete dal db andata a buon fine, elimino i file presenti in static
            for episode in episodes:
                os.remove('static/episode/' + episode['audio_path'])
            os.remove('static/serie/' + serie['img_path'])

            flash('Podcast "' + serie['title'] +
                  '" eliminato correttamente!', 'success')
            return redirect(url_for('home'))

    flash('Errore nella eliminazione del podcast: riprova!', 'danger')
    return redirect(url_for('home'))


# define EPISODE page and function
@app.route('/episode/<int:episode_id>')
def single_episode(episode_id):
    episode = dao.get_episode(episode_id)

    if episode is None:
        return render_template('404.html'), 404

    comments = dao.get_comments(episode_id)

    return render_template('episode.html', episode=episode, comments=comments)


@app.route('/episode/new', methods=['POST'])
@login_required
def put_episode():
    title = request.form.get('title')
    description = request.form.get('description')
    posted_at = request.form.get('posted_at')
    serie_id = request.form.get('serie_id')

    audio = request.files['audio_episode']
    ext = audio.filename.split('.')[1]

    if not current_user.is_creator:
        flash('Funzione disponibile solo ad acccount creator, crea nuovo account', 'danger')
        return redirect(url_for('home'))

    if len(title) < 5 or len(title) > 200:
        flash('Vincolo title len non rispettato', 'danger')
        return redirect(url_for('home'))    

    if len(description) < 30 or len(description) > 300:
        flash('Vincolo title len non rispettato', 'danger')
        return redirect(url_for('home'))

    if posted_at < date.today().strftime('%Y-%m-%d'):
        flash('La data scelta non può essere antecedente a quella odierna', 'danger')
        return redirect(url_for('home'))

    if "mp3" not in ext:
        flash('Sono accettati solo file audio .mp3','danger')
        return redirect(url_for('home'))

    audio_path = serie_id + '_' + \
        str(int(dao.get_max_id_episode(serie_id)['max_id']) + 1) + '.' + ext
    audio.save('static/episode/' + audio_path)

    new_episode = {
        'title': title,
        'description':  description,
        'posted_at':    posted_at,
        'serie_id':     serie_id,
        'audio_path':   audio_path
    }

    # check if the current_user is the same creator of the podcast
    if current_user.id == dao.get_serie(serie_id)['user_id'] and dao.put_episode(new_episode):
        flash('Episodio creato correttamente', 'success')
    else:
        flash('Errore nella creazione del episodio: riprova!', 'danger')

    return redirect(url_for('single_serie', serie_id=serie_id))


@app.route('/episode/del', methods=['POST'])
@login_required
def del_episode():
    if current_user.is_creator:

        episode = dao.get_episode(request.form.get('episode_id'))
        serie = dao.get_serie(episode['serie_id'])

        if current_user.id == serie['user_id'] and dao.del_episode(episode['id']):

            os.remove('static/episode/' + episode['audio_path'])

            flash('Episodio "' + episode['title'] + '"del podcast "' +
                  serie['title'] + '"eliminato correttamente!', 'success')
            return redirect(url_for('single_serie', serie_id=episode['serie_id']))

    flash('Errore nella eliminazione del suddetto episodio del podcast: riprova!', 'danger')
    return redirect(url_for('single_serie', serie_id=episode['serie_id']))


# define COMMENT function
@app.route('/comment/new', methods=['POST'])
@login_required
def put_comment():
    content = request.form.get('content')
    episode_id = request.form.get('episode_id')

    if content == '':
        flash(
            'Commento non creato correttamente: il commento non può essere vuoto!', 'danger')
        return redirect(url_for('single_episode', episode_id=episode_id))

    posted_at = datetime.today().strftime("%Y-%m-%d, %H:%M:%S")

    new_comment = {
        'content':   content,
        'user_id':   current_user.id,
        'posted_at':   posted_at,
        'episode_id':   episode_id
    }

    if dao.put_comment(new_comment):
        flash('Commento creato correttamente', 'success')
    else:
        flash('Errore nella creazione del commento: riprova!', 'danger')

    return redirect(url_for('single_episode', episode_id=episode_id))


@app.route('/comment/del', methods=['POST'])
@login_required
def del_comment():
    comment_id = request.form.get('comment_id')
    comment = dao.get_comment(comment_id)

    if comment is not None and current_user.id == comment['user_id'] and dao.del_comment(comment_id):
        flash('Commento eliminato correttamente!', 'success')
    else:
        flash('Errore nella eliminazione del suddetto episodio del podcast: riprova!', 'danger')

    return redirect(url_for('single_episode', episode_id=comment['episode_id']))


@app.route('/favorite/new', methods=['POST'])
@login_required
def put_favorite():
    serie_id = int(request.form.get('serie_id'))

    if dao.put_favorite(serie_id, current_user.id):
        flash('Podcast aggiunto ai preferiti!', 'success')
    else:
        flash('Errore, podcast NON aggiunto ai preferiti!', 'danger')

    return redirect(url_for('home'))

@app.route('/favorite/del', methods=['POST'])
@login_required
def del_favorite():
    serie_id = request.form.get('serie_id')

    if dao.del_favorite(serie_id, current_user.id):
        flash('Podcast rimosso dai preferiti!', 'success')
    else:
        flash('Errore, podcast NON aggiunto ai preferiti!', 'danger')

    #grazie ad Angelo dal gruppo telegram IAW per la chicca di request.referrer così da non fare modifiche al form usato sia su account che home
    if 'account' in request.referrer:
        return redirect(url_for('account'))

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)


@login_manager.unauthorized_handler
@app.errorhandler(405)
def unauthorized(e):
    return render_template('405.html'), 405

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# ty to stackoverflow user 7311767 'stephen-rauch', some change from RGBA to RGB
def make_square(im, min_size=500, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))

    if size != min_size:
        return new_im.resize((min_size, min_size))

    return new_im
