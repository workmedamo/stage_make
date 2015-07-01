# Makefile for INC hybrid publications
alldocx=$(wildcard docx/*.docx)
allmarkdown=$(filter-out md/book.md md/tmp.md, $(shell ls md/*.md))
django=$(shell ./scripts/find_module.py django) # system has django? If True, then run ./scripts/md_urlize.py md/book.md in book.md rule

test: $(allmarkdown)
	echo "start" ; 
	echo $(allmarkdown) ; 
	echo "end" ;

folders:
	mkdir docx/ ; \
	mkdir md/ ; \
	mkdir md/imgs/ ; \
	mkdir icml/ ; \
	mkdir lib/ ; \

markdown:$(alldocx) # convert docx to md
	for i in $(alldocx) ; \
	do md=md/`basename $$i .docx`.md ; \
	pandoc $$i \
	       	--from=docx \
		--to=markdown \
	       	--atx-headers \
		--template=template.markdown \
		-o $$md ; \
	./scripts/md_unique_footnotes.py $$md ; \
	done

icml: book.md
	for i in md/book.md ; \
	do icml=icml/`basename $$i .md`.icml ; \
	./scripts/md_stripmetada.py $$i > md/tmp.md ; \
	pandoc md/tmp.md \
		--from=markdown \
		--to=icml \
		--self-contained \
		-o $$icml ; \
	done

book.md: clean $(allmarkdown)
	for i in $(allmarkdown) ; \
	do ./scripts/md_unique_footnotes.py $$i  > md/tmp.md ; \
	./scripts/md_stripmetada.py md/tmp.md >> md/book.md ; \
	done
ifeq (True, $(django))
	echo $(django) ; \
         ./scripts/md_urlize.py md/book.md
endif


book.epub: clean book.md epub/metadata.xml epub/styles.epub.css epub/cover.jpg
	cd md && pandoc \
		--from markdown \
		--to epub3 \
		--self-contained \
		--epub-chapter-level=1 \
		--epub-stylesheet=../epub/styles.epub.css \
		--epub-cover-image=../epub/cover.jpg \
		--epub-metadata=../epub/metadata.xml \
		--default-image-extension png \
		--toc-depth=1 \
		-o ../book.epub \
		book.md ; \
		cd .. ; 


webpage:  clean book.md 	
	cd md && pandoc \
		--from markdown \
		--to html5 \
		--self-contained \
        -o ../webpage.html \
        book.md ;\
        cd .. ;


clean:  # remove outputs
	rm -f md/book.md  
	rm -f book.epub 
	rm -f *~ */*~  #emacs files
# improve rule: if file exits, then remove
