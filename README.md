# ncappzoo analysis tool

## Includes:

1. Python Script for Generating JSON and CSV Files
2. Jupyter Notebook for Visualizing Trends in Data

## Requirements for the Python Script

- Pandas
- Plotly
- Scikit-Learn
- Scipy


### Command to Install Required Packages
```
$ sudo pip3 install pandas scikit-learn scipy
```

### Using scripts to build database
`database_constructor.py` <br/>
Parameters: <br/>
`-u`: username <br/>
`-p`: password <br/>
`-oc`: path to a reference table for clones <br/>
`-ov`: path to a reference table for views <br/>
<br/><br/>
Output: 
- outputs json and csv files for current data pulled from github
- outputs csv file that builds upon reference file using current data
