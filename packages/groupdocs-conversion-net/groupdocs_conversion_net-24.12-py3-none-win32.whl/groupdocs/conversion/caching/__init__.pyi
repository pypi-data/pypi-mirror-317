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

class FileCache(ICache):
    '''File caching behaviour. Means that cache is stored on the file system'''
    
    def set(self, key : str, value : Any) -> None:
        '''Inserts a cache entry into the cache.
        
        :param key: A unique identifier for the cache entry.
        :param value: The object to insert.'''
        raise NotImplementedError()
    
    def try_get_value(self, key : str, value : List[Object]) -> bool:
        '''Gets the entry associated with this key if present.
        
        :param key: A key identifying the requested entry.
        :param value: The located value or null.
        :returns: True
        if the key was found.'''
        raise NotImplementedError()
    
    def get_keys(self, filter : str) -> Iterable[str]:
        '''Returns all keys matching filter.
        
        :param filter: The filter to use.
        :returns: Keys matching the filter.'''
        raise NotImplementedError()
    

class ICache:
    '''Defines methods required for storing rendered document and document resources сache.'''
    
    def set(self, key : str, value : Any) -> None:
        '''Inserts a cache entry into the cache.
        
        :param key: A unique identifier for the cache entry.
        :param value: The object to insert.'''
        raise NotImplementedError()
    
    def try_get_value(self, key : str, value : List[Object]) -> bool:
        '''Gets the entry associated with this key if present.
        
        :param key: A key identifying the requested entry.
        :param value: The located value or null.
        :returns: True
        if the key was found.'''
        raise NotImplementedError()
    
    def get_keys(self, filter : str) -> Iterable[str]:
        '''Returns all keys matching filter.
        
        :param filter: The filter to use.
        :returns: Keys matching the filter.'''
        raise NotImplementedError()
    

class MemoryCache(ICache):
    '''Memory caching behaviour. Means that cache is stored in the memory'''
    
    def set(self, key : str, value : Any) -> None:
        '''Inserts a cache entry into the cache.
        
        :param key: A unique identifier for the cache entry.
        :param value: The object to insert.'''
        raise NotImplementedError()
    
    def try_get_value(self, key : str, value : List[Object]) -> bool:
        '''Gets the entry associated with this key if present.
        
        :param key: A key identifying the requested entry.
        :param value: The located value or null.
        :returns: True
        if the key was found.'''
        raise NotImplementedError()
    
    def get_keys(self, filter : str) -> Iterable[str]:
        '''Returns all keys matching filter.
        
        :param filter: The filter to use.
        :returns: Keys matching the filter.'''
        raise NotImplementedError()
    

