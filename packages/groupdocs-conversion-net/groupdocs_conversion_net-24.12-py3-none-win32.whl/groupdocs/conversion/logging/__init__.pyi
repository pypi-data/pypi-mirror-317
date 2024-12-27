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

class ConsoleLogger(ILogger):
    '''Console logger implementation.'''
    
    def trace(self, message : str) -> None:
        '''Writes trace log message;
        Trace log messages provides generally useful information about application flow.
        
        :param message: The trace message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message;
        Warning log messages provides information about unexpected and recoverable event in application flow.
        
        :param message: The warning message.'''
        raise NotImplementedError()
    
    def error(self, message : str, exception : str) -> None:
        '''Writes error log message;
        Error log messages provides information about unrecoverable events in application flow.
        
        :param message: The error message.
        :param exception: The exception.'''
        raise NotImplementedError()
    

class FileLogger(ILogger):
    '''File logger implementation.'''
    
    def trace(self, message : str) -> None:
        '''Writes trace log message;
        Trace log messages provide generally useful information about application flow.
        
        :param message: The trace message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message;
        Warning log messages provide information about unexpected and recoverable events in application flow.
        
        :param message: The warning message.'''
        raise NotImplementedError()
    
    def error(self, message : str, exception : str) -> None:
        '''Writes error log message;
        Error log messages provide information about unrecoverable events in application flow.
        
        :param message: The error message.
        :param exception: The exception.'''
        raise NotImplementedError()
    

class ILogger:
    '''Defines the methods that are used to perform logging.'''
    
    def trace(self, message : str) -> None:
        '''Writes trace log message;
        Trace log messages provides generally useful information about application flow.
        
        :param message: The trace message.'''
        raise NotImplementedError()
    
    def warning(self, message : str) -> None:
        '''Writes warning log message;
        Warning log messages provides information about unexpected and recoverable event in application flow.
        
        :param message: The warning message.'''
        raise NotImplementedError()
    
    def error(self, message : str, exception : str) -> None:
        '''Writes error log message;
        Error log messages provides information about unrecoverable events in application flow.
        
        :param message: The error message.
        :param exception: The exception.'''
        raise NotImplementedError()
    

