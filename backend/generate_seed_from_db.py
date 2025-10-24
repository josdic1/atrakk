from server import app
from models import Status, Artist, Tag, Track, Link

def generate_seed_file():
    """Generate seed.py from current database state"""
    
    with app.app_context():
        seed_content = """from server import app
from extensions import db
from models import Status, Artist, Tag, Track, Link

def seed_database():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()
        
"""
        
        # Get all statuses
        statuses = Status.query.all()
        if statuses:
            seed_content += "        # Statuses\n"
            seed_content += "        print('Seeding statuses...')\n"
            status_vars = {}
            for status in statuses:
                var_name = status.name.lower().replace(' ', '_')
                status_vars[status.id] = var_name
                seed_content += f"        {var_name} = Status(name='{status.name}')\n"
            seed_content += f"        db.session.add_all([{', '.join(status_vars.values())}])\n"
            seed_content += "        db.session.commit()\n\n"
        
        # Get all artists
        artists = Artist.query.all()
        if artists:
            seed_content += "        # Artists\n"
            seed_content += "        print('Seeding artists...')\n"
            artist_vars = {}
            for artist in artists:
                var_name = artist.name.lower().replace(' ', '_').replace('/', '_').replace("'", "")
                artist_vars[artist.id] = var_name
                safe_name = artist.name.replace("'", "\\'")
                seed_content += f"        {var_name} = Artist(name='{safe_name}')\n"
            seed_content += f"        db.session.add_all([{', '.join(artist_vars.values())}])\n"
            seed_content += "        db.session.commit()\n\n"
        
        # Get all tags
        tags = Tag.query.all()
        if tags:
            seed_content += "        # Tags\n"
            seed_content += "        print('Seeding tags...')\n"
            tag_vars = {}
            for tag in tags:
                var_name = tag.name.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                tag_vars[tag.id] = var_name
                seed_content += f"        {var_name} = Tag(name='{tag.name}')\n"
            seed_content += f"        db.session.add_all([{', '.join(tag_vars.values())}])\n"
            seed_content += "        db.session.commit()\n\n"
        
        # Get all tracks
        tracks = Track.query.all()
        if tracks:
            seed_content += "        # Tracks\n"
            seed_content += "        print('Seeding tracks...')\n"
            track_vars = {}
            for track in tracks:
                var_name = track.title.lower().replace(' ', '_').replace('/', '_').replace("'", "").replace('-', '_')
                track_vars[track.id] = var_name
                status_var = status_vars.get(track.status_id, 'demo')
                artist_var = artist_vars.get(track.artist_id, 'artist')
                safe_title = track.title.replace("'", "\\'")
                seed_content += f"        {var_name} = Track(\n"
                seed_content += f"            title='{safe_title}',\n"
                seed_content += f"            artist_id={artist_var}.id,\n"
                seed_content += f"            status_id={status_var}.id\n"
                seed_content += f"        )\n"
            seed_content += f"        db.session.add_all([{', '.join(track_vars.values())}])\n"
            seed_content += "        db.session.commit()\n\n"
            
            # Add track-tag relationships
            has_tags = any(track.tags for track in tracks)
            if has_tags:
                seed_content += "        # Track-Tag Relationships\n"
                seed_content += "        print('Adding tags to tracks...')\n"
                for track in tracks:
                    if track.tags:
                        track_var = track_vars[track.id]
                        for tag in track.tags:
                            tag_var = tag_vars[tag.id]
                            seed_content += f"        {track_var}.tags.append({tag_var})\n"
                seed_content += "        db.session.commit()\n\n"
        
        # Get all links
        links = Link.query.all()
        if links:
            seed_content += "        # Links\n"
            seed_content += "        print('Seeding links...')\n"
            link_vars = []
            for i, link in enumerate(links):
                link_var = f"link_{i+1}"
                link_vars.append(link_var)
                track_var = track_vars.get(link.track_id, 'track')
                safe_url = link.link_url.replace("'", "\\'")
                seed_content += f"        {link_var} = Link(\n"
                seed_content += f"            track_id={track_var}.id,\n"
                seed_content += f"            link_type='{link.link_type}',\n"
                seed_content += f"            link_url='{safe_url}'\n"
                seed_content += f"        )\n"
            seed_content += f"        db.session.add_all([{', '.join(link_vars)}])\n"
            seed_content += "        db.session.commit()\n\n"
        
        # Add footer
        seed_content += """        print('✅ Database seeded successfully!')

if __name__ == '__main__':
    seed_database()
"""
        
        # Write to seed.py
        with open('seed.py', 'w') as f:
            f.write(seed_content)
        
        print("✅ seed.py generated from current database!")
        print("\nTo seed the database, run:")
        print("  python seed.py")

if __name__ == '__main__':
    generate_seed_file()