# Quiver2hexo
Export Quiver note/notebook to hexo blog post folder.

This simple script helps with coping with markdown filename, images, tags and categories
when exporting your quvier note/notebook to markdown files that can be published in hexo blog.

## Usage
`python3 quver2hexo.py from_path to_path [--categories categories]`

- from_path should be a file with extension .qvnote or .qvnotebook
- The exported markdown files will be placed in to_path/
- The images will be placed in to_path/static/img/markdown_filename/

### Hexo Blog Post Hierarchy
```text
_posts
|-- note1.md
|   |-- static
|   |   |-- img
|   |   |   |-- note1
|   |   |   |   |-- img_of_note1_1.png
```

## Features
### Filename
It's not always proper to set the title of Quiver note as our markdown filename,
especially when it's written in non-English language. Unfortunatelly, Quiver names
its notes after a unique hash string without providing a feature to set the filename of notes.

Thus the first cell of a note is used to set the exported markdown filename like this: 
```
<!--filename-->
```

### Images
Since CDN(e.g. Qiniu) is always used as the image link provider for markdown files, all the 
image link(quiver-image-url/xxx.png) in Quiver note will be changed into this format: cdn_domain/markdown_filename/imgname

Then what you need to do is to upload all images in to_path/static/img to CDN, with using foldername
as a prefix, e.g. markdown_filename/imgname. Tools such as [qshell by qiniu](https://github.com/qiniu/qshell)
can help you do this easily.

### Tags and Categories
Tags in quiver will be exported to markdown files and categories can be set with 
optional argument(Default categories of exported markdown file is 'Notes').

### Read More Tag
A 'Read More' tag(`<!--more-->`) will be inserted into a proper position of the exported markdown file.

## Thanks
Inspired by [quiver2jekyll](https://github.com/zxteloiv/quiver2jekyll) of [Haruki Kirigaya](https://github.com/zxteloiv)
