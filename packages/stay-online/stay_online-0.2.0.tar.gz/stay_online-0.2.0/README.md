# Simulate fake mouse movement and fake keyboard typing.

## How to use
### Programtically
#### Default Settings
```python
from stay_online.stay_online import stay_online
stay_online()
```

#### Optional Parameters Values
```python
stay_online(
        stop_hhmm:str='', 
        min_delay_seconds:int=120, 
        max_delay_seconds:int=180, 
        min_num_words:int=1, 
        max_num_words:int=10,
        show_timestamp:bool=False
        )
```
### CLI
#### Default Settings
```bash
stay-online
```
#### Optional Parameters
```bash
--stop STOP_HHMM
Automatically stop the simulation at the time, example '1700'. Default: Empty

--min_delay MIN_DELAY_SECONDS
Minimum delay seconds between each new line. Default: 120

--max_delay MAX_DELAY_SECONDS
Maximum delay seconds between each new line. Default: 180

--min_words MIN_NUM_WORDS
Minimum number of words to type per line. Default: 1

--max_words MAX_NUM_WORDS
Maximum number of words to type per line. Default: 10

--timestamp SHOW_TIMESTAMP
Type out the timestamp in front of the line to keep track of the time. Default: False
```
Once the Python program is initiated, a prompt will appear, requesting you to select the area where you want the cursor to move. 

This designated location will serve as the point where the cursor will autonomously navigate and perform left-click actions at specified intervals.
```bash
Place cursor at clicking position and left click once.
```
### Parameters
```
stop_hhmm: Automatically stop the simulation at the provided time, example '1700'.

min_delay_seconds: Minimum delay seconds between each new line.

max_delay_seconds: Maximum delay seconds between each new line.

min_num_words: Minimum number of words to type per line.

max_num_words: Maximum number of words to type per line.

show_timestamp: Type out the timestamp in front of the line to keep track of the time.
```

## Running it directly from github

stay_online uses hatch build system for backend.
To install dependencies for local development environment, run:

```bash
git clone [URL-HERE]
pipx install hatch
hatch shell
pip install -e .
```

This will create a venv environment and install all the dependencies needed.

You can invoke `stayonline` from your terminal once you are in hatch shell. A working shell output example is as below

```bash
(stay-online) ➜  stay_online git:(main) stayonline

Remeber to provide the optional parameters:
:param str stop_hhmm: Automatically stop the simulation at the provided time, example '1700'.
:param int min_delay_seconds: Minimum delay seconds between each new line.
:param int max_delay_seconds: Maximum delay seconds between each new line.
:param int min_num_words: Minimum number of words to type per line.
:param int max_num_words: Maximum number of words to type per line.
:param bool show_timestamp: Type out the timestamp.

Place cursor at clicking position and left click once.
```