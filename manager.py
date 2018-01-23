from flask_script import Manager, Server, Shell

from app import create_app


app = create_app('development')
manager = Manager(app)

manager.add_command('runserver', Server('127.0.0.1', port=5000))
manager.add_command('shell', Shell)


if __name__ == '__main__':
    manager.run()