import random
import sys

from datacenter.models import *
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def fix_marks(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=name)
    except MultipleObjectsReturned:
        print("С таким именем есть несколько учеников. Требуется уточнениею")
        return
    except Schoolkid.DoesNotExist:
        print("Не найден ученик с таким именем!")
        return
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=name)
    except MultipleObjectsReturned:
        print("С таким именем есть несколько учеников. Требуется уточнениею")
        return
    except Schoolkid.DoesNotExist:
        print("Не найден ученик с таким именем!")
        return
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(name, lesson):
    compliments = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Очень обрадовал!',
        'Именно этого я давно ждал',
        'Сказано здорово – просто и ясно!',
        'Как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
        ]
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=name)
    except MultipleObjectsReturned:
        print("С таким именем есть несколько учеников. Требуется уточнениею")
        return
    except Schoolkid.DoesNotExist:
        print("Не найден ученик с таким именем!")
        return
    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter
    try:
        subject = Subject.objects.get(title__icontains=lesson, year_of_study=year_of_study)
    except Subject.DoesNotExist:
        print("Нет такаого предмета в школе")
        return
    commendations = Commendation.objects.filter(schoolkid=schoolkid,
        subject=subject)
    lucky_days = []
    for commendation in commendations:
        lucky_days.append(commendation.created)
    selected_lessons = Lesson.objects.filter(year_of_study=year_of_study,
        group_letter=group_letter, subject=subject).exclude(date__in=lucky_days)
    lucky_lesson = random.choice(selected_lessons)
    text = random.choice(compliments)
    created = lucky_lesson.date
    teacher = lucky_lesson.teacher
    Commendation.objects.create(text=text, created=created, schoolkid=schoolkid,
        subject=subject, teacher=teacher)
