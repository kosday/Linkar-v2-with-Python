import ctypes
import sys
import LinkarClientPy
import logging


#LOG_FORMAT = '%(asctime)s :: %(levelname)8s :: %(filename)16s:%(lineno)3s :: %(message)s'
#LOG_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'
LOG_FORMAT = '%(asctime)s | %(levelname)4s | %(lineno)3s | %(message)s'
LOG_DATE_FORMAT = '%H:%M:%S'


def get_logger(appName='Console', logLevel=logging.INFO):
    logger = logging.getLogger(appName)

    # fileHandler = logging.FileHandler("{0}/{1}.log".format('.', 'linkar'))
    # fileHandler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    # logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    logger.addHandler(consoleHandler)

    logger.setLevel(logLevel)
    return logger


def get_console_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    return handler


def process_result(transaction, result):
    hasError = result['hasError']
    lkString = result['lkString']
    if hasError:
        logger.error("Error while " + transaction)
    else:
        # Check Errors in transaction
        lstError = linkar_client.LkGetErrorsFromLkString(lkString)
        if len(lstError) > 0:
            logger.info("Found " + str(len(lstError)) + " errors in '" + transaction + "' transaction")
            logger.info(lstError)
        else:
            logger.info("No errors in transaction!")

        # Retrieve created record
        lstRecordIds = linkar_client.LkGetRecordIdsFromLkString(lkString)
        lstRecord = linkar_client.LkGetRecordsFromLkString(lkString)
        return {'lstError': lstError, 'lstRecordIds':lstRecordIds, 'lstRecord':lstRecord}


if __name__ == "__main__":

    logger = get_logger()
    linkar_client = LinkarClientPy.LinkarClient()

    DBMV_Mark_AM = int('FE', base=16)
    DBMV_Mark_VM = int('FD', base=16)
    DBMV_Mark_AM_str = b"\xFE"
    ASCII_VT_str = b"\x0B"

    customVars = ''
    receiveTimeout = -1

    logger.info("LkLogin")
    logger.info("--------")
    crdOpt = linkar_client.LkCreateCredentialOptions("127.0.0.1",  	# IP or hostname of LINKAR SERVER
													 "EP_NAME", 	# ENTRYPOINT name
													 11300,			# EntryPoint Port number
 													 "user",		# LINKAR SERVER username
													 "password",	# LINKAR SERVER username password
													 "",			# LANGUAGE
													 "Test Python")	# Free Text

    port = linkar_client.LkGetDataFromCredentialOptions(crdOpt, LinkarClientPy.CredentialOptions.PORT)
    logger.info("PORT: " + str(port.decode(linkar_client.encoding)))


    result = linkar_client.LkLogin(crdOpt, "", 600)
    connectionInfo = result['lkString']
    hasError = result['hasError']
    if hasError:
        print("Failed login")
        print(result)
        logger.error("Failed login")
        sys.exit(-1)

    result = linkar_client.LkGetDataFromConnectionInfo(connectionInfo, LinkarClientPy.ConnectionInfo.SESSION_ID)
    logger.info( "SessionId:"+str(result.decode(linkar_client.encoding)) )

    #################
    # LkNew
    #################
    logger.info("-- LkNew --")
    logger.info("--------")
    filename = 'LK.CUSTOMERS'
    strNewId = 'A97'
    strNewRecord = 'CUSTOMER 99' + chr(DBMV_Mark_AM) +'ADDRESS 99' + chr(DBMV_Mark_AM) + '999 - 999 - 99'
    nop_newItemIdTypeNone = linkar_client.LkCreateNewRecordIdTypeNone()
    nop_readAfter = True
    nop_calculated = False
    nop_conversion = False
    nop_formatSpec = False
    nop_originalRecords = False
    newOptions = linkar_client.LkCreateNewOptions(nop_newItemIdTypeNone,
                                                            nop_readAfter, nop_calculated,
                                                            nop_conversion, nop_formatSpec,
                                                            nop_originalRecords)
    result = linkar_client.LkNew(connectionInfo, filename, strNewId, strNewRecord, newOptions,
                                        LinkarClientPy.IOFormat.MV, LinkarClientPy.IOFormatCru.MV,
                                        customVars, 600)

    strRecordId = None
    strRecord = None
    hasError = result['hasError']
    lkString = result['lkString']
    #logger.info(result)

    # Process Result
    output = process_result('New', result)
    lstRecordIds = output['lstRecordIds']
    lstRecord = output['lstRecord']
    strRecordId = str(lstRecordIds[0])
    strRecord = str(lstRecord[0])
    logger.info('strRecordId:' + strRecordId)
    logger.info('strRecord:' + strRecord)

    #################
    # LkExtract
    #################
    logger.info("-- LkExtract --")
    logger.info("--------")
    result = linkar_client.LkExtract(strRecord, 1, 0, 0)
    logger.info(result.decode(linkar_client.encoding))

    #################
    # LkReplace
    #################
    logger.info("-- LkReplace --")
    logger.info("--------")
    replaceVal = "UPDATED CUSTOMER"
    result = linkar_client.LkReplace(strRecord, replaceVal, 1, 0, 0)
    logger.info(result.decode(linkar_client.encoding))
    strRecord = result.decode(linkar_client.encoding)


    #################
    # LkChange
    #################
    logger.info("-- LkChange --")
    logger.info("--------")
    result = linkar_client.LkChange(strRecord, "9", "8", -1, -1)
    logger.info(result.decode(linkar_client.encoding))
    strRecord = result.decode(linkar_client.encoding)

    #################
    # LkCount
    #################
    logger.info("-- LkCount --")
    logger.info("--------")
    result = linkar_client.LkDCount(strRecord, chr(DBMV_Mark_AM))
    logger.info(result)

    #################
    # LkDCount
    #################
    logger.info("-- LkDCount --")
    logger.info("--------")
    result = linkar_client.LkDCount(strRecord, chr(DBMV_Mark_AM))
    logger.info(result)

    #################
    # LkUpdate
    #################
    logger.info("-- LkUpdate --")
    logger.info("--------")
    uop_optimisticLock = False
    uop_readAfter = True
    uop_calculated = False
    uop_conversion = False
    uop_formatSpec = False
    uop_originalRecords = False
    updateOptions = linkar_client.LkCreateUpdateOptions(uop_optimisticLock,
                                                        uop_readAfter, uop_calculated,
                                                        uop_conversion, uop_formatSpec,
                                                        uop_originalRecords)

    originalRecords = ''
    result = linkar_client.LkUpdate(connectionInfo, filename, strRecordId, strRecord,
                                        originalRecords, updateOptions,
                                        LinkarClientPy.IOFormat.MV, LinkarClientPy.IOFormatCru.MV,
                                        customVars, 600)
    output = process_result('Update', result)
    lstRecordIds = output['lstRecordIds']
    lstRecord = output['lstRecord']
	# In this example there is only 1 recordId (str_NewId), so only 1 record will be updated
	# But you can update more than 1 record and with this loop you can print all readed records	
    if len(lstRecordIds) > 0:
        logger.info("--> Data Contents")
        for i in range(len(lstRecordIds)):
            logger.info("Id:" + str(lstRecordIds[i]) + " Data:" + str(lstRecord[i]))


    #################
    # LkRead
    #################
    logger.info("-- LkRead --")
    logger.info("--------")

    rop_calculated = True
    rop_conversion = False
    rop_formatSpec = False
    rop_originalRecords = False
    readOptions = linkar_client.LkCreateReadOptions(rop_calculated,
                                                        rop_conversion, rop_formatSpec,
                                                        rop_originalRecords)
    dictionaries = "ADDR"
    result = linkar_client.LkRead(connectionInfo, filename, strNewId, dictionaries, readOptions,
                                        LinkarClientPy.IOFormatCru.MV,
                                        customVars, 600)


    output = process_result('Read', result)
    lstRecordIds = output['lstRecordIds']
    lstRecord = output['lstRecord']
	# In this example there is only 1 recordId (str_NewId), so only 1 record will be readed
	# But you can read more than 1 record and with this loop you can print all readed records
    if len(lstRecordIds) > 0:
        logger.info("--> Data Contents")
        for i in range(len(lstRecordIds)):
            logger.info("Id:" + str(lstRecordIds[i]) + " Data:" + str(lstRecord[i]))

    #################
    # LkDelete
    #################
    logger.info("-- LkDelete --")
    logger.info("--------")
    dop_optimisticLock = False
    dop_recoverIdType = linkar_client.LkCreateRecoverRecordIdTypeNone()
    deleteOptions = linkar_client.LkCreateDeleteOptions(dop_optimisticLock, dop_recoverIdType)
    originalRecords = ''
    result = linkar_client.LkDelete(connectionInfo, filename, strRecordId,
                                        originalRecords, deleteOptions,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)

    output = process_result('Delete', result)

    #################
    # LkSubroutine
    #################
    logger.info("-- LkSubRoutine --")
    logger.info("--------")

    subroutineName = 'SUB.DEMOLINKAR'
    strArgs = linkar_client.LkAddArgumentSubroutine("0", "qwerty")
    strArgs = linkar_client.LkAddArgumentSubroutine(strArgs, "")
    result = linkar_client.LkSubroutine(connectionInfo, subroutineName, 3, strArgs,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)
    output = process_result('Subroutine', result)
    if len(output['lstError']) == 0:
        lstConversion = linkar_client.LkGetArgumentsFromLkString(result['lkString'])
        logger.info("Arguments result -> " + str(lstConversion.decode(linkar_client.encoding)) )
    else:
        print(output)
        logger.error("Error while conversion")

    #################
    # LkConversion
    #################
    logger.info("-- LkConversion --")
    logger.info("--------")
    code = "D2-"
    expression = "13320"
    conversionType = ord('O')

    result = linkar_client.LkConversion(connectionInfo, code, expression, conversionType,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)
    output = process_result('Conversion', result)
    if len(output['lstError']) == 0:
        lstConversion = linkar_client.LkGetConversionFromLkString(result['lkString'])
        logger.info("Conversion result -> " + str(lstConversion.decode(linkar_client.encoding)) )
    else:
        logger.info(output)
        logger.error("Error while conversion")

    #################
    # LkFormat
    #################
    logger.info("-- LkFormat --")
    logger.info("--------")
    formatSpec = "R%10"
    expression = "HELLO"

    result = linkar_client.LkFormat(connectionInfo, formatSpec, expression,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)
    output = process_result('Format', result)
    if len(output['lstError']) == 0:
        lstConversion = linkar_client.LkGetFormatFromLkString(result['lkString'])
        logger.info("Format result -> " + str(lstConversion.decode(linkar_client.encoding)) )
    else:
        logger.info(output)
        logger.error("Error while conversion")


    #################
    # LkExecute
    #################
    logger.info("-- LkExecute --")
    logger.info("--------")
    statement = "WHO"
    result = linkar_client.LkExecute(connectionInfo, statement,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)
    output = process_result('Execute', result)
    if len(output['lstError']) == 0:
        returning = linkar_client.LkGetReturningFromLkString(result['lkString'])
        logger.info("Execute returning result -> " + str(returning.decode(linkar_client.encoding)) )
        capturing = linkar_client.LkGetCapturingFromLkString(result['lkString'])
        logger.info("Execute capturing result -> " + str(capturing.decode(linkar_client.encoding)) )
    else:
        logger.info(output)
        logger.error("Error while conversion")

    #################
    # LkDictionaries
    #################
    logger.info("-- LkDictionaries --")
    logger.info("--------")
    result = linkar_client.LkDictionaries(connectionInfo, filename,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)

    output = process_result('Dictionaries', result)
    if len(output['lstError']) == 0:
        logger.info("Dictionaries is OK!")
        lstDictionaryIds = linkar_client.LkGetDictionaryIdsFromLkString(result['lkString'])
        lstDictionary = linkar_client.LkGetDictionariesFromLkString(result['lkString'])
        if len(lstDictionaryIds) > 0:
            logger.info("--> Data Contents")
            for i in range(len(lstDictionaryIds)):
                logger.info("Id:" + str(lstDictionaryIds[i]) + " Data:" + str(lstDictionary[i]))
    else:
        logger.info(output)
        logger.error("Error while conversion")

    #################
    # LkSelect
    #################
    logger.info("-- LkSelect --")
    logger.info("--------")
    sop_onlyRecordId = False
    sop_pagination = False
    sop_regPage = 0
    sop_numPage = 0
    sop_calculated = True
    sop_conversion = False
    sop_formatSpec = False
    sop_originalRecords = False
    selectOptions = linkar_client.LkCreateSelectOptions(sop_onlyRecordId, sop_pagination, sop_regPage,
                                                        sop_numPage, sop_calculated, sop_conversion,
                                                        sop_formatSpec, sop_originalRecords)

    selectClause = ""
    sortClause = "BY CODE"
    dictClause = ""
    preSelectClause = ""
    result = linkar_client.LkSelect(connectionInfo, filename, selectClause, sortClause,
                                    dictClause, preSelectClause, selectOptions,
                                    LinkarClientPy.IOFormatCru.MV,
                                    customVars, 600)
    output = process_result('Select', result)
    if len(output['lstError']) == 0:
        logger.info("Select is OK!")

        # lstRecordIds
        lstRecordIds = output['lstRecordIds']
        lstRecord = output['lstRecord']
        if len(lstRecordIds) > 0:
            logger.info("--> Data Contents")
            for i in range(len(lstRecordIds)):
                logger.info("Id:" + str(lstRecordIds[i]) + " Data:" + str(lstRecord[i]))

    else:
        print(output)
        logger.error("Error while conversion")


    #################
    # LkSchemas
    #################
    logger.info("-- LkSchemas --")
    logger.info("--------")
    schop_rowHeadersType = LinkarClientPy.RowHeadersType.MAINLABEL
    schop_rowProperties = False
    schop_onlyVisibles = False
    schop_pagination = False
    schop_regPage = 0
    schop_numPage = 0
    lkSchemasOptions = linkar_client.LkCreateSchOptionsTypeLKSCHEMAS(schop_rowHeadersType, schop_rowProperties, schop_onlyVisibles,
																	 schop_pagination, schop_regPage, schop_numPage)

    result = linkar_client.LkSchemas(connectionInfo, lkSchemasOptions,
                                    LinkarClientPy.IOFormatSch.MV,
                                    customVars, 600)
    output = process_result('Schemas', result)
    if len(output['lstError']) == 0:
        logger.info("Schemas is OK!")

        # lstRecordIds
        lstRecordIds = output['lstRecordIds']
        lstRecord = output['lstRecord']
        if len(lstRecordIds) > 0:
            logger.info("--> Data Contents")
            for i in range(len(lstRecordIds)):
                logger.info("Id:" + str(lstRecordIds[i]) + " Data:" + str(lstRecord[i]))

    else:
        print(output)
        logger.error("Error while conversion")


    #################
    # LkProperties
    #################
    logger.info("-- LkProperties --")
    logger.info("--------")
    propop_rowHeadersType = LinkarClientPy.RowHeadersType.MAINLABEL
    propop_rowProperties = False
    propop_onlyVisibles = False
    propop_usePropertyNames = False
    propop_pagination = False
    propop_regPage = 0
    propop_numPage = 0
    lkPropertiesOptions = linkar_client.LkCreatePropOptionsTypeLKSCHEMAS(propop_rowHeadersType, propop_rowProperties, propop_onlyVisibles, propop_usePropertyNames, propop_pagination, propop_regPage,
                                                        propop_numPage)

    filename = "LK.ORDERS"														
    result = linkar_client.LkProperties(connectionInfo, filename, lkPropertiesOptions,
                                        LinkarClientPy.IOFormatSch.MV,
                                        customVars, 600)
    output = process_result('Properties', result)
    if len(output['lstError']) == 0:
        logger.info("Properties is OK!")

        # lstRecordIds
        lstRecordIds = output['lstRecordIds']
        lstRecord = output['lstRecord']
        if len(lstRecordIds) > 0:
            logger.info("--> Data Contents")
            for i in range(len(lstRecordIds)):
                logger.info("Id:" + str(lstRecordIds[i]) + " Data:" + str(lstRecord[i]))

    else:
        print(output)
        logger.error("Error while conversion")


    #################
    # LkGetTable
    #################
    logger.info("-- LkGetTable --")
    logger.info("--------")
    gtop_rowHeadersType = LinkarClientPy.RowHeadersType.MAINLABEL
    gtop_rowProperties = False
    gtop_onlyVisibles = False
    gtop_usePropertyNames = False
    gtop_repeatValues = False
    gtop_applyConversion = True
    gtop_applyFormat = True
    gtop_calculated = True
    gtop_pagination = True
    gtop_regPage = 50
    gtop_numPage = 1
    tableOptions = linkar_client.LkCreateTableOptionsTypeLKSCHEMAS(gtop_rowHeadersType, gtop_rowProperties, gtop_onlyVisibles, gtop_usePropertyNames,
                                                        gtop_repeatValues, gtop_applyConversion, gtop_applyFormat, gtop_calculated,
                                                        gtop_pagination, gtop_regPage, gtop_numPage)

    filename = "LK.ORDERS"
    selectClause = ""
    sortClause = "BY CODE"
    dictClause = ""

    result = linkar_client.LkGetTable(connectionInfo, filename, selectClause, sortClause, dictClause, tableOptions, customVars, 600)
    hasError = result['hasError']
    output = result['lkString']
    if hasError:
        print(output)
        logger.error("Error while LkGetTable")
    else:
        #rows = output.split(DBMV_Mark_AM_str)
        rows = output.split(ASCII_VT_str)
        logger.info("Lines of the Table:")
        for i in range (len(rows)):
            logger.info(rows[i].decode('utf-8'))

    #################
    # LkResetCommonBlocks
    #################
    logger.info("-- LkResetCommonBlocks --")
    logger.info("--------")
    result = linkar_client.LkResetCommonBlocks(connectionInfo,
                                        LinkarClientPy.IOFormat.MV,
                                        customVars, 600)
    output = process_result('ResetCommonBlocks', result)
    if len(output['lstError']) == 0:	
        returning = linkar_client.LkGetReturningFromLkString(result['lkString'])
        logger.info("ResetCommonBlocks returning result -> " + str(returning.decode(linkar_client.encoding)) )
        capturing = linkar_client.LkGetCapturingFromLkString(result['lkString'])
        logger.info("ResetCommonBlocks capturing result -> " + str(capturing.decode(linkar_client.encoding)) )	
    else:
        logger.info(output)
        logger.error("Error while conversion")



    #################
    # LkLogout
    #################
    logger.info("-- LkLogout --")
    logger.info("--------")
    result = linkar_client.LkLogout(connectionInfo, "", 600)
    hasError = result['hasError']
    if hasError:
        logger.error("Error Logout")

    logger.info("Demo OK!")
