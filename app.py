#!/usr/bin/env python3

import sqlite3
import logging
from os import path, mkdir
from json import load


class Application:
    def __init__(self):
        self.env = self.__init_environment()
        self.__init_logger()

        if not self.db_exists():
            self.__init_database()

        self.conn = sqlite3.connect(
            path.join(
                self.env["path"]["directory"]["project"],
                self.env["path"]["directory"]["database"],
                self.env["path"]["file"]["database"],
            )
        )

    def __init_environment(self) -> dict:
        with open("./config/env.json", "r") as env_file:
            env = load(env_file)
            env["path"]["directory"]["project"] = path.dirname(__file__)
            return env

    def __init_database(self):
        conn = sqlite3.connect(
            path.join(
                self.env["path"]["directory"]["project"],
                self.env["path"]["directory"]["database"],
                self.env["path"]["file"]["database"],
            )
        )
        logging.info("Database created successfully")

        with open(
            path.join(
                self.env["path"]["directory"]["project"],
                self.env["path"]["directory"]["scripts"],
                self.env["path"]["file"]["database_initializer"],
            ),
            "r",
        ) as sql_script:
            conn.executescript(sql_script.read())

        logging.info("Tables created successfully")
        conn.close()

    def __init_logger(self):
        if not path.exists(
            path.join(
                self.env["path"]["directory"]["project"],
                self.env["path"]["directory"]["logs"],
            )
        ):
            mkdir(
                path.join(
                    self.env["path"]["directory"]["project"],
                    self.env["path"]["directory"]["logs"],
                )
            )

        logging.basicConfig(
            filename=path.join(
                self.env["path"]["directory"]["project"],
                self.env["path"]["directory"]["logs"],
                self.env["path"]["file"]["log"],
            ),
            filemode="w",
            format="%(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

    def db_exists(self) -> bool:
        if path.exists(
            path.join(
                self.env["path"]["directory"]["project"],
                self.env["path"]["directory"]["database"],
                self.env["path"]["file"]["database"],
            )
        ):
            logging.info("Database exists")
            return True
        else:
            logging.warning("Database does not exist")
            return False


if __name__ == "__main__":
    Application()
