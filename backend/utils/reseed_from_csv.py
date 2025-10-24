import csv
from server import app
from extensions import db
from models import User, Status, Artist, Tag, Track, Link

def reseed_from_csv():
    with app.app_context():
        # Clear existing data
        print("Clearing database...")
        db.drop_all()
        db.create_all()
        
        # Read and seed statuses
        print("Seeding statuses...")
        with open('exports/status.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = Status(name=row['name'])
                status.id = int(row['id'])  # Preserve IDs
                db.session.add(status)
        
        # Read and seed artists
        print("Seeding artists...")
        with open('exports/artists.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                artist = Artist(name=row['name'])
                artist.id = int(row['id'])
                db.session.add(artist)
        
        # Read and seed tags
        print("Seeding tags...")
        with open('exports/tags.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tag = Tag(name=row['name'])
                tag.id = int(row['id'])
                db.session.add(tag)
        
        db.session.commit()
        
        # Read and seed tracks
        print("Seeding tracks...")
        with open('exports/tracks.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                track = Track(
                    title=row['title'],
                    artist_id=int(row['artist_id']),
                    status_id=int(row['status_id'])
                )
                track.id = int(row['id'])
                db.session.add(track)
        
        db.session.commit()
        
        # Read and seed links
        print("Seeding links...")
        with open('exports/links.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                link = Link(
                    track_id=int(row['track_id']),
                    link_type=row['link_type'],
                    link_url=row['link_url']
                )
                link.id = int(row['id'])
                db.session.add(link)
        
        # Read and seed track-tag relationships (many-to-many!)
        print("Seeding track-tag relationships...")
        with open('exports/track_tags.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                track = Track.query.get(int(row['track_id']))
                tag = Tag.query.get(int(row['tag_id']))
                track.tags.append(tag)
        
        db.session.commit()
        
        print("\n✅ Database reseeded successfully from CSVs!")
        print(f"- {User.query.count()} users")
        print(f"- {Status.query.count()} statuses")
        print(f"- {Artist.query.count()} artists")
        print(f"- {Tag.query.count()} tags")
        print(f"- {Track.query.count()} tracks")
        print(f"- {Link.query.count()} links")

if __name__ == '__main__':
    reseed_from_csv()