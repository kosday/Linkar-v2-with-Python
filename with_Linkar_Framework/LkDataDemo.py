################
## Library Links
################
from Linkar.Linkar import CredentialOptions
from Linkar_Functions.Linkar.Functions import LinkarFunctions
from Linkar_Strings.Linkar.Strings.StringFunctions import StringFunctions
from Linkar_Functions_Persistent_MV.Linkar.Functions.Persistent.MV.LinkarClient import LinkarClient
from Linkar_LkData.Linkar.LkData.LkDataCRUD import LkDataCRUD
from Linkar_LkData.Linkar.LkData.LkDataSubroutine import LkDataSubroutine
from Linkar_LkData.Linkar.LkData.LkDataExecute import LkDataExecute
from Linkar_LkData.Linkar.LkData.LkItems import LkItems
from Linkar_LkData.Linkar.LkData.LkItem import LkItem

################
## Auxiliary functions
################
def PrintErrors(errors):
	for err in errors:
		print(StringFunctions.FormatError(err))

def PrintRecord(lkItem):
	print("RecordId: " + lkItem.RecordId + " Record:" + lkItem.Record)

def PrintRecords(lkItems):
	for lkItem in lkItems:
		PrintRecord(lkItem)

################
## Demo
################

print("Demo start")

try:
	## Create credentials
	crdOpt = CredentialOptions(
		"127.0.0.1",			# Linkar Server IP or Hostname
		"EPNAME",				# EntryPoint Name
		11300,					# Linkar Server EntryPoint port
		"admin",				# Linkar Server Username
		"admin",				# Linkar Server Username Password
		"",						# Language
		"Test Python")			# Free text

	## Create Linkar Client
	lkClt = LinkarClient(60)
	## Execute Login operation
	lkClt.Login(crdOpt)
	## In this demo we are going to work with the LK.CUSTOMERS file
	filename = "LK.CUSTOMERS"

	## Create RECORD list with dictionaries
	print("NEW OPERATION (NEW98 and NEW)")

	lstLkRecords = LkItems(["ID"], ["NAME", "ADDRRESS"])

	## Create RECORD1 from original data
	record1 = "CUSTOMER NEW98" + LinkarFunctions.DBMV_Mark.AM_str + "ADDRESS NEW98" + LinkarFunctions.DBMV_Mark.AM_str + "998 - 998 - 998"
	lkRecord1 = LkItem("NEW98", record1)
	## Add RECORD1 to the list
	lstLkRecords.push(lkRecord1)

	## Create empty RECORD2
	lkRecord2 = LkItem("NEW99")
	## Add RECORD2 to the list
	lstLkRecords.push(lkRecord2)
	## Fill his properties using dictionaries
	lkRecord2.set("CUSTOMER NEW99", "NAME") ## Attribute 1 value
	lkRecord2.set("ADDRESS NEW99", "ADDRRESS", 1) ## Attribute 2, Multivalue 1
	lkRecord2.set("STATE COUNTRY", "ADDRRESS", 2) ## Attribute 2, Multivalue 2
	## Fill property using attribute number
	lkRecord2.set("999 - 999 - 999", 3) ## Attribute3 value

	## Generate New operation buffer from list
	records = lstLkRecords.ComposeNewBuffer()
	## Create New operation options
	newOptions = LinkarFunctions.NewOptions(None, True, False, False, False, True) ## ReadAfter and OriginalRecords
	## Execute New operation
	newResult = lkClt.New(filename, records, newOptions)
	## Create LkDataCRUD complex object from operation result string
	lkData = LkDataCRUD(newResult)
	## Print result
	print("TOTAL RECORDS: " + str(lkData.TotalItems))
	PrintErrors(lkData.Errors)
	PrintRecords(lkData.LkRecords)

	## You can extract records from list
	lkRecord1 = lkData.LkRecords.get("NEW98")
	## Or delete them from the list.
	lkData.LkRecords.removeId("NEW98")

	## After CRUD Operation we always get real dictionaries
	## You can modify values from list using these dictionaries
	lkData.LkRecords.get("NEW99").set("CUSTOMER UPDATE99", "NAME")
	lkData.LkRecords.get("NEW99").set("ADDRESS UPDATE 99", "ADDR")
	lkData.LkRecords.get("NEW99").set("(1) 999 - 999 - 999", "PHONE")

	print("")
	## Next step a Update
	print("UPDATE OPERATION (NEW99)")
	## With the optimistic lock you will avoid modifying records that have been previously modified by another user.
	OptimisticLockControl = True
	## Create Update operation options
	updateOptions = LinkarFunctions.UpdateOptions(OptimisticLockControl, True, False, False, False, True) ## OptimisticLockControl, ReadAfter and OriginalRecords  
	## Generate Update operation buffer from list      
	records = lkData.LkRecords.ComposeUpdateBuffer(OptimisticLockControl)
	## Execute Update operation
	updateResult = lkClt.Update(filename, records, updateOptions)
	## Create LkDataCRUD complex object from operation result string
	lkData = LkDataCRUD(updateResult)
	## Print result
	PrintErrors(lkData.Errors)
	PrintRecords(lkData.LkRecords)

	print("")
	## Next step a Read
	print("READ OPERATION (NEW98 and NEW99)")
	## Generate Read operation buffer
	recordIds = StringFunctions.ComposeRecordIds(["NEW98", "NEW99"])
	## Create Read operation options
	readOptions = LinkarFunctions.ReadOptions(False, False, False, OptimisticLockControl)
	## Execute Read operation
	readResult = lkClt.Read(filename, recordIds, "", readOptions)
	## Create LkDataCRUD complex object from operation result string
	lkDataRead = LkDataCRUD(readResult)
	## Print result
	print("TOTAL RECORDS: " + str(lkDataRead.TotalItems))
	## Here are different ways to access the records.
	## With position
	lkRecord1 = lkDataRead.LkRecords[0]
	PrintRecord(lkRecord1)
	## Or with ID
	lkRecord2 = lkDataRead.LkRecords.get("NEW99")
	PrintRecord(lkRecord2)
	## Now different ways to access the content of a record
	## Extract ID from his property
	id = lkRecord2.RecordId
	print("record2.RecordId: " + id)
	## Extract ID using his dictionary
	id = lkRecord2.get("ID")
	print("record2[\"ID\"]: " + id)
	## Get NAME attribute with his dictionary
	name = lkRecord2.get("NAME")
	print("record2[\"NAME\" , 1]: " + name)
	## Get ADDR attribute first multivalue with his dictionary
	addressLine1 = lkRecord2.get("ADDR", 1)
	print("record2[\"ADDR\" , 2]: " + addressLine1)
	## Get ADDR attribute second multivalue with his dictionary
	addressLine2 = lkRecord2.get("ADDR", 2)
	print("record2[\"ADDR\" , 2]: " + addressLine2)
	## Get the first record NAME attribute with his dictionary
	name = lkDataRead.LkRecords[1].get("NAME")
	print("lkReadResult.LkRecords[1][\"NAME\"]: " + name)

	print("")
	## Next step a Delete
	print("DELETE OPERATION (NEW98 and NEW99)")
	## With the optimistic lock you will avoid deleting records that have been previously modified by another user
	OptimisticLockControl = True
	## Create Delete operation options
	deleteOptions = LinkarFunctions.DeleteOptions(OptimisticLockControl)
	## Insert RECORD1 to the list, you had previously deleted it
	lkData.LkRecords.push(lkRecord1)
	## Generate Delete operation buffer
	records = lkData.LkRecords.ComposeDeleteBuffer(OptimisticLockControl)
	## Execute Delete operation
	deleteResult = lkClt.Delete(filename, records, deleteOptions)
	## Create LkDataCRUD complex object from operation result string
	lkData = LkDataCRUD(deleteResult)
	## Print result
	PrintErrors(lkData.Errors)
	PrintRecords(lkData.LkRecords)

	print("")
	## Next step a Subroutine
	print("SUBROUTINE OPERATION")
	## Generate Subroutine operation buffer
	subArgs = StringFunctions.ComposeSubroutineArgs(["0", "aaaaaaa", ""])
	## Execute Subroutine operation
	subroutineResult = lkClt.Subroutine("SUB.DEMOLINKAR", 3, subArgs)
	## Create LkDataSubroutine complex object from operation result string
	lkDataSubroutine = LkDataSubroutine(subroutineResult)
	## Print result
	PrintErrors(lkDataSubroutine.Errors)
	i = 0
	while i < len(lkDataSubroutine.Arguments):
		print("Arg " + str(i + 1) + " " + lkDataSubroutine.Arguments[i])
		i += 1

	print("")
	## Next step a Execute
	print("EXECUTE WHO")
	## Execute WHO database command
	executeResult = lkClt.Execute("WHO")
	## Create LkDataExecute complex object from operation result string
	lkDataExecute = LkDataExecute(executeResult)
	## Print result
	PrintErrors(lkDataExecute.Errors)
	print("CAPTURING: " + lkDataExecute.Capturing)
	print("RETURNING: " + lkDataExecute.Returning)

	## Execute Logout operation
	lkClt.Logout("",0)

	print("Demo OK!")

except Exception as ex:
	print("ERROR: " + str(ex))
