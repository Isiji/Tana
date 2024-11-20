#!/usr/bin/python3
"""this is where flask runs the app"""

from Tana import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
