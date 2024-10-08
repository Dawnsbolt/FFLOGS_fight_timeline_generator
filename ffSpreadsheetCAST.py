""" 
Script to convert a CSV of enemy casts into a clean timestring for spreadsheets where each line is of the form:
 TIME \t ABILITYNAME \n

SETTINGS.json contains the following:
    INPUT_FILENAME [filename]   -   name of the input file
    OUTPUT_FILENAME [filename]  -   name of the desired output file
    IGNORE_REPEATS [True/False] -   ignore consecutive events that occur within 1 second of each other
    IGNORE_UNKNOWN [True/False] -   ignore unknown_* events
    REPEAT_INTERVAL [int] -         time between repeated events allowed before they are considered to be repeats that should be ignored
                                    // Useful for ignoring spread mechanics which occur concurrently while allowing repeat raidwides through
Add event names you want to ignore to BLACKLIST.json
"""
import os, re, json
from dev.log import Log, LogFileNotFound, timecode_to_seconds

def main():
    # set CWD
    os.chdir(os.path.dirname(__file__))
    # load settings
    OUTPUT_FILENAME, IGNORE_UNKNOWN, IGNORE_REPEATS, REPEAT_INTERVAL, FILLER_GCDS = loadSettings()
    # load blacklist
    blacklistFile = open("BLACKLIST.json")
    BLACKLIST = json.load(blacklistFile)
    blacklistFile.close()
    
    # file I/O
    results = open(OUTPUT_FILENAME, 'w', encoding="utf-8")
    input_directory = os.path.join(os.getcwd(), "inputs")
    os.chdir(input_directory)
    directory_list = os.listdir(input_directory)
    # initialize generator
    t = 0
    results.write(seconds_to_timecode(t) + '\t' + 'PULL' + '\n')
    t += 2.5
    for file in directory_list:
        try:
            myLog = Log(file)
        except LogFileNotFound:
                print("Log file not found. Do you have a file in the inputs folder?")
                input("Press ENTER to exit...")
                return -1

        # parse log
        previous_event = ''
        for event in myLog:
            seconds = int(event[0].split(":")[1].split(".")[0])
            if IGNORE_UNKNOWN and re.search('unknown_.*', event[1]) or event[1] in BLACKLIST:
                continue
            if IGNORE_REPEATS and previous_event == event[1] and seconds-previous_time < REPEAT_INTERVAL:
                previous_time = seconds
                continue
            if FILLER_GCDS:
                event_sec = timecode_to_seconds(event[0])
                while (event_sec >= t):
                    results.write(seconds_to_timecode(t)+'\t'+'\n')
                    t+=2.5
            if event[1] not in BLACKLIST:
                results.write(event[0] + '\t' + event[1] + '\n')
                previous_time = seconds
                previous_event = event[1]
    results.close()

def loadSettings():
    jsonFile = open('SETTINGS.json', 'r', encoding='utf-8')
    jsonObj = json.load(jsonFile)
    settings = [jsonObj["OUTPUT_FILENAME"],
                jsonObj["IGNORE_UNKNOWN"].lower() == "true",
                jsonObj["IGNORE_REPEATS"].lower() == "true",
                int(jsonObj["REPEAT_INTERVAL"]),
                jsonObj["FILLER_GCDS"].lower() == "true"]
    jsonFile.close()
    return settings

def seconds_to_timecode(input):
    t=input
    subsec = 0
    if (isinstance(input,float)):
        t, subsec = str(input).split(".")
    minutes = int(t) // 60
    seconds = int(t) % 60
    final_sec = str(seconds)
    final_min = str(minutes)
    if seconds < 10:
        final_sec = '0' + final_sec
    if minutes < 10:
        final_min = '0' + final_min
    return final_min + ":" + final_sec + '.' + str(subsec) + '00'

if __name__ == '__main__':
    main()