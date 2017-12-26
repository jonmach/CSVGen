'''
Class that can generate random dummy data (CSV format) for general data tests.

Author: Jon Machtynger
Date: 21 December 2017

See README.md for description of usage
'''

import json
import string
import random
import datetime
import time
import logging as log
import rstr


class CSVGen:

	# Define some Class Constants
	defaultRows = 10
	defaultNullOdds = 10
	minFloat = -2.0 ** 32  # -2 ^ 32
	maxFloat = 2.0 ** 32  # 2 ^ 32
	minInt = int(minFloat)  # Same range as Int, but with decimal point
	maxInt = int(maxFloat)  # Same range as Int, but with decimal point
	minDate = "19700101"  # Specify this in YYYYMMDD format
	maxDate = "20361231"  # Specify this in YYYYMMDD format
	minDateTime = "19700101000000"  # Specify this in YYYYMMDDHHMMSS format
	maxDateTime = "20361231235959"  # Specify this in YYYYMMDDHHMMSS format
	defaultIntOPFormat = "d"
	defaultFloatOPFormat = "0.2f"
	defaultStringOPFormat = "s"
	defaultDateOPFormat = "s"
	defaultDateFormat = "%d/%m/%Y"  # e.g. 13/01/2003
	defaultDateTimeFormat = "%d/%m/%Y %H:%M:%S"  # e.g. 13/01/2003 12:34:12
	defaultStringLen = 30  # This is long enough to have something in it, but not too long


	def __init__(self, numRows=defaultRows, nullOdds = 10, iFile="", oFile="", verbose=False):

		self.nullOdds = nullOdds  # 1 in NullOdds chance of generating a NULL
		self.numRows = numRows
		self.verbose = verbose

		if verbose:
			log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
		else:
			log.basicConfig(format="%(levelname)s: %(message)s")

		log.info("Validating Schema...")

		if (iFile == ""):
			log.error("Error: You must specify a schema file argument (iFile=...)")
			return

		if (oFile == ""):
			log.error("Error: You must specify an output CSV file argument (oFile=...)")
			return

		data = self.valid8Schema(iFile)
		if (not data):
			return

		# Now write out the CSV File
		log.info("Writing output file...")
		self.writeCSVFile(oFile, data)

	'''
	For a CSV format, we don't need a table name
	We simply go through each column and populate it with dummy data
	'''
	def writeCSVFile(self, fName, data):
		log.info("Creating the CSV file... %s" % fName)

		try:
			opFile = open(fName, 'w')
		except IOError as e:
			log.error("Error creating '%s': %s" % (fName, e.strerror))
			return None

		# The first row contains the column names
		for idx, c in enumerate(data['columns']):
			if (idx > 0):
				opFile.write(', "%s"' % c['name'])
			else:
				opFile.write('"%s"' % c['name'])

		opFile.write("\n")
		# Now populate it with some data...

		for i in range(self.numRows):
			for idx, c in enumerate(data['columns']):
				if (idx > 0):
					s = ', %s' % (self.generate_column(c))
				else:
					s = '%s' % (self.generate_column(c))
				opFile.write(s)
			opFile.write("\n")
		log.info("Wrote %d rows" % self.numRows)

		opFile.close()

	def parseJSON(self, text):
		try:
			return json.loads(text)
		except ValueError as e:
			log.error('Invalid JSON: %s' % e)
			return None

	def validFloat(self, str):
		try:
			f = float(str)
			return True
		except ValueError:
			return False

	def validDate(self, date_text):
		try:
			datetime.datetime.strptime(date_text, '%Y%m%d')
			return True
		except ValueError:
			return False

	def validDateTime(self, date_text):
		try:
			datetime.datetime.strptime(date_text, '%Y%m%d%H%M%S')
			return True
		except ValueError:
			return False

	def valid8Field(self, data, column):
		colName = column.get('name')
		if (not colName):						# name is a mandatory attribute
			log.error("Error: Missing column 'name' attribute")
			return None

		log.info("Validating column %s " % colName)
		colType = column.get('type')			# type is a mandatory attribute
		if (not colType):
			log.warning("Error: Column '%s' is missing the 'type' attribute" % colName)
			return None

		if colType not in '01234':
			log.error("Error: Column %s is set to %s. It must be either:" % (colName, colType))
			log.error("     0 - Integer, 1 - Float, 2 - String, 3 - Date, 4 - DateTime")
			return None

		colMin = column.get('minimum')	# Numeric and date columns may have a minimum
		colMax = column.get('maximum')	# Numeric and date columns may have a maximum
		colNULLS = column.get('NULLS')	# Allow NULL (i.e. empty) data tp be generated
		colIncremental = column.get('incremental')	# Use this as an incremental (e.g. unique key) column
		colChoice = column.get('choice')	# Provide a choice of values

		if colType in "01":		# numeric

			if (colType == "0"): # Integer

				# If no minimum is defined, start the incremental at 1
				if (colIncremental and not colMin):
					colMin = 1

				if (colMin and (colMin.isdigit() == False)):
					log.error("Error: Column '%s': Minimum value of '%s' is not an integer" % (colName, colMin))
					return None
				if (colMax and colMax.isdigit() == False):
					log.error("Error: Column '%s': Maximum value of '%s' is not an integer" % (colName, colMax))
					return None

				if (not colMin):
					colMin = self.minInt
				if (not colMax):
					colMax = self.maxInt

				if (colIncremental):
					column['counter'] = str(colMin)  # Add a counter column to increment from
					if (int(colMin) + int(self.numRows)) > int(colMax):
						log.error("Error: Column '%s': Incremental row would exceed Maximum value of '%s' for %s rows" % (colName, colMax, self.numRows))
						return None
					if (colChoice):
						log.error("Error: Column '%s': You cannot specify a choice of values in an incremental row " % (colName))
						return None

			if (colType == "1"): # Float/Decimal
				if (colIncremental == "1"):
					log.error("Error: Column '%s': Only Integer columns can be defined as incremental" % (colName))
					return None

				if (not colMin):
					colMin = self.minFloat
				if (not colMax):
					colMax = self.maxFloat

				if (colMin and self.validFloat(colMin) == False):
					log.error("Error: Column '%s': Minimum value of '%s' is not a float" % (colName, colMin))
				if (colMax and self.validFloat(colMax) == False):
					log.error("Error: Column '%s': Maximum value of '%s' is not a float" % (colName, colMax))

			# Test ranges by casting to float. That works for both float and int
			if (colMin and colMax) and (float(colMin) > float(colMax)):
				log.error("Error: Column '%s': Minimum of %s is greater than Maximum of %s" % (colName, colMin, colMax))
				return None

			# If minimum specified, but no maximum, set it
			if (colMin and not colMax):
				if (colType == "0"):
					column['maximum'] = self.maxInt
				else:
					column['maximum'] = self.maxFloat
				log.warning("Warning: Column '%s': Minimum specified of %s, but no maximum" % (colName, colMin))
				log.warning('  --> Assigning a maximum value of %s' % column['maximum'])

			if (not colMin and colMax):
				if (colType == "0"):		# Integer
					column['minimum'] = str(self.minInt)
				else:						# Float / Decimal
					column['minimum'] = str(self.minFloat)
				log.warning("Warning: Column '%s': Maximum specified of %s, but no minimum" % (colName, colMax))
				log.warning('  --> Assigning a minimum value of %s' % column['minimum'])

		if (colType == "2"):
			if (colIncremental == "1"):
				log.error("Error: Column '%s': Only Integer columns can be defined as incremental" % (colName))
				return None

		if colType in "34":					# Date or DateTime
			if (colIncremental == "1"):
				log.error("Error: Column '%s': Only Integer columns can be defined as incremental" % (colName))
				return None

			if colType == "3":
				if (not colMin):
					colMin = self.minDate
				if (not colMax):
					colMax = self.maxDate

				if (self.validDate(colMin) == False):
					log.error("Error: Column '%s': Minimum value of '%s' is not valid date in the format YYYYMMDD" % (colName, colMin))
					return None

			if colType == "4":
				if (not colMin):
					colMin = self.minDateTime
				if (not colMax):
					colMax = self.maxDateTime

				if (self.validDateTime(colMin) == False):
					log.error("Error: Column '%s': Minimum value of '%s' is not valid datetime in the format YYYYMMDDHHMMSS" % (colName, colMin))
					return None

			if (colMin and not colMax):
				column['maximum'] = self.maxDate
				log.warning("Warning: Column '%s': Minimum specified of %s, but no maximum" % (colName, colMin))
				log.warning('  --> Assigning a maximum value of %s' % column['maximum'])

			if (colMax and not colMin):
				column['minimum'] = self.minDate
				log.warning("Warning: Column '%s': maximum specified of %s, but no minimum" % (colName, colMax))
				log.warning('  --> Assigning a minimum value of %s' % column['minimum'])

		# We make a huge assumption here that formats are valid. It's pointless going
		# overboard trying to valid every possibility
		colFormat = column.get('format')

		if (not colFormat):	# A format is mandatory
			log.warning("Warning: Column '%s' is missing the 'format' attribute. A default will be used" % colName)

		# Strings
		if (colNULLS and colNULLS not in "01"):
			log.error("Column '%s': NULLS has value '%s' but can only have a value of '0' or '1'" % (colName, colNULLS))

		return column

	'''
		Load the Schema file and validate its contents
	'''
	def valid8Schema(self, fname):

		try:
			file = open(fname, 'r')
		except IOError as e:
			log.error("Error opening '%s': %s" % (fname, e.strerror))
			return None

		schema = file.read()
		data = self.parseJSON(schema)

		if (data == None):		# Structural error
			return None

		# Now confirm mandatory fields are there

		# Table must have a name
		if (not data.get('name')):
			log.error("Validating Schema: You must provide a core name attribute")
			return None

		columns = data.get('columns')

		if (not columns):
			log.error("Validating Schema: You must have a columns attribute")
			return None

		# Remove the columns entries - we'll rebuild them while validating (and adding values)
		data.pop('columns')
		data['columns']=[]

		for c in columns:
			if not self.valid8Field(data, c):
				log.error('Error in processing column %s ' % c)
				return None
			else:	# Data may have been updated in the validation process
				data['columns'].append(c)

		if (data != None):
			return data

	def RandomNull(self, val):
		isNull = random.randint(0, self.nullOdds)
		if (isNull == int(self.nullOdds / 2)):
			return ""
		else:
			return val

	'''
	Generate random data for a column
	'''
	def generate_column(self, column):
		colType = column.get('type')
		colMin = column.get('minimum')
		colMax = column.get('maximum')
		colLen = column.get('length')
		colNULLS = column.get('NULLS')
		colFormat = column.get('format')
		colIncremental = column.get('incremental')
		colChoice = column.get('choice')
		colRegex = column.get('regex')

		# With a choice of values, no need for min/max
		if (colChoice):
			colMin="0"
			colMax="0"

		if colNULLS == "1":
			isNullable = True
		else:
			isNullable = False

		coreVal=""
		if colType == "0":	# Integer

			if (not colFormat):
				colFormat = self.defaultIntOPFormat

			if (colIncremental):
				# We don't allow NULLS
				coreVal = int(column.get('counter'))
				column['counter'] = str(int(coreVal) + 1)
			else:
				if not colMin:
					colMin = self.minInt
				if not colMax:
					colMax = self.maxInt
				coreVal = random.randint(int(colMin), int(colMax))
				if (colChoice):
					coreVal = random.choice(colChoice)
				else:
					if isNullable:
						coreVal = self.RandomNull(coreVal)

		if colType == "1":	# Float
			if not colMin:
				colMin = self.minFloat
			if not colMax:
				colMax = self.maxFloat

			coreVal = random.uniform(float(colMin), float(colMax))
			if (not colFormat):
				colFormat = self.defaultFloatOPFormat
			if (colChoice):
				coreVal = random.choice(colChoice)
			else:
				if isNullable:
					coreVal = self.RandomNull(coreVal)

		if colType == "2":	# String
			if not colLen:
				colLen = self.defaultStringLen
			colLen = int(colLen)
			if (not colFormat):
				colFormat = self.defaultDateOPFormat
			if colRegex:
				coreVal = rstr.xeger(colRegex)
			else:
				coreVal = rstr.xeger('[A-Z][A-Za-z     0-9]{1,%s}' % colLen)
				# coreVal = ''.join(random.choice(string.ascii_lowercase + "             " + string.ascii_uppercase + string.digits) for _ in range(colLen))
			if (colChoice):
				coreVal = random.choice(colChoice)
			else:
				if isNullable:
					coreVal = self.RandomNull(coreVal)

		if colType == "3":	# Date
			if (not colFormat):
				colFormat = self.defaultDateFormat			# This is not the OP format, but used for strftime

			if (colChoice):
				choice = time.mktime(time.strptime('%s' % (random.choice(colChoice)), '%Y%m%d'))
				coreVal = time.strftime(colFormat, time.localtime(choice))
			else:
				if not colMin:
					colMin = self.minDate
				if not colMax:
					colMax = self.maxDate

				d1 = time.mktime(time.strptime('%s' % (colMin), '%Y%m%d'))
				d2 = time.mktime(time.strptime('%s' % (colMax), '%Y%m%d'))

				# Take the default output date format from constants at beginning of File
				coreVal = time.strftime(colFormat, time.localtime(d1 + random.random() * (d2 - d1)))

				if isNullable:
					coreVal = self.RandomNull(coreVal)

			colFormat = self.defaultDateOPFormat		# Reuse variable for python format

		if colType == "4":	# DateTime
			if (not colFormat):
				colFormat = self.defaultDateTimeFormat			# This is not the OP format, but used for strftime

			if (colChoice):
				choice = time.mktime(time.strptime('%s' % (random.choice(colChoice)), '%Y%m%d%H%M%S'))
				coreVal = time.strftime(colFormat, time.localtime(choice))
			else:
				if not colMin:
					colMin = self.minDateTime
				if not colMax:
					colMax = self.maxDateTime

				d1 = time.mktime(time.strptime('%s' % (colMin), '%Y%m%d%H%M%S'))
				d2 = time.mktime(time.strptime('%s' % (colMax), '%Y%m%d%H%M%S'))

				# Take the default output date format from constants at beginning of File
				coreVal = time.strftime(colFormat, time.localtime(d1 + random.random() * (d2 - d1)))

				if isNullable:
					coreVal = self.RandomNull(coreVal)

			colFormat = self.defaultDateOPFormat		# Reuse variable for python format

		# If the value is blank (i.e. NULL), then it doesn't need a formatted string
		if (coreVal == ""):
			return ""
		else:
			return "{:{fmt}}".format(coreVal, fmt=colFormat)


#G = GenerateData(iFile="sample.json", oFile="opfile.csv", numRows=20, verbose=True)
