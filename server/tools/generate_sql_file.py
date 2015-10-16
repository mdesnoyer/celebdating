#!/usr/bin/env python

import os.path
import sys
__base_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys.path[0] != __base_path__:
    sys.path.insert(0, __base_path__)

#import _mysql 
import MySQLdb as mdb
def main():
    try:
        con = mdb.connect('dateaceleb.cnvazyzlgq2v.us-east-1.rds.amazonaws.com', 'admin', 'admin123', 'celebs')
        celebs = open('./celebs.csv', 'r')
        relationships = open('./relationships.csv', 'r')
        rows_inserted = 0
        print 'Inserting:'
        with con:
            cur = con.cursor()
            for line in celebs:
                celeb_info = line.split(',')
                query_str = "INSERT INTO celebrities (name, gender, age) VALUES('%s', %d, %d)" % (celeb_info[0], int(celeb_info[1]), int(celeb_info[2]))
                cur.execute(query_str)
                rows_inserted += 1
                print '.',
            for line in relationships:
                main_celeb_row = None
                dated_row = None
                relationship_info = line.split(',')
                print '.',
                query_str = "SELECT celebrity_id FROM celebrities WHERE LOWER(name) = LOWER('%s')" % (relationship_info[0])
                cur.execute(query_str)
                if cur.rowcount > 0:
                    main_celeb_row = cur.fetchone()
                query_str = "SELECT celebrity_id FROM celebrities WHERE LOWER(name) = LOWER('%s')" % (relationship_info[1].rstrip())
                cur.execute(query_str)
                if cur.rowcount > 0:
                    dated_row = cur.fetchone()
                if dated_row and main_celeb_row:
                    query_str = "INSERT INTO dated VALUES(%d, %d)" % (main_celeb_row[0], dated_row[0])
                    cur.execute(query_str)
                    rows_inserted += 1
    except _mysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()
        print 'We inserted %d rows to our celebs database' % (rows_inserted)

if __name__ == "__main__":
    main()
