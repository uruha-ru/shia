import glob
import os
import shutil
import datetime

from jinja2 import Environment, FileSystemLoader
import yaml

# Delete output directory if exists
if (os.path.isdir("./output")):
    shutil.rmtree("./output")

# Copy Static Directory
shutil.copytree("./templates/static", "./output")

generated_site = {'pages': [], 'baseurl': 'https://uruha.ru/shia/',
                  'now': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}

SITENAMEMAP = {
    'spotify': 'Spotify',
    'musicbrainz': 'MusicBrainz',
    'ragtag-archive': 'Ragtag Archive',
}

with open("history.yaml", 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("history.html")

    for lang in data['outputs'].keys():
        data['i_title'] = data['page-title'][lang]
        data['i_path'] = data['outputs'][lang].replace('index', '')
        data['i_baseurl'] = generated_site['baseurl']

        data['i_lang'] = lang

        for h in data['history']:
            h['i_title'] = h['title'][lang]

            if 'embed' in h:
                if 'type' in h['embed']:
                    tmp = h['embed']
                    h['embed'] = []
                    h['embed'].append(tmp)

                for e in h['embed']:
                    if e['type'] == 'tweet':
                        if lang in e:
                            e['i_html'] = e[lang]
                        else:
                            e['i_html'] = e['ja']

        with open("./output/{}.html".format(data['outputs'][lang]), 'w', encoding='utf-8') as fe:
            generated_site['pages'].append(data['i_path'])
            fe.write(template.render(data))

with open("discography.yaml", 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

    env = Environment(loader=FileSystemLoader("./templates"))
    template = env.get_template("discography.html")

    for lang in data['outputs'].keys():
        data['i_title'] = data['page-title'][lang]
        data['i_path'] = data['outputs'][lang].replace('index', '')
        data['i_baseurl'] = generated_site['baseurl']

        data['i_lang'] = lang

        for h in data['discography']:
            h['i_title'] = h['title'][lang]
            for link in h['links']:
                link['name'] = SITENAMEMAP[link['type']]

        output = "./output/{}.html".format(data['outputs'][lang])
        os.makedirs(os.path.dirname(output), exist_ok=True)
        with open(output, 'w', encoding='utf-8') as fe:
            generated_site['pages'].append(data['i_path'])
            fe.write(template.render(data))


sitemap_template = env.get_template("sitemap.xml")
with open("./output/sitemap.xml", 'w', encoding='utf-8') as f:
    f.write(sitemap_template.render(generated_site))
