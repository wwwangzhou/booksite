import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    b = open("books_test.csv")
    reader = csv.reader(b) # read b as csv file

    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book title is: {title} written by {author} in {year}.")

    books = db.execute("select * from books where year=1998;").fetchall()
    for book in books:
        print(f"Book found: title : {book.title} written by {book.author} in {book.year}.")

    db.commit()

if __name__ == "__main__":
    main()
