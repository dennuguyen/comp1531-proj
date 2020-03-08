#Raymond: user.py helper functions

import message
import auth
import channels


def get_new_user1():
    email = 'z1111111@unsw.cedu.au'
    password = 'qwert111'
    name_first = 'James'
    name_last = 'Bond'

    return email, password, name_first, name_last


def get_new_user2():
    email = 'z1111111@unsw.edu.au'
    password = 'qwert111'
    name_first = 'John'
    name_last = 'Wick'

    return email, password, name_first, name_last
