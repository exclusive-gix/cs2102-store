from django.db import connection
from django.db import models
from django.core.urlresolvers import reverse

from .utils import (
    dictfetchall, dictfetchone
)

class MovieManager(models.Manager):
    def all(self):
        movies = []
        with connection.cursor() as c:
            c.execute('''
                SELECT m.id, m.name, description, duration, price, o.name AS studio
                FROM movie mo, multimedia m, organisation o
                WHERE mo.multimedia_id = m.id
                  AND m.organisation_id = o.id
            ''')

            for movie in dictfetchall(c):
                movies.append(movie)

        for movie in movies:
            movie['url'] = reverse('multimedia:movie_detail', args=(movie['id'],))
        return movies

    def get(self, *args, **kwargs):
        with connection.cursor() as c:
            c.execute('''
                SELECT 
                  m.id, 
                  m.name, 
                  description,
                  duration,  
                  price, 
                  o.name AS studio
                FROM 
                  movie mo, 
                  multimedia m, 
                  organisation o
                WHERE mo.multimedia_id = m.id
                  AND m.organisation_id = o.id
                  AND m.id = %s
            ''', [kwargs['id'], ])
            return dictfetchone(c)

class ApplicationManager(models.Manager):
    def all(self):
        applications = []
        with connection.cursor() as c:
            c.execute('''
                SELECT m.id, m.name, description, version, price, o.name AS developer
                FROM application a, multimedia m, organisation o
                WHERE a.multimedia_id = m.id
                  AND m.organisation_id = o.id
            ''')

            for application in dictfetchall(c):
                applications.append(application)

        for application in applications:
            application['url'] = reverse('multimedia:application_detail', args=(application['id'],))
        return applications

    def get(self, *args, **kwargs):
        with connection.cursor() as c:
            c.execute('''
                SELECT 
                  m.id, 
                  m.name, 
                  description, 
                  version, 
                  price, 
                  o.name AS developer
                FROM 
                  application a, 
                  multimedia m, 
                  organisation o
                WHERE a.multimedia_id = m.id
                  AND m.organisation_id = o.id
                  AND m.id = %s
            ''', [kwargs['id'], ])
            return dictfetchone(c)

class BookManager(models.Manager):
    def all(self):
        books = []
        with connection.cursor() as c:
            c.execute('''
                SELECT m.id, m.name, description, isbn13, isbn10, price, o.name AS publisher
                FROM book, multimedia m, organisation o
                WHERE book.multimedia_id = m.id
                  AND m.organisation_id = o.id
            ''')

            for book in dictfetchall(c):
                books.append(book)

        for book in books:
            book['url'] = reverse('multimedia:book_detail', args=(book['id'],))
        return books

    def get(self, *args, **kwargs):
        with connection.cursor() as c:
            c.execute('''
                SELECT m.id, m.name, description, isbn13, isbn10, price, o.name AS publisher
                FROM book, multimedia m, organisation o
                WHERE book.multimedia_id = m.id
                  AND m.organisation_id = o.id
                  AND book.multimedia_id = %s
            ''', [kwargs['id']])
            return dictfetchone(c)

    def delete(self, *args, **kwargs):
        with connection.cursor() as c:
            c.execute('''
                DELETE FROM multimedia
                WHERE id = %s
            ''', [kwargs['id'], ])

class MusicManager(models.Manager):
    def all(self):
        items = []
        with connection.cursor() as c:
            c.execute('''
                SELECT
                  mul.id AS id,
                  mul.name AS name,
                  a.name AS album,
                  price,
                  o.name AS organisation
                FROM multimedia mul, music mus, album_music am, album a, organisation o
                WHERE mul.id = mus.multimedia_id
                  AND am.music_id = mus.multimedia_id
                  AND am.album_id = a.id
                  AND mul.organisation_id = o.id
            ''')

            for item in dictfetchall(c):
                items.append(item)

        for item in items:
            item['url'] = reverse('multimedia:music_detail', args=(item['id'],))

        return items

    def get(self, *args, **kwargs):
        with connection.cursor() as c:
            c.execute('''
                SELECT
                  mul.id AS id,
                  mul.name AS name,
                  a.name AS album,
                  description,
                  duration,
                  price,
                  o.name AS organisation
                FROM multimedia mul, music mus, album_music am, album a, organisation o
                WHERE mul.id = mus.multimedia_id
                  AND am.music_id = mus.multimedia_id
                  AND am.album_id = a.id
                  AND mul.organisation_id = o.id
                  AND mul.id = %s;
            ''', [kwargs['id'], ])
            return dictfetchone(c)
