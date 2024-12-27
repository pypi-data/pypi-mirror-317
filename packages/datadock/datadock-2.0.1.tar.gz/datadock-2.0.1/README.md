# DataDockPy Library  

---------------

![Python Versions](https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue) 
![License](https://img.shields.io/pypi/l/paystackease.svg) 
![PyPi - Version](https://img.shields.io/pypi/v/paystackease.svg)

<p align="center">    
<a href="https://github.com/DataDock-AI/DataDockPy">
    <img src="media/20241001135438-ezgif.com-video-to-gif-converter.gif" alt="DataDock demo" height="350">
</a>
</p>



## Introduction

`datadock` is a powerful and user-friendly Python package designed to enhance data analysis. 
It simplifies the extraction and presentation of information for various forms from the SEC website, 
offering enriched data display for SEC form types, filing details, and financial statements, 
making it an essential tool for professionals working with regulatory filings.


## Features

- 📁 **Access any SEC filing**: You can access any filings on SEC forms of Form 8-K and Form 10-K etc.
- 📅 **List filings for any date range**: List filings by date e.g. or date range `2024-02-29:2024-03-15`
- 🌟 **User Friendly library**: Uses **[rich](https://rich.readthedocs.io/en/stable/introduction.html) & [tabulate](https://github.com/astanin/python-tabulate)** library to display SEC Edgar data in a beautiful way.
- 🏗️ **Filter filings data**: Build data filtering by cik, accession number, form type, filing date
- 🔍 **Preview the text data for a filing**: You can preview the filing (sections) in the terminal or a notebook.
- 📊 **Parse to Dataframe**: You can parse filings to a dataframe.
- 📈 **Financial Statement**: Get financial statements of Form 8-K and Form 10-K of various companies.


## Get Started on Windows/MacOS/Linux Terminal

-------

You can use `Poetry` or any dependency manager or use the general `pip install` command to install `datadock`.

### Using pip command to install `datadock`

```commandline
pip install datadock
```

### Using Poetry to install `datadock`


1. Open your terminal and install poetry _[if you do not have poetry]_ using `pip`.
    
    ```commandline
   pip install poetry
   ```
   or Install poetry using `pipx`.
    
    ```commandline 
   pipx install poetry
    ```
   or Install using `curl`

   ```commandline
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Create a project using poetry command. This will create a `pyproject.TOML` in your project.
Follow the instructions to finish creating your project

    ```commandline
    poetry new project_name
    ```

3. Change directory to your project

   ```commandline
   cd project_name
   ```

4. Run the poetry command to add `datadock`: 

    ```commandline
   poetry add datadock
   ```


## Use DataDockPy with Jupyter

----------

1. Open notebook in your project and install `datadock` using `pip` command.
    
    ```bash
   !pip install datadock
   ```

----------

## Do you have any issue or want to contribute to `datadock` library?

If you have any issue or contribution, please write an issue with this link: https://github.com/DataDock-AI/DataDockPy/issues
