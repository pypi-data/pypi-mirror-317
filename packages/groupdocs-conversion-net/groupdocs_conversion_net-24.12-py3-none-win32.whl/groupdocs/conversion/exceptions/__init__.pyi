from typing import List, Optional, Dict, Iterable, Any, overload
import io
import collections.abc
from datetime import datetime
from aspose.pyreflection import Type
import aspose.pycore
import aspose.pydrawing
from uuid import UUID
import groupdocs.conversion
import groupdocs.conversion.caching
import groupdocs.conversion.contracts
import groupdocs.conversion.exceptions
import groupdocs.conversion.filetypes
import groupdocs.conversion.logging
import groupdocs.conversion.options
import groupdocs.conversion.options.convert
import groupdocs.conversion.options.load

class ConversionNotSupportedException(GroupDocsConversionException):
    '''GroupDocs exception thrown when the conversion from source file to target file type is not supported'''
    

class CorruptOrDamagedFileException(GroupDocsConversionException):
    '''GroupDocs exception thrown when the file is corrupt or damaged'''
    

class FileTypeNotSupportedException(GroupDocsConversionException):
    '''GroupDocs exception thrown when the file type is not supported'''
    

class FontSubstituteException(GroupDocsConversionException):
    '''Thrown if font substitute is illegal'''
    

class GroupDocsConversionException:
    '''GroupDocs.Conversion general exception'''
    

class IncorrectPasswordException(GroupDocsConversionException):
    '''GroupDocs exception thrown when the file is password protected, password is provided but is incorrect'''
    

class InvalidConvertOptionsException(GroupDocsConversionException):
    '''Thrown if provided convert options are invalid'''
    

class InvalidConverterSettingsException(GroupDocsConversionException):
    '''Thrown if provided converter settings are invalid'''
    

class PasswordRequiredException(GroupDocsConversionException):
    '''GroupDocs exception thrown when the file is password protected and password is not provided'''
    

class SourceDocumentFactoryNotProvidedException(GroupDocsConversionException):
    '''GroupDocs exception thrown when the source document factory is not provided'''
    

