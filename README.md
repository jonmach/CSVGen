# CSVGen
Generate a CSV file containing configurable random data

This Python class allows you to generate random dummy data (CSV format) for general data tests.

**Author**: Jon Machtynger
**Date**: 21 December 2017

Available Attributes include

- **name** : Name of the field (**mandatory**)
- **columns** : An array of columns (see **sample.json**)
- - **description** : Longer description (for your own documentation)
- **type** : (**mandatory**)
	- **"0"**: Integer
    - **"1"**: Float/Decimal
    - **"2"**: String (random uppercase/lowercase/numeric/blank characters)
    - **"3"**: Date
    - **"4"**: DateTime
- **incremental** : Integer fields only, useful for a unique key
- **minimum** : Lower bound on your data type (Integers, Float, Date, and DateTime only)
- **maximum** : Upper bound on your data type (Integers, Float, Date, and DateTime only)
- **length** : Used with Strings. If you don't specify this, a default value is used
- **NULLS** : "1": Allow blanks to be generated
- **format** : Column format for your data (uses Python formats).  For example
    - value = 15, format = "0d" ==> output = '015'
    - value = 3.14, format = "06.3f" ==> output = '03.142'
    - value = 'this is a string', format = "20s" ==> output = 'this is a string    '
    - Date values use Python Date formats (%Y, %m, %d, etc.)
    - DateTime values use Python Date formats (%Y, %m, %d, %H, %M, %S etc.)
- **choice** : Provide an array of values (must match data type).  For example
    - [1, 2, 3] for Integer
    - ["M", "F"] for String
    - ["20031231", "19700101"] for Date, or ["20031231120000", "19700101133000"] for DateTime
- **regex** : Can be used with String fields
    - Generate a random string satisfying a Regular Expression.  For example:
	- Phone numbers: "0[1-9]{2,4}-[1-9]\\d{7}"
	- UK Post Code format: "[A-Z]{2,3}\\d{1,2} \\d{1,2}[A-Z]{2}"

Usage:

```
from CSVGen import CSVGen

CSVG = CSVGen(iFile=<schema file>, oFile=>CSV File>, numRows=<num>, verbose=True)
```

The generated file contains a header row column names. Subsequent rows contain the generated data.
