from flask import Flask, render_template, request, redirect, send_file
from SO_scrapper import get_SO_jobs
from RO_scrapper import get_RO_jobs
from WWR_scrapper import get_WWR_jobs
from exporter import save_to_file

app = Flask("SupperScrapper")

db = {}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
      word = word.lower()
      existingJobs = db.get(word)
      if existingJobs:
        jobs = existingJobs
      else:
        SO_jobs = get_SO_jobs(word)
        RO_jobs = get_RO_jobs(word)
        WWR_jobs = get_WWR_jobs(word)
        jobs = SO_jobs + RO_jobs + WWR_jobs
        db[word] = jobs
    else:
      return redirect('/')
    return render_template(
      "report.html",
      searchingBy=word, 
      resultsNumber=len(jobs),
      jobs=jobs
    )


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")

