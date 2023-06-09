import time
import redis
from flask import Flask, render_template
#import os
#from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

#load_dotenv() 
app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

@app.route('/titanic')
def titanic():
    df = pd.read_csv("titanic.csv")
    table = df.head(5).to_html()
    gender_counts = df.groupby(['Sex', 'Survived']).size().unstack()
    plot = gender_counts.plot(kind='bar')
    plot.set_xlabel("Gender")
    plot.set_ylabel("Number of Survivors")
    plot.legend(["Did Not Survive", "Survived"])
    plt.title("Survival by Gender")
    plt.xticks(rotation=0)
    plt.tight_layout()
    chart = plot.get_figure()
    chart.savefig('static/chart.png')
    return render_template('titanic.html', table=table, chart_url = url_for("static",filename="chart.png"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)