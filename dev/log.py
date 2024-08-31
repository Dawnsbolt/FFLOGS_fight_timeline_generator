import os
from math import floor
"""
LOG is an iterator which parses a CSV textfile into [TIMESTAMP, EVENT_NAME]
Expects each CSV line to be of the form: 
    "Time","Event",""
Example:
    "00:01.137","Valigarmanda casts  attack on Ryuusei Hoshizora",""
Set ROUND to the decimal you want the timestamp to be rounded to
"""
ROUND = 100
class Log:
    def __init__(self, INPUT_FILENAME):
        self.file = None
        self.previous_event = ''
        # Verify input file path
        if not os.path.isfile(INPUT_FILENAME):
            raise LogFileNotFound(INPUT_FILENAME)
        # Open input file
        self.file = open(INPUT_FILENAME, 'r', encoding="utf-8")
    
    def __del__(self):
        if self.file and not self.file.closed:
            self.file.close()

    def __iter__(self):
        next(self.file) # Skip initial ["Time","Event",""] line
        return self
    
    def __next__(self):
        line = next(self.file)
        tokens = generate_tokens(line)
        time = parse_time(tokens[0])
        event = parse_event(tokens[1])
        self.previous_event = event
        return [time, event]

class LogFileNotFound(FileNotFoundError):
    def __init__(self, EXPECTED_FILENAME):
        self.expected = EXPECTED_FILENAME

### HELPER METHODS ###

"""
Splits str separated by , returns list [TIME, EVENT]
tokens[0] = RAW_TIME
tokens[1] = RAW_EVENT
INPUT_LINE is just a string
"""
def generate_tokens(input_line):
    tokens = input_line.split(',')
    return [tokens[0], str.strip(tokens[1])]

def parse_event(event_input):
    event_tokens = event_input.split(" ")
    next_token_is_ability = False
    ability_name = ''
    for token in event_tokens:
        if token =='casts' or token == 'casting': # next token is part of ability_name
            next_token_is_ability = True
            continue
        if token == 'on': # end of ability_name
            next_token_is_ability = False
        if token and next_token_is_ability:
            ability_name += token + ' '
    return ability_name.replace('\"', '')[:-1]
    
def parse_time(time_input):
    clean_time = time_input.replace("\"", '') #clean timestamp input
    time_tokens = clean_time.split('.')
    main_timestamp = time_tokens[0]
    rounded_sub = str(floor(int(time_tokens[1])/ROUND)) +'00'
    return main_timestamp + '.' + rounded_sub[0:3]

def timecode_to_seconds(timecode):
    minute, tokens = timecode.split(':')
    seconds, subseconds = tokens.split('.')
    return 60*int(minute) + int(seconds)