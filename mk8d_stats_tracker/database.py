import datetime

from tinydb import TinyDB, Query
from pathlib import Path

from mk8d_stats_tracker.config import Config
from mk8d_stats_tracker.util import tracks

class Database:
    def __init__(self):
        self.db_path = Path(Config.DB_PATH)
        self.db_path.mkdir(exist_ok=True)

        self.sessions = TinyDB(self.db_path / 'sessions.json')
        self.tracks = TinyDB(self.db_path / 'tracks.json')
        self.shared = TinyDB(self.db_path / 'shared.json')

        if not self.tracks.all():
            self.tracks.insert_multiple(tracks)

    def insert_current_session_date(self, date):
        self.shared.insert({'date': date, 'is_active': True})
    
    def deactivate_current_session(self):
        shared = self.shared.get(Query().is_active == True)
        shared['is_active'] = False
        self.shared.update(shared, doc_ids=[shared.doc_id])

    def get_current_session(self):
        shared = self.shared.get(Query().is_active == True)
        return shared.get('date')

    def get_session(self, user_id, date):
        return self.sessions.get((Query().user_id == user_id) & (Query().date == date))

    def start_session(self, user_id, date, start_vr):
        self.sessions.insert({'user_id': user_id, 'date': date, 'start_vr': start_vr, 'end_vr': None, 'races': []})

    def add_race(self, session, placement, track_name, cc_mode):
        if session:
            session['races'].append({'placement': placement, 'track_name': track_name, 'cc_mode': cc_mode})
            self.sessions.update(session, doc_ids=[session.doc_id])

db = Database()