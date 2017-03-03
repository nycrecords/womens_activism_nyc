import os
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
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import csv
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
    if featured:
        with open('csv/featured.csv', 'r') as csvfile:
            featured_csv = csv.reader(csvfile, delimiter= ';')
            next(featured_csv)  # skip the header
            row = next(featured_csv)

            story_id = row[0]
            quote = row[1]

            # disables the current featured story
            current_featured = None
            try:
                current_featured = Modules.query.filter_by(type=FEATURED, is_active=True).one()
            except NoResultFound:
                print("No featured module set")
            if current_featured is not None:
                current_featured.is_active = False
                db.session.commit()

            featured_story = Stories.query.filter_by(id=story_id).one()
            activist_first = featured_story.activist_first
            activist_last = featured_story.activist_last
            media_url = featured_story.image_url

            featured_module = Modules(story_id=story_id,
                                      type=FEATURED,
                                      title1=None,
                                      title2=None,
                                      activist_first=activist_first,
                                      activist_last=activist_last,
                                      content=quote,
                                      media_url=media_url,
                                      event_date=None,
                                      activist_year=None,
                                      is_active=True)
            create_object(featured_module)

            if current_featured is None:
                edit_featured_event = Events(_type=EDIT_FEATURED_STORY,
                                        module_id=featured_module.id,
                                        new_value=featured_module.val_for_events)
            else:
                edit_featured_event = Events(_type=EDIT_FEATURED_STORY,
                                             module_id=featured_module.id,
                                             previous_value=current_featured.val_for_events,
                                             new_value=featured_module.val_for_events)
            create_object(edit_featured_event)
            print("New featured story module set")
        csvfile.close()

if __name__ == '__main__':
    manager.run()

