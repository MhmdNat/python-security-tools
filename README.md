# Python Security Tools
A collection of custom-built Python tools developed to explore offensive security concepts, including web enumeration, network attacks, and system-level monitoring.

This repository focuses on understanding how common attack techniques work at a low level, with an emphasis on building tools from scratch rather than relying solely on existing frameworks.

## Current Tools
**1. Directory Buster**

A multithreaded web directory and file enumeration tool.

Key Features:

- Multithreaded scanning using ThreadPoolExecutor
- Depth-first traversal using a LIFO queue
- Recursive discovery of directories
- Configurable status code matching and filtering

Location: `directory_buster/`

## Work in Progress

This repository is actively being developed. Upcoming tools and improvements include:

- ARP/DNS spoofing tool for MITM attack simulation
- Keylogger for studying input capture and persistence mechanisms
- Enhancements to existing tools (error handling, performance, detection evasion)

## Disclaimer
These tools are developed strictly for educational purposes and testing in controlled environments where explicit authorization has been granted.

## Goals
- Strengthen understanding of offensive security techniques
- Build custom tools to explore real-world attack scenarios
- Improve knowledge of networking, operating systems, and detection mechanisms
