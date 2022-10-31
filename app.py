from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import re

app = Flask(__name__)
dataframe = pickle.load(open("anime_dataframe.pkl", "rb"))
cos_matrix = pickle.load(open("anime_recommendation.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/recommend", methods = ["GET", "POST"])
@cross_origin()
def recommend():
    if request.method == "POST":

        #Getting anime name as input
        name = request.form["anime_name"]
        # print(name)
        
        anime_name = re.sub(' ',''," ".join(re.findall('[a-zA-Z0-9]',name.lower())))
        
        if anime_name in list(dataframe['name']):
        
            anime_id = dataframe[dataframe.name==anime_name]['id'].values[0]
            sorted_scores = sorted(list(enumerate(cos_matrix[anime_id])), key=lambda x: x[1], reverse=True)
            sorted_ten = sorted_scores[1:11]
            top_ten = [dataframe[anime[0]==dataframe['id']]['anime_name'].values[0] for anime in sorted_ten]

            return render_template('home.html', text="Great! You may also like", anime_1="{}".format(top_ten[0]), anime_2="{}".format(top_ten[1]),anime_3="{}".format(top_ten[2]), anime_4="{}".format(top_ten[3]), anime_5="{}".format(top_ten[4]), anime_6="{}".format(top_ten[5]), anime_7="{}".format(top_ten[6]), anime_8="{}".format(top_ten[7]), anime_9="{}".format(top_ten[8]), anime_10="{}".format(top_ten[9]))
        
        else:
            
            return render_template('home.html', text="Sorry, this anime does not exist in our database.")


    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
