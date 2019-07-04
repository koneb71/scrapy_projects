import itertools
import MySQLdb

from gamecollection_com.settings import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB


def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD,
                                    MYSQL_DB, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        chunks_data = list(split_seq(self.data, 50))
        for chunk in chunks_data:
            try:
                self.cursor.executemany(
                    """ 
                    INSERT INTO xGamecollection 
                        (`Master_URL`, `URL`, `Name`, `Image`, `Price`, `new_or_old`, `Stock`, `Data`)       
                    VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, chunk)
                self.conn.commit()
            except MySQLdb.Error as e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
        self.conn.close()

    def process_item(self, item, spider):
        self.data.append(tuple((
            item.get('Master_URL', '').encode('utf-8'),
            item.get('URL', '').encode('utf-8'),
            item.get('Name', '').encode('utf-8'),
            item.get('Image', '').encode('utf-8'),
            item.get('Price', '').encode('utf-8'),
            item.get('New_or_old', '').encode('utf-8') if item.get('New_or_old') else '',
            item.get('Stock', '').encode('utf-8'),
            item.get('Data_Large', '').encode('utf-8'),
        )))
        return item
