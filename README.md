# QRadar-ruleset
QRadar Export the rule set for printing


On QRadar system run:

/opt/qradar/bin/contentManagement.pl --action export -c fgroup -i all


copy the resulting file to a workstation and unpack the file:

tar -xvzf [filename.gz]


run the Python script:

python3 QRadar-ruleset.py [filename.xml] > rules.txt
OR
python3 QRadar-rule2html.py [filename.xml] > rules.html

open the resulting rules.htl file in a browser.
OR
Import the rules.txt file into a spreadsheet, field delimiter is "#"

format and print as needed.


