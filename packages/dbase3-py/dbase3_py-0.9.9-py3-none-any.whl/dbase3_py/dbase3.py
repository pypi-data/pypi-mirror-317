#!/usr/bin/env python3
#-*- coding: utf_8 -*-

"""
dbase3.py

This module provides a class to manipulate DBase III database files.
It allows reading, writing, adding, updating and deleting records in the database.

Classes:
    DBaseFile
    DbaseHeader
    DbaseField
"""

# Title: dBase III File Reader and Writer

import struct, os
from mmap import mmap as memmap, ACCESS_WRITE
from enum import Enum
from typing import List, Dict, Tuple, Callable, AnyStr, ByteString
from dataclasses import dataclass #, fields, field, is_dataclass
from datetime import datetime

getYear = lambda: datetime.now().year - 1900
getMonth = lambda: datetime.now().month
getDay = lambda: datetime.now().day

class FieldType(Enum):
    CHARACTER = b'C'
    DATE = b'D'
    FLOAT = b'F'
    LOGICAL = b'L'
    MEMO = b'M'
    NUMERIC = b'N'

    def __str__(self):
        return self.value   


@dataclass
class DbaseHeader:
    version: int = 3 # 1 byte
    year: int = getYear() # 1 byte
    month: int = getMonth() # 1 byte
    day: int = getDay() # 1 byte
    records: int = 0 # 4 bytes
    header_size: int = 0 # 2 bytes
    record_size: int = 0 # 2 bytes
    reserved: bytes = b'\x00' * 20

    def load_bytes(self, bytes):
        (self.version, self.year, self.month, self.day, 
         self.records, self.header_size, self.record_size, 
         self.reserved) = struct.unpack('<BBBBLHH20s', bytes)
 
    def to_bytes(self):
        return struct.pack('<BBBBLHH20s', self.version, self.year, self.month, self.day, 
                           self.records, self.header_size, self.record_size, 
                           self.reserved)
    
    def __post_init__(self):
        curr_year = getYear()
        # curr_month = getMonth()
        # curr_day = getDay()
        if not (3 == self.version & 0b111):
            raise ValueError(f"Version must be a byte (3-5), got {self.version}")            
        if not (0 <= self.year <= curr_year):
            raise ValueError(f"Year must be a byte (0-{curr_year}), got {self.year}")
        if not (1 <= self.month <= 12):
            raise ValueError(f"Month must be a byte (1-12), got {self.month}")    
        if not (1 <= self.day <= 31):
            raise ValueError(f"Day must be a byte (1-31), got {self.day}")
        if not (0 <= self.records <= 2**32-1):
            raise ValueError(f"Records must be a 4-byte integer (0-{2**32-1}), got {self.records}")
        if not (0 <= self.header_size <= 2**16-1):
            raise ValueError(f"Header size must be a 2-byte integer (0-{2**16-1}), got {self.header_size}")
        if not (0 <= self.record_size <= 2**16-1):
            raise ValueError(f"Record size must be a 2-byte integer (0-{2**16-1}), got {self.record_size}")
        if not (20 == len(self.reserved)):
            raise ValueError(f"Reserved must be 20 bytes, got {len(self.reserved)}")


@dataclass
class DbaseField:
    name: bytes = b'' # 11 bytes
    type: FieldType = b'C' # 1 byte
    address: int = 0 # 4 bytes
    length: int = 0 # 1 byte
    decimal: int = 0 # 1 byte
    reserved: bytes = b'\x00' * 14

    def load_bytes(self, bytes):
        (self.name, self.type, self.address, 
         self.length, self.decimal, self.reserved) = struct.unpack('<11sBIBB14s', bytes)
        self.name = self.name.strip(b'\x00')
        # self.type = chr(self.type).encode()
        
    def to_bytes(self):
        return struct.pack('<11sBIBB14s', self.name.ljust(11, b'\x00'), self.type, self.address, 
                           self.length, self.decimal, self.reserved)


class DbaseFile:
    """
    Class to manipulate DBase III database files (read and write).

    Methods:
        __init__(self, filename: str)
        __del__(self)
        __len__(self)
        __getitem__(self, key)
        __iter__(self)
         _init(self)
        istartswith(f: str, v: str) -> bool
        iendswith(f: str, v: str) -> bool
        create(cls, filename: str, fields: List[Tuple[str, FieldType, int, int]])
        add_record(self, record_data: dict)
        update_record(self, index: int, record_data: dict)
        del_record(self, key, value = True)
        get_record(self, key)
        get_field(self, fieldname)
        search(self, fieldname, value, start=0, funcname="", comp_func=None)
        find(self, fieldname, value, start=0, comp_func=None)
        index(self, fieldname, value, start=0, comp_func=None)
        filter(self, fieldname, value, comp_func=None)
        save_record(self, key, record)
        write(self)
    """
    
    @staticmethod
    def istartswith(f: str, v: str) -> bool:
        """
        Checks if the string 'f' starts with the string 'v', ignoring case.

        :param f: String to check.
        :param v: Prefix to look for.
        :return: True if 'f' starts with 'v', False otherwise.
        """

        return f.lower().startswith(v.lower())

    @staticmethod
    def iendswith(f: str, v: str) -> bool:
        """
        Checks if the string 'f' ends with the string 'v', ignoring case.

        :param f: String to check.
        :param v: Suffix to look for.
        :return: True if 'f' ends with 'v', False otherwise.
        """
        return f.lower().endswith(v.lower())

    @classmethod
    def create(cls, filename: str, fields: List[Tuple[str, FieldType, int, int]]):
        """
        Creates a new DBase III database file with the specified fields.

        :param filename: Name of the file to create.
        :param fields: List of tuples describing the fields (name, type, length, decimals).
        :raises FileExistsError: If the file already exists.
        """
        if os.path.exists(filename):
            raise FileExistsError(f"File {filename} already exists")
        with open(filename, 'wb') as file:
            header = DbaseHeader()
            header.header_size = 32 + 32 * len(fields) + 1
            header.record_size = sum(field[2] for field in fields) + 1
            file.write(header.to_bytes())
            for field in fields:
                name, ftype, length, decimal = field
                if type(name) == str:
                    name = name.encode()
                field = DbaseField(name, ord(ftype), 0, length, decimal)
                file.write(field.to_bytes())
            file.write(b'\x0D')
        dbf = cls(filename)
        return dbf

    def __init__(self, filename):
        """
        Initializes an instance of DBase3.

        :param filename: Name of the database file.
        """
        self.filename = filename
        self.filesize = os.path.getsize(filename)
        self.file = open(filename, 'r+b')
        # self.memfile = memmap(self.file.fileno(), 0, access=ACCESS_WRITE)
        self.num_fields = 0
        self.fields = []
        self.header = None
        self.datasize = 0
        self. _init()

    def __del__(self):
        """
        Closes the database file when the instance is destroyed.
        """
        self.file.close()

    def __len__(self):
        """
        Returns the number of records in the database, including records marked to be deleted.
        """
        return self.header.records
    
    def __getitem__(self, key):
        """
        Returns from the database a single record (dictionary with field names and field values) 
        or a list of them (if a slice is used).
        """
        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or self.header.records
            step = key.step or 1
            if start < 0:
                start += self.header.records + 1
            if stop < 0:
                stop += self.header.records + 1
            if stop < start:
                if step > 0:
                    step = -step
            elif stop > start:
                if step < 0:
                    step = -step    
            else:
                return []
            if stop > self.header.records:
                stop = self.header.records

            return [self.get_record(i) for i in range(start, stop, step)]
        else:
            if -self.header.records > key or key >= self.header.records:
                raise IndexError("Record index out of range")
            if key < 0:
                key += self.header.records 
            return self.get_record(key)

    def __iter__(self):
        """
        Returns an iterator over the records in the database, 
        allowing notation like 'for record in dbf'.
        """
        self.file.seek(self.header.header_size)
        return iter(self.get_record(i) for i in range(self.header.records))
        
    def __str__(self):
        # return f"{self.header}\n{self.fields}\n{self.records}"
        lastmodified = datetime.strftime(datetime(1900 + self.header.year, self.header.month, self.header.day), '%Y-%m-%d')
        return f"""
        File: {self.filename}
        Size; {self.filesize}
        Last Modified: {lastmodified}
        Records: {self.header.records}
"""
    
    def _init(self):
        """
        Initializes the database structure by reading the header and fields.
        """
        self.header = DbaseHeader()
        self.header.load_bytes(self.file.read(32))
        self.num_fields = (self.header.header_size - 32) // 32
        self.datasize = self.header.record_size * self.header.records
        for i in range(self.num_fields):
            field = DbaseField()
            field.load_bytes(self.file.read(32))
            if not field.name:
                break
            self.fields.append(field)
        assert(self.header.header_size + self.datasize == self.filesize)
        # self.file.seek(self.header.header_size)

    def write(self, filename=None):
        numdeleted = 0
        for record in self[:]:
            if record.get('deleted'):
                numdeleted += 1
        self.header.records -= numdeleted
        file = open('tmp.dbf', 'wb')
        file.write(self.header.to_bytes())
        for field in self.fields:
            file.write(field.to_bytes())
        file.write(b'\x0D')
        for record in self[:]:
            if record['deleted']:    
                # self.file.write(b'*')
                continue
            else:   
                file.write(b' ')
            for field in self.fields:
                ftype = chr(field.type)
                if ftype == 'C':
                    file.write(record[field.name.decode('latin1')].ljust(field.length, ' ').encode('latin1'))
                elif ftype == 'N' or ftype == 'F':
                    file.write(str(record[field.name.decode('latin1')]).rjust(field.length, ' ').encode('latin1'))   
                elif ftype == 'D':
                    file.write(record[field.name.decode('latin1')].strftime('%Y%m%d').encode('latin1'))
                elif ftype == 'L':
                    file.write(b'\x01' if record[field.name.decode('latin1')] else b'\x00')
                else:
                    raise ValueError(f"Unknown field type {field.type}")
        # file.write(b'\x1A')
        file.flush()
        self.file.close()
        if not filename:
            filename = self.filename
            os.remove(filename)
        self.filename = filename
        os.rename('tmp.dbf', self.filename)
        self.file = open(self.filename, 'r+b')
        self.num_fields = 0
        self.fields = []
        self.header = None
        self.datasize = 0
        self. _init()

    # def add_field(self, name, type, length, decimal=0):
    #     if len(self.records) > 0:
    #         raise ValueError("Cannot add field after records")
    #     if len(self.fields) > 0:
    #         address = self.fields[-1].address + self.fields[-1].length
    #     else:
    #         address = 1
    #     field = DbaseField(name, type, address, length, decimal)
    #     self.fields.append(field)
    #     self.header.header_size += 32

    def _test_key(self, key):
        """
        Tests if the key is within the valid range of record indexes.
        Raises an IndexError if the key is out of range.
        Meant for internal use only.
        """
        if 0 > key >= self.header.records:  
            raise IndexError("Record index out of range")

    def add_record(self, *data):
        """
        Adds a new record to the database.

        :param record_data: Dictionary with the new record's data.
        """
        if len(data) != len(self.fields):
            raise ValueError("Wrong number of fields")
        value = b''
        for field, val in zip(self.fields, data):
            ftype = chr(field.type).encode()
            if ftype == FieldType.CHARACTER.value:
                value += str(val).encode('latin1').ljust(field.length, b' ')
            elif ftype == FieldType.NUMERIC.value or ftype == FieldType.FLOAT.value:
                value += str(val).encode('latin1').rjust(field.length, b' ')
            elif ftype == FieldType.DATE.value:
                value += val.strftime('%Y%m%d').encode('latin1')
        # self.file.seek(self.header.header_size + self.header.record_size * self.header.records)
        self.file.seek(self.filesize)
        self.file.write(b'\x20' + value)
        self.header.records += 1
        self.filesize = self.header.header_size + self.header.record_size * self.header.records
        hoy = datetime.now()
        self.header.year = hoy.year - 1900
        self.header.month = hoy.month
        self.header.day = hoy.day
        self.datasize = self.header.record_size * self.header.records
        self.file.seek(0)
        self.file.write(self.header.to_bytes())        
        self.file.flush()

    def del_record(self, key, value = True):
        """
        Marks a record as deleted.
        To effectively delete the record, use the write() method afterwards.
        """
        self._test_key(key)
        record = self.get_record(key)
        record['deleted'] = value
        self.save_record(key, record)
        self.file.flush()

    def update_record(self, key, record):
        """
        Updates an existing record in the database.

        :param index: Index of the record to update.
        :param record_data: Dictionary with the updated data.
        :raises IndexError: If the record index is out of range.
        """
        self._test_key(key)
        record['deleted'] = False
        self.save_record(key, record)
        self.file.flush()

    def get_record(self, key):
        """
        Retrieves a record (dictionary with field names and field values) from the database.
        Used internally by the __getitem__ method.
        """
        self._test_key(key)
        self.file.seek(self.header.header_size + key * self.header.record_size)
        rec_bytes = self.file.read(self.header.record_size)
        if not len(rec_bytes):
            return None
        to_be_deleted = rec_bytes[0] == 0x2A
        rec_bytes = rec_bytes[1:]
        record = {'deleted': to_be_deleted}
        for field in self.fields:
            fieldtype = chr(field.type)
            fieldname = field.name.decode('latin1').strip("\0x00").strip()
            if fieldtype == 'C':
                record[fieldname] = rec_bytes[:field.length].decode('latin1').strip("\0x00").strip()
            elif fieldtype == 'N':
                record[fieldname] = int(rec_bytes[:field.length])
            elif fieldtype == 'F':
                record[fieldname] = float(rec_bytes[:field.length])
            elif fieldtype == 'D':
                record[fieldname] = datetime.strptime(rec_bytes[:field.length].decode('latin1'), '%Y%m%d')
            elif fieldtype == 'L':
                record[fieldname] = not not rec_bytes[:field.length]
            else:
                raise ValueError(f"Unknown field type {fieldtype}")
            rec_bytes = rec_bytes[field.length:]
        return record
    
    def get_field(self, fieldname):
        """
        Returns the field object with the specified name.
        """
        for field in self.fields:
            if field.name.decode('latin1').strip().lower() == fieldname.strip().lower():
                return field
        return None

    def search(self, fieldname, value, start=0, funcname="", comp_func=None):
        """
        Searches for a record with the specified value in the specified field,
        starting from the specified index, for which the specified comparison function returns True.
        """
        if funcname not in ("find", "index", ""):
            raise ValueError("Invalid function name") 
        field = self.get_field(fieldname)
        if not field:
            raise ValueError(f"Field {fieldname} not found")
        elif fieldname != field.name.decode('latin1').strip():
            fieldname = field.name.decode('latin1').strip()
        fieldtype = chr(field.type).encode()
        if not comp_func:
            if fieldtype == FieldType.CHARACTER.value:
                # comp_func = lambda f, v: f.lower().startswith(v.lower())
                comp_func = self.istartswith
            elif fieldtype == FieldType.NUMERIC.value or fieldtype == FieldType.FLOAT.value:
                comp_func = lambda f, v: f == v 
            elif fieldtype == FieldType.DATE.value:
                comp_func = lambda f, v: f == v
            else:
                raise ValueError(f"Invalid field type {fieldtype} for comparison")
            
        for i, record in enumerate(self[start:]):
            if comp_func(record[fieldname], value):
                if funcname == "":
                    return i + start, record
                elif funcname == "find":
                    return record
                elif funcname == "index":
                    return i + start
        if funcname == "":
            return -1, None
        elif funcname == "find":
            return None
        elif funcname == "index":
            return -1

    def find(self, fieldname, value, start=0, comp_func=None): 
        """
        Wrapper for search() with funcname="find".
        Returns the first record (dictionary) found, or None if no record meeting given criteria is found.
        """ 
        return self.search(fieldname, value, start, "find", comp_func)
    
    def index(self, fieldname, value, start=0, comp_func=None):
        """
        Wrapper for search() with funcname="index".
        Returns index of the first record found, or -1 if no record meeting given criteria is found.
        """ 
        return self.search(fieldname, value, start, "index", comp_func)

    def filter(self, fieldname, value, comp_func=None):
        """
        Returns a list of records (dictionaries) that meet the specified criteria.
        """
        ret = []
        index = -1
        while True:
            index, record = self.search(fieldname, value, index + 1, "", comp_func)  
            if index < 0:
                return ret
            else:    
                ret.append(record)

    def list(self, start=0, stop=None, fieldsep="|", recordsep='\n', records:list=None):
        """
        Returns a list of records from the database.
        """
        if start is None:
            start = 0
        if stop is None:
            stop = self.header.records
        l = records or [self.get_record(i) for i in range(start, stop)]
        return recordsep.join(fieldsep.join(str(record[field.name.decode('latin1')]) for field in self.fields) for record in l)

    def csv(self, start=0, stop=None, records:list = None):
        """
        Returns a CSV string with the records in the database.
        """
        return self.list(start, stop, ",", "\n", records)
    
    def table(self, start=0, stop=None, records:list = None):
        """
        Returns a table string with the records in the database.
        """
        def _format_field(field, record):
            if field.type == ord(FieldType.CHARACTER.value):
                return record.get(field.name.decode('latin1')).ljust(field.length + 2)
            else: 
                return str(record.get(field.name.decode('latin1'))).rjust(field.length + 2)
            
        if start is None:
            start = 0
        if stop is None:
            stop = self.header.records
        l = records or [self.get_record(i) for i in range(start, stop)]
        line_bracket = "+"
        line_divider = line_bracket + line_bracket.join("-" * (field.length + 2) for field in self.fields) + line_bracket + "\n"
        header_line = "|" + "|".join(field.name.decode('latin1').center(field.length + 2) for field in self.fields) + "|" + "\n"
        record_lines =  ('\n' + line_divider).join("|" + "|".join(_format_field(field, record) for field in self.fields) + "|" for record in l)
        return line_divider + header_line + line_divider + record_lines + "\n" + line_divider
    
    def save_record(self, key, record):
        """
        Writes a record (dictionary with field names and field values) to the database
        at the specified index.
        """
        self._test_key(key)
        self.file.seek(self.header.header_size + key * self.header.record_size)
        if record.get('deleted'):
            self.file.write(b'*')
        else:
            self.file.write(b' ')
        for field in self.fields:
            ftype = chr(field.type)
            if ftype == 'C':
                self.file.write(record[field.name.decode('latin1')].ljust(field.length, ' ').encode('latin1'))
            elif ftype == 'N' or ftype == 'F':
                self.file.write(str(record[field.name.decode('latin1')]).rjust(field.length, ' ').encode('latin1'))
            elif ftype == 'D':
                self.file.write(record[field.name.decode('latin1')].strftime('%Y%m%d').encode('latin1'))
            elif ftype == 'L':
                self.file.write(b'\x01' if record[field.name.decode('latin1')] else b'\x00')
            else:
                raise ValueError(f"Unknown field type {field.type}")

    def exec(self, sql_cmd: str):
        """
        Executes a SQL command on the database.
        """
        raise NotImplementedError("SQL commands are not supported as yet.")

def testdb():
    global test
    
    if os.path.exists('test.dbf'):
        # os.remove('db/test.dbf')
        test = DbaseFile('test.dbf')
        # test.add_record('River Plate', 2024 - 1901)
    else:
        test = DbaseFile.create('test.dbf',
                            [('name', FieldType.CHARACTER.value, 50, 0),
                             ('age', FieldType.NUMERIC.value, 3, 0)])
        test.add_record('John Doe', 30)
        test.add_record('Jane Doe', 25)

    print(test)
    print()

if __name__ == '__main__':
    testdb()  
