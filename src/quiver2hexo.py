#!~/.pyenv/shims/python3
# -*- coding: utf-8 -*-
import os, argparse, json, re
from datetime import datetime
from distutils import file_util

parser = argparse.ArgumentParser(
    description="Convert quiver notes/notebooks to hexo markdown")
parser.add_argument('from_path', help='Path to quiver note/notebook')
parser.add_argument('to_path', help='Path to hexo _posts dir')
parser.add_argument('--categories', nargs='?', help='Set categories for output markdowns')


# ---
# title: Title
# date: %Y-%m-%d %H:%M:%S
# tags: tag1 tag2
# categories: Notes(default)
# ---

qiniu_domain = 'http://7xrgcf.com1.z0.glb.clouddn.com'

def gen_valid_filename(filename):
    return re.sub(r':*\s+|/','-', filename.lower())

def fetch_hexomd_filename(content):
    cell = content['cells'][0]
    cdata = cell['data']
    begin = cdata.find('<') + 4
    end = cdata.rfind('>') - 2

    # Set the first cell of quiver note as hexo markdown file name
    if begin < len(cdata) and end > 0:
        filename = cdata[begin:end]
    else:
        print('First cell of quiver note should provide'
              'file name like this: \'<!--file-name-->\''
              )
    return gen_valid_filename(filename)



def gen_hexomd_template(meta, categories):
    title = meta['title']
    create_date = datetime.fromtimestamp(meta['created_at'])
    tags = meta['tags']
    categories = categories if categories else 'Notes'
    return ('---\n'
            'title: \'%s\'\n'
            'date: %s\n'
            'tags: %s\n'
            'categories: %s\n'
            '---\n' %
            (title,
             create_date.strftime('%Y-%m-%d %H:%M:%S'),
             tags,
             categories
            ))

def note_to_md(meta, content, md_filename):
    md_content = ''
    resources = []
    for cell in content['cells'][1:]:
        ctype = cell['type']
        cdata = cell['data']
        if ctype == 'markdown':
            resources.extend([ x[0] for x in re.findall('quiver-image-url\/(.*\.(png|jpg))', cdata) ])
            md_content += '\n%s\n' % cdata.replace('quiver-image-url',qiniu_domain + '/' + md_filename)
        elif ctype == 'code':
            md_content += '\n```\n%s\n```\n' % cdata
        else:
            md_content += '\n%s\n' % cdata

    # Add <!--more--> at proper position
    # Use an object to help with replacing the nth occurence of pattern string
    class NthRepl:
        def __init__(self, nth, repl):
            self.nth = nth
            self.repl = repl
            self.call_time = 0
        def __call__(self, match_obj):
            self.call_time += 1
            if self.call_time == self.nth:
                return match_obj.group(1) + self.repl
            return match_obj.group(0)
    # Replace 7th occurence of '\n' not stated with [{}$\] with '<!--more-->'
    md_content = re.sub(r'([^{}\$\\])(\n)', NthRepl(5, '\n<!--more-->'), md_content)
    return md_content, resources


def export_note_to_hexo_path(from_path, to_path, categories):
    print('Processing qvnote:',from_path)
    meta = json.loads(open(os.path.join(from_path, 'meta.json'), 'r').read())
    content = json.loads(open(os.path.join(from_path, 'content.json'), 'r').read())

    md_filename = fetch_hexomd_filename(content)

    md_tpl = gen_hexomd_template(meta, categories)
    md_content, resources = note_to_md(meta, content, md_filename)

    # write markdown content to hexo post dir
    with open(os.path.join(to_path, md_filename + '.md'), 'w') as f:
        f.write(md_tpl + md_content)
    print('Write markdown content to',os.path.join(to_path,md_filename + '.md'))

    if resources:
        # make dir for resources, resources stored in to_path/static/img/md_filenmame/
        res_dirpath = os.path.join(to_path, 'static', 'img', md_filename)
        if not os.path.exists(res_dirpath):
            os.mkdir(res_dirpath)
            print('Make dir for resources:',res_dirpath)

        # copy resources to corresponding dir of the note
        if os.path.exists(res_dirpath):
            for f in resources:
                file_util.copy_file(os.path.join(from_path, 'resources', f), os.path.join(res_dirpath, f))
                print('Copy', f, 'to resources dir')

def export_notebook_to_hexo_path(from_path, to_path, categories=None):
    print('Processing qvnotebook:',from_path)
    for note_name in [x for x in os.listdir(from_path) if os.path.splitext(x)[1] == '.qvnote']:
        export_note_to_hexo_path(os.path.join(from_path, note_name), to_path, categories)

def main(args):
    from_path = args.from_path
    to_path = args.to_path
    categories = args.categories
    if os.path.splitext(from_path)[1] == '.qvnotebook':
        export_notebook_to_hexo_path(from_path, to_path, categories)
    elif os.path.splitext(from_path)[1] == '.qvnote':
        export_note_to_hexo_path(from_path, to_path, categories)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
















