import re

import markdown

from bs4 import BeautifulSoup

from py3o.template import Template

from werkzeug.utils import secure_filename

import os
import os.path

import shutil
import config

def md_to_text(markdown_text):
    html = markdown.markdown(markdown_text)

    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code>', ' ', html)

    soup = BeautifulSoup(html, 'html.parser')
    text = ''.join(soup.find_all(string=True))

    return text


def render_file(animation=None, sequences=None, medias=None, tags=None, outil=None, path=None):
    try:
        os.mkdir(path)
    except Exception as e:
        pass

    if animation and sequences:

        secure_name = secure_filename(animation.titre)

        filepath = path + '/' + secure_name + '.odt'

        template = Template('static/modeles/py3o_animation.odt', 
            filepath)

        data = dict(animation=animation, sequences=sequences, tags=tags)

        template.render(data)
        for media in medias:
            try:
                shutil.copy(media.url,re.sub(config.UPLOAD_FOLDER, path, media.url))
            except Exception:
                pass

    elif outil:

        secure_name = secure_filename(outil.nom)
        filepath = path + '/' + secure_name + '.odt'

        template = Template('static/modeles/py3o_outil.odt',
            filepath)

        data = dict(outil=outil)

        template.render(data)

        if outil.url:
            shutil.copy(outil.url,re.sub(config.UPLOAD_FOLDER, path, outil.url))
        
    else:
        raise ValueError('render_file: (animation et sequences) ou (outil) doit être fourni')