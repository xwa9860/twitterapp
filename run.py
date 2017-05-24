from app import app
import os

if __name__ == '__main__':
    print(os.environ.get('APP_SETTINGS'))
    app.run()
