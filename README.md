# Pedaparc

Plateforme de sessions pédagogiques

## install

precond : install python3-venv

```
git clone https://github.com/PnCevennes/Pedaparc-pub
cd Pedaparc-pub
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## configuration

Rename file **config.py.sample** -> **config.py and complete** :

- LDAP informations
- Mail informations
- DB informations

You can add or remove tags **carefully** in **models/__init__.py** and add or remove the linked images in **static/ressources**
Replace the **static/ressources/favicon.png** for personalization.

Then :

```
cd Pedaparc
source venv/bin/activate
python
>>> import models
>>> models.pop_refs_thes()
>>> models.pop_thes()
```

## run (development mode)

```
	rundev.sh
. venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=server.py
flask run
```

## run (server mode)

```
	run.sh
kill $(cat pedaparc.pid)
source venv/bin/activate
gunicorn --daemon -b '0.0.0.0:4800' --pid=pedaparc.pid --error-log=./errors.log server:app
```
