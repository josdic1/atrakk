# export_data.py
from server import app
from extensions import db
from models import *
import json

def export_data():
    with app.app_context():
        data = {
            'statuses': [{'id': s.id, 'name': s.name} for s in Status.query.all()],
            'artists': [{'id': a.id, 'name': a.name} for a in Artist.query.all()],
            'tags': [{'id': t.id, 'name': t.name} for t in Tag.query.all()],
            'tracks': [{
                'id': t.id,
                'title': t.title,
                'artist_id': t.artist_id,
                'status_id': t.status_id,
                'tag_ids': [tag.id for tag in t.tags]
            } for t in Track.query.all()],
            'links': [{
                'track_id': l.track_id,
                'link_type': l.link_type,
                'link_url': l.link_url
            } for l in Link.query.all()]
        }
        
        with open('data_export.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Data exported to data_export.json")

if __name__ == '__main__':
    export_data()