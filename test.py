#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import wykop

APPKEY=""
SECRETKEY=""

def getTags(body):
    return re.findall(r'#<a href="#([^"]+)">\1</a>', body, re.MULTILINE)

def getCommitMsg(body):
    g = re.search(r'((\d+) files? changed, (\d+) insertions?\(\+\), (\d+) deletions?\(-\))', body, re.MULTILINE)
    return g.groups() if g else ("", 0,0,0)

def main():
    api = wykop.WykopAPI(APPKEY, SECRETKEY)
    entries=api.search_entries("#programujzwykopem")
    files_sum = insertions_sum = deletions_sum = 0
    
    dic={}
    for entry in entries:
        body = entry["body"]
        tags = getTags(body)
        if "programujzwykopem" in tags and not "programujzwykopemraport" in tags:
            (msg, files, insertions, deletions) = getCommitMsg(body)
            if msg != "":
                print msg
                files_sum += int(files)
                insertions_sum += int(insertions)
                deletions_sum += int(deletions)

    print "git-squach: %d files changed, %d insertions(+), %d deletions(-)" % (files_sum, insertions_sum, deletions_sum)         

if __name__ == '__main__':
    main()

