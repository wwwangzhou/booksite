"""
WSGI config for gettingstarted project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

from booksite import app

application = app

# if __name__ == "__main__":
#     # main()
#     app.run(debug=True) #  python3 application.py REPLACEs flask run
