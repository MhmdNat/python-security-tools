#!/usr/bin/env python3
"""
Directory Buster

Description:
    A multithreaded directory and file brute-forcer that checks common wordlist
    entries against a target web server and recursively explores matching paths.

Requirements:
    - Python 3.x
    - pycurl

Usage:
    python directory_buster.py -u <target-url> -w <wordlist>
    python directory_buster.py -u http://example.com -w words.txt -t 40 -mc 200 302 -fc 404 -max 5

Notes:
    - Use only on systems you own or are explicitly authorized to test.
    - The target URL should include the scheme, for example http:// or https://.

Muhammad Al Natour
"""

import argparse
import pycurl 
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import LifoQueue, Empty

green = '\033[32m'
red = '\033[31m'
reset = '\033[0m'

path_stack = LifoQueue()
visited = set()
visited_lock = Lock()

class Config:
    url = ""
    wordlist = []
    match_codes = []
    filter_codes = []
    match_length = -1 #-1 means no match length filtering
    filter_length = -1 #-1 means no filter length filtering
    max_depth = 0
    threads = 0
    extension = ['']
    connect_timeout = 5
    total_timeout = 10

    @classmethod
    def initialize(cls, args, wordlist_data):
        cls.url = args.url
        cls.url = cls.url + '/' if not cls.url.endswith('/') else cls.url # e.g. http://example.com -> http://example.com/
        cls.wordlist = wordlist_data
        cls.match_codes = args.match_code
        cls.filter_codes = args.filter_code
        cls.match_length = args.match_length
        cls.filter_length = args.filter_length
        cls.max_depth = args.max_depth
        cls.threads = args.threads
        cls.extension = args.extension 
        cls.connect_timeout, cls.total_timeout = cls._get_curl_timeout_option(args.timeout)
        print(f'{green}[i]{reset} Configuration: URL={cls.url}, Threads={cls.threads}, Match Codes={cls.match_codes}, Filter Codes={cls.filter_codes}, Match Length={cls.match_length}, Filter Length={cls.filter_length}, Max Depth={cls.max_depth}, Extensions={cls.extension}, Connect Timeout={cls.connect_timeout}ms, Total Timeout={cls.total_timeout}ms')


    @classmethod
    def _get_curl_timeout_option(cls, timeout_seconds):
        if timeout_seconds <= 0:
            timeout_seconds = 10
        connect_timeout = min(timeout_seconds * 0.5, 5) 

        total_timeout = timeout_seconds
        return int(connect_timeout * 1000), int(total_timeout * 1000)


def get_status_code_and_length(path : str):
    '''Perform a curl request to the given path appended to base URL.'''
    c=pycurl.Curl()
    url = f'{Config.url}{path}'
    c.setopt(c.URL, url)
    c.setopt(c.NOBODY, True)
    c.setopt(c.CONNECTTIMEOUT_MS, Config.connect_timeout)
    c.setopt(c.TIMEOUT_MS, Config.total_timeout)
    c.setopt(c.NOSIGNAL, 1)

    try:
        c.perform()
        status_code = c.getinfo(pycurl.RESPONSE_CODE)
        length = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
    except pycurl.error as e:
        status_code = 0
        length = -1
    finally:
        c.close()

    return status_code, length


def check_path(new_path : str):
    '''Check a single path and return status code.'''
    results = ''
    for ext in (Config.extension): # also checks as a directory
        full_path = f'{new_path}{ext}/' if ext == '' else f'{new_path}{ext}'

        status_code, length = get_status_code_and_length(full_path)

        #filter out timeouts
        if status_code == 0:
            continue
        
        #filter out lengths if specified
        if length == Config.filter_length:
            continue

        # match if status code is in match codes and length matches (if specified)
        if status_code in Config.match_codes and (Config.match_length == -1 or Config.match_length == length):
            results += f'{green}[+]{reset} {Config.url}{full_path} (Status Code: {green}{status_code}{reset}, Length: {green}{length}{reset})\n'

        # show result if not being filtered out by code
        elif status_code not in Config.filter_codes:
            results += f'{red}[-]{reset} {Config.url}{full_path} (Status Code: {red}{status_code}{reset}, Length: {red}{length}{reset})\n'

    if results:
        print(results.strip())
    return status_code, length # important in the case of directory brute forcing to know if we should explore child directories


def push_child_directories(path : str, depth : int):
    if depth < Config.max_depth:
                with visited_lock:
                    if path not in visited:
                        visited.add(path)
                        path_stack.put((path + '/', depth + 1, 0))


def worker():
    '''Worker function for processing word tasks from the stack.'''
    while True:
        try:
            path, depth, i = path_stack.get(timeout=1)
        except Empty:
            return
        
        if depth > Config.max_depth or i >= len(Config.wordlist):
            continue
        
        word = Config.wordlist[i]
        new_path = f'{path}{word}' if path else word

        # Push continuation for next word in this directory
        if i + 1 < len(Config.wordlist):
            path_stack.put((path, depth, i + 1))
        # Check this word
        status_code, _ = check_path(new_path)
        
        # If found directory, and not file brute forcing, push child directory
        if status_code in Config.match_codes and Config.extension==['']:
            push_child_directories(new_path, depth)


def main():
    parser = argparse.ArgumentParser(prog='directory_buster', description='Multithreaded directory buster')
    parser.add_argument('-u', '--url', help='The target URL to scan', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file', required=True)
    parser.add_argument('-t', '--threads', help='Number of threads to use (default: 20)', type=int, default=20)
    parser.add_argument('-mc', '--match-code', help='HTTP status code to match (default: 200, 301, 302, 400, 401, 403)', nargs='+', type=int, default=[200, 301, 302, 400, 401, 403])
    parser.add_argument('-fc', '--filter-code', help='HTTP status code to filter out (default: 404)', nargs='+', type=int, default=[404])
    parser.add_argument('--max-depth', help='Maximum depth to explore (/ is 0, default is 5)', type=int, default=5)
    parser.add_argument('-e', '--extension', help='File extension to append to each word default checks directories (e.g. .php)', nargs='+', type=str, default=[''])
    parser.add_argument('-ml', '--match-length', help='Content length to match (default: any)', type=int, default=-1)
    parser.add_argument('-fl', '--filter-length', help='Content length to filter out (default: any)', type=int, default=-1)
    parser.add_argument('--timeout', help='Timeout for each request in seconds (default: 10)', type=int, default=10)


    args = parser.parse_args()

    wordlist_path = args.wordlist
    with open(wordlist_path, 'r') as file:
        wordlist_data = [line.strip() for line in file.readlines() if line.strip()]

    Config.initialize(args, wordlist_data)
    # Reset stack and visited for fresh scan
    while not path_stack.empty():
        try:
            path_stack.get_nowait()
        except Empty:
            break
    visited.clear()
    path_stack.put(('', 0, 0))  # (path, depth, word_index)

    with ThreadPoolExecutor(max_workers=Config.threads) as executor:
        futures = [executor.submit(worker) for _ in range(Config.threads)]
        for future in futures:
            future.result()


if __name__ == '__main__':
    main()