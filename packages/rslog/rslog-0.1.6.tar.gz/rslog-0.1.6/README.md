# rslog

A simple, opinionated python library for logging locally.  

It will log a timestamp, the function name and add colours based on keywords in the log string that may indicate an error or warning.  

Drop-in replacement for `print()`. 

<img src="misc/ss.png" alt="Screenshot" width="70%">

## Installation

```bash
pip install rslog
```

## Usage

```python
from rslog import rslog

rslog("Hello, world!")
rslog("An error occurred!")
rslog("Warning: something went wrong.")
```

