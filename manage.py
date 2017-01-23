from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from db import db

app = create_app()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server(port=5555))
manager.add_command('db', MigrateCommand)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)

    def __init__(self, title):
        self.title = title

    def json(self):
        return {"title": self.title}

@manager.command
def populatedb():
    for i in range(10):
        db.session.add(Course('title-{}'.format(i)))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
