import json
import re
from xml.etree import ElementTree as etree
import os
import sys
from bs4 import BeautifulSoup

startdir = "" # The directory to find all the wiki files
outfilename = "" # The filename to dump plots to
titlefilename = "" # The filename to dump title names to

# Check command line parameters
if len(sys.argv) > 3:
	startdir = sys.argv[1]
	outfilename = sys.argv[2]
	titlefilename = sys.argv[3]
else:
	print "usage:", sys.argv[0], "directory plotfile titlefile"
	exit()

files = [] # All the wiki files

# Get all the wiki files left by wikiextractor
for dirname, dirnames, filenames in os.walk(os.path.join('.', startdir)):
	for filename in filenames:
		if filename[0] != '.':
			files.append(os.path.join(dirname, filename))

with open(outfilename, "w") as outfile:
	# Opened the output file
	with open(titlefilename, "w") as titlefile:
		# Opened the title file
		# Walk through each file. Each file has a json for each wikipedia article. Look for jsons with "plot" subheaders
		for file in files:
			#print >> outfile, "file:", file #FOR DEBUGGING
			data = [] # Each element is a json record
			# Read the file and get all the json records
			for line in open(file, 'r'):
				data.append(json.loads(line))
			# Look for "plot" in a "h2" tag inside the text of the json
			for j in data:
				# j is a json record
				# Text element contains HTML
				soup = BeautifulSoup(j['text'].encode('utf-8'), "html.parser")
				plot = "" # The plot found (if any)
				# Look for a "h2" tag that contains the word "plot"
				# The next element(s) will be the text of the plot
				inplot = False # Am I inside a plot section of the article?
				previousHeader = "" # What was the last subheading I saw? (plots may have sub-sub-headings)
				# Walk through each element in the html soup object
				for n in range(len(soup.contents)):
					current = soup.contents[n] # The current html element
					if current is not None and current.name == 'h2' and 'plot' in current.get_text().lower():
						# I found a plot header
						inplot = True
						previousHeader = previousHeader + current.get_text() + '. '
					elif inplot and current is not None and (current.name == 'h3' or current.name == 'h4'):
						# I'm probably seeing a sub-heading inside a plot block
						previousHeader = previousHeader + current.get_text() + '. '
					elif inplot and current is not None and (current.name is None or current.name == 'b' or current.name == 'a' or current.name == 'i' or current.name == 'strong' or current.name == 'em'):
						# I'm probably looking at text inside a plot block
						current = current.strip()
						# Sometimes we see the header name duplicated inside the text block that succeeds the sub-section header. Crop it off
						if len(current) > 0:
							if len(previousHeader) > 0:
								headerLength = len(previousHeader)
								plot = plot + current[headerLength:].strip() + ' '
							else:
								plot = plot + current.strip() + ' '
							# Forget the previous header. It was either consumed or wasn't duplicated in the first place.
							previousHeader = ""
					elif inplot and current is not None and (current.name == 'h1' or current.name == 'h2'):
						# Probably left the plot block. All done with this json!
						break
				# Did we find a plot?
				if len(plot) > 0:
					# ASSERT: I have a plot
					# Record the name of the article with the plot
					print >> titlefile, j['title'].encode('utf-8')
					# remove newlines
					plot = plot.replace('\n', ' ').replace('\r', '').strip()
					# remove html tags (probably mainly hyperlinks)
					plot = re.sub('<[^<]+?>', '', plot)
					# remove character name initials and take periods off mr/mrs/ms/dr/etc.
					plot = re.sub(' [M|m]r\.', ' mr', plot)
					plot = re.sub(' [M|m]rs\.', ' mrs', plot)
					plot = re.sub(' [M|m]s\.', ' ms', plot)
					plot = re.sub(' [D|d]r\.', ' dr', plot)
					plot = re.sub(' [M|m]d\.', ' md', plot)
					plot = re.sub(' [P|p][H|h][D|d]\.', ' phd', plot)
					plot = re.sub(' [E|e][S|s][Q|q]\.', ' esq', plot)
					plot = re.sub(' [L|l][T|t]\.', ' lt', plot)
					plot = re.sub(' [G|g][O|o][V|v]\.', ' lt', plot)
					plot = re.sub(' [C|c][P|p][T|t]\.', ' cpt', plot)
					plot = re.sub(' [S|s][T|t]\.', ' st', plot)
					plot = re.sub(' [A-Z|a-z]\.', '', plot) # remove single letter initials
					plot = re.sub('\.\"', '\".', plot) # deal with periods in quotes
					# Acroymns with periods are not fun. Need two steps to get rid of those periods.
					# I don't think this is working quite right
					p1 = re.compile('([A-Z|a-z])\.([)| |\"|\,])')
					plot = p1.sub(r'\1\2', plot)
					p2 = re.compile('\.([A-Z|a-z])')
					plot = p2.sub(r'\1', plot)
					# periods in numbers
					p3 = re.compile('([0-9]+)\.([0-9]+)')
					plot = p3.sub(r'\1,\2', plot)
					# Break into sentences
					sentences = re.split('[\?\.\!]', plot)
					#print >> outfile, j['title'].encode('utf-8') #FOR DEBUGGING
					# Write the sentences to the plot file
					for s in sentences:
						if len(s.strip()) > 0:
							print >> outfile, s.strip().encode('utf-8')+'.'
					print >> outfile, "<EOS>"
