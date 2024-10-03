#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import os.path
from lib.views.app import Application
from lib.models.base import DBEngine


def base_dir(*files):
    return os.path.join(os.path.dirname(__file__), *files)


if __name__ == "__main__":
    DBEngine.DB_PATH = base_dir("assets", "data.db")
    DBEngine.init_db()
    DBEngine.init_tables()

    ft.app(
        target=Application(),
        name="رصيد يمن نت"
    )