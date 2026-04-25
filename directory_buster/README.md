# Directory Buster
A multithreaded directory and file brute-forcing tool designed to enumerate web application attack surfaces.

## Overview
This tool performs recursive directory discovery by combining multithreading with a depth-first traversal approach. It is built to better understand how web enumeration tools operate internally.

## Features
- Multithreaded scanning
- Recursive directory exploration
- Configurable match and filter status codes
- Depth-limited traversal
## Usage
```powershell
python directory_buster.py -u http://example.com -w wordlist.txt -t 40 -mc 200 302 -fc 404 -max 5
```

## Limitations
- Relies only on HTTP status codes (no content-length filtering yet)
- No wildcard response detection
- No rate limiting or retry logic
- Assumes directory-based paths (limited file detection)

## Future Improvements
- Add content-length and response comparison filtering
- Implement wildcard detection
- Support file extensions
- Improve error handling and request reliability
- Add output logging to file

## Learning Focus
This project was built to explore:
- Multithreading in Python
- Web enumeration techniques
- HTTP response analysis
- Trade-offs between performance and accuracy
