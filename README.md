# se_project

## 
This repository contains a web application written in Flask, which allows to print the repositories, total stargazers and used languages of a selected GitHub user.


### Instructions
1. Create a parent directory.
2. Create a virtual evironment and activate it in the parent directory.
3. Install the dependecies which are listed in requirements.txt (yml?).
4. Clone the repo into the parent directory.
5. Set up the name of the application to run.  
On Windows (PowerShell):  
`$env:FLASK_APP = 'user_stats'`  
On Linux:  
`export FLASK_APP = user_stats`  
6. Type command:  
`flask run`
7. Open the address http://127.0.0.1:5000/ in your web browser (or any other if you specified a different port, the address will be printed out in you terminal).
  

### Further ideas
- enable authenticated requests to overcome the GitHub API access per IP limit
- asynchronous API calls - for users with many repositories even counting the total stars takes a significant amount of time, asynchronous 
- tests on a mock server
- caching / temporary cache for saving requests (also would help overcome the hourly limit)