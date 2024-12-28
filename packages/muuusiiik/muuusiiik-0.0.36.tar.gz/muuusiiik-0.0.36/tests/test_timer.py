import muuusiiik.util as msk
import time

def test_timer_run_when_init():
    """ round time() to int for approximation """
    now = int( time.time() )
    t   = msk.timer()
    tik = int( t._start )
    assert tik == now


def test_timer_run_when_reset():
    """ round time() to int for approximation """
    now = int( time.time() )
    t   = msk.timer()
    t.reset()
    tik = int( t._start )
    assert tik == now


def test_time_function_by_given_duration_in_second():
    t      = msk.timer()
    result = t.time(305)
    assert result == '00:05:05'


def test_taketime_function_for_being_called_by_the_class():
    result = msk.timer.taketime(305)
    assert result == '00:05:05'



