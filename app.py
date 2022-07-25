from flask import Flask, redirect, url_for, render_template, request, session
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sqlite3
from sqlite3 import Error
import re


database = './static/db/expert.db'
lecturerList = []
publication_count = []
publicationList = []
current_keywords = ""
current_title = ""

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

conn = None
try:
    conn = sqlite3.connect(database, check_same_thread=False)
    c = conn.cursor()

except Error as e:
    print(e)


@app.route('/')
def home():  # put application's code here
    return render_template("index.html")


@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        global lecturerList
        global publicationList
        global current_keywords
        global current_title
        global publication_count

        # Reset Search Result when a new search is performed
        lecturerList = []
        publication_count = []
        publicationList = []
        publicationfinalList = []
        current_keywords = ""
        current_title = ""

        unwanted_characters = ["(", ")", ","]
        keywords = request.form['keywords']
        projectTitle = request.form['projectTitle']
        current_keywords = keywords
        current_title = projectTitle
        # keywords = keywords.replace(';', ' ')
        # keywords = keywords.replace(',', ' ')
        keywords = keywords.replace(";", ',')
        keywords = keywords.split(",")

        print(keywords)
        for i in keywords:
            word = i
            keyword = '%' + word + '%',
            sql = ''' SELECT DISTINCT pub.* FROM (Publication pub INNER JOIN Inverted_Index inv ON 
            pub.PublicationID = inv.PublicationID)
            WHERE Term LIKE ? AND (AuthorKeyword = "Yes" OR IndexKeyword = "Yes")
            '''
            c.execute(sql, keyword)
            publicationinitialList = c.fetchall()
            [publicationfinalList.append(x) for x in publicationinitialList if x not in publicationfinalList]
            for l in publicationfinalList:
                print(l)

            if not publicationList:
                publicationList.extend(publicationfinalList)
            else:
                for data in publicationList:
                    for data2 in publicationfinalList:
                        if data[0] == data2[0]:
                            publicationfinalList.remove(data2)
                        else:
                            continue
                publicationList.extend(publicationfinalList)

            count = 0
            for publication in publicationfinalList:
                lecturerID = publication[1]
                if not publication_count:
                    count = 1
                    publication_count.append([lecturerID, count])
                elif not any(str(lecturerID) in str(eachCount[0]) for eachCount in publication_count):
                    count = 1
                    publication_count.append([lecturerID, count])
                else:
                    for eachCount in publication_count:
                        if eachCount[0] == lecturerID:
                            count = count + 1
                            eachCount[1] = count
                            #print(publication_count)
            publication_count = sorted(publication_count, key=lambda row: row[1], reverse=True)

        if projectTitle:
            projectTitle = projectTitle.lower()
            projectTitleCleaned = re.sub('[^A-Za-z ]', "", projectTitle)
            print(projectTitleCleaned)
            text_tokens = word_tokenize(projectTitleCleaned)
            tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
            for eachToken in tokens_without_sw:
                find_token_sql = ''' SELECT DISTINCT pub.* FROM (Publication pub INNER JOIN Inverted_Index inv ON
                pub.PublicationID = inv.PublicationID)
                WHERE Term LIKE ? AND inv.Title = "Yes"
                '''

                c.execute(find_token_sql, [eachToken])
                publicationinitialList = c.fetchall()
                if publicationinitialList:
                    [publicationfinalList.append(x) for x in publicationinitialList if x not in publicationfinalList]
                    if not publicationList:
                        publicationList.extend(publicationfinalList)
                    else:
                        for data in publicationList:
                            for data2 in publicationfinalList:
                                if data[0] == data2[0]:
                                    publicationfinalList.remove(data2)
                                else:
                                    continue
                        publicationList.extend(publicationfinalList)

                    count = 0
                    for publication in publicationfinalList:
                        lecturerID = publication[1]
                        if not publication_count:
                            count = 1
                            publication_count.append([lecturerID, count])
                        elif not any(str(lecturerID) in str(eachCount[0]) for eachCount in publication_count):
                            count = 1
                            publication_count.append([lecturerID, count])
                        else:
                            for eachCount in publication_count:
                                if eachCount[0] == lecturerID:
                                    count = count + 1
                                    eachCount[1] = count
                                    # print(publication_count)
                    publication_count = sorted(publication_count, key=lambda row: row[1], reverse=True)

        for eachExpert in publication_count:
            expertID = str(eachExpert[0])
            obtain_lecturer_sql = '''SELECT LecturerID, Name, Position, Email, Telephone, Fax, Room, Address,
            ResearchCluster, Interest, Specialization, Qualification, Image from expertInfo WHERE LecturerID = ?'''
            c.execute(obtain_lecturer_sql, [expertID])
            lecturer = c.fetchall()
            lecturerList.extend(lecturer)

        return redirect(url_for("dashboard"))
    else:
        return render_template('search.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')


@app.route("/admin", methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')


@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    if request.method == "POST":
        name = request.form["expName"]
        return redirect(url_for("expertInfo", expertname=name))
    else:
        for expert in lecturerList:
            print(expert[0])
        return render_template("dashboard.html", publicationList=publicationList,
                               expertInfo=zip(publication_count, lecturerList), current_keywords=current_keywords,
                               current_title=current_title)


@app.route("/supervisorList")
def supervisorList():
    sql = "SELECT * FROM expertInfo"
    c.execute(sql)
    statement = c.fetchall()
    print(statement)
    return render_template("supervisorList.html", statement=statement)


@app.route("/modify")
def modify():
    return render_template("modify.html")


@app.route("/expertInfo/<expertname>")
def expertInfo(expertname):
    global lecturerList
    global publicationList
    global publication_count
    expert_pub_list = []
    expert_count = ""
    for expert in lecturerList:
        if expertname in expert[1]:
            expertID = expert[0]
            for publication in publicationList:
                if expertID == publication[1]:
                    expert_pub_list.append(publication)
            for count in publication_count:
                if expertID == count[0]:
                    expert_count = count[1]
            return render_template("expertInfo.html", expertname=expertname, expertdata=expert,
                                   expert_pub_list=expert_pub_list, expert_count=expert_count)
        else:
            error = "No Data Selected"
            print(error)


@app.route("/insertNewExpert")
def insertNewExpert():
    return render_template("insertNewExpert.html")


@app.route("/modifyExpert")
def modifyExpert():
    sql = "SELECT * FROM expertInfo"
    c.execute(sql)


@app.route("/deleteExpert")
def deleteExpert():
    return render_template("deleteExpert.html")


if __name__ == '__main__':
    app.run()

