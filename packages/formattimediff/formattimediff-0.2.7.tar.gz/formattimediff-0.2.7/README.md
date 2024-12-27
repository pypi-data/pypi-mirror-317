# FormatTimeDiff

![version](https://img.shields.io/badge/version-0.2.7-blue)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Simply accepts a Start Time and End Time variables created with datetime.now(), calculates the time difference, then outputs a nicely formatted output to use with print() statements with the seconds rounded up for half seconds and greater, down for under half seconds. 

This can be useful for scripts that you run manually and want to keep track of how long certain actions take, but also want to have more elegant output to quickly reference. 

This is my first personal project to understand how creating and deploying modules work mostly. Overall it's very simplistic and "purpose-made" for my personal use across projects, and originally created as just a basic run-of-the-mill definition I used frequently. I figured someone might get some use out of it, and it may open the gates for me to start building more broader modules down the road. 
![]()

**Table of Contents**

- [Installation](#installation)
- [Execution / Usage](#execution--usage)
- [Technologies](#technologies)
- [Features](#features)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [Author](#author)
- [Change log](#change-log)
- [License](#license)

## Installation

On macOS and Linux:

```sh
$ python -m pip install formattimediff
```

On Windows:

```sh
PS> python -m pip install formattimediff
```

## Execution / Usage

Here are a few examples of using the formattimediff library in your code:

```python
from formattimediff import formattimediff as ftd

processStart = datetime.now()
print("Start Time:", processStart)
### do some work here ###
### or, to test, run a time.sleep(10.7) to simulate a workload ###
delta = datetime.now()
print("End Time:",delta)

timeElapsed = ftd(processStart, delta)
print("Time Elapsed:",timeElapsed)

#Output: 
#Time Elapsed: 0 Hours, 0 Minutes, 11 Seconds
...
```

## Technologies

formattimediff uses the following technologies and tools:

- [Python](https://www.python.org/): ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


## Features

It's really just the one thing it does, no additional features. 

Possible formatting options in the future? Who knows?

## Contributing

To contribute to the development of formattimediff, follow the steps below:

1. Fork < project's name > from <https://github.com/Datascripter/FormatTimeDiff/fork>
2. Create your feature branch (`git checkout -b feature-new`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some new feature'`)
5. Push to the branch (`git push origin feature-new`)
6. Create a new pull request

## Contributors

Me and only me. I am fresh on the Python bandwagon too... 

## Author

Cody Walls - "Datascripter"
<https://github.com/Datascripter/FormatTimeDiff/fork>

## Change log

- 0.2.5
    - Project creation for GitHub and releasing into the wild
- 0.1.0
    - First working version
- ...

## License

formattimediff is distributed under the MIT license. See [`LICENSE`](LICENSE) for more details.