from django.shortcuts import render
from .models import (
        Book, Music, MultimediaImage
)
from crew.models import Crew


def book_list(request):
    books = Book.objects.all()
    book_ids = list(map(lambda book: book['id'], books))
    multimedia_images = MultimediaImage.objects.filter(multimedia_id__in=book_ids)
    for book in books:
        multimedia_image = multimedia_images.filter(multimedia_id=book['id']).first()
        if multimedia_image:
            book['thumbnail'] = multimedia_image.thumb150x150.url
        else:
            book['thumbnail'] = ''
    return render(request, 'multimedia/book_list.html', {'multimedia': books, 'multimedia_type': 'Book'})


def book_detail(request, isbn13):
    book = Book.objects.get(isbn13=isbn13)

    multimedia_images = MultimediaImage.objects.filter(multimedia_id=book['id'])
    image = multimedia_images.first()
    book['thumbnail'] = image.thumb250x250.url if image else None

    return render(request, 'multimedia/book_detail.html', {'book': book})

def music_list(request):
    musics = Music.objects.all()

    for music in musics:
        crews = Crew.objects.filter(multimedia_id=music['id'])
        music['crews'] = crews

        multimedia_image = MultimediaImage.objects.filter(multimedia_id=music['id']).first()
        if multimedia_image:
            music['thumbnail'] = multimedia_image.thumb150x150.url
        else:
            music['thumbnail'] = ''

    return render(request, 'multimedia/music_list.html', {'multimedia': musics, 'multimedia_type': 'Music'})

def music_detail(request, music_id):
    music = Music.objects.get(id=music_id)
    crews = Crew.objects.filter(multimedia_id=music_id)
    music['crews'] = crews

    multimedia_images = MultimediaImage.objects.filter(multimedia_id=music['id'])
    image = multimedia_images.first()
    music['thumbnail'] = image.thumb250x250.url if image else None

    return render(request, 'multimedia/music_detail.html', {'music': music})
