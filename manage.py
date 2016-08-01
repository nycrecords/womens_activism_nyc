#!/usr/bin/env python
import os
<<<<<<< HEAD
from App import create_app
from App.models import *
=======
from app import create_app
from app.models import *
>>>>>>> remotes/origin/feature/WOM-12_2
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Post=Post, Tag=Tag, Post_Tag=PostTag,
<<<<<<< HEAD
                Comment=Comment, CommentEdit=CommentEdit, Role=Role, User=User, Post_Edit=PostEdit, Flag=Flag, Feedback=Feedback)
=======
                Comment=Comment, CommentEdit=CommentEdit, User=User, Post_Edit=PostEdit, Flag=Flag, Feedback=Feedback)
>>>>>>> remotes/origin/feature/WOM-12_2
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
