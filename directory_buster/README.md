# Directory Buster

A multithreaded web content discovery tool written in Python for recursive directory and file enumeration.

This project was built to explore how modern web enumeration tools operate internally, with a focus on multithreading, traversal strategies, and HTTP response analysis.

## Features

- Multithreaded scanning
- Recursive directory traversal
- File extension brute forcing
- Configurable match and filter status codes
- Depth-limited exploration
- Depth-first traversal using a LIFO queue
- Thread-safe visited path tracking
- Timeout handling

## Usage

### Basic Directory Enumeration
```powershell
python directory_buster.py -u http://example.com -w wordlist.txt
```

### Recursive Scanning
```powershell
python directory_buster.py -u http://example.com -w wordlist.txt --max-depth 5
```

### File Extension Brute Forcing
```powershell
python directory_buster.py -u http://example.com/directory -w wordlist.txt -e .php .txt
```

### Custom Match / Filter Codes
```powershell
python directory_buster.py -u http://example.com -w wordlist.txt -mc 200 302 -fc 404
```

### Custom Timeouts
```powershell
python directory_buster.py -u http://example.com -w wordlist.txt --timeout 3
```

## Example Output

```text
[+] http://example.com/admin/ (Status Code: 200)
[+] http://example.com/login.php (Status Code: 200)
[-] http://example.com/test/ (Status Code: 403)
```

## Current Limitations

- Relies primarily on HTTP status codes
- No response-body filtering yet
- No wildcard response detection
- No rate limiting or retry logic
- Curl handles are not reused between requests
- Recursive scanning currently focuses on directory discovery only

## Future Improvements

- Add response fingerprint filtering
- Implement wildcard response detection
- Add request retry
- Support request headers, cookies, and proxies
- Add rate limiting and throttling
- Improve connection reuse for performance
- Add logging and structured output support
- Explore asynchronous request handling


## Legal Disclaimer

This tool is intended for educational purposes and authorized security testing only.

Do not use this tool against systems you do not own or explicitly have permission to test.