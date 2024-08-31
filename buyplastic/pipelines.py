import pymysql


class BuyplasticPipeline:
    def open_spider(self, spider):
        # Connect to the MySQL database
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='actowiz',
            database='buy_plastic',
            autocommit=True
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                price DECIMAL(10, 2),
                url TEXT
            )
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        try:
            # Insert item data into the table, ignoring duplicate entries
            self.cursor.execute('''
                INSERT IGNORE INTO products (name, price, url) VALUES (%s, %s, %s)
            ''', (item.get('name'), item.get('price'), item.get('url')))
            self.conn.commit()
        except pymysql.MySQLError as e:
            spider.logger.error(f"Failed to insert item: {e}")
        return item
