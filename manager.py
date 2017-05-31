'''
set up a manager
to provide supoort for 
running python shell scripts to set up  and update database
'''
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from twitterapp import app, twitter_db

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, twitter_db)
manager = Manager(app)
# add the db command to the manager, so that we can run the migration from the command line
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
