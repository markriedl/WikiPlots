# WikiPlots

This repository holds the WikiPlot dataset, containing 116,945 story plots extracted from English language [Wikipedia](https://en.wikipedia.org/wiki/Main_Page). These stories are extracted from any English language article that contains a sub-header that contains the word "plot" (e.g., "Plot", "Plot Summary", etc.)

The *plots* file contains each story with one sentence per line. Each story is followed by <EOS> on a line by itself.

``
Charley finds herself with her memory wiped and caught in one of the Celestial Toymaker's games
To make matters worse, the Eighth Doctor has been turned into a ventriloquist's dummy as a part of the game and can only communicate to a limited degree with Charley
<EOS>
Venugopal (Ranga Rao) and Janaki (Devika) are a couple in love
They soon have a baby boy, with much excitement
During the boy's childhood, he contracts tuberculosis
His family consults their doctor (Nagaiah) to obtain the best possible treatment for him and they decide to send him to Europe with a pilot (Nagesh)
During their journey the pilot suffers a sudden heart attack, and the plane crashes in the desert
The boy has to face several obstacles and finally survives to reunite with his family
<EOS>
``

The *titles* file contains a list of articles in the story plots were found and extracted.

## wikiPlots.py

I have also included the Python script used to extract the story plots.

wikiPlots.py requires:
- An English Wikipedia dump
- [Wikiextractor](https://github.com/attardi/wikiextractor)

To use wikiPlots.py:

1. Download an [English Wikipedia dump](https://dumps.wikimedia.org/enwiki/). From this link you fill find a file named something like "enwiki-20170401-pages-articles-multistream.xml.bz2". Make sure you download the .bz2 file that is **not** the index file.
2. Unzip the bz2 file to extract the .xml file.
3. Download [wikiextractor](https://github.com/attardi/wikiextractor). You do not need to set it up. Run it as follows:

``
python wikiextractor.py -o output_directory --json --html -s enwiki-...xml
``

You must run wikiextractor.py with these parameters. wikiPlots.py requires json files with nested html and with section header information preserved. Wikiextractor will produce a number of subfolders named "AA", "AB", "AC"... Within each folder will be a wiki_xx file containing a number of json records, one per article.

4. Run wikiPlots.py as follows:

``python wikiPlots.py wiki_dump_directory plot_file_name title_file_name``

`wiki_dump_director` should be the path to the directory containing the "AA", "AB", etc. folders. `plot_file_name` will be the name of the file that will contain the story plots. `title_file_name` will be the name of the file that will contain the list of story titles.
