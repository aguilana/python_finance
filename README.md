# PYTHON SCRIPTING

Welcome, this is my python scripting test.

## Objective

Become better at scripting and scraping some data that can be used in a personal projects database.
This project parsed an entire HTML file and extracted stock names and values from that file to be uploaded in a JSON formatted document.
The document was uploaded to a backend server and was then seeded into a postgresql database

### The Scripts

/tests is the testing folder
/utils contains most of the scripting logic

The logic uses BeautifulSoup to parse Yahoo Finance web pages and extract (all legal within their ToS) certain data values
I pass in each symbol and from there am able to get the values that are needed to update the database

### Limitations

If yahoo decides to alter their class's and data-values or alter anything within their individual stock view HTML then everything will ultimately break.
