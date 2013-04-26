#@+leo-ver=5-thin
#@+node:1.20130426141258.2950: * @file basedb.py
#encoding: utf-8
#
# Copyright (c) 2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This  module provide access to the basic operation on pythoncad database
#



#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:1.20130426141258.2951: ** <<declarations>> (basedb)
import os
import sys
import tempfile
import sqlite3 as sql

from Kernel.exception import *
#@-<<declarations>>
#@+others
#@+node:1.20130426141258.2952: ** class BaseDb
class BaseDb(object):
    """
        this class provide base db operation
    """
    commit=True
    #@+others
    #@+node:1.20130426141258.2953: *3* __init__
    def __init__(self):
        self.__dbConnection=None
        self.dbPath=None
    #@+node:1.20130426141258.2954: *3* createConnection
    def createConnection(self,dbPath=None):
        """
            create the connection with the database
        """
        if dbPath is None:
            f=tempfile.NamedTemporaryFile(prefix='PyCad_', suffix='.pdr')
            dbPath=f.name
            f.close()
        self.__dbConnection = sql.connect(str(dbPath))
        self.dbPath=dbPath
    #@+node:1.20130426141258.2955: *3* setConnection
    def setConnection(self,dbConnection):
        """
            set the connection with the database
        """
        if not self.__dbConnection is None:
            # Todo fire a warning
            self.__dbConnection.close()
        self.__dbConnection=dbConnection
    #@+node:1.20130426141258.2956: *3* getConnection
    def getConnection(self):
        """
            Get The active connection
        """
        return self.__dbConnection
    #@+node:1.20130426141258.2957: *3* makeSelect
    def makeSelect(self,statment):
        """
            perform a select operation
        """
        try:
            _cursor = self.__dbConnection.cursor()
            _rows = _cursor.execute(statment)
        except sql.Error as _e:
            msg="Sql Phrase: %s"%str(statment)+"\nSql Error: %s"%str( _e.args[0] )
            raise StructuralError(msg)
        except :
            for s in sys.exc_info():
                print("Generic Error: %s"%str(s))
            raise StructuralError
        #_cursor.close()
        return _rows
    #@+node:1.20130426141258.2958: *3* fetchOneRow
    def fetchOneRow(self,sqlSelect, tupleArgs=None):
        """
            get the first row of the select
        """
        try:
            _cursor = self.__dbConnection.cursor()
            if tupleArgs:
                _rows = _cursor.execute(sqlSelect,tupleArgs )
            else:
                _rows = _cursor.execute(sqlSelect)
        except sql.Error as _e:
            msg="Sql Phrase: %s"%str(sqlSelect)+"\nSql Error: %s"%str( _e.args[0] )
            raise StructuralError(msg)
        except :
            for s in sys.exc_info():
                print("Generic Error: %s"%str(s))
            raise StructuralError
        _row=_rows.fetchone()
        _cursor.close()
        if _row is None or _row[0] is None:
            return None
        return _row[0]
    #@+node:1.20130426141258.2959: *3* makeUpdateInsert
    def makeUpdateInsert(self,statment, tupleArgs=None):
        """
            make an update Inster operation
        """
        #print "qui1 : sql ",statment
        try:
            _cursor = self.__dbConnection.cursor()
            if tupleArgs:
                _rows = _cursor.execute(statment,tupleArgs )
            else:
                _rows = _cursor.execute(statment)
            #if self.__commit:
            if BaseDb.commit:
                self.performCommit()
                _cursor.close()
        except sql.Error as _e:
            msg="Sql Phrase: %s"%str(statment)+"\nSql Error: %s"%str( _e.args[0] )
            raise sql.Error(msg)
        except :
            for s in sys.exc_info():
                print("Generic Error: %s"%str(s))
            raise KeyError
    #@+node:1.20130426141258.2960: *3* close
    def close(self):
        """
            close the database connection
        """
        self.__dbConnection.close()
    #@+node:1.20130426141258.2961: *3* suspendCommit
    def suspendCommit(self):
        """
            suspend the commit in the update\insert
        """
        #self.__commit=False
        BaseDb.commit=False
    #@+node:1.20130426141258.2962: *3* reactiveCommit
    def reactiveCommit(self):
        """
            reactive the commit in the update\insert
        """
        #self.__commit=True
        BaseDb.commit=True
    #@+node:1.20130426141258.2963: *3* performCommit
    def performCommit(self):
        """
            perform a commit
        """
        try:
            self.__dbConnection.commit()
        except:
            print("Error on commit")
    #@-others
#@-others
#@-leo
