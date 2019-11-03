#!/usr/bin/python3

import argparse
import sys
import keywordsgen

desc = 'CLI program to generate keyword file and package arduino library'


def main():
    argparser = argparse.ArgumentParser(description=desc)
    argparser.add_argument(
                            '-f', 
                            '--file', 
                            help='Library header file', 
                            required=True
                          )
    argparser.add_argument(
                            '-k', 
                            '--keywords', 
                            help='Keywords output file', 
                            default='KEYWORDS.txt'
                          )
    args = argparser.parse_args()
    
    parser = keywordsgen.Parser()
    parser.parse(args.file)
    keywordsFile = args.keywords
    if not keywordsFile:
        keywordsFile = 'KEYWORDS.txt'
    parser.write_keywords(keywordsFile)
    # parser = keywordsgen.Parser()
    # parser.parse('TestClass.h')


if __name__=='__main__':
    main()
