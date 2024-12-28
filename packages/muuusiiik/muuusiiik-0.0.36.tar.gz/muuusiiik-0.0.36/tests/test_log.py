import muuusiiik.util as msk
from   pytest import raises


def test_there_is_a_log_file_when_set_filename():
    path   = 'tests/_data'
    f_log  = 'demo.log'
    f      = f'{path}/{f_log}'
    # make sure the path does not exist
    msk.data.rm(path)
    # make sure there is a folder
    assert msk.data.exist(path) == False
    msk.data.make_path(path, pathtype='folder')
    assert msk.data.exist(path) == True
    # make logger
    logger = msk.log.GetLogger(filename=f)
    logger.debug('hello')
    # check the log file is created
    assert msk.data.exist(f) == True
    # reset content
    msk.data.rm(path)
    assert msk.data.exist(f) == False


def test_there_is_a_log_file_when_set_filename_even_the_path_does_not_exist():
    path   = 'tests/_data'
    f_log  = 'demo.log'
    f      = f'{path}/{f_log}'
    # make sure the path does not exist
    msk.data.rm(path)
    assert msk.data.exist(path) == False
    # make logger
    logger = msk.log.GetLogger(filename=f)
    logger.debug('hello')
    # check the log file is created
    assert msk.data.exist(f) == True
    # reset content
    msk.data.rm(path)
    assert msk.data.exist(f) == False


def test_there_is_2_handlers_as_setting():
    path   = 'tests/_data'
    f_log  = 'tests/_data/demo.log'
    logger = msk.log.GetLogger()
    hand   = msk.log.GetHandler(filename=f_log)
    logger.addHandler(hand)
    assert len(logger.handlers) == 2
    # reset content
    msk.data.rm(path)
    assert msk.data.exist(f_log) == False


def test_logger_is_cleared_properly():
    name = 'demo_logger'
    # init root logger
    logger = msk.log.GetLogger(name)
    assert logger.name          == name
    assert len(logger.handlers) == 1
    # adding an extra handler
    hand   = msk.log.GetHandler()
    assert logger.name          == name
    logger.addHandler(hand)
    assert len(logger.handlers) == 2
    # clear logger
    msk.log.clear_by_name(name)
    assert logger.name          == name
    assert len(logger.handlers) == 0


def test_having_handler_only_one_even_init_it_twice():
    path   = 'tests/_data'
    f_log  = 'tests/_data/demo.log'
    # batch no.1
    logger = msk.log.GetLogger()
    hand   = msk.log.GetHandler(filename=f_log)
    logger.addHandler(hand)
    # batch no.2
    logger = msk.log.GetLogger()
    hand   = msk.log.GetHandler(filename=f_log)
    logger.addHandler(hand)
    # logger should not have 4 handlers
    assert len(logger.handlers) == 2
    # reset content
    msk.data.rm(path)
    assert msk.data.exist(f_log) == False


def test_formatter_validation():
    # general use
    formatter = 'nothing'
    assert msk.log._validate_formatter(formatter) == 'nothing'
    formatter = 'minimal'
    assert msk.log._validate_formatter(formatter) == 'minimal'

    # formatter is None
    formatter = None
    assert msk.log._validate_formatter(formatter) == 'minimal'
    # upper case
    formatter = 'NOTHING'
    assert msk.log._validate_formatter(formatter) == 'nothing'
    # not supporting value -> nothing
    formatter = 'non-exsisting'
    assert msk.log._validate_formatter(formatter) == 'nothing'


def test_when_validation():
    # daily and weekly
    when = 'daily'
    assert msk.log._validate_when(when) == 'midnight'
    when = 'weekly'
    assert msk.log._validate_when(when) == 'W0'

    # when is None
    when = None
    assert msk.log._validate_when(when) == when
    # when is any
    when = 'something-else'
    assert msk.log._validate_when(when) == when
