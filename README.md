# A  a book review website
- A website that let user register and log in and allows user search and write reviews for a particular book and see the reviews made by others.

- Utilized Python Framework Flask to set up server, and used a third-party API by Goodreads, another book review website, to allow users browse a broader set of reviews.

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
           
## To create database in terminal using SQLite
- import modesl from booksite package

       from booksite.models import User, Post
        
- create locak db file

       db.create_all()
        
- to make query

       User.query.all()
           
           
