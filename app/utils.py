# -*- coding: utf-8 -*-

import string
import random
import os
import io
import tarfile
import time

from datetime import datetime

def get_current_time():
    return datetime.utcnow()

def user_is_authenticated(user):
    if user is None:
        return False

    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated
