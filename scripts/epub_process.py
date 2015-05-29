#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys, zipfile, os, shutil, glob, textwrap, re
#from os.path import join
from xml.etree import ElementTree as ET
import html5lib
import argparse
"""
(C) 2014 Andre Castro
License: [GPL3](http://www.gnu.org/copyleft/gpl.html)

Script changes the EPUB created by Pandoc, namely:
* Removes <sub> from footnotes, since these interferes with the iPad response, and use instead CSS rule: a.footnoteRef{ vertical-align: super; line-height: normal; font-size: 0.5em;}
* Replaces back arrows - '↩'' - with work 'back'. Some reading devices don't containt the character '↩''
* makes cover linear inside content.opf <spine>
"""

epubFilename = sys.argv[1]
# unzip ePub
fh = open(str(epubFilename), 'rb')
z = zipfile.ZipFile(fh)
for name in z.namelist():
    outpath = "temp"
    z.extract(name, outpath)
fh.close()
temp_dir="temp/"
os.remove(temp_dir+'mimetype') # delete mimetype (will be added later with epub.writestr)

def fn_rm_sup(tree, element): # Removes <sub> wrapper to footnotes
    for fn in tree.findall(element):
        for child in list(fn):
            if child.tag == 'sup':                
                number = child.text
                fn.remove(child)
                fn.text=number

def replace_fn_links(tree, element): # Replace back- arrows '↩'' with work "back"
    for parag in tree.findall(element):
        anchors = parag.findall("./a")
        for anchor in anchors:
            if '#fn'in anchor.get('href'):
                anchor.text = 'back'
   
def edit_spine(opf): # makes cover & title page linear in <spine>
    tree = ET.parse(opf)
    ET.register_namespace('epub', 'http://www.idpf.org/2007/ops')
    spine = tree.find('.//{http://www.idpf.org/2007/opf}spine')
    manifest = tree.find('.//{http://www.idpf.org/2007/opf}manifest')
    guide = tree.find('.//{http://www.idpf.org/2007/opf}guide')
    cover = ET.SubElement(guide, 'reference', attrib={'href':'cover.xhtml','title':'Cover','type':'title'}) # Add the cover as (title)element of guide: the cover becomes the first "page" the reader sees when starts reading
    return tree

def save_html(content_dir, content_file, tree ):
    doctype = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html>\n'
    html = ET.tostring(tree,  encoding='utf-8', method='xml')
    html = doctype + html
    xhtml_file = open(content_dir + content_file, "w") 
    xhtml_file.write(html) 
    xhtml_file.close()

temp_ls=os.listdir(temp_dir)
temp_ls.sort()

            
for f in temp_ls: #loop EPUB contained files
    if os.path.isfile(temp_dir + f):
        epubfile = temp_dir + f
        xhtml = open(epubfile, "r") 
        
        if f[:2]=='ch' and f[-6:]==".xhtml": # content files
            xhtml_parsed = html5lib.parse(xhtml, namespaceHTMLElements=False)
            fn_rm_sup(xhtml_parsed, './/a[@class="footnoteRef"]')
            replace_fn_links(xhtml_parsed, './/section[@class="footnotes"]/ol/li/p')    
            save_html( content_dir=temp_dir,
                       content_file=f,
                       tree=xhtml_parsed )

        elif f[-4:] == '.opf': # opf
            tree = edit_spine(epubfile)
            ET.register_namespace('', 'http://www.idpf.org/2007/opf')
            tree.write(epubfile, encoding='utf-8', xml_declaration='True' )
        
# Zip EPUB
epub = zipfile.ZipFile(epubFilename, "w")
epub.writestr("mimetype", "application/epub+zip")
def fileList(openEpubDir):
    matches = []
    for root, dirnames, filenames in os.walk(openEpubDir):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

openEpubDir_dirlist=fileList(temp_dir)
for name in openEpubDir_dirlist:
    path = name[5:] # removes 'temp/'
    epub.write(name, path, zipfile.ZIP_DEFLATED)

epub.close()
shutil.rmtree(temp_dir) 
print
print "** EPUB {epubfile} processed by epub_process.py without errors **".format(epubfile=epubFilename)

