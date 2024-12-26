#!/usr/bin/env python3
#-*- coding: utf_8 -*-

class ExcelFile:
    def __init__(self, filename):
        self.filename = filename

    def open(self):
        print("Opening Excel 97/2003 file: ", self.filename)

    def close(self):
        print("Closing Excel 97/2003 file: ", self.filename)

    def save(self):
        print("Saving Excel 97/2003 file: ", self.filename)

    def save_as(self, new_filename):
        print("Saving Excel 97/2003 file as: ", new_filename)

    def __str__(self):
        return "Excel 97/2003 file: " + self.filename

def test():
    print("Welcome to Excel 97/2003")

if __name__ == '__main__':
    test()
