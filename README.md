# python-abfallplus
A Python wrapper for [Abfall+](https://www.abfallplus.de/) API

# Description
This library provides a Python interface for the [Abfall+](https://www.abfallplus.de/) API.

[Abfall+](https://www.abfallplus.de/) provides the export of waste collection dates for a lot of waste management companies in Germany.

# Installing
You can install python-abfallplus using:
```
$ pip install python-abfallplus
```

# Getting the source code
This project is hosted at https://github.com/temesinko/python-abfallplus

You can clone the project using:
```
$ git clone git://github.com/temesinko/python-abfallplus.git
$ cd python-abfallplus
```

Install the minimal dependencies:
```
$ pip install -Ur requirements.txt
```

For installing the testing dependencies:
```
$ pip install -Ur requirements.testing.txt
```

# Running tests
Make sure you installed the testing dependencies.

Run the tests using:
```
$ pytest -s
```

# Using
The library uses the namespace `abfallplus`.

## Models
*  abfallplus.Community
*  abfallplus.Street
*  abfallplus.WasteType

## API
The API is exposed via the `abfallplus.Api` class.

For fetching data you will need to provide a key. In this library it is called `company_key`, because it differs from
one waste management company to another.

Most probably you will already have such a key. Otherwise you can extract it from the form your waste management
company provides for exporting the waste collection plan. Of course it must be compatible with Abfall+. You're looking
for something like `//api.abfall.io/?key=248deacbb49b06e868d29cb53c8ef034` in the source code of the page containing
the export form where `248deacbb49b06e868d29cb53c8ef034` is the `company_key` in this example.

### Instantiating the API class
To create an instance of `abfallplus.Api` you can use the following code example:
```python
import abfallplus
api = abfallplus.Api()
```

### Fetching all available communities
To fetch all available communities of a waste management company:
```python
print(api.get_communities('248deacbb49b06e868d29cb53c8ef034'))
# [Community(ID=2430, Title='Ailertchen'), Community(ID=2292, Title='Alpenrod'), ...]
```

### Fetching all available streets
To fetch all available streets in a community of a waste management company:
```python
print(api.get_streets('248deacbb49b06e868d29cb53c8ef034', 2326))
# [Street(ID=1459, Title='Am Alten Bahnhof'), Street(ID=1460, Title='Am Fichtenstrauch'), ...]
```

### Fetching all available waste types
To fetch all available waste types for a street in a community of a waste management company:
```python
print(api.get_waste_types('248deacbb49b06e868d29cb53c8ef034', 2326, 1459))
# [WasteType(ID=27, Title='Altpapier'), WasteType(ID=28, Title='Bioabfall'), WasteType(ID=17, Title='Gelber Sack'), ...]
```

### Fetching all waste collection dates
To fetch all waste collection dates grouped by waste type for a street (you don't need the community id here):
```python
print(api.get_waste_collection_dates('248deacbb49b06e868d29cb53c8ef034', 1459, datetime(2020, 1, 1), datetime(2020, 12, 31)))
# {'Bioabfall': ['07.01.2020', '21.01.2020', '04.02.2020', ...], ...}
```
This returns a dictionary containing the waste types as keys and the waste collection dates as values. Unfortunately
there is no possibility to identify the fetched waste types (for example by its waste type ID), because the CSV
contains only the titles in the first row, no IDs (the titles even do not match the titles returned by `get_waste_types()`
sometimes, so we cannot create links.

You can filter for specific waste types by additionally adding a sequence of waste type IDs to the method call. **Note:**
If you define a waste type which cannot be found by the API it doesn't raise an error but it simply returns the result
set reduced by the waste type which could not be found (for example you request 9 waste types of which 1 could not be
found, then the resulting dictionary will contain 8 waste types - there will be no error).

# Notice of Non-Affiliation and Disclaimer
This library is not affiliated, associated, authorized, endorsed by, or in any way officially connected with
Abfall+ GmbH & Co. KG or any of its subsidiaries or its affiliates. The official Abfall+ website can be found
[here](https://www.abfallplus.de/).

The names Abfall+ and ABFALLPLUS as well as related names, marks, emblems and images are registered trademarks of their
respective owners.
