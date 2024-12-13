from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# ===========================================================
# Предметна областть: бібліотека - жанр, автор, та книга
# ===========================================================

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"<Genre id={self.id} name={self.name}>"

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    
    books = relationship("Book", back_populates="author", cascade="all, delete")

    def __repr__(self):
        return f"<Author id={self.id} name={self.name}>"

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", lazy="joined")

    def __repr__(self):
        return f"<Book id={self.id} title={self.title} author_id={self.author_id} genre_id={self.genre_id}>"

engine = create_engine('sqlite:///library.db', echo=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ===========================================================
# 1. Insert models in the database
# ===========================================================
genre_fiction = Genre(name="Fiction")
genre_scifi = Genre(name="Science Fiction")
author_asimov = Author(name="Isaac Asimov")
author_orwell = Author(name="George Orwell")

session.add_all([genre_fiction, genre_scifi, author_asimov, author_orwell])
session.commit() 

book_foundation = Book(title="Foundation", author=author_asimov, genre=genre_scifi)
book_1984 = Book(title="1984", author=author_orwell, genre=genre_fiction)

session.add_all([book_foundation, book_1984])
session.commit()

print("=== After Insertion ===")
all_books = session.query(Book).all()
print("All books:", all_books)


# ===========================================================
# 2. Get models by ID from the database
# ===========================================================
book_id = book_foundation.id
book_by_id = session.query(Book).filter_by(id=book_id).first()
print(f"Book with id={book_id}:", book_by_id)


# ===========================================================
# 3. Updating models
# ===========================================================
book_1984.title = "Nineteen Eighty-Four"
session.commit()

print("=== After Updating ===")
updated_book = session.query(Book).filter_by(id=book_1984.id).first()
print("Updated book:", updated_book)


# ===========================================================
# 4. Retrieve a list of all models
# ===========================================================
all_authors = session.query(Author).all()
all_genres = session.query(Genre).all()
print("All authors:", all_authors)
print("All genres:", all_genres)


# ===========================================================
# 5. Delete models
# ===========================================================
session.delete(book_foundation)
session.commit()

print("=== After Deletion of a Book ===")
all_books_after_deletion = session.query(Book).all()
print("Books after deletion:", all_books_after_deletion)


# ===========================================================
# 6. Delete models with relationships using cascades
# ===========================================================
book_robot = Book(title="I, Robot", author=author_asimov, genre=genre_scifi)
session.add(book_robot)
session.commit()

print("=== Before Cascade Deletion of Author Asimov ===")
all_books = session.query(Book).all()
print("All books:", all_books)

session.delete(author_asimov)
session.commit()

print("=== After Cascade Deletion of Author Asimov ===")
all_books = session.query(Book).all()
print("All books:", all_books)
