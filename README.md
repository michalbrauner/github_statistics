# Github Statistics
Set of two simple scripts to download information about pull requests and generate some charts from these data.
## Download data from Github
Script `download_data_from_github.py` download all pull requests from GitHub and save them in JSON format.

### Rate limits 
When you have a lot of pull requests you need to run this script more times and use pagination parameters. 

The reason is the API limit on Github (5000 requests / hour). 
Script needs 31 requests per one page. 

### Example 
```.env
download_data_from_github.py -o data1.json -r yourName/repository -u githubUsername -t githubApiToken --page-start 1 --page-end 2
download_data_from_github.py -o data2.json -r yourName/repository -u githubUsername -t githubApiToken --page-start 3 --page-end 4
```

## Generate charts
To generate charts you need to have account in [Plotly](https://plot.ly).
 
Script `generate_report.py` load input files, transform them into PandaDataframe and then generate charts.  

### Example 
```.env
generate_report.py -o report.html -r yourName/repository -u plotlyUsername -a plotlyApiKey -d data1.json data2.json
```
