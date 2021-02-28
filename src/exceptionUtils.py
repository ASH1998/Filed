
class Error(Exception):
    '''
    Base Class for other Exceptions
    '''
    pass

class NotEnoughValues(Error):
    '''
    Raised when number of values are not enough or more than required.
    '''
    pass

class ConstraintError(Error):
    '''
    Raised when error with constraints provided.
    '''
    pass

class DBError(Error):
    '''
    Raised in case of DB inconsistency
    '''
    # print("DB connection failed, check config.json")
    pass

class BadRequest(Error):
    """
    Raised when request doesnt have correct or enough values.
    """
    pass

class AudioTypeDoesNotExist(Error):
    '''
    Raised incase of wrong audio type.
    '''
    pass

class ShutDownAudioServer(Error):
    '''
    Incase a shutdown is needed.
    '''
    pass