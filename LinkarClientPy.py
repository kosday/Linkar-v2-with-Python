from ctypes import *
from enum import Enum
import os

class CredentialOptions(Enum):
    HOST = 0
    PORT = 1
    USERNAME = 2
    PASSWORD = 3
    ENTRYPOINT = 4
    LANGUAGE = 5
    FREETEXT = 6


class ConnectionInfo(Enum):
    CREDENTIAL_OPTIONS = 0
    SESSION_ID = 1


class IOFormat(Enum):
    MV = 1
    XML = 2
    JSON = 3

class IOFormatSch(Enum):
    MV = 1
    XML = 2
    JSON = 3
    TABLE = 4

class RowHeadersType(Enum):
    MAINLABEL = 1
    SHORTLABEL = 2
    NONE = 3


class LinkarClient:

    def __init__(self):

        # Load library
        if os.name == 'nt':
            self.encoding = 'cp1252'
            self.lib_linkar = cdll.LoadLibrary('../Clients/Clib/x64/LinkarClientC.dll')
        else:
            self.encoding = 'iso-8859-1'
            self.lib_linkar = cdll.LoadLibrary('../Clients/Clib/x64/libLinkarClientC.so')


    #
    # Helper functions for management complex "string object"  *
    #

    def LkCreateCredentialOptions(self, host, entrypoint, port, username, password, language, freetext):
        self.lib_linkar.LkCreateCredentialOptions.argtypes = (c_char_p,
                                                              c_char_p,
                                                              c_long,
                                                              c_char_p,
                                                              c_char_p,
                                                              c_char_p,
                                                              c_char_p)
        self.lib_linkar.LkCreateCredentialOptions.restype = c_void_p

        ret_cxx_value =  self.lib_linkar.LkCreateCredentialOptions(c_char_p(host.encode(self.encoding)),
                                                    c_char_p(entrypoint.encode(self.encoding)),
                                                    c_long(port),
                                                    c_char_p(username.encode(self.encoding)),
                                                    c_char_p(password.encode(self.encoding)),
                                                    c_char_p(language.encode(self.encoding)),
                                                    c_char_p(freetext.encode(self.encoding)))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkGetDataFromCredentialOptions(self, credentialOptions, index):
        self.lib_linkar.LkGetDataFromCredentialOptions.argtypes = (c_char_p,
                                                                            c_long)
        self.lib_linkar.LkGetDataFromCredentialOptions.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkGetDataFromCredentialOptions(c_char_p(credentialOptions),
                                                    c_long(index.value))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkGetDataFromConnectionInfo(self, credentialOptions, index):
        self.lib_linkar.LkGetDataFromConnectionInfo.argtypes = (c_char_p,
                                                                       c_long)
        self.lib_linkar.LkGetDataFromConnectionInfo.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkGetDataFromConnectionInfo(c_char_p(credentialOptions),
                                                    c_long(index.value))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkCreateReadOptions(self, calculated, conversion, formatSpec, originalRecords, dictionaries):
        self.lib_linkar.LkCreateReadOptions.argtypes = (c_bool,
                                                               c_bool,
                                                               c_bool,
                                                               c_bool,
                                                               c_bool)
        self.lib_linkar.LkCreateReadOptions.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateReadOptions(c_bool(calculated),
                                                            c_bool(conversion),
                                                            c_bool(formatSpec),
                                                            c_bool(originalRecords),
                                                            c_bool(dictionaries))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateUpdateOptions(self, optimisticLock, readAfter, calculated,
                                    conversion, formatSpec, originalRecords, dictionaries):
        self.lib_linkar.LkCreateUpdateOptions.argtypes = (c_bool,
                                                                 c_bool,
                                                                 c_bool,
                                                                 c_bool,
                                                                 c_bool,
                                                                 c_bool,
                                                                 c_bool)
        self.lib_linkar.LkCreateUpdateOptions.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkCreateUpdateOptions(c_bool(optimisticLock),
                                                            c_bool(readAfter),
                                                            c_bool(calculated),
                                                            c_bool(conversion),
                                                            c_bool(formatSpec),
                                                            c_bool(originalRecords),
                                                            c_bool(dictionaries))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateNewRecordIdTypeNone(self):
        self.lib_linkar.LkCreateNewRecordIdTypeNone.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateNewRecordIdTypeNone()
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateNewRecordIdTypeLinkar(self, prefix, separator, formatSpec):
        self.lib_linkar.LkCreateNewRecordIdTypeLinkar.argtypes = (c_char_p,
                                                                  c_char_p,
                                                                  c_char_p)
        self.lib_linkar.LkCreateNewRecordIdTypeLinkar.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateNewRecordIdTypeLinkar(c_char_p(prefix.encode(self.encoding)),
                                                             c_char_p(separator.encode(self.encoding)),
                                                             c_char_p(formatSpec.encode(self.encoding)))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateNewRecordIdTypeCustom(self):
        self.lib_linkar.LkCreateNewRecordIdTypeCustom.argtypes = ()
        self.lib_linkar.LkCreateNewRecordIdTypeCustom.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateNewRecordIdTypeCustom()
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkCreateNewRecordIdTypeRandom(self, numeric, length):
        self.lib_linkar.LkCreateNewRecordIdTypeRandom.argtypes = (c_bool,
                                                                  c_long)
        self.lib_linkar.LkCreateNewRecordIdTypeRandom.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateNewRecordIdTypeRandom(c_bool(numeric),
                                                             c_long(length))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkCreateNewOptions(self, newItemIdType, readAfter, calculated, conversion,
                            formatSpec, originalRecords, dictionaries):
        self.lib_linkar.LkCreateNewOptions.argtypes = (c_char_p,
                                                              c_bool,
                                                              c_bool,
                                                              c_bool,
                                                              c_bool,
                                                              c_bool,
                                                              c_bool)
        self.lib_linkar.LkCreateNewOptions.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateNewOptions(newItemIdType,
                                                         c_bool(readAfter),
                                                         c_bool(calculated),
                                                         c_bool(conversion),
                                                         c_bool(formatSpec),
                                                         c_bool(originalRecords),
                                                         c_bool(dictionaries))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateRecoverRecordIdTypeNone(self):
        # LkCreateRecoverRecordIdTypeNone
        self.lib_linkar.LkCreateRecoverRecordIdTypeNone.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateRecoverRecordIdTypeNone()
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkCreateRecoverRecordIdTypeLinkar(self, prefix, separator):
        self.lib_linkar.LkCreateRecoverRecordIdTypeLinkar.argtypes = (c_char_p,
                                                                      c_char_p)
        self.lib_linkar.LkCreateRecoverRecordIdTypeLinkar.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateRecoverRecordIdTypeLinkar(c_char_p(prefix.encode(self.encoding)),
                                                                 c_char_p(separator.encode(self.encoding)))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateRecoverRecordIdTypeCustom(self):
        self.lib_linkar.LkCreateRecoverRecordIdTypeCustom.argtypes = ()
        self.lib_linkar.LkCreateRecoverRecordIdTypeCustom.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateRecoverRecordIdTypeCustom()
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateDeleteOptions(self, optimisticLock, recoverIdType):
        # LkCreateDeleteOptions
        self.lib_linkar.LkCreateDeleteOptions.argtypes = (c_bool,
                                                                 c_char_p)
        self.lib_linkar.LkCreateDeleteOptions.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateDeleteOptions(c_bool(optimisticLock),
                                                            recoverIdType)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value


    def LkCreateSelectOptions(self, onlyRecordId, pagination, regPage, numPage,
                                calculated, conversion, formatSpec, originalRecords, dictionaries):
        self.lib_linkar.LkCreateSelectOptions.argtypes = (c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool)
        self.lib_linkar.LkCreateSelectOptions.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateSelectOptions(c_bool(onlyRecordId),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage),
                                                        c_bool(calculated),
                                                        c_bool(conversion),
                                                        c_bool(formatSpec),
                                                        c_bool(originalRecords),
                                                        c_bool(dictionaries))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value



    def LkAddArgumentSubroutine(self, arguments, newArgument):
        self.lib_linkar.LkAddArgumentSubroutine.argtypes = (c_char_p,
                                                            c_char_p)
        self.lib_linkar.LkAddArgumentSubroutine.restype = c_void_p
        if isinstance(arguments, bytes):
            ret_cxx_value = self.lib_linkar.LkAddArgumentSubroutine(arguments,
                                                           c_char_p(newArgument.encode(self.encoding)) )
        else:
            ret_cxx_value = self.lib_linkar.LkAddArgumentSubroutine(c_char_p(arguments.encode(self.encoding)),
                                                           c_char_p(newArgument.encode(self.encoding)) )
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateSchOptionsTypeLKSCHEMAS(self, rowHeaders, rowProperties, onlyVisibles, pagination, regPage, numPage):
        self.lib_linkar.LkCreateSchOptionsTypeLKSCHEMAS.argtypes = (c_short,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateSchOptionsTypeLKSCHEMAS.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateSchOptionsTypeLKSCHEMAS(c_short(rowHeaders.value),
                                                        c_bool(rowProperties),
                                                        c_bool(onlyVisibles),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateSchOptionsTypeSQLMODE(self, onlyVisibles, pagination, regPage, numPage):
        self.lib_linkar.LkCreateSchOptionsTypeSQLMODE.argtypes = (c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateSchOptionsTypeSQLMODE.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateSchOptionsTypeSQLMODE(c_bool(onlyVisibles),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateSchOptionsTypeDICTIONARIES(self, rowHeaders, pagination, regPage, numPage):
        self.lib_linkar.LkCreateSchOptionsTypeDICTIONARIES.argtypes = (c_short,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateSchOptionsTypeDICTIONARIES.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateSchOptionsTypeDICTIONARIES(c_short(rowHeaders.value),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreatePropOptionsTypeLKSCHEMAS(self, rowHeaders, rowProperties, onlyVisibles, usePropertyNames, pagination, regPage, numPage):
        self.lib_linkar.LkCreatePropOptionsTypeLKSCHEMAS.argtypes = (c_short,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreatePropOptionsTypeLKSCHEMAS.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreatePropOptionsTypeLKSCHEMAS(c_short(rowHeaders.value),
                                                        c_bool(rowProperties),
                                                        c_bool(onlyVisibles),
                                                        c_bool(usePropertyNames),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreatePropOptionsTypeSQLMODE(self, onlyVisibles, pagination, regPage, numPage):
        self.lib_linkar.LkCreatePropOptionsTypeSQLMODE.argtypes = (c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreatePropOptionsTypeSQLMODE.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreatePropOptionsTypeSQLMODE(c_bool(onlyVisibles),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreatePropOptionsTypeDICTIONARIES(self, rowHeaders, pagination, regPage, numPage):
        self.lib_linkar.LkCreatePropOptionsTypeDICTIONARIES.argtypes = (c_short,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreatePropOptionsTypeDICTIONARIES.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreatePropOptionsTypeDICTIONARIES(c_short(rowHeaders.value),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateTableOptionsTypeLKSCHEMAS(self, rowHeaders, rowProperties, onlyVisibles, usePropertyNames, repeatValues, applyConversion, applyFormat, calculated, pagination, regPage, numPage):
        self.lib_linkar.LkCreateTableOptionsTypeLKSCHEMAS.argtypes = (c_short,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateTableOptionsTypeLKSCHEMAS.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateTableOptionsTypeLKSCHEMAS(c_short(rowHeaders.value),
                                                        c_bool(rowProperties),
                                                        c_bool(onlyVisibles),
                                                        c_bool(usePropertyNames),
                                                        c_bool(repeatValues),
                                                        c_bool(applyConversion),
                                                        c_bool(applyFormat),
                                                        c_bool(calculated),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateTableOptionsTypeSQLMODE(self, onlyVisibles, applyConversion, applyFormat, calculated, pagination, regPage, numPage):
        self.lib_linkar.LkCreateTableOptionsTypeSQLMODE.argtypes = (c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateTableOptionsTypeSQLMODE.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateTableOptionsTypeSQLMODE(c_bool(onlyVisibles),
                                                        c_bool(applyConversion),
                                                        c_bool(applyFormat),
                                                        c_bool(calculated),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateTableOptionsTypeDICTIONARIES(self, rowHeaders, repeatValues, applyConversion, applyFormat, calculated, pagination, regPage, numPage):
        self.lib_linkar.LkCreateTableOptionsTypeDICTIONARIES.argtypes = (c_short,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateTableOptionsTypeDICTIONARIES.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateTableOptionsTypeDICTIONARIES(c_short(rowHeaders.value),
                                                        c_bool(repeatValues),
                                                        c_bool(applyConversion),
                                                        c_bool(applyFormat),
                                                        c_bool(calculated),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    def LkCreateTableOptionsTypeNONE(self, rowHeaders, repeatValues, pagination, regPage, numPage):
        self.lib_linkar.LkCreateTableOptionsTypeNONE.argtypes = (c_short,
                                                            c_bool,
                                                            c_bool,
                                                            c_long,
                                                            c_long)
        self.lib_linkar.LkCreateTableOptionsTypeNONE.restype = c_void_p
        ret_cxx_value = self.lib_linkar.LkCreateTableOptionsTypeNONE(c_short(rowHeaders.value),
                                                        c_bool(repeatValues),
                                                        c_bool(pagination),
                                                        c_long(regPage),
                                                        c_long(numPage))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value
		
		
		
    #
    # Persistent function
    #

    def LkLogin(self, crdOpt, customVars, receiveTimeout):
        self.lib_linkar.LkLogin.argtypes = (c_char_p,
                                             POINTER(c_bool),
                                             c_char_p,
                                             c_long)
        self.lib_linkar.LkLogin.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkLogin(crdOpt, byref(hasError),
                                c_char_p(customVars.encode(self.encoding)), c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}


    def LkLogout(self, crdOpt, customVars, receiveTimeout):
        self.lib_linkar.LkLogout.argtypes = (c_char_p,
                                                    POINTER(c_bool),
                                                    c_char_p,
                                                    c_long)
        self.lib_linkar.LkLogout.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkLogout(crdOpt, byref(hasError),
                                c_char_p(customVars.encode(self.encoding)), c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkRead(self, connectionInfo, filename, recordsIds, dictClause,
               readOptions, outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkRead.argtypes = (c_char_p,
                                                    POINTER(c_bool),
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_short,
                                                    c_char_p,
                                                    c_long)
        self.lib_linkar.LkRead.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkRead(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(dictClause.encode(self.encoding)),
                                                    readOptions,
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkUpdate(self, connectionInfo, filename, recordsIds, records, originalRecords,
                updateOptions, inputDataFormat, outputStringType,
                customVars, receiveTimeout):
        self.lib_linkar.LkUpdate.argtypes = (c_char_p,
                                                    POINTER(c_bool),
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_short,
                                                    c_short,
                                                    c_char_p,
                                                    c_long)
        self.lib_linkar.LkUpdate.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkUpdate(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(records.encode(self.encoding)),
                                                    c_char_p(originalRecords.encode(self.encoding)),
                                                    updateOptions,
                                                    c_short(inputDataFormat.value),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}


    def LkNew(self, connectionInfo, filename, recordsIds, records, newOptions,
              inputDataFormat, outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkNew.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkNew.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkNew(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(records.encode(self.encoding)),
                                                    c_char_p(newOptions),
                                                    c_short(inputDataFormat.value),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}


    def LkDelete(self, connectionInfo, filename, recordsIds, originalRecords, deleteOptions,
              outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkDelete.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkDelete.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkDelete(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(originalRecords.encode(self.encoding)),
                                                    c_char_p(deleteOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSelect(self, connectionInfo, filename, selectClause, sortClause,
                 dictClause, preSelectClause, selectOptions, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkSelect.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkSelect.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSelect(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(selectClause.encode(self.encoding)),
                                                    c_char_p(sortClause.encode(self.encoding)),
                                                    c_char_p(dictClause.encode(self.encoding)),
                                                    c_char_p(preSelectClause.encode(self.encoding)),
                                                    c_char_p(selectOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSubroutine(self, connectionInfo, name, numArguments, arguments,
                 outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkSubroutine.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkSubroutine.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSubroutine(connectionInfo,
                                                byref(hasError),
                                                c_char_p(name.encode(self.encoding)),
                                                c_short(numArguments),
                                                arguments,
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkConversion(self, connectionInfo, code, expression, conversionOptions,
                     outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkConversion.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkConversion.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkConversion(connectionInfo,
                                                byref(hasError),
                                                c_char_p(code.encode(self.encoding)),
                                                c_char_p(expression.encode(self.encoding)),
                                                c_char(conversionOptions),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkFormat(self, connectionInfo, formatSpec, expression,
                 outputStringType, customVars, receiveTimeout):
        # LkFormat
        self.lib_linkar.LkFormat.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkFormat.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkFormat(connectionInfo,
                                                byref(hasError),
                                                c_char_p(formatSpec.encode(self.encoding)),
                                                c_char_p(expression.encode(self.encoding)),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkDictionaries(self, connectionInfo, filename,
                       outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkDictionaries.argtypes = (c_char_p,
                                                   POINTER(c_bool),
                                                   c_char_p,
                                                   c_short,
                                                   c_char_p,
                                                   c_long)
        self.lib_linkar.LkDictionaries.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkDictionaries(connectionInfo,
                                                  byref(hasError),
                                                  c_char_p(filename.encode(self.encoding)),
                                                  c_short(outputStringType.value),
                                                  c_char_p(customVars.encode(self.encoding)),
                                                  c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkExecute(self, connectionInfo, statement, outputStringType,
                  customVars, receiveTimeout):
        self.lib_linkar.LkExecute.argtypes = (c_char_p,
                                              POINTER(c_bool),
                                              c_char_p,
                                              c_short,
                                              c_char_p,
                                              c_long)
        self.lib_linkar.LkExecute.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkExecute(connectionInfo,
                                                byref(hasError),
                                                c_char_p(statement.encode(self.encoding)),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSendCommand(self, connectionInfo, data, outputStringType, receiveTimeout):
        self.lib_linkar.LkSendCommand.argtypes = (c_char_p,
                                              POINTER(c_bool),
                                              c_char_p,
                                              c_short,
                                              c_long)
        self.lib_linkar.LkSendCommand.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSendCommand(connectionInfo,
                                                 byref(hasError),
                                                 c_char_p(data.encode(self.encoding)),
                                                 c_short(outputStringType.value),
                                                 c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkGetVersion(self, connectionInfo, outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkGetVersion.argtypes = (c_char_p,
                                                  POINTER(c_bool),
                                                  c_short,
                                                  c_char_p,
                                                  c_long)
        self.lib_linkar.LkGetVersion.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkGetVersion(connectionInfo,
                                                byref(hasError),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSchemas(self, connectionInfo, lkSchemasOptions, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkSchemas.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkSchemas.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSchemas(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(lkSchemasOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkProperties(self, connectionInfo, filename, lkPropertiesOptions, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkProperties.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkProperties.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkProperties(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(lkPropertiesOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkGetTable(self, connectionInfo, filename, selectClause, sortClause,
                 dictClause, tableOptions,
                 customVars, receiveTimeout):
        self.lib_linkar.LkGetTable.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkGetTable.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkGetTable(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(selectClause.encode(self.encoding)),
                                                    c_char_p(sortClause.encode(self.encoding)),
                                                    c_char_p(dictClause.encode(self.encoding)),
                                                    c_char_p(tableOptions),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}
				

    def LkResetCommonBlocks(self, connectionInfo, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkResetCommonBlocks.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkResetCommonBlocks.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkResetCommonBlocks(connectionInfo,
                                                    byref(hasError),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    #
    # Direct Functions
    #

    def LkReadD(self, connectionInfo, filename, recordsIds, dictClause,
                readOptions, outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkReadD.argtypes = (c_char_p,
                                                    POINTER(c_bool),
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_short,
                                                    c_char_p,
                                                    c_long)
        self.lib_linkar.LkReadD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkReadD(connectionInfo,
                                            byref(hasError),
                                            c_char_p(filename.encode(self.encoding)),
                                            c_char_p(recordsIds.encode(self.encoding)),
                                            c_char_p(dictClause.encode(self.encoding)),
                                            readOptions,
                                            c_short(outputStringType.value),
                                            c_char_p(customVars.encode(self.encoding)),
                                            c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}


    def LkUpdateD(self, connectionInfo, filename, recordsIds, records, originalRecords,
                updateOptions, inputDataFormat, outputStringType,
                customVars, receiveTimeout):
        self.lib_linkar.LkUpdateD.argtypes = (c_char_p,
                                                    POINTER(c_bool),
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_char_p,
                                                    c_short,
                                                    c_short,
                                                    c_char_p,
                                                    c_long)
        self.lib_linkar.LkUpdateD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkUpdateD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(records.encode(self.encoding)),
                                                    c_char_p(originalRecords.encode(self.encoding)),
                                                    updateOptions,
                                                    c_short(inputDataFormat.value),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}


    def LkNewD(self, connectionInfo, filename, recordsIds, records, newOptions,
              inputDataFormat, outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkNewD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkNewD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkNewD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(records.encode(self.encoding)),
                                                    c_char_p(newOptions),
                                                    c_short(inputDataFormat.value),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}


    def LkDeleteD(self, connectionInfo, filename, recordsIds, originalRecords, deleteOptions,
              outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkDeleteD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkDeleteD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkDeleteD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(recordsIds.encode(self.encoding)),
                                                    c_char_p(originalRecords.encode(self.encoding)),
                                                    c_char_p(deleteOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSelectD(self, connectionInfo, filename, selectClause, sortClause,
                 dictClause, preSelectClause, selectOptions, outputStringType,
                 customVars, receiveTimeout):
        # LkSelect
        self.lib_linkar.LkSelectD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkSelectD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSelectD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(selectClause.encode(self.encoding)),
                                                    c_char_p(sortClause.encode(self.encoding)),
                                                    c_char_p(dictClause.encode(self.encoding)),
                                                    c_char_p(preSelectClause.encode(self.encoding)),
                                                    c_char_p(selectOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSubroutineD(self, connectionInfo, name, numArguments, arguments,
                 outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkSubroutineD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkSubroutineD.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSubroutineD(connectionInfo,
                                                byref(hasError),
                                                c_char_p(name.encode(self.encoding)),
                                                c_short(numArguments),
                                                arguments,
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkConversionD(self, connectionInfo, code, expression, conversionOptions,
                     outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkConversionD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkConversionD.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkConversionD(connectionInfo,
                                                byref(hasError),
                                                c_char_p(code.encode(self.encoding)),
                                                c_char_p(expression.encode(self.encoding)),
                                                c_char(conversionOptions),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkFormatD(self, connectionInfo, formatSpec, expression,
                  outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkFormatD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkFormatD.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkFormatD(connectionInfo,
                                                byref(hasError),
                                                c_char_p(formatSpec.encode(self.encoding)),
                                                c_char_p(expression.encode(self.encoding)),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkDictionariesD(self, connectionInfo, filename,
                       outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkDictionariesD.argtypes = (c_char_p,
                                                   POINTER(c_bool),
                                                   c_char_p,
                                                   c_short,
                                                   c_char_p,
                                                   c_long)
        self.lib_linkar.LkDictionariesD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkDictionariesD(connectionInfo,
                                                  byref(hasError),
                                                  c_char_p(filename.encode(self.encoding)),
                                                  c_short(outputStringType.value),
                                                  c_char_p(customVars.encode(self.encoding)),
                                                  c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkExecuteD(self, connectionInfo, statement, outputStringType,
                  customVars, receiveTimeout):
        self.lib_linkar.LkExecuteD.argtypes = (c_char_p,
                                              POINTER(c_bool),
                                              c_char_p,
                                              c_short,
                                              c_char_p,
                                              c_long)
        self.lib_linkar.LkExecuteD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkExecuteD(connectionInfo,
                                                byref(hasError),
                                                c_char_p(statement.encode(self.encoding)),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSendCommandD(self, connectionInfo, data, outputStringType, receiveTimeout):
        self.lib_linkar.LkSendCommandD.argtypes = (c_char_p,
                                              POINTER(c_bool),
                                              c_char_p,
                                              c_short,
                                              c_long)
        self.lib_linkar.LkSendCommandD.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSendCommandD(connectionInfo,
                                                 byref(hasError),
                                                 c_char_p(data.encode(self.encoding)),
                                                 c_short(outputStringType.value),
                                                 c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkGetVersionD(self, connectionInfo, outputStringType, customVars, receiveTimeout):
        self.lib_linkar.LkGetVersionD.argtypes = (c_char_p,
                                                  POINTER(c_bool),
                                                  c_short,
                                                  c_char_p,
                                                  c_long)
        self.lib_linkar.LkGetVersionD.restype = c_void_p
        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkGetVersionD(connectionInfo,
                                                byref(hasError),
                                                c_short(outputStringType.value),
                                                c_char_p(customVars.encode(self.encoding)),
                                                c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkSchemasD(self, connectionInfo, lkSchemasOptions, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkSchemasD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkSchemasD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkSchemasD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(lkSchemasOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkPropertiesD(self, connectionInfo, filename, lkPropertiesOptions, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkPropertiesD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkPropertiesD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkPropertiesD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(lkPropertiesOptions),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkGetTableD(self, connectionInfo, filename, selectClause, sortClause,
                 dictClause, tableOptions, 
                 customVars, receiveTimeout):
        self.lib_linkar.LkGetTableD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkGetTableD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkGetTableD(connectionInfo,
                                                    byref(hasError),
                                                    c_char_p(filename.encode(self.encoding)),
                                                    c_char_p(selectClause.encode(self.encoding)),
                                                    c_char_p(sortClause.encode(self.encoding)),
                                                    c_char_p(dictClause.encode(self.encoding)),
                                                    c_char_p(tableOptions),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    def LkResetCommonBlocksD(self, connectionInfo, outputStringType,
                 customVars, receiveTimeout):
        self.lib_linkar.LkResetCommonBlocksD.argtypes = (c_char_p,
                                                 POINTER(c_bool),
                                                 c_short,
                                                 c_char_p,
                                                 c_long)
        self.lib_linkar.LkResetCommonBlocksD.restype = c_void_p

        hasError = c_bool(True)
        ret_cxx_value = self.lib_linkar.LkResetCommonBlocksD(connectionInfo,
                                                    byref(hasError),
                                                    c_short(outputStringType.value),
                                                    c_char_p(customVars.encode(self.encoding)),
                                                    c_long(receiveTimeout))
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return {'lkString': ret_value, 'hasError': hasError.value}

    #
    # Helper Data Functions
    #

    def LkGetStringArray(self, lkStringMatrix, lkStringMatrixLength):

        # Copy to local python array
        lkStringArrayPy = []
        for i in range(lkStringMatrixLength.value):
            lkStringArrayPy.append(lkStringMatrix[i].decode(self.encoding))

        # Free Memory Matrix
        self.lib_linkar.WrapperPy_LkFreeMemoryStringArray.argtypes = (c_char_p,
                                                                    c_long)
        self.lib_linkar.WrapperPy_LkFreeMemoryStringArray.restype = c_void_p
        self.lib_linkar.WrapperPy_LkFreeMemoryStringArray(cast(lkStringMatrix, c_char_p), lkStringMatrixLength)

        return lkStringArrayPy


    def LkGetErrorsFromLkString(self, lkString):

        self.lib_linkar.LkGetErrorsFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetErrorsFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetErrorsFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))

        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetTotalRecordsFromLkString(self, lkString):
        self.lib_linkar.LkGetTotalRecordsFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetTotalRecordsFromLkString.restype = c_long
        return self.LkGetTotalRecordsFromLkString(lkString)

    def LkGetRecordIdsFromLkString(self, lkString):

        self.lib_linkar.LkGetRecordIdsFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetRecordIdsFromLkString.restype = c_void_p

        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetRecordIdsFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetRecordsFromLkString(self, lkString):

        self.lib_linkar.LkGetRecordsFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetRecordsFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetRecordsFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetRecordsCalculatedFromLkString(self, lkString):

        self.lib_linkar.LkGetRecordsCalculatedFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetRecordsCalculatedFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetRecordsCalculatedFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetRecordsDictionariesFromLkString(self, lkString):

        self.lib_linkar.LkGetRecordsDictionariesFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetRecordsDictionariesFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetRecordsDictionariesFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetRecordsIdDictsFromLkString(self, lkString):

        self.lib_linkar.LkGetRecordsIdDictsFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetRecordsIdDictsFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetRecordsIdDictsFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetRecordsCalculatedDictionariesFromLkString(self, lkString):

        self.lib_linkar.LkGetRecordsCalculatedDictionariesFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetRecordsCalculatedDictionariesFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetRecordsCalculatedDictionariesFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetOriginalRecordsFromLkString(self, lkString):

        self.lib_linkar.LkGetOriginalRecordsFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetOriginalRecordsFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetOriginalRecordsFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetDictionaryIdsFromLkString(self, lkString):

        self.lib_linkar.LkGetDictionaryIdsFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetDictionaryIdsFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetDictionaryIdsFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)

    def LkGetDictionariesFromLkString(self, lkString):

        self.lib_linkar.LkGetDictionariesFromLkString.argtypes = (c_char_p,
                                                                    POINTER(c_long))
        self.lib_linkar.LkGetDictionariesFromLkString.restype = c_void_p


        lkStringMatrixLength = c_long(0)
        lkStringMatrix = self.lib_linkar.LkGetDictionariesFromLkString(lkString,
                                                    byref(lkStringMatrixLength))

        lkStringMatrixChar_p = cast(lkStringMatrix, POINTER(c_char_p))
        return self.LkGetStringArray(lkStringMatrixChar_p, lkStringMatrixLength)


    def LkGetCapturingFromLkString(self, lkString):
        self.lib_linkar.LkGetCapturingFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetCapturingFromLkString.restype = c_char_p

        ret_cxx_value = self.lib_linkar.LkGetCapturingFromLkString(lkString)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkGetCapturingFromLkString(self, lkString):
        self.lib_linkar.LkGetCapturingFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetCapturingFromLkString.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkGetCapturingFromLkString(lkString)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkGetConversionFromLkString(self, lkString):
        self.lib_linkar.LkGetConversionFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetConversionFromLkString.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkGetConversionFromLkString(lkString)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkGetFormatFromLkString(self, lkString):
        self.lib_linkar.LkGetFormatFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetFormatFromLkString.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkGetFormatFromLkString(lkString)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkGetReturningFromLkString(self, lkString):
        self.lib_linkar.LkGetReturningFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetReturningFromLkString.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkGetReturningFromLkString(lkString)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    def LkGetArgumentsFromLkString(self, lkString):
        self.lib_linkar.LkGetArgumentsFromLkString.argtypes = (c_char_p, )
        self.lib_linkar.LkGetArgumentsFromLkString.restype = c_void_p

        ret_cxx_value = self.lib_linkar.LkGetArgumentsFromLkString(lkString)
        ret_value = cast(ret_cxx_value, c_char_p).value
        self.LkFreeMemory(cast(ret_cxx_value, c_char_p))
        return ret_value

    #
    # Helper MV Functions
    #

    def LkCount(self, str, delimiter):
        self.lib_linkar.LkCount.argtypes = (c_char_p,
                                                        c_char)
        self.lib_linkar.LkCount.restype = c_long

        return self.lib_linkar.LkCount(c_char_p(str.encode(self.encoding)),
                                                c_char(ord(delimiter)))

    def LkDCount(self, str, delimiter):
        self.lib_linkar.LkDCount.argtypes = (c_char_p,
                                                        c_char)
        self.lib_linkar.LkDCount.restype = c_long

        return self.lib_linkar.LkDCount(c_char_p(str.encode(self.encoding)),
                                                    c_char(ord(delimiter)))


    def LkExtract(self, str, field, value, subvalue):
        self.lib_linkar.LkExtract.argtypes = (c_char_p,
                                                        c_long,
                                                        c_long,
                                                        c_long)
        self.lib_linkar.LkExtract.restype = c_char_p

        return self.lib_linkar.LkExtract(c_char_p(str.encode(self.encoding)),
                                                c_long(field),
                                                    c_long(value),
                                                c_long(subvalue))


    def LkReplace(self, str, newVal, field, value, subvalue):
        self.lib_linkar.LkReplace.argtypes = (c_char_p,
                                                        c_char_p,
                                                        c_long,
                                                        c_long,
                                                        c_long)
        self.lib_linkar.LkReplace.restype = c_char_p

        return self.lib_linkar.LkReplace(c_char_p(str.encode(self.encoding)),
                                                c_char_p(newVal.encode(self.encoding)),
                                                c_long(field),
                                                c_long(value),
                                                c_long(subvalue))

    def LkChange(self, str, strOld, strNew, occurrence, start):
        self.lib_linkar.LkChange.argtypes = (c_char_p,
                                                        c_char_p,
                                                        c_char_p,
                                                        c_long,
                                                        c_long)
        self.lib_linkar.LkChange.restype = c_char_p
        ret_val = self.lib_linkar.LkChange(c_char_p(str.encode(self.encoding)),
                                                c_char_p(strOld.encode(self.encoding)),
                                                c_char_p(strNew.encode(self.encoding)),
                                                c_long(occurrence),
                                                c_long(start))
        return ret_val

    def LkFreeMemory(self, lkString):
        self.lib_linkar.LkFreeMemory.argtypes = (c_char_p,)

        self.lib_linkar.LkFreeMemory(lkString)
