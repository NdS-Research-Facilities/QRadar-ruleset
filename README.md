# QRadar-ruleset
QRadar Export the rule set for printing


On QRadar system run:

/opt/qradar/bin/contentManagement.pl --action export -c fgroup -i all


copy the resulting file to a workstation and unpack the file:

tar -xvzf [filename.gz]


run the Python script:

python3 QRadar-rules2csv.py [filename.xml] > rules.csv
OR
python3 QRadar-rule2html.py [filename.xml] > rules.html

open the resulting rules.htl file in a browser.
OR
Import the rules.csv file into a spreadsheet, field delimiter is ","

format and print as needed.

DISCLAIMER: This code is free to use, feedback is welcome, do not call IBM with support issues or questions on this code. 

