
How to use the Aho Corasick Algorithm:

- Insert a text u want analyze into input_text.txt 
- Determine the keywords you are looking for, seperated by commas in keywords.txt
- Run Aho_Corasick_Algorithm.py



How to do a speed comparison:
- Move to /time_comparison/text_files/
- Define the length of the keywords that should be generated for the time comparison in length_of_keywords.txt
- minimum_keyword_occurrences.txt instructs the random number generator to fill the text with a certain percentage of keywords.
- number_of_chars.txt expects one or more values to generate 10^x random characters from 0-9  
- To determine the number of keywords to be used in the x-axes, fill number_of_keywords.txt
- Go to directory /time_comparison/ and run time_comparison.py
- The plots should be saved as PDFs in the plots folder 
