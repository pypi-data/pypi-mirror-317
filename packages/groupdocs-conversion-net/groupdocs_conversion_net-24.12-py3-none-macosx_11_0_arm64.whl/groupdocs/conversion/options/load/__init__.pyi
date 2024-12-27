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

class BaseImageLoadOptions(LoadOptions):
    '''Options for loading Image documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.ImageFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.ImageFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Psd, Emf, Wmf document types. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Psd, Emf, Wmf document types. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    

class CadDrawTypeMode(groupdocs.conversion.contracts.Enumeration):
    '''Represents possible modes for colorization of objects.'''
    
    def equals(self, other : groupdocs.conversion.contracts.Enumeration) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares current object to other.
        
        :param obj: The other object
        :returns: zero if equal'''
        raise NotImplementedError()
    
    @staticmethod
    def get_all() -> Iterable[groupdocs.conversion.options.load.CadDrawTypeMode]:
        '''Returns all enumeration values.
        
        :returns: Enumerable of the provided type'''
        raise NotImplementedError()
    
    USE_DRAW_COLOR : groupdocs.conversion.options.load.CadDrawTypeMode
    '''Allows to use common color.'''
    USE_OBJECT_COLOR : groupdocs.conversion.options.load.CadDrawTypeMode
    '''Allows to use separate color for every object.'''

class CadLoadOptions(LoadOptions):
    '''Options for loading CAD documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.CadFileType:
        '''Input document file type'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.CadFileType) -> None:
        '''Input document file type'''
        raise NotImplementedError()
    
    @property
    def layout_names(self) -> List[str]:
        '''Specifies which CAD layouts to be converted'''
        raise NotImplementedError()
    
    @layout_names.setter
    def layout_names(self, value : List[str]) -> None:
        '''Specifies which CAD layouts to be converted'''
        raise NotImplementedError()
    
    @property
    def draw_type(self) -> groupdocs.conversion.options.load.CadDrawTypeMode:
        '''Gets type of drawing.'''
        raise NotImplementedError()
    
    @draw_type.setter
    def draw_type(self, value : groupdocs.conversion.options.load.CadDrawTypeMode) -> None:
        '''Sets type of drawing.'''
        raise NotImplementedError()
    
    @property
    def draw_color(self) -> aspose.pydrawing.Color:
        '''Gets foreground color.'''
        raise NotImplementedError()
    
    @draw_color.setter
    def draw_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets foreground color.'''
        raise NotImplementedError()
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        '''Gets a background color.'''
        raise NotImplementedError()
    
    @background_color.setter
    def background_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets a background color.'''
        raise NotImplementedError()
    
    @property
    def ctb_sources(self) -> List[groupdocs.conversion.options.load.CtbSource]:
        '''Gets the CTB sources.'''
        raise NotImplementedError()
    
    @ctb_sources.setter
    def ctb_sources(self, value : List[groupdocs.conversion.options.load.CtbSource]) -> None:
        '''Sets the CTB sources.'''
        raise NotImplementedError()
    

class CompressionLoadOptions(LoadOptions):
    '''Options for loading compression documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.CompressionFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.CompressionFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Readonly. Set to false. The owner will not be converted'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Readonly. Set to true. The owned documents will be converted'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        Default: 3'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        Default: 3'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to load protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to load protected document.'''
        raise NotImplementedError()
    

class CsvLoadOptions(SpreadsheetLoadOptions):
    '''Options for loading Csv documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.SpreadsheetFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def sheets(self) -> List[str]:
        '''Sheet name to convert'''
        raise NotImplementedError()
    
    @sheets.setter
    def sheets(self, value : List[str]) -> None:
        '''Sheet name to convert'''
        raise NotImplementedError()
    
    @property
    def sheet_indexes(self) -> List[int]:
        '''List of sheet indexes to convert.
        The indexes must be zero-based'''
        raise NotImplementedError()
    
    @sheet_indexes.setter
    def sheet_indexes(self, value : List[int]) -> None:
        '''List of sheet indexes to convert.
        The indexes must be zero-based'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for spreadsheet document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for spreadsheet document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting spreadsheet document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting spreadsheet document.'''
        raise NotImplementedError()
    
    @property
    def show_grid_lines(self) -> bool:
        '''Show grid lines when converting Excel files.'''
        raise NotImplementedError()
    
    @show_grid_lines.setter
    def show_grid_lines(self, value : bool) -> None:
        '''Show grid lines when converting Excel files.'''
        raise NotImplementedError()
    
    @property
    def show_hidden_sheets(self) -> bool:
        '''Show hidden sheets when converting Excel files.'''
        raise NotImplementedError()
    
    @show_hidden_sheets.setter
    def show_hidden_sheets(self, value : bool) -> None:
        '''Show hidden sheets when converting Excel files.'''
        raise NotImplementedError()
    
    @property
    def one_page_per_sheet(self) -> bool:
        '''If OnePagePerSheet is true the content of the sheet will be converted to one page in the PDF document. Default value is true.'''
        raise NotImplementedError()
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool) -> None:
        '''If OnePagePerSheet is true the content of the sheet will be converted to one page in the PDF document. Default value is true.'''
        raise NotImplementedError()
    
    @property
    def optimize_pdf_size(self) -> bool:
        '''If True and converting to Pdf the conversion is optimized for better file size than print quality.'''
        raise NotImplementedError()
    
    @optimize_pdf_size.setter
    def optimize_pdf_size(self, value : bool) -> None:
        '''If True and converting to Pdf the conversion is optimized for better file size than print quality.'''
        raise NotImplementedError()
    
    @property
    def convert_range(self) -> str:
        '''Convert specific range when converting to other than spreadsheet format. Example: "D1:F8".'''
        raise NotImplementedError()
    
    @convert_range.setter
    def convert_range(self, value : str) -> None:
        '''Convert specific range when converting to other than spreadsheet format. Example: "D1:F8".'''
        raise NotImplementedError()
    
    @property
    def skip_empty_rows_and_columns(self) -> bool:
        '''Skips empty rows and columns when converting. Default is True.'''
        raise NotImplementedError()
    
    @skip_empty_rows_and_columns.setter
    def skip_empty_rows_and_columns(self, value : bool) -> None:
        '''Skips empty rows and columns when converting. Default is True.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @property
    def hide_comments(self) -> bool:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @hide_comments.setter
    def hide_comments(self, value : bool) -> None:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @property
    def check_excel_restriction(self) -> bool:
        '''Whether check restriction of excel file when user modify cells related objects. For example, excel does not allow inputting string value longer than 32K. When you input a value longer than 32K, if this property is true, you will get an Exception. If this property is false, we will accept your input string value as the cell\'s value so that later you can output the complete string value for other file formats such as CSV. However, if you have set such kind of value that is invalid for excel file format, you should not save the workbook as excel file format later. Otherwise there may be unexpected error for the generated excel file.'''
        raise NotImplementedError()
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool) -> None:
        '''Whether check restriction of excel file when user modify cells related objects. For example, excel does not allow inputting string value longer than 32K. When you input a value longer than 32K, if this property is true, you will get an Exception. If this property is false, we will accept your input string value as the cell\'s value so that later you can output the complete string value for other file formats such as CSV. However, if you have set such kind of value that is invalid for excel file format, you should not save the workbook as excel file format later. Otherwise there may be unexpected error for the generated excel file.'''
        raise NotImplementedError()
    
    @property
    def culture_info(self) -> str:
        '''Get or set the system culture info at the time file is loaded, e.g. "en-US".'''
        raise NotImplementedError()
    
    @culture_info.setter
    def culture_info(self, value : str) -> None:
        '''Get or set the system culture info at the time file is loaded, e.g. "en-US".'''
        raise NotImplementedError()
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        '''If AllColumnsInOnePagePerSheet is true, all column content of one sheet will output to only one page in result. The width of paper size of pagesetup will be invalid, and the other settings of pagesetup will still take effect.'''
        raise NotImplementedError()
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool) -> None:
        '''If AllColumnsInOnePagePerSheet is true, all column content of one sheet will output to only one page in result. The width of paper size of pagesetup will be invalid, and the other settings of pagesetup will still take effect.'''
        raise NotImplementedError()
    
    @property
    def auto_fit_rows(self) -> bool:
        '''Autofits all rows when converting'''
        raise NotImplementedError()
    
    @auto_fit_rows.setter
    def auto_fit_rows(self, value : bool) -> None:
        '''Autofits all rows when converting'''
        raise NotImplementedError()
    
    @property
    def columns_per_page(self) -> int:
        '''Split a worksheet into pages by columns. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @columns_per_page.setter
    def columns_per_page(self, value : int) -> None:
        '''Split a worksheet into pages by columns. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @property
    def rows_per_page(self) -> int:
        '''Split a worksheet into pages by rows. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @rows_per_page.setter
    def rows_per_page(self, value : int) -> None:
        '''Split a worksheet into pages by rows. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def separator(self) -> str:
        '''Delimiter of a Csv file.'''
        raise NotImplementedError()
    
    @separator.setter
    def separator(self, value : str) -> None:
        '''Delimiter of a Csv file.'''
        raise NotImplementedError()
    
    @property
    def is_multi_encoded(self) -> bool:
        '''True means the file contains several encodings.'''
        raise NotImplementedError()
    
    @is_multi_encoded.setter
    def is_multi_encoded(self, value : bool) -> None:
        '''True means the file contains several encodings.'''
        raise NotImplementedError()
    
    @property
    def has_formula(self) -> bool:
        '''Indicates whether text is formula if it starts with "=".'''
        raise NotImplementedError()
    
    @has_formula.setter
    def has_formula(self, value : bool) -> None:
        '''Indicates whether text is formula if it starts with "=".'''
        raise NotImplementedError()
    
    @property
    def convert_numeric_data(self) -> bool:
        '''Indicates whether the string in the file is converted to numeric. Default is True.'''
        raise NotImplementedError()
    
    @convert_numeric_data.setter
    def convert_numeric_data(self, value : bool) -> None:
        '''Indicates whether the string in the file is converted to numeric. Default is True.'''
        raise NotImplementedError()
    
    @property
    def convert_date_time_data(self) -> bool:
        '''Indicates whether the string in the file is converted to date. Default is True.'''
        raise NotImplementedError()
    
    @convert_date_time_data.setter
    def convert_date_time_data(self, value : bool) -> None:
        '''Indicates whether the string in the file is converted to date. Default is True.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> str:
        '''Encoding. Default is Encoding.Default.'''
        raise NotImplementedError()
    
    @encoding.setter
    def encoding(self, value : str) -> None:
        '''Encoding. Default is Encoding.Default.'''
        raise NotImplementedError()
    

class CtbSource:
    '''Represents a CTB source with a name and associated data stream.'''
    
    @property
    def name(self) -> str:
        '''Gets the name of the CTB source.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> io.RawIOBase:
        '''Gets the data stream associated with the CTB source.'''
        raise NotImplementedError()
    

class DatabaseLoadOptions(LoadOptions):
    '''Options for loading database documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.DatabaseFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.DatabaseFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    

class DiagramLoadOptions(LoadOptions):
    '''Options for loading Diagram documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.DiagramFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.DiagramFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Diagram document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Diagram document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    

class EBookLoadOptions(LoadOptions):
    '''Options for loading EBook documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.EBookFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.EBookFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    

class EmailField(groupdocs.conversion.contracts.Enumeration):
    '''Describes email fields enumeration'''
    
    def equals(self, other : groupdocs.conversion.contracts.Enumeration) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares current object to other.
        
        :param obj: The other object
        :returns: zero if equal'''
        raise NotImplementedError()
    
    START : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Start".'''
    ATTACHMENTS : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Attachments".'''
    CC : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Cc".'''
    BCC : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Bcc".'''
    END : groupdocs.conversion.options.load.EmailField
    '''Default field text is "End".'''
    FROM : groupdocs.conversion.options.load.EmailField
    '''Default field text is "From".'''
    IMPORTANCE : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Importance".'''
    LOCATION : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Location".'''
    ORGANIZER : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Organizer".'''
    PAGE_HEADER : groupdocs.conversion.options.load.EmailField
    '''Default field text is "PageHeader".'''
    RECURRENCE : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Recurrence".'''
    RECURRENCE_PATTERN : groupdocs.conversion.options.load.EmailField
    '''Default field text is "RecurrencePattern".'''
    REQUIRED_ATTENDEES : groupdocs.conversion.options.load.EmailField
    '''Default field text is "RequiredAttendees".'''
    SENT : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Sent".'''
    SHOW_TIME_AS : groupdocs.conversion.options.load.EmailField
    '''Default field text is "ShowTimeAs".'''
    SUBJECT : groupdocs.conversion.options.load.EmailField
    '''Default field text is "Subject".'''
    TAB_FIELD : groupdocs.conversion.options.load.EmailField
    '''Default field text is "TabField".'''
    TO : groupdocs.conversion.options.load.EmailField
    '''Default field text is "To".'''

class EmailFieldText:
    '''Represents a mapping between an email field and its text representation.'''
    
    @property
    def email_field(self) -> groupdocs.conversion.options.load.EmailField:
        '''Gets the email field.'''
        raise NotImplementedError()
    
    @property
    def text_representation(self) -> str:
        '''Gets the text representation of the email field.'''
        raise NotImplementedError()
    

class EmailLoadOptions(LoadOptions):
    '''Options for loading Email documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.EmailFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.EmailFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def display_header(self) -> bool:
        '''Option to display or hide the email header. Default: true.'''
        raise NotImplementedError()
    
    @display_header.setter
    def display_header(self, value : bool) -> None:
        '''Option to display or hide the email header. Default: true.'''
        raise NotImplementedError()
    
    @property
    def display_from_email_address(self) -> bool:
        '''Option to display or hide "from" email address. Default: true.'''
        raise NotImplementedError()
    
    @display_from_email_address.setter
    def display_from_email_address(self, value : bool) -> None:
        '''Option to display or hide "from" email address. Default: true.'''
        raise NotImplementedError()
    
    @property
    def display_to_email_address(self) -> bool:
        '''Option to display or hide "to" email address. Default: true.'''
        raise NotImplementedError()
    
    @display_to_email_address.setter
    def display_to_email_address(self, value : bool) -> None:
        '''Option to display or hide "to" email address. Default: true.'''
        raise NotImplementedError()
    
    @property
    def display_cc_email_address(self) -> bool:
        '''Option to display or hide "Cc" email address. Default: false.'''
        raise NotImplementedError()
    
    @display_cc_email_address.setter
    def display_cc_email_address(self, value : bool) -> None:
        '''Option to display or hide "Cc" email address. Default: false.'''
        raise NotImplementedError()
    
    @property
    def display_bcc_email_address(self) -> bool:
        '''Option to display or hide "Bcc" email address. Default: false.'''
        raise NotImplementedError()
    
    @display_bcc_email_address.setter
    def display_bcc_email_address(self, value : bool) -> None:
        '''Option to display or hide "Bcc" email address. Default: false.'''
        raise NotImplementedError()
    
    @property
    def display_attachments(self) -> bool:
        '''Option to display or hide attachments in the header. Default: true.'''
        raise NotImplementedError()
    
    @display_attachments.setter
    def display_attachments(self, value : bool) -> None:
        '''Option to display or hide attachments in the header. Default: true.'''
        raise NotImplementedError()
    
    @property
    def display_subject(self) -> bool:
        '''Option to display or hide subject in the header. Default: true.'''
        raise NotImplementedError()
    
    @display_subject.setter
    def display_subject(self, value : bool) -> None:
        '''Option to display or hide subject in the header. Default: true.'''
        raise NotImplementedError()
    
    @property
    def display_sent(self) -> bool:
        '''Option to display or hide sent date/time in the header. Default: true.'''
        raise NotImplementedError()
    
    @display_sent.setter
    def display_sent(self, value : bool) -> None:
        '''Option to display or hide sent date/time in the header. Default: true.'''
        raise NotImplementedError()
    
    @property
    def time_zone_offset(self) -> TimeSpan:
        '''Gets the Coordinated Universal Time (UTC) offset for the message dates. This property defines the time zone difference, between the localtime and UTC.'''
        raise NotImplementedError()
    
    @time_zone_offset.setter
    def time_zone_offset(self, value : TimeSpan) -> None:
        '''Sets the Coordinated Universal Time (UTC) offset for the message dates. This property defines the time zone difference, between the localtime and UTC.'''
        raise NotImplementedError()
    
    @property
    def field_text_map(self) -> List[groupdocs.conversion.options.load.EmailFieldText]:
        '''The mapping between email message :py:class:`groupdocs.conversion.options.load.EmailField` and field text representation'''
        raise NotImplementedError()
    
    @field_text_map.setter
    def field_text_map(self, value : List[groupdocs.conversion.options.load.EmailFieldText]) -> None:
        '''The mapping between email message :py:class:`groupdocs.conversion.options.load.EmailField` and field text representation'''
        raise NotImplementedError()
    
    @property
    def preserve_original_date(self) -> bool:
        '''Defines whether need to keep original date header string in mail message when saving or not (Default value is true)'''
        raise NotImplementedError()
    
    @preserve_original_date.setter
    def preserve_original_date(self, value : bool) -> None:
        '''Defines whether need to keep original date header string in mail message when saving or not (Default value is true)'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def resource_loading_timeout(self) -> TimeSpan:
        '''Timeout for loading external resources'''
        raise NotImplementedError()
    
    @resource_loading_timeout.setter
    def resource_loading_timeout(self, value : TimeSpan) -> None:
        '''Timeout for loading external resources'''
        raise NotImplementedError()
    

class EpubLoadOptions(LoadOptions):
    '''Options for loading Epub documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.EBookFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    

class FinanceLoadOptions(LoadOptions):
    '''Options for loading finance documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FinanceFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.FinanceFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    

class FontLoadOptions(LoadOptions):
    '''Options for loading Font documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FontFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.FontFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    

class GisLoadOptions(LoadOptions):
    '''Options for loading GIS documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.GisFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.GisFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Sets desired page width for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets desired page width for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Sets desired page height for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets desired page height for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    

class GmlLoadOptions(GisLoadOptions):
    '''Options for loading Gml documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.GisFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Sets desired page width for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets desired page width for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Sets desired page height for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets desired page height for converting GIS document. Default is 1000.'''
        raise NotImplementedError()
    
    @property
    def schema_location(self) -> str:
        '''Space separated list of URI pairs. First URI in every pair is a URI of the namespace, second URI is a Path to XML schema of the namespace. If set to null, Conversion will try read schemaLocation from the root element of the document. Default is null'''
        raise NotImplementedError()
    
    @schema_location.setter
    def schema_location(self, value : str) -> None:
        '''Space separated list of URI pairs. First URI in every pair is a URI of the namespace, second URI is a Path to XML schema of the namespace. If set to null, Conversion will try read schemaLocation from the root element of the document. Default is null'''
        raise NotImplementedError()
    
    @property
    def restore_schema(self) -> bool:
        '''Determines whether Conversion is allowed to parse attributes in a Gml file in which an XML schema is missing or cannot be loaded. If set to true, Conversion reader does not require the presence of an XML Schema. Default is false.'''
        raise NotImplementedError()
    
    @restore_schema.setter
    def restore_schema(self, value : bool) -> None:
        '''Determines whether Conversion is allowed to parse attributes in a Gml file in which an XML schema is missing or cannot be loaded. If set to true, Conversion reader does not require the presence of an XML Schema. Default is false.'''
        raise NotImplementedError()
    
    @property
    def load_schemas_from_internet(self) -> bool:
        '''Determines whether Conversion is allowed to load XML schema from Internet. If set to false, schemas with absolute URIs that does not start with ‘file://’ would not be loaded. Default is false.'''
        raise NotImplementedError()
    
    @load_schemas_from_internet.setter
    def load_schemas_from_internet(self, value : bool) -> None:
        '''Determines whether Conversion is allowed to load XML schema from Internet. If set to false, schemas with absolute URIs that does not start with ‘file://’ would not be loaded. Default is false.'''
        raise NotImplementedError()
    

class Header:
    '''Represents a header with a name and value.'''
    
    @property
    def header_name(self) -> str:
        '''Gets the header name.'''
        raise NotImplementedError()
    
    @property
    def header_value(self) -> str:
        '''Gets the header value.'''
        raise NotImplementedError()
    

class HyphenationDictionary:
    '''Represents a mapping between an ISO language code and its associated hyphenation dictionary stream.'''
    
    @property
    def language_code(self) -> str:
        '''Gets the ISO language code.'''
        raise NotImplementedError()
    
    @property
    def dictionary_stream(self) -> io.RawIOBase:
        '''Gets the stream of the hyphenation dictionary.'''
        raise NotImplementedError()
    

class HyphenationOptions(groupdocs.conversion.contracts.ValueObject):
    '''Options for setting hyphenation documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def auto_hyphenation(self) -> bool:
        '''Gets value determining whether automatic hyphenation is turned on for the document. Default value for this property is false.'''
        raise NotImplementedError()
    
    @auto_hyphenation.setter
    def auto_hyphenation(self, value : bool) -> None:
        '''Sets value determining whether automatic hyphenation is turned on for the document. Default value for this property is false.'''
        raise NotImplementedError()
    
    @property
    def hyphenate_caps(self) -> bool:
        '''Gets value determining whether words written in all capital letters are hyphenated. Default value for this property is true.'''
        raise NotImplementedError()
    
    @hyphenate_caps.setter
    def hyphenate_caps(self, value : bool) -> None:
        '''Sets value determining whether words written in all capital letters are hyphenated. Default value for this property is true.'''
        raise NotImplementedError()
    
    @property
    def hyphenation_dictionaries(self) -> List[groupdocs.conversion.options.load.HyphenationDictionary]:
        '''Dictionary containing associates between ISO language codes with provided hyphenation dictionary streams.'''
        raise NotImplementedError()
    
    @hyphenation_dictionaries.setter
    def hyphenation_dictionaries(self, value : List[groupdocs.conversion.options.load.HyphenationDictionary]) -> None:
        '''Dictionary containing associates between ISO language codes with provided hyphenation dictionary streams.'''
        raise NotImplementedError()
    

class ICredentialsProvider:
    '''Interface for providing credentials for a given URI.'''
    
    def get_credentials(self, uri : str) -> groupdocs.conversion.options.load.NetworkCredentials:
        '''Gets the credentials associated with the specified URI.
        
        :param uri: The URI for which to get credentials.
        :returns: The credentials for the specified URI.'''
        raise NotImplementedError()
    

class IHeaderConfigurator:
    '''Interface for configuring request headers.'''
    
    def configure(self, uri : str, headers : List[groupdocs.conversion.options.load.Header]) -> None:
        '''Configures the request headers for the given URI.
        
        :param uri: The URI for which headers are being configured.
        :param headers: The collection of headers to configure.'''
        raise NotImplementedError()
    

class IMetadataLoadOptions:
    '''Options to control metadata in the converted document.'''
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    

class IPageNumberingLoadOptions:
    '''Options to control page numbering in the converted document.'''
    
    @property
    def page_numbering(self) -> bool:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @page_numbering.setter
    def page_numbering(self, value : bool) -> None:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    

class IResourceLoadingOptions:
    '''Represents set of options to control how external resources will be loaded'''
    
    @property
    def skip_external_resources(self) -> bool:
        '''If true all external resource will not be loading with exception of the resources in the :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @skip_external_resources.setter
    def skip_external_resources(self, value : bool) -> None:
        '''If true all external resource will not be loading with exception of the resources in the :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @property
    def whitelisted_resources(self) -> List[str]:
        '''External resources that will be always loaded'''
        raise NotImplementedError()
    
    @whitelisted_resources.setter
    def whitelisted_resources(self, value : List[str]) -> None:
        '''External resources that will be always loaded'''
        raise NotImplementedError()
    

class IXslFoFactory:
    '''Interface for creating an XSL-FO document stream.'''
    
    def create_xsl_fo_stream(self) -> io.RawIOBase:
        '''Creates a stream for the XSL-FO document.
        
        :returns: A stream representing the XSL-FO document.'''
        raise NotImplementedError()
    

class IXsltFactory:
    '''Interface for creating an XSLT document stream.'''
    
    def create_xslt_stream(self) -> io.RawIOBase:
        '''Creates a stream for the XSLT document.
        
        :returns: A stream representing the XSLT document.'''
        raise NotImplementedError()
    

class ImageLoadOptions(BaseImageLoadOptions):
    '''Options for loading Image documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.ImageFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.ImageFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Psd, Emf, Wmf document types. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Psd, Emf, Wmf document types. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    

class LoadOptions(groupdocs.conversion.contracts.ValueObject):
    '''Abstract document load options class.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FileType:
        '''Input document file type.'''
        raise NotImplementedError()
    

class MboxLoadOptions(LoadOptions):
    '''Options for loading Mbox documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Readonly. Set to false. The owner will not be converted'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Readonly. Set to true. The owned documents will be converted'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    

class NetworkCredentials:
    '''Represents network credentials with a username, password, and domain.'''
    
    @property
    def user_name(self) -> str:
        '''Gets the username.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Gets the password.'''
        raise NotImplementedError()
    
    @property
    def domain(self) -> str:
        '''Gets the domain.'''
        raise NotImplementedError()
    

class NoteLoadOptions(LoadOptions):
    '''Options for loading One documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.NoteFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Note document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Note document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting Note document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting Note document.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    

class NsfLoadOptions(LoadOptions):
    '''Options for loading Nsf documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Readonly. Set to false. The owner will not be converted'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Readonly. Set to true. The owned documents will be converted'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    

class OlmLoadOptions(LoadOptions):
    '''Options for loading Olm documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def folder(self) -> str:
        '''Folder which to be processed
        Default is Inbox'''
        raise NotImplementedError()
    
    @folder.setter
    def folder(self, value : str) -> None:
        '''Folder which to be processed
        Default is Inbox'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Readonly. Set to false. The owner will not be converted'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Readonly. Set to true. The owned documents will be converted'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    

class PageDescriptionLanguageLoadOptions(LoadOptions):
    '''Options for loading page description language documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.PageDescriptionLanguageFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.PageDescriptionLanguageFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    

class PdfLoadOptions(LoadOptions):
    '''Options for loading Pdf documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.PdfFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def remove_embedded_files(self) -> bool:
        '''Remove embedded files.'''
        raise NotImplementedError()
    
    @remove_embedded_files.setter
    def remove_embedded_files(self, value : bool) -> None:
        '''Remove embedded files.'''
        raise NotImplementedError()
    
    @property
    def remove_javascript(self) -> bool:
        '''Remove javascript.'''
        raise NotImplementedError()
    
    @remove_javascript.setter
    def remove_javascript(self, value : bool) -> None:
        '''Remove javascript.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Pdf document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Pdf document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting Pdf document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting Pdf document.'''
        raise NotImplementedError()
    
    @property
    def hide_pdf_annotations(self) -> bool:
        '''Hide annotations in Pdf documents.'''
        raise NotImplementedError()
    
    @hide_pdf_annotations.setter
    def hide_pdf_annotations(self, value : bool) -> None:
        '''Hide annotations in Pdf documents.'''
        raise NotImplementedError()
    
    @property
    def flatten_all_fields(self) -> bool:
        '''Flatten all the fields of the PDF form.'''
        raise NotImplementedError()
    
    @flatten_all_fields.setter
    def flatten_all_fields(self, value : bool) -> None:
        '''Flatten all the fields of the PDF form.'''
        raise NotImplementedError()
    
    @property
    def page_numbering(self) -> bool:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @page_numbering.setter
    def page_numbering(self, value : bool) -> None:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    

class PersonalStorageLoadOptions(LoadOptions):
    '''Options for loading personal storage documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.FileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def folder(self) -> str:
        '''Folder which to be processed
        Default is Inbox'''
        raise NotImplementedError()
    
    @folder.setter
    def folder(self, value : str) -> None:
        '''Folder which to be processed
        Default is Inbox'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Readonly. Set to false. The owner will not be converted'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Readonly. Set to true. The owned documents will be converted'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 3'''
        raise NotImplementedError()
    

class PresentationLoadOptions(LoadOptions):
    '''Options for loading Presentation documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.PresentationFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.PresentationFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for rendering the presentation. The following font will be used if a presentation font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for rendering the presentation. The following font will be used if a presentation font is missing.'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting Presentation document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting Presentation document.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @property
    def hide_comments(self) -> bool:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @hide_comments.setter
    def hide_comments(self, value : bool) -> None:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @property
    def show_hidden_slides(self) -> bool:
        '''Show hidden slides.'''
        raise NotImplementedError()
    
    @show_hidden_slides.setter
    def show_hidden_slides(self, value : bool) -> None:
        '''Show hidden slides.'''
        raise NotImplementedError()
    
    @property
    def skip_external_resources(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @skip_external_resources.setter
    def skip_external_resources(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @property
    def whitelisted_resources(self) -> List[str]:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @whitelisted_resources.setter
    def whitelisted_resources(self, value : List[str]) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    

class PublisherLoadOptions(LoadOptions):
    '''Options for loading Publisher documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.PublisherFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    

class RasterImageLoadOptions(BaseImageLoadOptions):
    '''Options for loading Image documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.ImageFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.ImageFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Psd, Emf, Wmf document types. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Psd, Emf, Wmf document types. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def vectorization_options(self) -> groupdocs.conversion.options.load.VectorizationOptions:
        '''Sets vectorization options'''
        raise NotImplementedError()
    
    @vectorization_options.setter
    def vectorization_options(self, value : groupdocs.conversion.options.load.VectorizationOptions) -> None:
        '''Sets vectorization options'''
        raise NotImplementedError()
    

class SpreadsheetLoadOptions(LoadOptions):
    '''Options for loading Spreadsheet documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.SpreadsheetFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.SpreadsheetFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def sheets(self) -> List[str]:
        '''Sheet name to convert'''
        raise NotImplementedError()
    
    @sheets.setter
    def sheets(self, value : List[str]) -> None:
        '''Sheet name to convert'''
        raise NotImplementedError()
    
    @property
    def sheet_indexes(self) -> List[int]:
        '''List of sheet indexes to convert.
        The indexes must be zero-based'''
        raise NotImplementedError()
    
    @sheet_indexes.setter
    def sheet_indexes(self, value : List[int]) -> None:
        '''List of sheet indexes to convert.
        The indexes must be zero-based'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for spreadsheet document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for spreadsheet document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting spreadsheet document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting spreadsheet document.'''
        raise NotImplementedError()
    
    @property
    def show_grid_lines(self) -> bool:
        '''Show grid lines when converting Excel files.'''
        raise NotImplementedError()
    
    @show_grid_lines.setter
    def show_grid_lines(self, value : bool) -> None:
        '''Show grid lines when converting Excel files.'''
        raise NotImplementedError()
    
    @property
    def show_hidden_sheets(self) -> bool:
        '''Show hidden sheets when converting Excel files.'''
        raise NotImplementedError()
    
    @show_hidden_sheets.setter
    def show_hidden_sheets(self, value : bool) -> None:
        '''Show hidden sheets when converting Excel files.'''
        raise NotImplementedError()
    
    @property
    def one_page_per_sheet(self) -> bool:
        '''If OnePagePerSheet is true the content of the sheet will be converted to one page in the PDF document. Default value is true.'''
        raise NotImplementedError()
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool) -> None:
        '''If OnePagePerSheet is true the content of the sheet will be converted to one page in the PDF document. Default value is true.'''
        raise NotImplementedError()
    
    @property
    def optimize_pdf_size(self) -> bool:
        '''If True and converting to Pdf the conversion is optimized for better file size than print quality.'''
        raise NotImplementedError()
    
    @optimize_pdf_size.setter
    def optimize_pdf_size(self, value : bool) -> None:
        '''If True and converting to Pdf the conversion is optimized for better file size than print quality.'''
        raise NotImplementedError()
    
    @property
    def convert_range(self) -> str:
        '''Convert specific range when converting to other than spreadsheet format. Example: "D1:F8".'''
        raise NotImplementedError()
    
    @convert_range.setter
    def convert_range(self, value : str) -> None:
        '''Convert specific range when converting to other than spreadsheet format. Example: "D1:F8".'''
        raise NotImplementedError()
    
    @property
    def skip_empty_rows_and_columns(self) -> bool:
        '''Skips empty rows and columns when converting. Default is True.'''
        raise NotImplementedError()
    
    @skip_empty_rows_and_columns.setter
    def skip_empty_rows_and_columns(self, value : bool) -> None:
        '''Skips empty rows and columns when converting. Default is True.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @property
    def hide_comments(self) -> bool:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @hide_comments.setter
    def hide_comments(self, value : bool) -> None:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @property
    def check_excel_restriction(self) -> bool:
        '''Whether check restriction of excel file when user modify cells related objects. For example, excel does not allow inputting string value longer than 32K. When you input a value longer than 32K, if this property is true, you will get an Exception. If this property is false, we will accept your input string value as the cell\'s value so that later you can output the complete string value for other file formats such as CSV. However, if you have set such kind of value that is invalid for excel file format, you should not save the workbook as excel file format later. Otherwise there may be unexpected error for the generated excel file.'''
        raise NotImplementedError()
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool) -> None:
        '''Whether check restriction of excel file when user modify cells related objects. For example, excel does not allow inputting string value longer than 32K. When you input a value longer than 32K, if this property is true, you will get an Exception. If this property is false, we will accept your input string value as the cell\'s value so that later you can output the complete string value for other file formats such as CSV. However, if you have set such kind of value that is invalid for excel file format, you should not save the workbook as excel file format later. Otherwise there may be unexpected error for the generated excel file.'''
        raise NotImplementedError()
    
    @property
    def culture_info(self) -> str:
        '''Get or set the system culture info at the time file is loaded, e.g. "en-US".'''
        raise NotImplementedError()
    
    @culture_info.setter
    def culture_info(self, value : str) -> None:
        '''Get or set the system culture info at the time file is loaded, e.g. "en-US".'''
        raise NotImplementedError()
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        '''If AllColumnsInOnePagePerSheet is true, all column content of one sheet will output to only one page in result. The width of paper size of pagesetup will be invalid, and the other settings of pagesetup will still take effect.'''
        raise NotImplementedError()
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool) -> None:
        '''If AllColumnsInOnePagePerSheet is true, all column content of one sheet will output to only one page in result. The width of paper size of pagesetup will be invalid, and the other settings of pagesetup will still take effect.'''
        raise NotImplementedError()
    
    @property
    def auto_fit_rows(self) -> bool:
        '''Autofits all rows when converting'''
        raise NotImplementedError()
    
    @auto_fit_rows.setter
    def auto_fit_rows(self, value : bool) -> None:
        '''Autofits all rows when converting'''
        raise NotImplementedError()
    
    @property
    def columns_per_page(self) -> int:
        '''Split a worksheet into pages by columns. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @columns_per_page.setter
    def columns_per_page(self, value : int) -> None:
        '''Split a worksheet into pages by columns. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @property
    def rows_per_page(self) -> int:
        '''Split a worksheet into pages by rows. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @rows_per_page.setter
    def rows_per_page(self, value : int) -> None:
        '''Split a worksheet into pages by rows. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    

class StreamXslFoFactory(IXslFoFactory):
    '''Default implementation of the :py:class:`groupdocs.conversion.options.load.IXslFoFactory` interface that accepts a stream in the constructor.'''
    
    def create_xsl_fo_stream(self) -> io.RawIOBase:
        '''Returns the provided stream for the XSL-FO document.
        
        :returns: The stream representing the XSL-FO document.'''
        raise NotImplementedError()
    

class StreamXsltFactory(IXsltFactory):
    '''Default implementation of the :py:class:`groupdocs.conversion.options.load.IXsltFactory` interface that accepts a stream in the constructor.'''
    
    def create_xslt_stream(self) -> io.RawIOBase:
        '''Returns the provided stream for the XSLT document.
        
        :returns: The stream representing the XSLT document.'''
        raise NotImplementedError()
    

class ThreeDLoadOptions(LoadOptions):
    '''Options for loading 3D documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.ThreeDFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.ThreeDFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    

class TsvLoadOptions(SpreadsheetLoadOptions):
    '''Options for loading Tsv documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones current instance.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.SpreadsheetFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def sheets(self) -> List[str]:
        '''Sheet name to convert'''
        raise NotImplementedError()
    
    @sheets.setter
    def sheets(self, value : List[str]) -> None:
        '''Sheet name to convert'''
        raise NotImplementedError()
    
    @property
    def sheet_indexes(self) -> List[int]:
        '''List of sheet indexes to convert.
        The indexes must be zero-based'''
        raise NotImplementedError()
    
    @sheet_indexes.setter
    def sheet_indexes(self, value : List[int]) -> None:
        '''List of sheet indexes to convert.
        The indexes must be zero-based'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for spreadsheet document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for spreadsheet document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting spreadsheet document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting spreadsheet document.'''
        raise NotImplementedError()
    
    @property
    def show_grid_lines(self) -> bool:
        '''Show grid lines when converting Excel files.'''
        raise NotImplementedError()
    
    @show_grid_lines.setter
    def show_grid_lines(self, value : bool) -> None:
        '''Show grid lines when converting Excel files.'''
        raise NotImplementedError()
    
    @property
    def show_hidden_sheets(self) -> bool:
        '''Show hidden sheets when converting Excel files.'''
        raise NotImplementedError()
    
    @show_hidden_sheets.setter
    def show_hidden_sheets(self, value : bool) -> None:
        '''Show hidden sheets when converting Excel files.'''
        raise NotImplementedError()
    
    @property
    def one_page_per_sheet(self) -> bool:
        '''If OnePagePerSheet is true the content of the sheet will be converted to one page in the PDF document. Default value is true.'''
        raise NotImplementedError()
    
    @one_page_per_sheet.setter
    def one_page_per_sheet(self, value : bool) -> None:
        '''If OnePagePerSheet is true the content of the sheet will be converted to one page in the PDF document. Default value is true.'''
        raise NotImplementedError()
    
    @property
    def optimize_pdf_size(self) -> bool:
        '''If True and converting to Pdf the conversion is optimized for better file size than print quality.'''
        raise NotImplementedError()
    
    @optimize_pdf_size.setter
    def optimize_pdf_size(self, value : bool) -> None:
        '''If True and converting to Pdf the conversion is optimized for better file size than print quality.'''
        raise NotImplementedError()
    
    @property
    def convert_range(self) -> str:
        '''Convert specific range when converting to other than spreadsheet format. Example: "D1:F8".'''
        raise NotImplementedError()
    
    @convert_range.setter
    def convert_range(self, value : str) -> None:
        '''Convert specific range when converting to other than spreadsheet format. Example: "D1:F8".'''
        raise NotImplementedError()
    
    @property
    def skip_empty_rows_and_columns(self) -> bool:
        '''Skips empty rows and columns when converting. Default is True.'''
        raise NotImplementedError()
    
    @skip_empty_rows_and_columns.setter
    def skip_empty_rows_and_columns(self, value : bool) -> None:
        '''Skips empty rows and columns when converting. Default is True.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @property
    def hide_comments(self) -> bool:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @hide_comments.setter
    def hide_comments(self, value : bool) -> None:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @property
    def check_excel_restriction(self) -> bool:
        '''Whether check restriction of excel file when user modify cells related objects. For example, excel does not allow inputting string value longer than 32K. When you input a value longer than 32K, if this property is true, you will get an Exception. If this property is false, we will accept your input string value as the cell\'s value so that later you can output the complete string value for other file formats such as CSV. However, if you have set such kind of value that is invalid for excel file format, you should not save the workbook as excel file format later. Otherwise there may be unexpected error for the generated excel file.'''
        raise NotImplementedError()
    
    @check_excel_restriction.setter
    def check_excel_restriction(self, value : bool) -> None:
        '''Whether check restriction of excel file when user modify cells related objects. For example, excel does not allow inputting string value longer than 32K. When you input a value longer than 32K, if this property is true, you will get an Exception. If this property is false, we will accept your input string value as the cell\'s value so that later you can output the complete string value for other file formats such as CSV. However, if you have set such kind of value that is invalid for excel file format, you should not save the workbook as excel file format later. Otherwise there may be unexpected error for the generated excel file.'''
        raise NotImplementedError()
    
    @property
    def culture_info(self) -> str:
        '''Get or set the system culture info at the time file is loaded, e.g. "en-US".'''
        raise NotImplementedError()
    
    @culture_info.setter
    def culture_info(self, value : str) -> None:
        '''Get or set the system culture info at the time file is loaded, e.g. "en-US".'''
        raise NotImplementedError()
    
    @property
    def all_columns_in_one_page_per_sheet(self) -> bool:
        '''If AllColumnsInOnePagePerSheet is true, all column content of one sheet will output to only one page in result. The width of paper size of pagesetup will be invalid, and the other settings of pagesetup will still take effect.'''
        raise NotImplementedError()
    
    @all_columns_in_one_page_per_sheet.setter
    def all_columns_in_one_page_per_sheet(self, value : bool) -> None:
        '''If AllColumnsInOnePagePerSheet is true, all column content of one sheet will output to only one page in result. The width of paper size of pagesetup will be invalid, and the other settings of pagesetup will still take effect.'''
        raise NotImplementedError()
    
    @property
    def auto_fit_rows(self) -> bool:
        '''Autofits all rows when converting'''
        raise NotImplementedError()
    
    @auto_fit_rows.setter
    def auto_fit_rows(self, value : bool) -> None:
        '''Autofits all rows when converting'''
        raise NotImplementedError()
    
    @property
    def columns_per_page(self) -> int:
        '''Split a worksheet into pages by columns. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @columns_per_page.setter
    def columns_per_page(self, value : int) -> None:
        '''Split a worksheet into pages by columns. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @property
    def rows_per_page(self) -> int:
        '''Split a worksheet into pages by rows. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @rows_per_page.setter
    def rows_per_page(self, value : int) -> None:
        '''Split a worksheet into pages by rows. Default is 0, no pagination.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    

class TxtLeadingSpacesOptions(groupdocs.conversion.contracts.Enumeration):
    '''Describes txt leading spaces options enumeration.'''
    
    def equals(self, other : groupdocs.conversion.contracts.Enumeration) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares current object to other.
        
        :param obj: The other object
        :returns: zero if equal'''
        raise NotImplementedError()
    
    @staticmethod
    def get_all() -> Iterable[groupdocs.conversion.options.load.TxtLeadingSpacesOptions]:
        '''Returns all enumeration values.
        
        :returns: Enumerable of the provided type'''
        raise NotImplementedError()
    
    CONVERT_TO_INDENT : groupdocs.conversion.options.load.TxtLeadingSpacesOptions
    '''Converts leading spaces to indents.'''
    PRESERVE : groupdocs.conversion.options.load.TxtLeadingSpacesOptions
    '''Preserves leading spaces.'''
    TRIM : groupdocs.conversion.options.load.TxtLeadingSpacesOptions
    '''Trims leading spaces.'''

class TxtLoadOptions(LoadOptions):
    '''Options for loading Txt documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.WordProcessingFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def detect_numbering_with_whitespaces(self) -> bool:
        '''Allows to specify how numbered list items are recognized when plain text document is converted.
        The default value is true.'''
        raise NotImplementedError()
    
    @detect_numbering_with_whitespaces.setter
    def detect_numbering_with_whitespaces(self, value : bool) -> None:
        '''Allows to specify how numbered list items are recognized when plain text document is converted.
        The default value is true.'''
        raise NotImplementedError()
    
    @property
    def trailing_spaces_options(self) -> groupdocs.conversion.options.load.TxtTrailingSpacesOptions:
        '''Gets preferred option of a trailing space handling.
        Default value is :py:attr:`groupdocs.conversion.options.load.TxtTrailingSpacesOptions.TRIM`.'''
        raise NotImplementedError()
    
    @trailing_spaces_options.setter
    def trailing_spaces_options(self, value : groupdocs.conversion.options.load.TxtTrailingSpacesOptions) -> None:
        '''Sets preferred option of a trailing space handling.
        Default value is :py:attr:`groupdocs.conversion.options.load.TxtTrailingSpacesOptions.TRIM`.'''
        raise NotImplementedError()
    
    @property
    def leading_spaces_options(self) -> groupdocs.conversion.options.load.TxtLeadingSpacesOptions:
        '''Gets preferred option of a leading space handling.
        Default value is :py:attr:`groupdocs.conversion.options.load.TxtLeadingSpacesOptions.CONVERT_TO_INDENT`.'''
        raise NotImplementedError()
    
    @leading_spaces_options.setter
    def leading_spaces_options(self, value : groupdocs.conversion.options.load.TxtLeadingSpacesOptions) -> None:
        '''Sets preferred option of a leading space handling.
        Default value is :py:attr:`groupdocs.conversion.options.load.TxtLeadingSpacesOptions.CONVERT_TO_INDENT`.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> str:
        '''Gets the encoding that will be used when loading Txt document. Can be null. Default is null.'''
        raise NotImplementedError()
    
    @encoding.setter
    def encoding(self, value : str) -> None:
        '''Sets the encoding that will be used when loading Txt document. Can be null. Default is null.'''
        raise NotImplementedError()
    

class TxtTrailingSpacesOptions(groupdocs.conversion.contracts.Enumeration):
    '''Describes txt trailing spaces options enumeration.'''
    
    def equals(self, other : groupdocs.conversion.contracts.Enumeration) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares current object to other.
        
        :param obj: The other object
        :returns: zero if equal'''
        raise NotImplementedError()
    
    @staticmethod
    def get_all() -> Iterable[groupdocs.conversion.options.load.TxtTrailingSpacesOptions]:
        '''Returns all enumeration values.
        
        :returns: Enumerable of the provided type'''
        raise NotImplementedError()
    
    PRESERVE : groupdocs.conversion.options.load.TxtTrailingSpacesOptions
    '''Preserves trailing spaces'''
    TRIM : groupdocs.conversion.options.load.TxtTrailingSpacesOptions
    '''Trims trailing spaces'''

class VcfLoadOptions(LoadOptions):
    '''Options for loading Vcf documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.EmailFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> str:
        '''Gets the encoding that will be used when loading Vcf document. Default is Encoding.Default.'''
        raise NotImplementedError()
    
    @encoding.setter
    def encoding(self, value : str) -> None:
        '''Sets the encoding that will be used when loading Vcf document. Default is Encoding.Default.'''
        raise NotImplementedError()
    

class VectorizationOptions(groupdocs.conversion.contracts.ValueObject):
    '''Options for vectorization images.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def enable_vectorization(self) -> bool:
        '''Enable vectorization images. Default is false.'''
        raise NotImplementedError()
    
    @enable_vectorization.setter
    def enable_vectorization(self, value : bool) -> None:
        '''Enable vectorization images. Default is false.'''
        raise NotImplementedError()
    
    @property
    def severity(self) -> int:
        '''Sets image trace smoother severity'''
        raise NotImplementedError()
    
    @severity.setter
    def severity(self, value : int) -> None:
        '''Sets image trace smoother severity'''
        raise NotImplementedError()
    
    @property
    def colors_limit(self) -> int:
        '''Gets the maximum number of colors used to quantize an image. Default value is 25.'''
        raise NotImplementedError()
    
    @colors_limit.setter
    def colors_limit(self, value : int) -> None:
        '''Sets the maximum number of colors used to quantize an image. Default value is 25.'''
        raise NotImplementedError()
    
    @property
    def line_width(self) -> float:
        '''Gets the line width. The value of this parameter is affected by the graphics scale. Default value is 1.'''
        raise NotImplementedError()
    
    @line_width.setter
    def line_width(self, value : float) -> None:
        '''Sets the line width. The value of this parameter is affected by the graphics scale. Default value is 1.'''
        raise NotImplementedError()
    
    @property
    def image_size_limit(self) -> int:
        '''Gets maximal dimension of image determined by multiplication image width and height. The size of the image will be scaled based on this property. Default value is 1800000.'''
        raise NotImplementedError()
    
    @image_size_limit.setter
    def image_size_limit(self, value : int) -> None:
        '''Sets maximal dimension of image determined by multiplication image width and height. The size of the image will be scaled based on this property. Default value is 1800000.'''
        raise NotImplementedError()
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        '''Gets background color. Default value is transparent white.'''
        raise NotImplementedError()
    
    @background_color.setter
    def background_color(self, value : aspose.pydrawing.Color) -> None:
        '''Sets background color. Default value is transparent white.'''
        raise NotImplementedError()
    

class WebLoadOptions(LoadOptions):
    '''Options for loading web documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.WebFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.WebFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def page_numbering(self) -> bool:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @page_numbering.setter
    def page_numbering(self, value : bool) -> None:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @property
    def base_path(self) -> str:
        '''The base path/url for the html'''
        raise NotImplementedError()
    
    @base_path.setter
    def base_path(self, value : str) -> None:
        '''The base path/url for the html'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> str:
        '''Get the encoding to be used when loading the web document.
        If the property is null the encoding will be determined from document character set attribute'''
        raise NotImplementedError()
    
    @encoding.setter
    def encoding(self, value : str) -> None:
        '''Get or sets the encoding to be used when loading the web document.
        If the property is null the encoding will be determined from document character set attribute'''
        raise NotImplementedError()
    
    @property
    def resource_loading_timeout(self) -> TimeSpan:
        '''Timeout for loading external resources'''
        raise NotImplementedError()
    
    @resource_loading_timeout.setter
    def resource_loading_timeout(self, value : TimeSpan) -> None:
        '''Timeout for loading external resources'''
        raise NotImplementedError()
    
    @property
    def skip_external_resources(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @skip_external_resources.setter
    def skip_external_resources(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @property
    def whitelisted_resources(self) -> List[str]:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @whitelisted_resources.setter
    def whitelisted_resources(self, value : List[str]) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @property
    def use_pdf(self) -> bool:
        '''Use pdf for the conversion. Default: false'''
        raise NotImplementedError()
    
    @use_pdf.setter
    def use_pdf(self, value : bool) -> None:
        '''Use pdf for the conversion. Default: false'''
        raise NotImplementedError()
    
    @property
    def configure_headers(self) -> groupdocs.conversion.options.load.IHeaderConfigurator:
        '''Interface for configuring request headers. The implementation should define the behavior for configuring headers based on the URI.'''
        raise NotImplementedError()
    
    @configure_headers.setter
    def configure_headers(self, value : groupdocs.conversion.options.load.IHeaderConfigurator) -> None:
        '''Interface for configuring request headers. The implementation should define the behavior for configuring headers based on the URI.'''
        raise NotImplementedError()
    
    @property
    def credentials_provider(self) -> groupdocs.conversion.options.load.ICredentialsProvider:
        '''Credentials provider for the URI.'''
        raise NotImplementedError()
    
    @credentials_provider.setter
    def credentials_provider(self, value : groupdocs.conversion.options.load.ICredentialsProvider) -> None:
        '''Credentials provider for the URI.'''
        raise NotImplementedError()
    

class WordProcessingBookmarksOptions(groupdocs.conversion.contracts.ValueObject):
    '''Options for handling bookmarks in WordProcessing'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def bookmarks_outline_level(self) -> int:
        '''Specifies the default level in the document outline at which to display Word bookmarks. Default is 0. Valid range is 0 to 9.'''
        raise NotImplementedError()
    
    @bookmarks_outline_level.setter
    def bookmarks_outline_level(self, value : int) -> None:
        '''Specifies the default level in the document outline at which to display Word bookmarks. Default is 0. Valid range is 0 to 9.'''
        raise NotImplementedError()
    
    @property
    def headings_outline_levels(self) -> int:
        '''Specifies how many levels of headings (paragraphs formatted with the Heading styles) to include in the document outline. Default is 0. Valid range is 0 to 9.'''
        raise NotImplementedError()
    
    @headings_outline_levels.setter
    def headings_outline_levels(self, value : int) -> None:
        '''Specifies how many levels of headings (paragraphs formatted with the Heading styles) to include in the document outline. Default is 0. Valid range is 0 to 9.'''
        raise NotImplementedError()
    
    @property
    def expanded_outline_levels(self) -> int:
        '''Specifies how many levels in the document outline to show expanded when the file is viewed. Default is 0. Valid range is 0 to 9. Note that this options will not work when saving to XPS.'''
        raise NotImplementedError()
    
    @expanded_outline_levels.setter
    def expanded_outline_levels(self, value : int) -> None:
        '''Specifies how many levels in the document outline to show expanded when the file is viewed. Default is 0. Valid range is 0 to 9. Note that this options will not work when saving to XPS.'''
        raise NotImplementedError()
    

class WordProcessingLoadOptions(LoadOptions):
    '''Options for loading WordProcessing documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.WordProcessingFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : groupdocs.conversion.filetypes.WordProcessingFileType) -> None:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> str:
        '''Default font for Words document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : str) -> None:
        '''Default font for Words document. The following font will be used if a font is missing.'''
        raise NotImplementedError()
    
    @property
    def auto_font_substitution(self) -> bool:
        '''If AutoFontSubstitution is disabled, GroupDocs.Conversion uses the DefaultFont for the substitution of missing fonts. If AutoFontSubstitution is enabled,
        GroupDocs.Conversion evaluates all the related fields in FontInfo (Panose, Sig etc) for the missing font and finds the closest match among the available font sources.
        Note that font substitution mechanism will override the DefaultFont in cases when FontInfo for the missing font is available in the document. The default value is True.'''
        raise NotImplementedError()
    
    @auto_font_substitution.setter
    def auto_font_substitution(self, value : bool) -> None:
        '''If AutoFontSubstitution is disabled, GroupDocs.Conversion uses the DefaultFont for the substitution of missing fonts. If AutoFontSubstitution is enabled,
        GroupDocs.Conversion evaluates all the related fields in FontInfo (Panose, Sig etc) for the missing font and finds the closest match among the available font sources.
        Note that font substitution mechanism will override the DefaultFont in cases when FontInfo for the missing font is available in the document. The default value is True.'''
        raise NotImplementedError()
    
    @property
    def embed_true_type_fonts(self) -> bool:
        '''If EmbedTrueTypeFonts is true, GroupDocs.Conversion embed true type fonts in the output document. Default: false'''
        raise NotImplementedError()
    
    @embed_true_type_fonts.setter
    def embed_true_type_fonts(self, value : bool) -> None:
        '''If EmbedTrueTypeFonts is true, GroupDocs.Conversion embed true type fonts in the output document. Default: false'''
        raise NotImplementedError()
    
    @property
    def update_page_layout(self) -> bool:
        '''Update page layout after loading. Default: false'''
        raise NotImplementedError()
    
    @update_page_layout.setter
    def update_page_layout(self, value : bool) -> None:
        '''Update page layout after loading. Default: false'''
        raise NotImplementedError()
    
    @property
    def update_fields(self) -> bool:
        '''Update fields after loading. Default: false'''
        raise NotImplementedError()
    
    @update_fields.setter
    def update_fields(self, value : bool) -> None:
        '''Update fields after loading. Default: false'''
        raise NotImplementedError()
    
    @property
    def keep_date_field_original_value(self) -> bool:
        '''Keep original value of date field. Default: false'''
        raise NotImplementedError()
    
    @keep_date_field_original_value.setter
    def keep_date_field_original_value(self, value : bool) -> None:
        '''Keep original value of date field. Default: false'''
        raise NotImplementedError()
    
    @property
    def font_substitutes(self) -> List[groupdocs.conversion.contracts.FontSubstitute]:
        '''Substitute specific fonts when converting Words document.'''
        raise NotImplementedError()
    
    @font_substitutes.setter
    def font_substitutes(self, value : List[groupdocs.conversion.contracts.FontSubstitute]) -> None:
        '''Substitute specific fonts when converting Words document.'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Set password to unprotect protected document.'''
        raise NotImplementedError()
    
    @property
    def hide_word_tracked_changes(self) -> bool:
        '''Hide markup and track changes for Word documents.'''
        raise NotImplementedError()
    
    @hide_word_tracked_changes.setter
    def hide_word_tracked_changes(self, value : bool) -> None:
        '''Hide markup and track changes for Word documents.'''
        raise NotImplementedError()
    
    @property
    def hide_comments(self) -> bool:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @hide_comments.setter
    def hide_comments(self, value : bool) -> None:
        '''Hide comments.'''
        raise NotImplementedError()
    
    @property
    def bookmark_options(self) -> groupdocs.conversion.options.load.WordProcessingBookmarksOptions:
        '''Bookmarks options'''
        raise NotImplementedError()
    
    @bookmark_options.setter
    def bookmark_options(self, value : groupdocs.conversion.options.load.WordProcessingBookmarksOptions) -> None:
        '''Bookmarks options'''
        raise NotImplementedError()
    
    @property
    def preserve_form_fields(self) -> bool:
        '''Specifies whether to preserve Microsoft Word form fields as form fields in PDF or convert them to text. Default is false.'''
        raise NotImplementedError()
    
    @preserve_form_fields.setter
    def preserve_form_fields(self, value : bool) -> None:
        '''Specifies whether to preserve Microsoft Word form fields as form fields in PDF or convert them to text. Default is false.'''
        raise NotImplementedError()
    
    @property
    def use_text_shaper(self) -> bool:
        '''Specifies whether to use a text shaper for better kerning display. Default is false.'''
        raise NotImplementedError()
    
    @use_text_shaper.setter
    def use_text_shaper(self, value : bool) -> None:
        '''Specifies whether to use a text shaper for better kerning display. Default is false.'''
        raise NotImplementedError()
    
    @property
    def skip_external_resources(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @skip_external_resources.setter
    def skip_external_resources(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @property
    def whitelisted_resources(self) -> List[str]:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @whitelisted_resources.setter
    def whitelisted_resources(self, value : List[str]) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @property
    def preserve_document_structure(self) -> bool:
        '''Determines whether the document structure should be preserved when converting to PDF (default is false).'''
        raise NotImplementedError()
    
    @preserve_document_structure.setter
    def preserve_document_structure(self, value : bool) -> None:
        '''Determines whether the document structure should be preserved when converting to PDF (default is false).'''
        raise NotImplementedError()
    
    @property
    def page_numbering(self) -> bool:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @page_numbering.setter
    def page_numbering(self, value : bool) -> None:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @property
    def hyphenation_options(self) -> groupdocs.conversion.options.load.HyphenationOptions:
        '''Set hyphenation options for WordProcessing documents.'''
        raise NotImplementedError()
    
    @hyphenation_options.setter
    def hyphenation_options(self, value : groupdocs.conversion.options.load.HyphenationOptions) -> None:
        '''Set hyphenation options for WordProcessing documents.'''
        raise NotImplementedError()
    
    @property
    def convert_owner(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @convert_owner.setter
    def convert_owner(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owner`
        
        Default is true'''
        raise NotImplementedError()
    
    @property
    def convert_owned(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @convert_owned.setter
    def convert_owned(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.convert_owned`
        
        Default is false'''
        raise NotImplementedError()
    
    @property
    def depth(self) -> int:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @depth.setter
    def depth(self, value : int) -> None:
        '''Implements :py:attr:`groupdocs.conversion.contracts.IDocumentsContainerLoadOptions.depth`
        
        Default: 1'''
        raise NotImplementedError()
    
    @property
    def clear_built_in_document_properties(self) -> bool:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_built_in_document_properties.setter
    def clear_built_in_document_properties(self, value : bool) -> None:
        '''Removes built-in metadata properties from the document.'''
        raise NotImplementedError()
    
    @property
    def clear_custom_document_properties(self) -> bool:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    
    @clear_custom_document_properties.setter
    def clear_custom_document_properties(self, value : bool) -> None:
        '''Removes custom metadata properties from the document.'''
        raise NotImplementedError()
    

class XmlLoadOptions(WebLoadOptions):
    '''Options for loading XML documents.'''
    
    def equals(self, other : groupdocs.conversion.contracts.ValueObject) -> bool:
        '''Determines whether two object instances are equal.
        
        :param other: The object to compare with the current object.
        :returns: ``true`` if the specified object is equal to the current object; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> groupdocs.conversion.filetypes.WebFileType:
        '''Input document file type.'''
        raise NotImplementedError()
    
    @property
    def page_numbering(self) -> bool:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @page_numbering.setter
    def page_numbering(self, value : bool) -> None:
        '''Enable or disable generation of page numbering in converted document. Default: false'''
        raise NotImplementedError()
    
    @property
    def base_path(self) -> str:
        '''The base path/url for the html'''
        raise NotImplementedError()
    
    @base_path.setter
    def base_path(self, value : str) -> None:
        '''The base path/url for the html'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> str:
        '''Get the encoding to be used when loading the web document.
        If the property is null the encoding will be determined from document character set attribute'''
        raise NotImplementedError()
    
    @encoding.setter
    def encoding(self, value : str) -> None:
        '''Get or sets the encoding to be used when loading the web document.
        If the property is null the encoding will be determined from document character set attribute'''
        raise NotImplementedError()
    
    @property
    def resource_loading_timeout(self) -> TimeSpan:
        '''Timeout for loading external resources'''
        raise NotImplementedError()
    
    @resource_loading_timeout.setter
    def resource_loading_timeout(self, value : TimeSpan) -> None:
        '''Timeout for loading external resources'''
        raise NotImplementedError()
    
    @property
    def skip_external_resources(self) -> bool:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @skip_external_resources.setter
    def skip_external_resources(self, value : bool) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.skip_external_resources`'''
        raise NotImplementedError()
    
    @property
    def whitelisted_resources(self) -> List[str]:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @whitelisted_resources.setter
    def whitelisted_resources(self, value : List[str]) -> None:
        '''Implements :py:attr:`groupdocs.conversion.options.load.IResourceLoadingOptions.whitelisted_resources`'''
        raise NotImplementedError()
    
    @property
    def use_pdf(self) -> bool:
        '''Use pdf for the conversion. Default: false'''
        raise NotImplementedError()
    
    @use_pdf.setter
    def use_pdf(self, value : bool) -> None:
        '''Use pdf for the conversion. Default: false'''
        raise NotImplementedError()
    
    @property
    def configure_headers(self) -> groupdocs.conversion.options.load.IHeaderConfigurator:
        '''Interface for configuring request headers. The implementation should define the behavior for configuring headers based on the URI.'''
        raise NotImplementedError()
    
    @configure_headers.setter
    def configure_headers(self, value : groupdocs.conversion.options.load.IHeaderConfigurator) -> None:
        '''Interface for configuring request headers. The implementation should define the behavior for configuring headers based on the URI.'''
        raise NotImplementedError()
    
    @property
    def credentials_provider(self) -> groupdocs.conversion.options.load.ICredentialsProvider:
        '''Credentials provider for the URI.'''
        raise NotImplementedError()
    
    @credentials_provider.setter
    def credentials_provider(self, value : groupdocs.conversion.options.load.ICredentialsProvider) -> None:
        '''Credentials provider for the URI.'''
        raise NotImplementedError()
    
    @property
    def xsl_fo_factory(self) -> groupdocs.conversion.options.load.IXslFoFactory:
        '''XSL-FO document stream to convert XML using XSL-FO markup file.'''
        raise NotImplementedError()
    
    @xsl_fo_factory.setter
    def xsl_fo_factory(self, value : groupdocs.conversion.options.load.IXslFoFactory) -> None:
        '''XSL-FO document stream to convert XML using XSL-FO markup file.'''
        raise NotImplementedError()
    
    @property
    def xslt_factory(self) -> groupdocs.conversion.options.load.IXsltFactory:
        '''XSLT document stream to convert XML performing XSL transformation to HTML.'''
        raise NotImplementedError()
    
    @xslt_factory.setter
    def xslt_factory(self, value : groupdocs.conversion.options.load.IXsltFactory) -> None:
        '''XSLT document stream to convert XML performing XSL transformation to HTML.'''
        raise NotImplementedError()
    
    @property
    def use_as_data_source(self) -> bool:
        '''Use Xml document as data source'''
        raise NotImplementedError()
    
    @use_as_data_source.setter
    def use_as_data_source(self, value : bool) -> None:
        '''Use Xml document as data source'''
        raise NotImplementedError()
    

