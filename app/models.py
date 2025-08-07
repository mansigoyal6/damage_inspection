from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Inspection(db.Model):
    __tablename__ = 'inspections'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    inspected_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    damage_report = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'reviewed', 'completed', name='status_enum'), default='pending')
    image_url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('inspections', lazy=True))


def create_user(username, password):
    check_query = text('''SELECT id FROM users WHERE username = '{}' LIMIT 1'''.format(username))
    existing_user = db.session.execute(check_query).fetchone()
    if existing_user:
        return None
    password_hash = generate_password_hash(password)
    insert_query = text('''INSERT INTO users (username, password_hash) VALUES ('{}', '{}') '''.format(username, password_hash))
    result = db.session.execute(insert_query)
    db.session.commit()
    return result.lastrowid

def get_user_by_username(username):
    query = text('''SELECT id, username, password_hash FROM users WHERE username = '{}' LIMIT 1'''.format(username))
    result = db.session.execute(query).fetchone()
    if result:
        user = User()
        user.id = result[0]
        user.username = result[1]
        user.password_hash = result[2]
        return user
    return None

def create_inspection(vehicle_number, inspected_by, damage_report, image_url):
    now = datetime.utcnow()
    query = text('''INSERT INTO inspections (vehicle_number, inspected_by, damage_report, image_url, created_at)
        VALUES ('{}', {}, '{}', '{}', '{}')'''.format(vehicle_number, inspected_by, damage_report, image_url, now))
    result = db.session.execute(query)
    db.session.commit()
    return result.lastrowid

def get_inspection_by_id(inspection_id):
    query = text('''SELECT id, vehicle_number, inspected_by, damage_report, status, image_url, created_at
        FROM inspections WHERE id = {} LIMIT 1 '''.format(inspection_id))
    result = db.session.execute(query).fetchone()
    if result:
        inspection = Inspection()
        inspection.id = result[0]
        inspection.vehicle_number = result[1]
        inspection.inspected_by = result[2]
        inspection.damage_report = result[3]
        inspection.status = result[4]
        inspection.image_url = result[5]
        # Handle created_at as string or datetime
        created_at = result[6]
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            except:
                created_at = datetime.utcnow()
        inspection.created_at = created_at
        return inspection
    return None

def update_inspection_status(inspection_id, status, user_id):
    check_query = text('''select id FROM inspections WHERE id = {} AND inspected_by = {} LIMIT 1 '''.format(inspection_id, user_id))
    existing = db.session.execute(check_query).fetchone()
    if not existing:
        return False
    update_query = text('''update inspections SET status = '{}' WHERE id = {} AND inspected_by = {} '''.format(status, inspection_id, user_id))
    db.session.execute(update_query)
    db.session.commit()
    return True

def get_inspections_by_user(user_id, status=None):
    if status:
        query = text('''select id, vehicle_number, damage_report, status, image_url, created_at
        FROM inspections WHERE inspected_by = {} AND status = '{}' ORDER BY created_at DESC '''.format(user_id, status))
        results = db.session.execute(query).fetchall()
        if not results:
            return "No inspection exist with this status"
    else:
        query = text('''SELECT id, vehicle_number, damage_report, status, image_url, created_at
        FROM inspections WHERE inspected_by = {} ORDER BY created_at DESC '''.format(user_id))
        results = db.session.execute(query).fetchall()
    
    def format_created_at(created_at):
        if isinstance(created_at, str):
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                return dt.isoformat()
            except:
                return created_at
        elif isinstance(created_at, datetime):
            return created_at.isoformat()
        else:
            return str(created_at) if created_at else None
    
    return [
        {
            'id': row[0],
            'vehicle_number': row[1],
            'damage_report': row[2],
            'status': row[3],
            'image_url': row[4],
            'created_at': format_created_at(row[5])
        } for row in results
    ]

def check_inspection_status(inspection_id, user_id):
    query = text('''select status FROM inspections WHERE id = {} AND inspected_by = {} LIMIT 1 '''.format(inspection_id, user_id))
    result = db.session.execute(query).fetchone()
    return result[0] if result else None

def get_pending_inspections_count(user_id):
    query = text('''select count(*) FROM inspections where inspected_by = {} AND status = 'pending' '''.format(user_id))
    result = db.session.execute(query).fetchone()
    return result[0] if result else 0
