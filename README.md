# Pandas-TD

[![Build Status](https://travis-ci.org/treasure-data/pandas-td.svg?branch=master)](https://travis-ci.org/treasure-data/pandas-td)
[![Code Health](https://landscape.io/github/treasure-data/pandas-td/master/landscape.svg?style=flat)](https://landscape.io/github/treasure-data/pandas-td/master)
[![Coverage Status](https://coveralls.io/repos/treasure-data/pandas-td/badge.svg?branch=master)](https://coveralls.io/r/treasure-data/pandas-td?branch=master)
[![PyPI version](https://badge.fury.io/py/pandas-td.svg)](http://badge.fury.io/py/pandas-td)

[![Pandas-TD](https://raw.githubusercontent.com/treasure-data/pandas-td/master/doc/images/pandas-td.png)](https://github.com/treasure-data/pandas-td/blob/master/doc/tutorial.ipynb)

## Install

You can install the releases from [PyPI](https://pypi.python.org/):

```sh
$ pip install pandas-td
```

For Mac OS X users, you can install [Pandas](http://pandas.pydata.org/) and [Jupyter](https://jupyter.org/) as follows:

```sh
# Use Homebrew to install Python 3.x
$ brew install python3

# Install pandas, pandas-td, matplotlib, and ipython[notebook]
$ pip3 install -r https://raw.githubusercontent.com/treasure-data/pandas-td/master/contrib/jupyter/requirements.txt

# Set API key and start a session
$ export TD_API_KEY=...
$ ipython notebook
```

## Examples

```python
import os
import pandas_td as td

# Initialize connection
con = td.connect(apikey=os.environ['TD_API_KEY'], endpoint='https://api.treasuredata.com/')
engine = con.query_engine(database='sample_datasets', type='presto')

# Read Treasure Data query into a DataFrame.
df = td.read_td('select * from www_access', engine)

# Read Treasure Data table, sampling 5 percent of data, into a DataFrame.
df = td.read_td_table('nasdaq', engine, sample=0.05, limit=10000)

# Write a DataFrame to a Treasure Data table.
td.to_td(df, 'my_db.test_table', con, if_exists='replace', index=False)
```

If you are using IPython or Jupyter, you can enable magic functions:

```python
%load_ext td.ipython

%use sample_datasets
import www_access
import nasdaq

%dt
...

%%presto
select * from www_access limit 3
```

## Documentation

- Tutorial (https://github.com/treasure-data/pandas-td/blob/master/doc/tutorial.ipynb)

## License

Apache Software License, Version 2.0
