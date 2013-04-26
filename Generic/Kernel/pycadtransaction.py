#@+leo-ver=5-thin
#@+node:1.20130426141258.2764: * @file pycadtransaction.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:1.20130426141258.2765: ** class Transaction
class Transaction(object):
    #@+others
    #@+node:1.20130426141258.2766: *3* __init__
    def __init__(self, connection):
        
        self._connection = connection
        self._cursor = self._connection.cursor()
    #@+node:1.20130426141258.2767: *3* _GetCursor
    def _GetCursor(self):
        return self._cursor
    #@+node:1.20130426141258.2768: *3* Close
    Cursor = property(_GetCursor, None, None, "gets the cursor")


    def Close(self, commit):
        
        if commit == True:
            # commit transaction
            self._connection.commit()
        else:
            # abort transaction
            self._connection.abort()
        # close cursor
        self._cursor.close()
    #@-others
#@-others
#@-leo
