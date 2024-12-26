<!-- exclude in toc -->
# Table of Contents

- [Table of Contents](#table-of-contents)
- [About *Corny Commons*](#about-corny-commons)
- [Contents](#contents)
- [Standalone modules](#standalone-modules)
  - [1. console\_graphics.py](#1-console_graphicspy)
  - [2. file\_manager.py](#2-file_managerpy)
- [Packages](#packages)
  - [1. util](#1-util)
    - [a) web.py](#a-webpy)
    - [b) currency.py](#b-currencypy)
    - [c) polish.py](#c-polishpy)

# About *Corny Commons*

Corny Commons is a Python package containing modules for use by Konrad Guzek. They are used projects such as [Dzwonnik 2](https://github.com/MagicalCornFlake/dzwonnik-2) and other private work-in-progress projects.

# Contents

There are currently two core modules and one package inside Corny Commons: the `console_graphics` and `file_manager` modules, and the `util` package.

# Standalone modules

## 1. console_graphics.py

This module contains a graphics engine that can display a text-based GUI, rather than having to rely on window managers such as Tkinter or Pygame. It's useful for quick console output for games or simulators. It's currently used in projects such as [lcd-display](https://www.github.com/MagicalCornFlake/lcd-display) or [console-dino](https://www.github.com/MagicalCornFlake/console-dino).

## 2. file_manager.py

This module contains many functions related to file handling on the server as well as general input/output.

`log()` -- Formats and outputs a log message both to the terminal and a log file, defaulting to a file called `.log` in the current working directory.

`read_env()` -- Reads the file in `.env` in the current working directory and applies the environment variable assignments contained within it.

... and more!

# Packages

## 1. util

As you can guess, this package contains more specific, utility-oriented modules.

### a) web.py

The `web` module implements functionality for creating web requests. It is used in various web APIs that must retrieve information from an external source. In essence, this module is a wrapper around the built-in `requests` module.

`make_request()` -- takes a URL and creates a web request to that address. If the function has been called before the maximum request cooldown has passed, `web.TooManyRequestsException` is raised. Otherwise, the request is made. If the response is not retrieved within 10 seconds, or if it returns a response with a HTTP code that is not between 200-299, raises `web.InvalidResponseException`. If all checks pass, returns the response object.

`get_html()` -- makes a request using the `make_request()` function, then decodes the binary content and returns it as a string.

### b) currency.py

The `currency` module contains functions that utilise a public API to get the latest currency exchange information and provide it as-needed for a given fiat currency.

`convert()` -- this function converts a value from one currency into another.

### c) polish.py

Since Konrad Guzek is Polish by blood and currently lives in the Silesian area of Poland at the time of writing, some projects involve the Polish language. It is a complex language that has in-depth conjugation rules, which means that lots of boilerplate code has to be used when dealing with worded numbers, for example. This module contains code that was necessary for a project and may see future use in other projects.

`conjugate_numeric()` -- this function correctly conjugates a noun when used with a quantifing number, since the noun form changes depending on the amount of the item that is present. Take for example the word *jabłko* meaning 'apple': 1 apple would be 1 jabł*ko*, 2 apples would be 2 jabł*ka*, and 7 apples would be 7 jabł*ek* -- note the suffix change.
