from flask_migrate import MigrateCommand
from flask_script import Manager

from app import createapp

app = createapp()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()