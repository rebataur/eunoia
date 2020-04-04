# Eunoia.uno

A playground for Entrepreneurs to evolve, refine, validate and structure their product ideas

## Brainstorm
Empathise with users and Brainstorm ideas around topic, like them, mark them as your strength, take feedback

## Ideate
Ideate and Validate your brainstomed ideas using Design Thinking, incubate, productize or put them in attic

## Execute
Add features, prioritize, add tasks to feature, adapt based on new information and execute using kanban board

## Installation

We offer a hosted version with more features, but for solopreneurs or enthusiast you can run this on your own
as a Django application

* Clone this project
* Make sure your Virtualenv is setup 
* Setup email notifications in settings.py otherwise you can
  lookup the registration url in the console and register yourself
```bash
# On Windows
(venv)C:\eunoia>
SET EUNOIA_ENV='LOCAL'
cd eunoiaproject
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.