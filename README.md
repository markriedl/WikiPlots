# WikiPlots

The WikiPlots corpus is a collection of 112,936 story plots extracted from English language [Wikipedia](https://en.wikipedia.org/wiki/Main_Page). These stories are extracted from any English language article that contains a sub-header that contains the word "plot" (e.g., "Plot", "Plot Summary", etc.).

This repository contains code and instructions for how to recreate the WikiPlots corpus.

The dataset itself can be downloaded from here: [*plots.zip*](https://www.dropbox.com/s/24pa44w7u7wvtma/plots.zip?dl=0) (updated: 09/26/2017). The zip file contains two files:

- *plots*: a text file containing all story plots. Each story plot is given with one sentence per line. Each story is followed by `<EOS>` on a line by itself.
- *titles*: a text file containing a list of titles for each article in whih a story plot was found and extracted.

## Using the code to recreate the corpus

I have also included the Python script used to extract the story plots.

wikiPlots.py requires:
- An English Wikipedia dump
- [Wikiextractor](https://github.com/attardi/wikiextractor)
- The [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) library

To use wikiPlots.py:

1. Download an [English Wikipedia dump](https://dumps.wikimedia.org/enwiki/). From this link you will find a file named something like "enwiki-20170401-pages-articles-multistream.xml.bz2". Make sure you download the .bz2 file that is **not** the index file.
2. Unzip the bz2 file to extract the .xml file.
3. Download [wikiextractor](https://github.com/attardi/wikiextractor). You do not need to set it up. Run it as follows:


python wikiextractor.py -o output_directory --json --html -s enwiki-...xml


You must run wikiextractor.py with these parameters. wikiPlots.py requires json files with nested html and with section header information preserved. Wikiextractor will produce a number of subfolders named "AA", "AB", "AC"... Within each folder will be a wiki_xx file containing a number of json records, one per article.

4. [Install the BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) python package
5. Download and run wikiPlots.py from this repository:

python wikiPlots.py wiki_dump_directory plot_file_name title_file_name

`wiki_dump_directory` should be the path to the directory containing the "AA", "AB", etc. folders. `plot_file_name` will be the name of the file that will contain the story plots. `title_file_name` will be the name of the file that will contain the list of story titles.
