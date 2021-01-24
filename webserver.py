from flask import Flask, render_template, request, redirect, send_file
from indeed_crawler import IndeedCrawler

app = Flask('SuperScrapper')

DB = {}


@app.route('/')
def home():

    #    return '<h1>Job Search </h1> <form> <input placeholder = "waht job do you want?" type = "text"> <input type = "submit"></form>'
    return render_template("main.html")


@app.route('/contact')
def contact():
    return "Contact me.. "


@app.route('/report')
def report():
    word = request.args.get('word')
    if word is None or len(word) == 0:
        return redirect('/')

    if word in DB:
        data = DB[word]
    else:
        crawler = IndeedCrawler()
        crawler.allGetJobInfoCrawling(word=word)
        data = crawler.getArrayInfo()
        DB[word] = data
        crawler.saveInfoToCsv(word=word)

    return render_template('report.html', search_word=word, result=data, job_number=len(data))


@app.route('/user/<username>')
def nameRoute(username):
    return "hello your name is {}".format(username)


@app.route('/export')
def export():
    try:
        word = request.args.get('word')

        if not word:
            raise Exception()

        #return f"Generate csv export {word}"
        return send_file(f'csv/{word}_info.csv', as_attachment=True, attachment_filename=f"{word}_info.csv", mimetype='text/csv')

    except:
        return redirect('/')


app.run(host='0.0.0.0')
