# EternalDraft
A Django app for basic stat tracking and analysis for Eternal Drafts.

/new_deck/ allows you to submit a decklist  
/decks/ shows the list of submitted decks  
/card_stats/ shows how well each card has performed historically  

# Setup

```
pip install django-bootstrap3  (https://django-bootstrap3.readthedocs.io/en/latest/installation.html)
cd <project_dir>
django-admin startproject almostmatt .  
git submodule add https://github.com/AlmostMatt/EternalDraft.git  
```

add `'EternalDraft',` and `'bootstrap3'`, to settings.py INSTALLED_APPS  
add `url(r'^eternal/', include('EternalDraft.urls')),` to almostmatt/urls.py  

```
python manage.py migrate
python manage.py runserver
```

127.0.0.1:8000/eternal/
