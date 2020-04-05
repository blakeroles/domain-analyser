# domain-analyser

## Running the program
At a terminal window, run: 'python2.7 Program.py'

## Command line arguments
None at the moment

## Required files outside of Git
For this program to work, you will need to create an account with Domain Developer and retrieve a client_id and client_secret string. You will need to create a file in the root directory of this repository called 'api_info.secret'. This file should have the following structure:

{"api_info": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
}}

This file is in the .gitignore for security purposes.

config.json is also required which stores all the configuration settings for the program

## Package that this program uses
json,requests,pandas,matplotlib