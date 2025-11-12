from flask import Flask, request, jsonify, session, render_template
from extensions import db, bcrypt, ma, cors
from models import User, user_schema, users_schema, Status, status_schema, statuses_schema, Artist, artist_schema, artists_schema, Track, track_schema, tracks_schema, Link, link_schema, links_schema, Tag, tag_schema, tags_schema
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Handle Render's PostgreSQL URL format
database_url = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db.init_app(app)
bcrypt.init_app(app)
ma.init_app(app)

# Update CORS for production - allow multiple origins
allowed_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://localhost:5555').split(',')
cors.init_app(app, supports_credentials=True, origins=allowed_origins)
# ================ USER ================ #


# REGISTER #
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(username=username)
        user.password_hash = password
        
        db.session.add(user)
        db.session.commit()
        
        # Store user data in session
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({
            'message': 'User created successfully',
            'user': {'id': user.id, 'username': user.username}
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")  # This will show in terminal
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

# LOGIN #
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.authenticate(password):
        session['user_id'] = user.id
        session['username'] = user.username  # Add this line
        return jsonify({
            'message': 'Logged in successfully',
            'user': {'id': user.id, 'username': user.username}
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

# LOGOUT #
@app.route('/logout', methods=['POST'])
def logout():    
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'}), 200  

# CHECK SESSION #
@app.route('/check-session')
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'logged_in': True,
                'user': {'id': user.id, 'username': user.username}
            })
    return jsonify({'logged_in': False, 'user': {}})


# ================ ARTISTS ================ #

# GET ALL ARTISTS #
@app.route('/artists', methods=['GET'])
def get_all_artists():
    artists = Artist.query.all()
    return artists_schema.jsonify(artists), 200

# GET ARTIST BY ID #
@app.route('/artists/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return artist_schema.jsonify(artist), 200   

# CREATE ARTIST #
@app.route('/artists', methods=['POST'])
def create_artist():
    data = request.get_json()
    name = data.get('name')

    new_artist = Artist(name=name)
    db.session.add(new_artist)
    db.session.commit()

    return artist_schema.jsonify(new_artist), 201

# DELETE ARTIST #
@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):    
    artist = Artist.query.get_or_404(artist_id)
    db.session.delete(artist)
    db.session.commit()

    return jsonify({'message': 'Artist deleted'}), 200


# ================ TRACKS ================ #

# GET ALL TRACKS #
@app.route('/tracks', methods=['GET'])
def get_all_tracks():
    tracks = Track.query.order_by(Track.updated_at.desc()).all()
    return tracks_schema.jsonify(tracks), 200

# GET TRACK BY ID #
@app.route('/tracks/<int:track_id>', methods=['GET'])
def get_track(track_id):
    track = Track.query.get(track_id)
    return track_schema.jsonify(track), 200

# CREATE TRACK #
@app.route('/tracks', methods=['POST'])
def create_track():
    data = request.get_json()
    title = data.get('title')
    artist_id = data.get('artist_id')
    status_id = data.get('status_id')

    new_track = Track(title=title, artist_id=artist_id, status_id=status_id)
    db.session.add(new_track)
    db.session.commit()

    return track_schema.jsonify(new_track), 201

# UPDATE TRACK #
@app.route('/tracks/<int:track_id>', methods=['PATCH'])
def update_track(track_id):
    track = Track.query.get_or_404(track_id)
    data = request.get_json()
    
    if 'title' in data:
        track.title = data['title']
    if 'artist_id' in data:
        track.artist_id = data['artist_id']
    if 'status_id' in data:
        track.status_id = data['status_id']
    
    db.session.commit()
    return track_schema.jsonify(track), 200

# DELETE TRACK #
@app.route('/tracks/<int:track_id>', methods=['DELETE'])
def delete_track(track_id):
    track = Track.query.get_or_404(track_id)
    db.session.delete(track)
    db.session.commit()
    
    return jsonify({'message': 'Track deleted'}), 200


# ================ LINKS ================ #

# GET ALL LINKS FOR A TRACK #
@app.route('/tracks/<int:track_id>/links', methods=['GET'])
def get_track_links(track_id):
    links = Link.query.filter_by(track_id=track_id).all()
    return links_schema.jsonify(links), 200

# CREATE A LINK FOR A TRACK #
@app.route('/tracks/<int:track_id>/links', methods=['POST'])
def create_link(track_id):
    data = request.get_json()
    link_type = data.get('link_type')
    link_url = data.get('link_url')
    
    new_link = Link(track_id=track_id, link_type=link_type, link_url=link_url)
    db.session.add(new_link)
    db.session.commit()
    
    return link_schema.jsonify(new_link), 201

# DELETE A LINK #
@app.route('/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    
    return jsonify({'message': 'Link deleted'}), 200


# ================ TAGS ================ #

# GET ALL TAGS #
@app.route('/tags', methods=['GET'])
def get_all_tags():
    tags = Tag.query.all()
    return tags_schema.jsonify(tags), 200

# CREATE A TAG #
@app.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()
    name = data.get('name')
    
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    
    return tag_schema.jsonify(new_tag), 201

# ADD TAG TO TRACK #
@app.route('/tracks/<int:track_id>/tags/<int:tag_id>', methods=['POST'])
def add_tag_to_track(track_id, tag_id):
    track = Track.query.get_or_404(track_id)
    tag = Tag.query.get_or_404(tag_id)
    
    track.tags.append(tag)
    db.session.commit()
    
    return track_schema.jsonify(track), 200

# REMOVE TAG FROM TRACK #
@app.route('/tracks/<int:track_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_track(track_id, tag_id):
    track = Track.query.get_or_404(track_id)
    tag = Tag.query.get_or_404(tag_id)
    
    track.tags.remove(tag)
    db.session.commit()
    
    return track_schema.jsonify(track), 200


# ================ COMMAND CENTER ================ #

# DISPLAY #
@app.route('/command-center')
def command_center():
    return render_template('command_center.html')

# HEALTH CHECK #
@app.route('/command/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'users_count': User.query.count()
    }), 200

# WHO'S LOGGED IN #
@app.route('/command/sessions', methods=['GET'])
def check_sessions():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify({
            'logged_in': True,
            'user': user_schema.dump(user)
        }), 200
    return jsonify({'logged_in': False}), 200

# SHOW ALL USERS #
@app.route('/command/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify({
        'count': len(users),
        'users': users_schema.dump(users)
    }), 200

# SHOW ALL DATA #
@app.route('/command/data', methods=['GET'])
def show_all_data():
    users = User.query.all()
    statuses = Status.query.all()
    artists = Artist.query.all()
    tracks = Track.query.all()
    links = Link.query.all()
    tags = Tag.query.all()
    
    return jsonify({
        'users': users_schema.dump(users),
        'statuses': statuses_schema.dump(statuses),
        'artists': artists_schema.dump(artists),
        'tracks': tracks_schema.dump(tracks),
        'links': links_schema.dump(links),
        'tags': tags_schema.dump(tags)
    }), 200

# NUKE DB #
@app.route('/command/nuke', methods=['POST'])
def nuke_database():
    db.drop_all()
    return jsonify({'message': 'Database nuked!'}), 200

# RESET DB #
@app.route('/command/reset', methods=['POST'])
def reset_database():
    db.drop_all()
    db.create_all()
    return jsonify({'message': 'Database reset!'}), 200

# SEED DATABASE #
@app.route('/command/seed', methods=['POST'])
def seed_database():
    import os
    import subprocess
    
    # Check if seed.py exists
    seed_file = os.path.join(os.path.dirname(__file__), 'seed.py')
    
    if not os.path.exists(seed_file):
        return jsonify({
            'error': '❌ seed.py not found',
            'message': 'seed.py does not exist in the backend folder'
        }), 404
    
    try:
        # Run seed.py
        result = subprocess.run(
            ['python', 'seed.py'],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({
                'message': '✅ Database seeded successfully!',
                'output': result.stdout
            }), 200
        else:
            return jsonify({
                'error': '❌ Seed script failed',
                'message': result.stderr
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'error': '❌ Seed timeout',
            'message': 'Seeding took too long (>30s)'
        }), 500
    except Exception as e:
        return jsonify({
            'error': '❌ Seed error',
            'message': str(e)
        }), 500

# CONTEXT RUN #
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5555)