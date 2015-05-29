---
Title: title of the work
Author: name(s) of author(s)
Date: date of publishing
...

$if(titleblock)$
$titleblock$

$endif$
$for(header-includes)$
$header-includes$

$endfor$
$for(include-before)$
$include-before$

$endfor$

$body$
$for(include-after)$

$include-after$
$endfor$
