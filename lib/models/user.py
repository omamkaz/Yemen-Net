#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .base import DBEngine


class User:

    @staticmethod
    def get_users():
        return DBEngine.db().select(DBEngine.db.users.ALL)

    @staticmethod
    def add_user(
        atype: int,
        username: str, 
        password: str = None, 
        dname: str = None,
        data: dict[str, str] = None, 
        cookies: dict[str, str] = None):

        user_id = DBEngine.db.users.insert(
            atype=atype,
            username=username,
            password=password,
            dname=dname,
            data=data,
            cookies=cookies
        )
        DBEngine.db.commit()
        return user_id

    @staticmethod
    def edit_user(
        user_id: int, 
        atype: int, 
        username: str, 
        password: str, 
        dname: str) -> None:

        user = DBEngine.db(DBEngine.db.users.id == user_id).select().first()

        if user:
            user.dname = dname

            if (user.atype != atype or
                user.username != username or
                user.password != password):

                user.atype = atype
                user.username = username
                user.password = None if atype != 0 else (password or "123456")

                user.data = None
                user.cookies = None

            # Commit changes
            DBEngine.db(DBEngine.db.users.id == user_id).update(**user.as_dict())
            DBEngine.db.commit()

    @staticmethod
    def edit_data_and_cookies( 
        user_id: int,
        data: dict[str, str] = None,
        cookies: dict[str, str] = None):

        if (user := DBEngine.db(DBEngine.db.users.id == user_id).select().first()):
            user.data = data
            user.cookies = cookies

            DBEngine.db(DBEngine.db.users.id == user_id).update(**user.as_dict())
            DBEngine.db.commit()

    @staticmethod
    def get_user(user_id: int):
        return DBEngine.db(DBEngine.db.users.id == user_id).select().first()

    @staticmethod
    def delete_user(user_id: int):
        DBEngine.db(DBEngine.db.users.id == user_id).delete()
        DBEngine.db.commit()
