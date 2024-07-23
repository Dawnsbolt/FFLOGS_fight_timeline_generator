Python 3.x script used to convert a CSV of enemy casts into a clean timestring for spreadsheets where each line is of the form:
	[time]	[event_name]

[DEPENDENCIES]
Requires Python 3.x - https://www.python.org/

[USAGE]
	1. Place your input file in same directory as the script
	2. Configure SETTINGS.json and BLACKLIST.json
	3. Run ffSpreadsheetExec.py
	4. Output should be OUTPUT_FILENAME.txt within the directory script was run

[CONFIGURATION]
SETTINGS.json contains the following:
	INPUT_FILENAME [filename]   -   name of the input file
	OUTPUT_FILENAME [filename]  -   name of the desired output file
	IGNORE_REPEATS [True/False] -   ignore consecutive repeated events (eg spread mechanics);
	IGNORE_UNKNOWN [True/False] -   ignore unknown_* events
	REPEAT_INTERVAL [int] - minimum time allowed between repeated events before they are ignored

BLACKLIST.json contains the names of events the parser ignores
Ignores "attack" casts by default
Format Example:
	{
		"event_name":"",
		"event_name2":"",
			...
		"event_nameN":""
	}
