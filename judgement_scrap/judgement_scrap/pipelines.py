# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class JudgementScrapPipeline:
    def process_item(self, item, spider):
        return item


class SaveToDBpipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123",
            database="judge"
        )
        
        # Cursor is for running the SQL command
        self.cur = self.conn.cursor()
        
        # The SQL which creates the table if there is none
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS judgementDATA (
            id INT NOT NULL AUTO_INCREMENT,
            title TEXT,
            all_data MEDIUMTEXT,
            PRIMARY KEY (id)
        )
        """)
    
    def process_item(self, item, spider):  # Fixed method name from process_items to process_item
        # Insert into the judgementDATA
        self.cur.execute("""
        INSERT INTO judgementDATA (
            title, 
            all_data
        ) VALUES (%s, %s)""", 
        (
            item["title"],
            item["all_data"]
        ))
        
        self.conn.commit()
        return item  # Make sure to return the item
    
    def close_spider(self, spider):
        # Closing the cursor and the connection
        self.cur.close()
        self.conn.close()