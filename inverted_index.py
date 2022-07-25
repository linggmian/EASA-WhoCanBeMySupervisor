import sqlite3
from sqlite3 import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def main():
    db_file = './static/db/expert.db'
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute("DELETE FROM Inverted_index")

        # count the number of publications within the publication database
        count_sql = 'SELECT COUNT(*) FROM Publication;'
        c.execute(count_sql)
        number_of_rows = c.fetchall()
        number_of_rows = number_of_rows[-1][-1]
        print(number_of_rows)

        # create inverted_index from author keywords
        for i in range(number_of_rows):
            current_id = i+1
            current_id = str(current_id)
            query_sql = "SELECT `Author Keywords` FROM Publication WHERE PublicationID =? "
            c.execute(query_sql, [current_id])
            rows = c.fetchall()
            for j in rows:
                strings = j[0]
                print(strings)
                if strings is None:
                    continue
                else:
                    split = strings.split(";")
                    print(split)
                    length = len(split)
                    for k in range(length):
                        # remove blank space
                        keyword = split[k].strip()
                        insert_values = (keyword, current_id, 'Yes')
                        insert_sql = "INSERT INTO Inverted_index(Term, PublicationID, AuthorKeyword) VALUES (?,?,?)"
                        c.execute(insert_sql, insert_values)

            # create inverted_index from index keywords
            query_sql2 = "SELECT `Index Keywords` FROM Publication WHERE PublicationID =? "
            c.execute(query_sql2, [current_id])
            rows = c.fetchall()
            for j in rows:
                strings = j[0]
                print(strings)
                if strings is None:
                    continue
                else:
                    split = strings.split(";")
                    print(split)
                    length = len(split)
                    for k in range(length):
                        keyword = split[k].strip()
                        insert_values = (keyword, current_id, 'Yes')
                        insert_sql = "INSERT INTO Inverted_index(Term, PublicationID, IndexKeyword) VALUES (?,?,?)"
                        c.execute(insert_sql, insert_values)

            # create inverted_index from Title
            select_title_sql = 'SELECT Title FROM Publication WHERE PublicationID = ?'
            c.execute(select_title_sql, [current_id])
            rows = c.fetchall()
            for j in rows:
                text = j[0]
                if text is None:
                    continue
                else:
                    text = text.lower()
                    text = text.replace(":", "")
                    text = text.replace("!", "")
                    text_tokens = word_tokenize(text)
                    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
                    length = len(tokens_without_sw)
                    for k in range(length):
                        keyword = tokens_without_sw[k].strip()
                        insert_values = (keyword, current_id, 'Yes')
                        insert_sql = "INSERT INTO Inverted_index(Term, PublicationID, Title) VALUES (?,?,?)"
                        c.execute(insert_sql, insert_values)
                    print(tokens_without_sw)
        conn.commit()

    except Error as e:
        print(e)
    conn = None


if __name__ == '__main__':
    main()