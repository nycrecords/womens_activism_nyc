#!/usr/bin/env python
import os
<<<<<<< .merge_file_HrjkV1
from App import create_app
from App.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Post=Post, Tag=Tag, Post_Tag=PostTag,
                Comment=Comment, CommentEdit=CommentEdit, Role=Role, User=User, Post_Edit=PostEdit, Flag=Flag, Feedback=Feedback)
=======
from App import create_app, db
from App.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


current_app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(current_app)
migrate = Migrate(current_app, db)


def make_shell_context():
    return dict(current_app=current_app, db=db, User=User)
>>>>>>> .merge_file_MUzR88
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
