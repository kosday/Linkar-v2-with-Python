################
## Library Links
################
from Linkar.Linkar import CredentialOptions
from Linkar_Functions.Linkar.Functions import LinkarFunctions
from Linkar_Strings.Linkar.Strings.StringFunctions import StringFunctions
from Linkar_Functions_Persistent_MV.Linkar.Functions.Persistent.MV.LinkarClient import LinkarClient

import json

################
## Auxiliary functions
################
## Extract data from string result and print
def process_result(transaction, lkString):
## Check Errors in transaction
	lstError = StringFunctions.ExtractErrors(lkString)
	if len(lstError) > 0 :
		print("Found " + str(len(lstError)) + " errors in '" + transaction + "' transaction")
		for err in lstError:
			print(err)

		exit()
	else:
		print("No errors in transaction!")

		##Extract values
		if transaction == 'Subroutine':
			lstOutArgs = StringFunctions.ExtractSubroutineArgs(lkString)
			return json.dumps({ 'lstError': lstError, 'lstOutArgs': lstOutArgs })
		elif transaction == 'Conversion':
			lstConversion = StringFunctions.ExtractConversion(lkString)
			return json.dumps({ 'lstError': lstError, 'lstConversion': lstConversion })
		elif transaction == 'Format':
			lstFormat = StringFunctions.ExtractFormat(lkString)
			return json.dumps({'lstError': lstError, 'lstFormat': lstFormat })
		elif transaction == 'Execute' or transaction == 'ResetCommonBlocks':
			lstCapturing = StringFunctions.ExtractCapturing(lkString)
			lstReturning = StringFunctions.ExtractReturning(lkString)
			return json.dumps({ 'lstError': lstError, 'lstCapturing': lstCapturing, 'lstReturning': lstReturning })
		else:
			lstRecordIds = StringFunctions.ExtractRecordIds(lkString)
			lstRecord = StringFunctions.ExtractRecords(lkString)
			return json.dumps({ 'lstError': lstError, 'lstRecordIds': lstRecordIds, 'lstRecord': lstRecord })


#################################
# DEMO                          #
#################################

print("Demo start")

customVars = ''
receiveTimeout = -1

try:
	################
	## LkLogin
	################
	print("LkLogin")
	print("--------")
	
	# Create credentials
	crdOpt = CredentialOptions(
		"127.0.0.1",		  	# Linkar Server IP or Hostname
		"EPNAME",			  	# EntryPoint Name
		11300,				  	# Linkar Server EntryPoint port
		"admin",			  	# Linkar Server Username
		"admin",			  	# Linkar Server Username Password
		"",					    # Language
		"Test Python") 			# Free text
	
	print("PORT: " + str(crdOpt.Port))
	## Create Linkar Client
	clt = LinkarClient()
	## Execute Login operation
	clt.Login(crdOpt, "", 600)
	
	################
	## LkNew
	################
	print("-- LkNew --")
	print("--------")
	
	## In this demo we are going to work with the LK.CUSTOMERS file
	filename = 'LK.CUSTOMERS'
	## Generate New operation buffer
	strNewId = 'A90'
	strNewRecord = 'CUSTOMER 99' + LinkarFunctions.DBMV_Mark.AM_str + 'ADDRESS 99' + LinkarFunctions.DBMV_Mark.AM_str + '999 - 999 - 99'
	newBuffer = StringFunctions.ComposeNewBuffer(strNewId, strNewRecord)
	## Create New operation options
	newOptions = LinkarFunctions.NewOptions(LinkarFunctions.RecordIdType(), True, False, False, False, False)
	## Execute New operation
	result = clt.New(filename, newBuffer, newOptions, "", 60)
	## Extract data from string result and print
	output = process_result('New', result)
	jsonOutput = json.loads(output)
	lstRecordIds = jsonOutput['lstRecordIds']
	lstRecord = jsonOutput['lstRecord']
	strRecordId = lstRecordIds[0]
	strRecord = lstRecord[0]
	print('strRecordId: ' + strRecordId)
	print('strRecord: ' + strRecord)
	
	################/
	## LkExtract
	################/
	print("-- LkExtract --")
	print("--------")
	
	## Extract and print one element from multivalue string
	result = LinkarFunctions.MvOperations.LkExtract(strRecord, 1)
	print(result)
	
	################/
	## LkReplace
	################/
	print("-- LkReplace --")
	print("--------")
	
	## Replace one element from multivalue string and print
	replaceVal = "UPDATED CUSTOMER"
	result = LinkarFunctions.MvOperations.LkReplace(strRecord, replaceVal, 1)
	print(result)
	
	################/
	## LkChange
	################/
	print("-- LkChange --")
	print("--------")
	
	## Replaces the occurrences of a substring inside a string, by other substring and print
	result = LinkarFunctions.MvOperations.LkChange(strRecord, "9", "8")
	print(result)
	
	################/
	## LkCount
	################/
	print("-- LkCount --")
	print("--------")
	
	## Counts the occurrences of a substring inside a string and print
	result = LinkarFunctions.MvOperations.LkCount(strRecord, LinkarFunctions.DBMV_Mark.AM)
	print(result)
	
	################/
	## LkDCount
	################/
	print("-- LkDCount --")
	print("--------")
	
	## Counts the delimited substrings inside a string and print
	result = LinkarFunctions.MvOperations.LkDCount(strRecord, LinkarFunctions.DBMV_Mark.AM)
	print(result)
	
	################/
	## LkUpdate
	################/
	print("-- LkUpdate --")
	print("--------")
	
	## Create Update operation options
	updateOptions = LinkarFunctions.UpdateOptions(False, True, False, False, False, False)
	## Generate Update operation buffer
	updateBuffer = StringFunctions.ComposeUpdateBuffer(strNewId, strNewRecord, "")
	## Execute Update operation
	result = clt.Update(filename, updateBuffer, updateOptions, "", 60)
	## Extract data from string result and print
	output = process_result('Update', result)
	jsonOutput = json.loads(output)
	lstRecordIds = jsonOutput['lstRecordIds']
	lstRecord = jsonOutput['lstRecord']
	if len(lstRecordIds) > 0:
		print("--> Data Contents")
		i = 0
		while i < len(lstRecordIds):
			print("Id:" + lstRecordIds[i] + " Data:" + lstRecord[i])
			i += 1
	
	################/
	## LkRead
	################/
	print("-- LkRead --")
	print("--------")
	
	dictionaries = ""
	## Create Read operation options
	readOptions = LinkarFunctions.ReadOptions(True, False, False, False)
	## Execute Read operation
	result = clt.Read(filename, strNewId, dictionaries, readOptions, "", 60)
	## Extract data from string result and print
	output = process_result('Read', result)
	jsonOutput = json.loads(output)
	lstRecordIds = jsonOutput['lstRecordIds']
	lstRecord = jsonOutput['lstRecord']
	if len(lstRecordIds) > 0:
		print("--> Data Contents")
		i = 0
		while i < len(lstRecordIds):
			print("Id:" + lstRecordIds[i] + " Data:" + lstRecord[i])
			i += 1
	
	################/
	## LkDelete
	################/
	print("-- LkDelete --")
	print("--------")
	
	## Generate Delete operation buffer
	deleteBuffer = StringFunctions.ComposeDeleteBuffer(strNewId, "")
	## Create Delete operation options
	deleteOptions = LinkarFunctions.DeleteOptions(False, LinkarFunctions.RecoverIdType())
	## Execute Delete operation
	result = clt.Delete(filename, deleteBuffer, deleteOptions, "", 60)
	## Extract data from string result and print
	output = process_result('Delete', result)
	
	################/
	## LkSubroutine
	################/
	print("-- LkSubRoutine --")
	print("--------")  
	
	subroutineName = 'SUB.DEMOLINKAR'
	## Generate Subroutine operation buffer
	args = StringFunctions.ComposeSubroutineArgs(["0", "qwerty", ""])
	## Execute Subroutine operation
	result = clt.Subroutine(subroutineName, 3, args, "", 60)
	## Extract data from string result and print
	output = process_result('Subroutine', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput["lstError"]
	if len(lstError) == 0:
		lstOutArgs = jsonOutput['lstOutArgs']
		print("Arguments result -> ", end="")
		print(lstOutArgs, sep=" ")
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkConversion
	################/
	
	print("-- LkConversion --")
	print("--------")
	
	code = "D2-"
	expression = "13320"
	conversionType = LinkarFunctions.CONVERSION_TYPE.OUTPUT
	## Execute Conversion operation
	result = clt.Conversion(conversionType, expression, code, "", 60)
	## Extract data from string result and print
	output = process_result('Conversion', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		lstConversion = jsonOutput['lstConversion']
		print("Arguments result -> " + lstConversion)
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkFormat
	################/
	print("-- LkFormat --")
	print("--------")
	
	formatSpec = "R%10"
	expression = "HELLO"
	## Execute Format operation
	result = clt.Format(expression, formatSpec, "", 60)
	## Extract data from string result and print
	output = process_result('Format', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		lstFormat = jsonOutput['lstFormat']
		print("Format result -> " + lstFormat)
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkExecute
	################/
	print("-- LkExecute --")
	print("--------")
	
	statement = "WHO"
	## Run Execute operation
	result = clt.Execute(statement, "", 60)
	## Extract data from string result and print
	output = process_result('Execute', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		lstReturning = jsonOutput['lstReturning']
		print("Execute returning result -> " + lstReturning)
		lstCapturing = jsonOutput['lstCapturing']
		print("Execute capturing result -> " + lstCapturing)
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkDictionaries
	################/
	print("-- LkDictionaries --")
	print("--------")
	
	## Execute Dictionaries operation
	result = clt.Dictionaries(filename, "", 60)
	## Extract data from string result and print
	output = process_result('Dictionaries', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		print("Dictionaries is OK!")
		lstRecordIds = jsonOutput['lstRecordIds']
		lstRecord = jsonOutput['lstRecord']
		if len(lstRecordIds) > 0:
			print("--> Data Contents")
			i = 0
			while i < len(lstRecordIds):
				print("Id:" + lstRecordIds[i] + " Data:" + lstRecord[i])
				i += 1
		else:
			print(jsonOutput['lstError'])
			print("Error while Dictionaries")
	
	################/
	## LkSelect
	################/
	print("-- LkSelect --")
	print("--------")
	## Create Select operation options
	selectOptions = LinkarFunctions.SelectOptions(False, False, 0, 0, True, False, False, False)
	
	selectClause = ""
	sortClause = "BY ID"
	dictClause = ""
	preSelectClause = ""
	## Execute Select operation
	result = clt.Select(filename, selectClause, sortClause, dictClause, preSelectClause, selectOptions, "", 600)
	## Extract data from string result and print
	output = process_result('Select', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		print("Select is OK!")
		lstRecordIds = jsonOutput['lstRecordIds']
		lstRecord = jsonOutput['lstRecord']
		if len(lstRecordIds) > 0:
			print("--> Data Contents")
			i = 0
			while i < len(lstRecordIds):
				print("Id:" + lstRecordIds[i] + " Data:" + lstRecord[i])
				i += 1
		else:
			pass
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkSchemas
	################/
	print("-- LkSchemas --")
	print("--------")
	
	## Create LkSchemas operation options
	lkSchemasOptions = LinkarFunctions.LkSchemasOptions()
	## Execute LkSchemas operation
	result = clt.LkSchemas(lkSchemasOptions, "", 600)
	## Extract data from string result and print
	output = process_result('Schemas', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		print("Schemas is OK!")
		lstRecordIds = jsonOutput['lstRecordIds']
		lstRecord = jsonOutput['lstRecord']
		if len(lstRecordIds) > 0:
			print("--> Data Contents")
			i = 0
			while i < len(lstRecordIds):
				print("Id:" + lstRecordIds[i] + " Data:" + lstRecord[i])
				i += 1
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkProperties
	################/
	print("-- LkProperties --")
	print("--------")
	
	## Create LkProperties operation options
	lkPropertiesOptions = LinkarFunctions.LkPropertiesOptions();
	filename = "LK.ORDERS"
	## Execute LkProperties operation
	result = clt.LkProperties(filename, lkPropertiesOptions, "", 600)
	## Extract data from string result and print
	output = process_result('Properties', result)
	jsonOutput = json.loads(output)
	lstError = jsonOutput['lstError']
	if len(lstError) == 0:
		print("Properties is OK!")
		lstRecordIds = jsonOutput['lstRecordIds']
		lstRecord = jsonOutput['lstRecord']
		if len(lstRecordIds) > 0:
			print("--> Data Contents")      
			i=0
			while i < len(lstRecordIds):
				print("Id:" + lstRecordIds[i] + " Data:" + lstRecord[i])
				i += 1
	else:
		print(jsonOutput['lstError'])
		print("Error while conversion")
	
	################/
	## LkResetCommonBlocks
	################/
	print("-- LkResetCommonBlocks --")
	print("--------")
	
	## Execute ResetCommonBlocks operation
	result = clt.ResetCommonBlocks(600)
	## Extract data from string result and print
	output = process_result('ResetCommonBlocks', result)
	jsonOutput = json.loads(output)
	lstErro = jsonOutput['lstError']
	if len(lstError) == 0:
		lstReturning = jsonOutput['lstReturning']
		print("ResetCommonBlocks returning result -> " + lstReturning)
		lstCapturing = jsonOutput['lstCapturing']
		print("ResetCommonBlocks capturing result -> " + lstCapturing)
	else:
		print(jsonOutput['lstError'])
		print("Error while ResetCommonBlocks")
	
	################/
	## LkLogout
	################/
	print("-- LkLogout --")
	print("--------")
	
	## Execute Logout operation
	result = clt.Logout("", 600)
	
	print("Demo OK!")
	
except Exception as ex:
		print("ERROR: " + str(ex))
