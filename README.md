# A  a book review website
- https://bookees.herokuapp.com/
- A website that let user register and log in and allows user search and write reviews for a particular book and see the reviews made by others.
- Bookees is a place for you note segements from books when you feel like these words entails wisdom after daily reading.

- Utilized Python Framework Flask to set up server, and used a third-party API by Goodreads, another book review website, to allow users browse a broader set of reviews.

## To run on local host
- set envirotonal variable FLASK_APP 
        
        export FLASK_APP=application.py
        
- set debug mode for development

        export FLASK_ENV=development 
- run
        flask run
## To set up virtual environment
- make a virtual enviroment 

        virtualenv bookees_env
        
- activate the virtual enviroment 

        source bookees_env/bin/activate
        
- to exit the current virtual enviroment 

        deactivate
        
 - to intall all packages used in this project 

        pip install -r requirements.txt 
        
  - to delete the virtual enviroment  <br>

        rm -rf bookees_env     
           
## To create database in terminal using SQLite or psql
- import modesl and db from booksite package

       from booksite.models import User, Post
       from booksite import db 
- create database

       db.create_all()
        
- to make query

       User.query.all()

- to get the first entry
        
        User.query.first()


- to get specific entry

        user = User.query.filter_by(username="Wang Zhou").all()
  
- to access user's properity 
        
        user.id
        user.username

- to save changes

         db.session.commit()
         
- reset db

        db.drop_all()
        db.create_all()
           
## Deploy on Heroku
- check database url and make sure it is set to the the psql url on heroku
  
        heroku config
- create an file **Procfile** @ your repo directory booksite with the line below:
        
        web: gunicorn booksite.wsgi
        
- create wsgi.py @ your repo sub-directory booksite
- more info at https://devcenter.heroku.com/articles/python-gunicorn
