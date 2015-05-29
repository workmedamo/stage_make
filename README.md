# Hybrid Publishing Resources

## Description
This repository consists of a collection of resources aimed at the development hybrid publications, in both reflowable format (EPUB3) and fixed layout ([Scribus](wiki.scribus.net) and inDesign structured content). 
The resources propose a workflow based on the conversion between markup languages, using [Pandoc](http://johnmacfarlane.net/pandoc/) and [Markdown](http://daringfireball.net/projects/markdown/) source-files as its essential elements.
Most of the ideas materialized in this collections of resources originated from the [Digital Publishing Toolkit](http://networkcultures.org/digitalpublishing/) research project, specially the cotnributions of [Michael Murtaugh](http://automatist.org/) and [Silvio Lorusso](http://silviolorusso.com/).

Note: The section "6.3. Do-it-yourself EPUB using Pandoc" form [http://networkcultures.org/blog/publication/from-print-to-ebooks-a-hybrid-publishing-toolkit-for-the-arts/](From Print to Ebooks) is an important complement to this set of tools.

----

This repository is a small effort towards systematizing, automating and document a workflow for creating hybrid publications.
Don't hesitate to use, change, or comment upon these tools. Drop me a line, I'd love to hear your feedback.

André Castro 2015

<http://pinknoi.so/>

andre[At]andrecastro[dot]info

----


## Clone
`git clone --branch master https://github.com/DigitalPublishingToolkit/Hybrid-Publication-Resources.git`

`cd Hybrid-Publishing-Resources`

`rm -r .git`


## Dependencies
* Pandoc
* Make (on Mac XCode includes a Make package)
* Python 2
   * html5lib
   * Django (optional, it is used to urlize links in markdown file)

## Steps
The conversion from a manuscript to the desired outputs consists in a series of steps:
* 1. **.docx - Manuscript** - (manually) edit the manuscript according to the INC style guide
* 2. **Markdown - Source** - convert the manuscript files to Markdown files.
* 3.1. **ICML files for inDesign** - convert the individual Markdown source into ICML files that can be imported into inDesign
* 3.2. **HTML files for Scribus** - convert the individual Markdown source into HTML files that can be imported into Scribus
* 4.1. **EPUB Output** -convert the Markdown source files into an EPUB

![](http://networkcultures.org/wp-content/uploads/2015/02/workflow.png)


## 0. Folder structure
`make folders` creates the folder structure necessary to make use of the Hybrid Publishing Resources.

The following folders will be generated, which later will be used to store:
* manuscript files: .docx -> docx/
* generated files: Markdowns -> md/, ICMLs -> icml/, HTMLs for Scribus -> sribus_html/

Other folders were already there:
* epub/ for storing resources for the EPUB (cover, metadata, CSS stylesheet) and scripts/   
* script/ for the various scripts

Here is how the file tree looks like:
`
├── docx
├── epub
│   ├── cover.jpg
│   ├── metadata.xml
│   └── styles.epub.css
├── icml
├── lib
├── makefile
├── md
│   └── imgs
├── README.md
├── scribus_html
├── scripts
│   ├── epub_process.py
│   ├── find_module.py
│   ├── md_stripmetada.py
│   ├── md_unique_footnotes.py
│   └── md_urlize.py
├── template.markdown
└── template.scribus
`

## 1.  Manuscript: .docx
This is a preparatory stage. Yet it is highly important for the series of conversions that will lead to the different outputs.

You can be editing the .docx document - the manuscript - using **styles**, as to add a structures (headings, footnotes, blockquotes, etc), that will be preserved through the different conversion stages and into its outputs.

## 2. Markdown source
`make markdown` converts all the `.docx` files inside the `docx/ `folder into Markdown files inside `md/`.

The resulting Markdown files will become the **source files**, from which all of the publication's outputs will be generated.

Markdown was chosen as a source format based on easiness by which Markdown is both written and read, the high compatibility with other markup languages (HTML, ICML, LaTex), and its explicit structure.

### 2.1 Images in Markdown
If the publication contains images, at this stage, you should insert the images into the Markdown files.

The images should be save in the `md/imgs/` folder and inserted into the Markdown files: `![My image caption](imgs/myImage.jpg)`

### 2.2 Metadata in Markdown
Each Markdown file contains a **metadata header**. You either fill the fields with the corresponding information or ignore them.

You can alter the metadata fields and values by editing its template: `template.markdown`

## 3.1 ICML for inDesign
`make icml` converts the Markdown source files into ICML files (in `icml/`), that can be imported (placed) into inDesign.

ICML files are useful, since they ensure that the structural information from the Markdown source files remains present in an inDesign, and content and structure to remain updatable, even when the ICML is placed in a inDesign project. This connection between source and output (Markdown and inDesign project) is only possible if in the inDesign project, the **link to the source ICML is maintained**, meaning that the content has to be layout using paragraph and chapter styles, instead of intervening into the text.

Note: **malformed hyperlinks**  will cause problems (crashes) when imported into inDesign. Keep an eye for malformed hyperlinks in the Markdown sources.

## 3.2 HTML for Scribus
`make scribus` converts the Markdown source files, into HTML files (in `scribus_html/`) that can be imported by Scribus, since Scribus can import HTML wrapped only by a `<body>` tag.

To import an HTML files into Scribus you need to use the `Insert -> Insert Text Frame` tool.
Use it to select the space the text will occupy. Inside that space do a mouse right-click, select the option `Get Text` and import the HTML file. 

A list of HTML tags supported by Scribus can be found in <http://wiki.scribus.net/canvas/Help:Manual_Importhtml>.

# 4. Outputs
## 4.0 book.md
`make book.md` is a step essential to the creation of the EPUB, as it gathers onto `book.md`, content from all the Markdown source files inside the `md/` folder, in alphabetical order (00 to ZZ). However, you **don't have to perform this step**, as the Makefile does it for you every time you generate an EPUB.

## 4.1 EPUB
`make book.epub` creates the EPUB `book.epub`.

### Essential resources:
To produce an EPUB a few files come into play, namely: the cover image, metadata, stylesheet, and fonts.
* `epub/metadata.xml` -  EPUB metadata
* `epub/styles.epub.css`  - EPUB css stylesheet 
* `epub/cover.jpg`  - EPUB cover

These files will strongly influence the EPUB's outcome, consequently they **must be edited** for each publication.

### Fonts:
`lib/` store the custom fonts which will be used in the EPUB

Note: **If you choose to use fonts**, make sure to change the Makefile, as to include the fonts in book.epub rule.
Also remember include the font on th EPUB CSS stylesheet with `@font-face` rule



## A Circular Process
It is unlikely that the first time you go through this process of conversions, you'll achieve a satisfactory EPUB.
You might have to go through of a iterative process of editing (content, structure, styles, and metadata), make book.epub, view the result, a few time times, until you are happy with the result. 

## EPUB check
The health of the generate EPUB can be checked with [http://validator.idpf.org/](http://validator.idpf.org/)






