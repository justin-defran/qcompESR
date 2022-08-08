# Created by Gurudev Dutt <gdutt@pitt.edu> on 2020-07-28
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from pathlib import Path
import functools, logging, random, subprocess
import os, inspect, datetime
import psycopg2 as pg2
import numpy as np
from SQLInterface.decorators import decorator_insert, decorator_extract, decorator_table_insert
from SQLInterface.utils import get_bin
import psycopg2
from abc import ABC, abstractmethod
from SQLInterface.SQL_abstract import SQL_abstract

def generate_name():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    now = (datetime.datetime.now()).strftime("%H-%M-%S")
    name = str(today) + '-' + str(now)

    return name

def list_to_np(inlist):

    out = np.zeros(len(inlist))

    for i in range(0,len(inlist)):
        out[i] = float(inlist[i])

    return out


class Data:
    '''
    Empty class makes data readout convenient
    '''
    def __init__(self):
        pass


class SQL_object(SQL_abstract):
    """
    This class interacts with the SQL DB, uploads to the DB, creates tables
    in the DB, and extracts information from the DB.
    This is written based on the Query/Content model, in this model we have
    special functions for each type of data file that return a customized
    query and params to be uploaded. This is decorated with the appropriate
    decorator that establishes the connection to the DB, performs the functions,
    and closes the connection.

    The class specific for quantum pulse experiments.
    """

    def __init__(self):
        super().__init__()
        self.data_id = generate_name()
        self.TABLE_NAME = 'cwesr'

    @decorator_table_insert
    def create_table(self):
        query = """
             CREATE TABLE """ + self.TABLE_NAME + """( key SERIAL PRIMARY KEY, 
             data_id VARCHAR(200),
             startFreq NUMERIC,
             stopFreq NUMERIC,
             NumOfSteps NUMERIC,
             DwellTime NUMERIC,
             NumOfAvgs NUMERIC,
             PowerSyn NUMERIC,
             PowerAmp NUMERIC,
             PowerOutput NUMERIC,
             AttPower NUMERIC,
             LaserWavelength NUMERIC,
             LaserPower NUMERIC,
             FreqAtDip NUMERIC,
             x_arr BYTEA,
             data BYTEA,
             time_stamp TIMESTAMP);
            """
        return query

    @decorator_insert
    def insert(self, startFreq, stopFreq, NumOfSteps, DwellTime, NumOfAvgs, PowerSyn, PowerAmp, PowerOutput, AttPower, LaserWavelength, LaserPower, FreqAtDip, x_arr, data):

        query = 'INSERT INTO ' + self.TABLE_NAME + '(data_id, startFreq, stopFreq, NumOfSteps, DwellTime, NumOfAvgs, PowerSyn, PowerAmp, PowerOutput, AttPower, LaserWavelength, LaserPower, FreqAtDip, x_arr, data, time_stamp) ' \
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);'

        content = (self.data_id, startFreq, stopFreq, NumOfSteps, DwellTime, NumOfAvgs, PowerSyn, PowerAmp, PowerOutput, AttPower, LaserWavelength, LaserPower, FreqAtDip, psycopg2.Binary(x_arr.tobytes()), psycopg2.Binary(data.tobytes()))
        return (query,content)

    @decorator_extract
    def extract(self, data_id=None, key=None, startFreq=None, stopFreq=None, NumOfSteps=None, DwellTime=None, NumOfAvgs=None, PowerSyn=None, PowerAmp=None, PowerOutput=None, AttPower=None, LaserWavelength=None, LaserPower=None, FreqAtDip=None):

        """
                This function is used to extract data from the SQL DB.
                :param: Takes inputs of what you want to search.
                :type: string,list
                :rtype: list
                :return: returns data object.
                |
        """

        if (data_id != None):
            default = data_id + '%'
        else:
            default = None
        content = []
        input = [default, startFreq, stopFreq, NumOfSteps, DwellTime, NumOfAvgs, PowerSyn, PowerAmp, PowerOutput, AttPower, LaserWavelength, LaserPower, FreqAtDip]

        input_strings = [" data_id LIKE %s", " and key = %s", " and startFreq = %s", " and stopFreq = %s", " and DwellTime = %s", " and NumOfAvgs = %s", " and PowerSyn = %s", " and PowerAmp = %s", " and PowerOutput = %s", " and AttPower = %s", " and LaserWavelength = %s", " and LaserPower = %s", " and FreqAtDip = %s"]
        query = 'SELECT * FROM ' + self.TABLE_NAME + ' WHERE'
        val = True
        for i, j in enumerate(input):

            if (j != None):
                if (input[0] == None and val == True):
                    query = query + input_strings[i][4:]
                    content.append(j)
                    val = False
                    continue
                content.append(j)
                query = query + input_strings[i]

        return (query, content)

    def format(self, raw):
        '''
        Raw is the output of the psycopg2 query, a list of lists of lists etc...
        '''
        data = Data()

        data.key = [row[0] for row in raw]
        data.data_id = [row[1] for row in raw]
        data.startFreq = [row[2] for row in raw]
        data.stopFreq = [row[3] for row in raw]
        data.NumOfSteps = [row[4] for row in raw]
        data.DwellTime = [row[5] for row in raw]
        data.NumOfAvgs = [row[6] for row in raw]
        data.PowerSyn = [row[7] for row in raw]
        data.PowerAmp = [row[8] for row in raw]
        data.PowerOutput = [row[9] for row in raw]
        data.AttPower = [row[10] for row in raw]
        data.LaserWavelength = [row[11] for row in raw]
        data.LaserPower = [row[12] for row in raw]
        data.FreqAtDip = [row[13] for row in raw]
        data.x_arr = [np.frombuffer(row[14], dtype=np.int32) for row in raw]
        data.data = [np.frombuffer(row[15], dtype=np.float64) for row in raw]

        return data

    def load(self, **kwargs):
        '''
        Access the data here. Note that extract is defined to have a decorator. After completing the extract method and
        the decorator function, the result is passed through format for final adjustments.

        Kwargs are the searchable parameters.
        '''
        return self.format(self.extract(**kwargs))

    def backup(self):
        folder = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        # onedrivepath = "/Users/bmesi/Desktop/Onedrive/OneDrive - University of Pittsburgh/Duttlab/QuantumPulse/"+folder
        filepath = '"'+onedrivepath + "/backup.sql"+'"'
        if not(os.path.exists(onedrivepath)):
            os.makedirs(onedrivepath)

        try:
            subprocess.run('pg_dump -U postgres quantumpulse > ' + filepath,shell = True)
        except:
            print("Terminal Error")

if __name__ == '__main__':

    SQL = SQL_object()
    SQL.create_table()