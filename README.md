# QRadar-ruleset
QRadar Export the rule set for printing


On QRadar system run:

/opt/qradar/bin/contentManagement.pl --action export -c customrule -i all


copy the resulting file to a workstation and unpack the file:

tar -xvzf [filename]


run the Python script:

python3 QRadar-ruleset.py > rules.txt


Import the file into a spreadsheet field delimiter is "#"
