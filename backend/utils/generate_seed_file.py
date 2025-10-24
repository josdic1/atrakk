import csv

def generate_seed_file():
    """Read CSVs and generate a seed.py file with hardcoded data"""
    
    seed_content = """from server import app
from extensions import db
from models import Status, Artist, Tag, Track, Link

def seed_database():
    with app.app_context():
        print("Clearing database...")
        db.drop_all()
        db.create_all()
        
"""
    
    # Read and generate statuses
    seed_content += "        # Statuses\n"
    seed_content += "        print('Seeding statuses...')\n"
    with open('exports/status.csv', 'r') as f:
        reader = csv.DictReader(f)
        status_vars = []
        for row in reader:
            var_name = row['name'].lower().replace(' ', '_')
            status_vars.append(var_name)
            seed_content += f"        {var_name} = Status(name='{row['name']}')\n"
        seed_content += f"        db.session.add_all([{', '.join(status_vars)}])\n"
        seed_content += "        db.session.commit()\n\n"
    
    # Read and generate artists
    seed_content += "        # Artists\n"
    seed_content += "        print('Seeding artists...')\n"
    with open('exports/artists.csv', 'r') as f:
        reader = csv.DictReader(f)
        artist_vars = []
        for row in reader:
            var_name = row['name'].lower().replace(' ', '_').replace('/', '_')
            artist_vars.append(var_name)
            seed_content += f"        {var_name} = Artist(name='{row['name']}')\n"
        seed_content += f"        db.session.add_all([{', '.join(artist_vars)}])\n"
        seed_content += "        db.session.commit()\n\n"
    
    # Read and generate tags
    seed_content += "        # Tags\n"
    seed_content += "        print('Seeding tags...')\n"
    with open('exports/tags.csv', 'r') as f:
        reader = csv.DictReader(f)
        tag_vars = []
        for row in reader:
            var_name = row['name'].lower().replace(' ', '_').replace('/', '_')
            tag_vars.append(var_name)
            seed_content += f"        {var_name} = Tag(name='{row['name']}')\n"
        seed_content += f"        db.session.add_all([{', '.join(tag_vars)}])\n"
        seed_content += "        db.session.commit()\n\n"
    
    # Read and generate tracks
    seed_content += "        # Tracks\n"
    seed_content += "        print('Seeding tracks...')\n"
    with open('exports/tracks.csv', 'r') as f:
        reader = csv.DictReader(f)
        track_vars = []
        track_data = []
        for row in reader:
            var_name = row['title'].lower().replace(' ', '_').replace('/', '_')
            track_vars.append(var_name)
            track_data.append(row)
            
            # Map status_id to variable name
            status_map = {1: 'demo', 2: 'in_progress', 3: 'completed', 4: 'released'}
            status_var = status_map.get(int(row['status_id']), 'demo')
            
            # Get artist variable (assuming first artist for now)
            artist_var = artist_vars[int(row['artist_id']) - 1]
            
            seed_content += f"        {var_name} = Track(\n"
            seed_content += f"            title='{row['title']}',\n"
            seed_content += f"            artist_id={artist_var}.id,\n"
            seed_content += f"            status_id={status_var}.id\n"
            seed_content += f"        )\n"
        seed_content += f"        db.session.add_all([{', '.join(track_vars)}])\n"
        seed_content += "        db.session.commit()\n\n"
    
    # Read and generate track-tag relationships
    seed_content += "        # Track-Tag Relationships\n"
    seed_content += "        print('Adding tags to tracks...')\n"
    with open('exports/track_tags.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            track_var = track_vars[int(row['track_id']) - 1]
            tag_var = tag_vars[int(row['tag_id']) - 1]
            seed_content += f"        {track_var}.tags.append({tag_var})\n"
        seed_content += "        db.session.commit()\n\n"
    
    # Read and generate links
    seed_content += "        # Links\n"
    seed_content += "        print('Seeding links...')\n"
    link_vars = []
    with open('exports/links.csv', 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            track_var = track_vars[int(row['track_id']) - 1]
            link_var = f"link_{i+1}"
            link_vars.append(link_var)
            seed_content += f"        {link_var} = Link(\n"
            seed_content += f"            track_id={track_var}.id,\n"
            seed_content += f"            link_type='{row['link_type']}',\n"
            seed_content += f"            link_url='{row['link_url']}'\n"
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
    
    print("✅ seed.py generated successfully!")
    print("Run: python seed.py")

if __name__ == '__main__':
    generate_seed_file()