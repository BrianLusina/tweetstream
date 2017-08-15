import better_exceptions
import os
from app import create_app
from flask_script import Manager, Shell, Server
from click import echo, style

# this will setup the environment variables before the application is setup
if os.path.exists(".env"):
    echo(style(text=">>>> Importing environment variables", fg="green", bold=True))
    for line in open(".env"):
        var = line.strip().split("=")
        if len(var) == 2:
            os.environ[var[0]] = var[1]

cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# import models with app context
# this prevents the data from the db from being deleted on every migration
# with app.app_context():
#     from app.models import *

manager = Manager(app)
server = Server(host="127.0.0.1", port=5000)


def make_shell_context():
    return dict(app=app)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command("runserver", server)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverage')

        # generate html report
        cov.html_report(directory=covdir)

        # generate xml report
        cov.xml_report()

        print('HTML version: file://%s/index.html' % covdir)
        print("XML version: file://%s" % basedir)
        cov.erase()


if __name__ == '__main__':
    manager.run()
