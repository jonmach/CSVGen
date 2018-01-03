# CSVGen
Generate a CSV file containing configurable random data

This Python class allows you to generate random dummy data (CSV format) for general data tests.  Note that, unless otherwise specified, values come from a uniform distribution.

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
- **ratio** : Provide an array of values follwed by an associated ratio. Choices must match data type
	- [["M", "F"], [1, 3]] - for every "M", there will be roughly 3 "F" (i.e prob of .25/.75)
- **distribution** : For non choice/ratio/string types.
	- "uniform" - random values are uniformly generated
	- "normal" - mean = 0, stddev = 1
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

Here's an example showing different random distributions:

```
{
  "name" : "SampleDistributionTable",
  "columns": [
    {
      "name": "ID",
      "incremental": "1",
      "description" : "Unique Key - start at 1",
      "type": "0",
      "minimum": "1",
      "format": "0000d"
    },
    {
      "name" : "uniform-int",
      "description" : "Random integers between 1 and 1000",
      "type": "0",
      "minimum": "1",
      "maximum" : "1000",
      "distribution" : "uniform",
      "format" : "000d"
    },
    {
      "name" : "uniform-float",
      "description" : "Random floats between 1 and 1000",
      "type": "1",
      "minimum": "1",
      "maximum" : "1000",
      "distribution" : "uniform",
      "format" : "000.2f"
    },
    {
      "name" : "normal-int",
      "description" : "Normally distributed integers between 1 and 1000",
      "type": "0",
      "minimum": "1",
      "maximum" : "1000",
      "distribution" : "normal",
      "format" : "000d"
    },
    {
      "name" : "normal-float",
      "description" : "Normally distributed floats between 1 and 1000",
      "type": "0",
      "minimum": "1",
      "maximum" : "1000",
      "distribution" : "normal",
      "format" : "000.2f"
    }
  ]
}
```

And the resulting csv format:

```
"ID", "uniform-int", "uniform-float", "normal-int", "normal-float"
1, 433, 563.26, 1091, -401.00
2, 996, 95.54, 285, -1944.00
3, 826, 653.35, 1728, 481.00
4, 835, 28.26, -1685, 2016.00
5, 944, 287.54, 894, -1343.00
6, 450, 171.63, 1229, 1528.00
7, 559, 685.98, -872, 1506.00
8, 636, 173.06, 40, 811.00
9, 585, 754.92, -600, 81.00
10, 334, 980.51, -1466, -927.00
11, 738, 558.86, 915, -1417.00
12, 171, 874.17, 837, 744.00
13, 291, 596.12, -2001, 973.00
14, 298, 972.18, 453, 962.00
15, 957, 193.72, 390, 1169.00
16, 507, 719.78, 579, 721.00
17, 673, 988.89, 280, -734.00
18, 114, 905.38, -599, 1208.00
19, 387, 152.08, 467, 2417.00
20, 363, 386.25, 12, -464.00
21, 827, 312.18, 402, 725.00
22, 883, 358.24, -151, 1028.00
23, 965, 170.87, -24, 367.00
24, 94, 606.57, -165, 475.00
25, 720, 825.31, 732, 410.00
26, 822, 300.59, 800, 199.00
27, 9, 970.80, 2705, -185.00
28, 659, 988.13, 503, 1093.00
29, 536, 524.47, -297, -1315.00
30, 119, 856.55, 197, -246.00
31, 188, 569.63, 760, -1446.00
32, 89, 151.97, 637, -1417.00
33, 960, 461.95, 710, -24.00
34, 651, 451.81, -298, -518.00
35, 821, 772.92, -180, -354.00
36, 248, 668.12, -1020, -944.00
37, 806, 840.86, -1917, -681.00
38, 305, 589.04, 1162, 904.00
39, 143, 192.70, 1818, 120.00
40, 363, 966.02, -1582, -551.00
41, 696, 540.99, 719, 200.00
42, 888, 596.26, -1310, 527.00
43, 662, 499.83, 1711, 2603.00
44, 141, 551.31, 2383, -59.00
45, 488, 876.60, -143, 1154.00
46, 522, 59.49, 217, -326.00
47, 121, 831.75, -179, -536.00
48, 281, 661.00, -1104, 247.00
49, 64, 471.41, -54, 313.00
50, 638, 995.06, 337, 103.00
```



