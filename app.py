#!/usr/bin/python3
"""this is where flask runs the app"""

from Tana import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)