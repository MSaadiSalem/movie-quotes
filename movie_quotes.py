#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import time
import urllib


def read_script(script_path):
    """Read a script by using 'with open', python handles closing the file after code block has been finished."""

    # Inputs:
    # script_path: is a valid path of the desired file to be read.
    # Outputs:
    # script: is the content of the given file.

    try:
        with open(script_path, "r") as h_script:
            script = h_script.read()
            return script
    except:
        print "Input Error: %s." % script_path
        exit()


def write_script(updated_script, script_path):
    """Write the changes to the given script. This function has no return"""

    # Inputs:
    # updated_script: an updated content to be written into a given file.
    # script_path: is a valid path of the desired file to be read.
    # Outputs:
    # This function has no return.

    with open(script_path, "w") as h_script:
        h_script.write(updated_script)


def check_profanity(script):
    """Check words one by one for profanity in the given script.
    This function returns revised script with encrypted curse words if exis.
    With an empty list or a list of curse words"""

    # Inputs:
    # script: file contents to be checked for curse words
    # Outputs:
    # script: file contents with encrypted curse words exist
    # curse_words: curse words list if exist or an empty list

    profanity_count = 0
    curse_words = []
    words = script.split()

    for word in words:
        connection = urllib.urlopen(
            "http://www.wdylike.appspot.com/?q=" + word)
        output = connection.read()

        if output == "true":
            curse = word[0] + "*" * (len(word) - 2) + word[-1]
            script = script.replace(word, curse, 1)
            curse_words += [curse]
            profanity_count += 1

    print "Script has %d curse words.\n" % profanity_count
    return script, curse_words


def profanity_replacer(script, curse_words):
    """ Replace the curse words in the given script.
    This function returns a modified script has no curse words."""

    # Inputs:
    # script: file contents with curse words.
    # curse_words: curse words list.
    # Outputs:
    # script: file content after removing curse words.

    for curse in curse_words:
        modified = raw_input("Enter a correction for %s: " % curse)
        script = script.replace(curse, modified, 1)
    curse_words = None
    return script


def fun_trans(script):
    """API from 'http://funtranslations.com/api#' to translate to different options.
    Using public API calls is limited to 60 API calls a day with distribution of 5 calls an hour.
    This function has no return"""

    # Inputs:
    # script: file content to be translated to different selected speech option.
    # Outputs:
    # This function has no outputs.

    trans_options = {"pirates": "pirate.json",
                     "minions": "minion.json",
                     "morse": "morse.json",
                     "article rewrite": "article_rewrite.json",
                     "old english": "oldenglish.json"}

    s = "Please select the desired option from the following:"
    print s, "\n", "-" * len(s)
    for key in trans_options.keys():
        print key.capitalize()

    sel_op = raw_input("\nEnter your option:").lower()
    while not sel_op in trans_options.keys():
        sel_op = raw_input("Enter a valid option:").lower()

    op = trans_options[sel_op]
    api_url = "http://api.funtranslations.com/translate/%s" % op
    print api_url

    parameter = {"text": script,
                 "type": "string",
                 "description": "Text to translate"}

    encode = urllib.urlencode(parameter)
    connection = urllib.urlopen(api_url, encode)
    print connection
    output = connection.read()

    response = json.loads(output)
    if "success" in response.keys():
        print "Translation into %s speech:\n" % sel_op.capitalize(
        ), response["contents"]["translated"]
    else:
        print response["error"]["message"]


def main():
    """This is the main function, it has the Procedural and system sequences of the program."""

    # Inputs:
    # This function has no inputs.
    # Outputs:
    # This function has no outputs

    script_path = "/home/me/Programming/Python/Udacity/lesson20/movie-quotes/movie_quotes.txt"
    script = read_script(script_path)
    script, curse_words = check_profanity(script)

    if len(curse_words) > 0:
        reply = raw_input(
            "Do you want replace curse words?\nPress (N) to skip or hit (Enter) continue.")
        if reply.lower() != "n":
            preview = "\nFile contents preview after profanity checking:"
            print preview, "\n", "-" * len(preview), "\n", script, "\n"
            script = profanity_replacer(script, curse_words)
            modify = raw_input(
                "\nDo you want to wirte the changes into the given file?\nPress (N) to skip or hit (Enter) to continue.")
            if modify.lower != "n":
                print "\nSaving changes into the given file", "." * 10
                write_script(script, script_path)
                print "Done."

    print "\nlet's play a speech game!!!"

    for i in range(5, 0, -1):
        print i, "." * i
        time.sleep(2)

    print "\n"
    fun_trans(script)


if __name__ == "__main__":
    main()
