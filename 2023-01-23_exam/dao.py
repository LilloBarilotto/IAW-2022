import sqlite3
# not import of datetime because the insert of the string date in the correct format is verified by "app.py"
# la delete di elementi legati da foreign key (i commenti di un ep cancellato o gli ep di una serie cancellata) sono gestiti attraverso delle ON DELETE CASCADE

# Operation on table "serie"


def get_series():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM serie'
    cursor.execute(sql)
    series = cursor.fetchall()

    cursor.close()
    conn.close()

    return series


def put_serie(serie):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO serie(title,description,img_path, category_id, created_at, user_id) VALUES(?,?,?,?,?,?)'

    try:
        cursor.execute(
            sql, (serie['title'], serie['description'], serie['img_path'], serie['category_id'], serie['created_at'], serie['user_id']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def get_serie(serie_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT serie.id, serie.title, serie.created_at, serie.description, serie.img_path, serie.user_id, user.username, user.img_path AS user_img_path FROM serie LEFT JOIN user ON serie.user_id = user.id WHERE serie.id = ?'
    cursor.execute(sql, (serie_id,))
    serie = cursor.fetchone()

    cursor.close()
    conn.close()

    return serie


def del_serie(serie_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM serie WHERE serie.id = ?'

    try:
        cursor.execute(
            sql, (serie_id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def get_max_id_serie():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT IFNULL(MAX(id), 0) AS max_id FROM serie'
    cursor.execute(sql)
    serie = cursor.fetchone()

    cursor.close()
    conn.close()

    return serie


# Operation on table "episode"
def get_episodes(serie_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM episode WHERE episode.serie_id = ? ORDER BY posted_at ASC'
    cursor.execute(sql, (serie_id,))
    episodes = cursor.fetchall()

    cursor.close()
    conn.close()

    return episodes


def get_episode(episode_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT episode.id, episode.title, episode.description, episode.audio_path, episode.posted_at, episode.serie_id, serie.title AS serie_title, serie.img_path, serie.user_id FROM episode INNER JOIN serie ON serie.id = episode.serie_id WHERE episode.id = ?'
    cursor.execute(sql, (episode_id,))
    episode = cursor.fetchone()

    cursor.close()
    conn.close()

    return episode


def get_max_id_episode(serie_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT IFNULL(MAX(id), 0) AS max_id FROM episode WHERE serie_id = ?'
    cursor.execute(sql, (serie_id,))
    episode = cursor.fetchone()

    cursor.close()
    conn.close()

    return episode


def put_episode(episode):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO episode(title,description, audio_path, posted_at, serie_id) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(
            sql, (episode['title'], episode['description'], episode['audio_path'], episode['posted_at'], episode['serie_id']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def del_episode(episode_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM episode WHERE episode.id = ?'

    try:
        cursor.execute(
            sql, (episode_id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# Operation on table "comment"
def get_comments(episode_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT comment.id, comment.posted_at, comment.content, user.username, comment.user_id, user.img_path AS user_img_path  FROM comment INNER JOIN user ON comment.user_id = user.id WHERE comment.episode_id = ? ORDER BY posted_at DESC'
    cursor.execute(sql, (episode_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return comments


def get_comment(comment_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM comment WHERE comment.id = ?'
    cursor.execute(sql, (comment_id,))
    comment = cursor.fetchone()

    cursor.close()
    conn.close()

    return comment


def put_comment(comment):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO comment(content, posted_at, episode_id, user_id) VALUES(?,?,?,?)'

    try:
        cursor.execute(
            sql, (comment['content'], comment['posted_at'], comment['episode_id'], comment['user_id']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def del_comment(comment_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM comment WHERE comment.id = ?'

    try:
        cursor.execute(
            sql, (comment_id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# Operation on table "user"
def get_user(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM user WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def put_user(user):

    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO user(username,password,img_path, is_creator, email, firstname, surname) VALUES(?,?,?,?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['username'], user['password'], user['img_path'], user['is_creator'], user['email'], user['firstname'], user['surname']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


def get_user_by_username(username):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM user WHERE username = ?'
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


def get_user_by_email(email):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM user WHERE email = ?'
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# Operation on table "category"
def get_categories():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM category'
    cursor.execute(sql)
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return categories


def get_category(category_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM category WHERE id = ?'
    cursor.execute(sql, (category_id,))
    category = cursor.fetchone()

    cursor.close()
    conn.close()

    return category


# Operation on table "favorite" and "serie"
def put_favorite(serie_id, user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO favorite(user_id, serie_id) VALUES (?,?)'

    try:
        cursor.execute(
            sql, (user_id, serie_id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def del_favorite(serie_id, user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM favorite WHERE serie_id = ? AND user_id = ?'

    try:
        cursor.execute(
            sql, (serie_id, user_id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_fav_series_by_user(user_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM favorite WHERE user_id = ?'
    cursor.execute(sql, (user_id,))
    series = cursor.fetchall()

    cursor.close()
    conn.close()

    return series