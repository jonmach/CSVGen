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

CSVG = CSVGen(iFile=<schema file>, oFile=<CSV File>, numRows=<num>, verbose=<True|False>)
```

The generated file contains a header row column names. Subsequent rows contain the generated data.

---

A Sample schema file:
```
{
  "name" : "SampleTable",
  "columns": [
    {
      "name": "ID",
      "incremental": "1",
      "description" : "Unique Key - start at 100",
      "type": "0",
      "minimum": "100",
      "format": "0000d"
    },
    {
      "name" : "random-name-text",
      "description" : "Random Characters",
      "type": "2",
      "format" : "s"
    },
    {
      "name" : "sex",
      "description" : "Gender",
      "type": "2",
      "choice" : [ "M", "F"],
      "format" : "s"
    },
    {
      "name" : "department",
      "description" : "Department number",
      "type": "0",
      "choice" : [ 101, 102, 201, 202, 203, 301, 302, 401, 402],
      "format" : "d"
    },
    {
      "name": "height",
      "description" : "Person's height",
      "type": "1",
      "minimum": "1.65",
      "maximum": "1.85",
      "NULLS" : "0",
      "format": "000.2f"
    },
    {
      "name": "phone",
      "description" : "A character field containing a random phone number ",
      "type": "2",
      "regex": "0[1-9]{2,4}-[1-9]\\d{7}",
      "length": "10",
      "NULLS" : "1",
      "format": "s"
    },
    {
      "name": "UK-Postcode",
      "description" : "Random post code",
      "type": "2",
      "regex": "[A-Z]{2,3}\\d{1,2} \\d{1,2}[A-Z]{2}",
      "length": "10",
      "NULLS" : "0",
      "format": "s"
    },
    {
      "name": "last-login",
      "description" : "Arbitrary Time",
      "type": "4",
      "minimum": "20170101080000",
      "maximum": "20170101175959",
      "NULLS" : "0",
      "format": "%d/%m/%Y %H:%M:%S"
    },
    {
      "name": "DOB",
      "description" : "Date of Birth",
      "type": "3",
      "minimum" : "19700101",
      "maximum" : "19851231",
      "NULLS" : "0",
      "format": "%d/%m/%Y"
    },
    {
      "name": "StartDate",
      "description" : "One of three dates, they could have joined the company",
      "type": "3",
      "choice" : ["20170103", "20170401", "20170701"],
      "NULLS" : "0",
      "format": "%d-%m-%Y"
    }
  ]
}
```

Sample Output is:

```
"ID", "random-name-text", "sex", "department", "height", "phone", "UK-Postcode", "last-login", "DOB", "StartDate"
100, XlrEVi7X ORH2QGd, M, 401, 1.77, 0172-95426575, XI99 60GK, 01/01/2017 13:32:40, 22/11/1984, 03-01-2017
101, ObD rYyN86An5eM, F, 301, 1.72, 08668-88273483, FB22 13DZ, 01/01/2017 17:45:07, 22/03/1978, 01-07-2017
102, OulPVxUL s5u, M, 302, 1.70, 088-75139408, XT42 7LH, 01/01/2017 12:22:38, 29/11/1984, 01-04-2017
103, Ydu86 1gf j5B CQi wiS n1x0GgL, F, 202, 1.77, 066-57349920, NPB0 6ZO, 01/01/2017 15:34:53, 13/10/1985, 03-01-2017
104, FWiJvR424dys QdOOpUi, M, 102, 1.65, 058-11764888, NQF84 08VW, 01/01/2017 10:36:46, 12/10/1984, 01-04-2017
105, TyVGHoYV1 6UrW RZXbk0ryOAlAe0, F, 301, 1.75, 02965-56933753, QRP2 7ZU, 01/01/2017 09:59:09, 19/01/1982, 01-07-2017
106, G2XSFgESkhaG VxL vI v6, M, 401, 1.74, 02611-42495397, VR64 5HM, 01/01/2017 08:02:32, 11/12/1981, 01-04-2017
107, VFnp F9sypaNBHNzt sQMoOTyYmi, F, 401, 1.72, 074-73407971, TLS93 12NH, 01/01/2017 14:41:56, 05/06/1973, 03-01-2017
108, NU58hAqDR0ZmpUo3X, M, 402, 1.78, , NMV4 25DB, 01/01/2017 16:18:59, 14/04/1970, 01-04-2017
109, DYxW6dGsGfpXHq7dwmnKF, F, 302, 1.75, 03331-86519502, NCT66 05ZT, 01/01/2017 10:10:29, 30/09/1978, 01-04-2017
110, R1Ek7DsHmJ2gQZJhgHWrjODcDl, M, 401, 1.73, , JQ5 7GM, 01/01/2017 12:01:11, 11/08/1976, 01-04-2017
111, Dw2, F, 203, 1.65, 0613-81192473, SKS8 5VA, 01/01/2017 09:43:45, 17/09/1976, 01-07-2017
112, HgE2 YbIaGJ3IJY60sd3p, M, 402, 1.81, , GZP0 3NE, 01/01/2017 12:39:13, 10/09/1983, 01-04-2017
113, EjNWCKOliz84VyJ1JSo7lHvv, F, 102, 1.76, 08421-88839374, JCM4 86QH, 01/01/2017 08:33:53, 18/12/1981, 01-04-2017
114, CYOz, F, 203, 1.66, 0161-11334921, JTW56 13MS, 01/01/2017 13:14:18, 19/07/1972, 01-04-2017
115, XYbMBbQ3hepSBzTHTHGExQjbDB2T, F, 102, 1.80, 01659-25568110, DFL9 1AI, 01/01/2017 15:34:59, 15/08/1976, 01-07-2017
116, A8ZQ, M, 402, 1.79, 06919-92509779, BA49 71CT, 01/01/2017 17:33:32, 06/12/1972, 01-04-2017
117, BXh, F, 302, 1.75, , EVA8 3DA, 01/01/2017 12:23:56, 09/04/1970, 03-01-2017
118, XcD6DbmPFf5mJin, M, 202, 1.72, 05347-76368650, HB48 00UT, 01/01/2017 16:44:04, 22/06/1982, 03-01-2017
119, DeWoENZKGOh7GybJJn, F, 301, 1.75, 09571-54378361, HL83 5IA, 01/01/2017 14:34:56, 09/03/1974, 01-07-2017

```



