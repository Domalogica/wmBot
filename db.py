#!/usr/bin/env python
# coding=utf-8

import pymysql, sys
from collections import OrderedDict

class MysqlPython(object):

    __instance   = None
    __host       = None
    __user       = None
    __password   = None
    __database   = None
    __session    = None
    __connection = None

    def __init__(self, host='194.67.204.153', user='root', password='', database='', charset='utf8'):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__database = database
        self.__charset = charset

    def __open(self):
        try:
            cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database, charset=self.__charset)
            self.__connection = cnx
            self.__session    = cnx.cursor()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0],e.args[1]))

    def __close(self):
        self.__session.close()
        self.__connection.close()

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        try:
            number_columns = len(self.__session.description)
        except Exception as e:
            number_columns = 0

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result

    def update(self, table, where=None, *args, **kwargs):
        query  = "UPDATE %s SET " % table
        keys   = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        update_rows = self.__session.rowcount
        self.__close()

        return update_rows

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) %  tuple (keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid

    def delete(self, table: object, where: object = None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s ' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows

    def delete_branch(self, telegram):
        query = "DELETE FROM branches WHERE id = ( SELECT maxo FROM ( SELECT MAX(id) AS maxo FROM branches WHERE telegram = %i) AS tmp)" % telegram
        self.__open()
        self.__session.execute(query)
        self.__connection.commit()

        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows

    def select_advanced(self, sql, *args):
        od = OrderedDict(args)
        query  = sql
        values = tuple(od.values())
        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]

        self.__close()
        return result


connect_mysql = MysqlPython('127.0.0.1', 'root', '7087', 'wm_bot')


#select
# conditional_query = "telegram = %s"
# result = connect_mysql.select("branches", conditional_query, *["branch"], **{'telegram': 1})
# print(result)

#update
# conditional_query = 'id = %s'
# result = connect_mysql.update('report', conditional_query, *["245919343"], **{'morning': "Hi, name is Ahmad"})
# print(result)

# delete
# conditional_query = 'telegram = %s'
# result = connect_mysql.delete('branches', conditional_query, *["1"])
# print(result)

#insert
# result = connect_mysql.insert('report', *["id", "morning"], **{'id': "245919343", 'morning': "Hello World!"})
# print(result)


