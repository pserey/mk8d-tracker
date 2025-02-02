import datetime

from tinydb import TinyDB, Query
from pathlib import Path

from mk8d_stats_tracker.config import Config

class Database:
    def __init__(self):
        self.db_path = Path(Config.DB_PATH)
        self.db_path.mkdir(exist_ok=True)

        self.sessions = TinyDB(self.db_path / 'sessions.json')
        self.tracks = TinyDB(self.db_path / 'tracks.json')

    def get_session(self, user_id, date):
        return self.sessions.get((Query().user_id == user_id) & (Query().date == date))

    def start_session(self, user_id, date, start_vr):
        self.sessions.insert({'user_id': user_id, 'date': date, 'start_vr': start_vr, 'races': []})

    def add_race(self, user_id, placement, track_name):
        today = datetime.date.today().isoformat()
        session = self.get_session(user_id, today)
        print(session)

        if session:
            session['races'].append({'placement': placement, 'track_name': track_name})
            self.sessions.update(session, doc_ids=[session.doc_id])

db = Database()
Session = Query()