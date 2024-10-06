#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from pydal import DAL, Field
from datetime import datetime


class DBEngine:
    DB_PATH: str = ""
    db: DAL = None

    @classmethod
    def init_db(cls):
        cls.db = DAL(f'sqlite://{cls.DB_PATH}')

    @classmethod
    def init_tables(cls):
        try:
            cls.db.define_table(
                'users',
                Field('atype', 'integer', default=0),  # 0: ADSL, 1: 4G LTE, 2: Phone
                Field('username', 'string', length=32, required=True),
                Field('password', 'string', length=32),  # Just for '0' atype
                Field('dname', 'string', length=32),
                Field('data', 'json'),  # Dictionary-like structure
                Field('cookies', 'json'),  # Just for '0' atype
                Field('created', 'datetime', default=datetime.now()),  # Current datetime
            )
            cls.db.commit()
        except sqlite3.OperationalError:
            pass