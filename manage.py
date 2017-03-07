import csv
import os

from flask import current_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import (
    Roles,
    Users,
    Stories,
    Tags,
    Comments,
    Events,
    Modules,
    Flags,
    Feedback
)
from app.constants.module import FEATURED
from app.db_utils import create_object
from app.constants.event import EDIT_FEATURED_STORY
from sqlalchemy.orm.exc import NoResultFound

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,
                db=db,
                Roles=Roles,
                Users=Users,
                Stories=Stories,
                Tags=Tags,
                Comments=Comments,
                Events=Events,
                Modules=Modules,
                Flags=Flags,
                Feedback=Feedback)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def es_recreate():
    """Recreate elasticsearch index and request docs."""
    from app.search.utils import recreate
    recreate()


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.option("-f", "--featured", help="Create featured story module.", action="store_true", dest='featured')
def modules(featured=False):
    """
    Manage function modules that inserts a single featured story entry to the modules table.
    Takes in a csv file with a story_id and a quote; delimiting by a semicolon.
    If current featured story module is_active, set it to false and set new featured story to true.
    """
    if featured:
        # open csv file
        with open(current_app.config['FEATURED_DATA'], 'r') as csvfile:
            featured_csv = csv.reader(csvfile, delimiter=';')
            next(featured_csv)  # skip the header
            row = next(featured_csv)

            story_id = row[0]
            quote = row[1]

            # disable current featured story
            try:
                current_featured = Modules.query.filter(Modules.type == FEATURED, Modules.is_active == True).one()
            except NoResultFound:
                current_featured = None
                print("No featured module set")

            previous_value = None
            if current_featured:
                current_featured.is_active = False
                previous_value = current_featured.val_for_events
                db.session.commit()

            # create and store object into Modules table
            new_featured_story = Stories.query.filter(Stories.id == story_id, Stories.is_visible == True).one()
            featured_module = Modules(story_id=story_id,
                                      type=FEATURED,
                                      activist_first=new_featured_story.activist_first,
                                      activist_last=new_featured_story.activist_last,
                                      content=quote,
                                      media_url=new_featured_story.image_url,
                                      is_active=True)
            create_object(featured_module)

            # create and store Events object
            edit_featured_event = Events(_type=EDIT_FEATURED_STORY,
                                         module_id=featured_module.id,
                                         previous_value=previous_value,
                                         new_value=featured_module.val_for_events)
            create_object(edit_featured_event)
            print("New featured story module set")
        csvfile.close()

if __name__ == '__main__':
    manager.run()

