import GenerateForwardIndex 
import GenerateInvertedIndex
import GenerateLexicon
from Lexicon import Lexicon
import os
import ProjectConfiguration
#start of function
#simply prints menu
#takes user input
#returns option


def ProcessFile():
	starting = 0
	directory=ProjectConfiguration.INPUTPATH
	total_files=len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

	ending = total_files

	GenerateLexicon.GenerateLexicon(starting,ending)

	directory=ProjectConfiguration.UPDATED_JSONS
	total_files=len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

	ending = total_files

	GenerateForwardIndex.GenerateForwardIndex(starting,ending)
	GenerateInvertedIndex.GenerateInvertedIndex()

