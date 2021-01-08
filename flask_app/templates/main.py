from flask import Flask, flash, redirect, render_template, request, session, abort
app = Flask(__name__)

def make_aval_index(formData):
    aval_index = 0

    q_massif = formData["massif"]
    if q_massif == 'Vanoise':
        aval_index += 20
    elif q_massif in ['Haute-Tarentaise','Mont-Blanc','Haute-Maurienne']:
        aval_index += 16
    elif q_massif in ['Queyras','Oisans','Chablais','Pelvoux','Aravis']:
        aval_index += 12
    elif q_massif in ['Maurienne','Belledonne','Chartreuse','Grandes-Rousses','Beaufortain']:
        aval_index += 8
    else:
        aval_index += 4

    q_month = int(formData["month"])
    if q_month == 3 or q_month == 2 or q_month == 1:
        aval_index += 20
    elif q_month == 4 or q_month == 12:
        aval_index += 12
    elif q_month == 5 or q_month == 11:
        aval_index += 8
    else:
        aval_index += 0

    q_activity = formData["activity"]
    if q_activity == "hiking":
        aval_index += 20
    elif q_activity == "off-piste ski or snowboard":
        aval_index += 16
    elif q_activity == "cross_country ski, snowboard or snowshoes":
        aval_index += 8
    elif q_activity == "alpinist activity":
        aval_index += 8
    else:
        aval_index += 4

    q_group_size = int(formData["number of travelmates"])
    if q_group_size == 0:
        aval_index += 10
    elif q_group_size == 1:
        aval_index += 20
    elif q_group_size == 2:
        aval_index += 10
    elif q_group_size == 3 or q_group_size == 4 or q_group_size == 5 or q_group_size == 6:
        aval_index += 5
    else:
        aval_index += 2


    q_elevation = int(formData["elevation"])
    if q_elevation < 1500:
        aval_index += 0
    elif q_elevation <= 2000:
        aval_index += 12
    elif q_elevation <= 2500:
        aval_index += 20
    elif q_elevation <= 3000:
        aval_index += 16
    else:
        aval_index += 0

    return aval_index

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/questions",methods = ['POST', 'GET'])
def questions():
    options = ['Chablais', 'Aravis', 'Mont-Blanc', 'Bauges', 'Beaufortain',
       'Haute-Tarentaise', 'Vanoise', 'Maurienne', 'Chartreuse',
       'Belledonne', 'Grandes-Rousses', 'Oisans', 'Vercors', 'Devoluy',
       'Champsaur', 'Pelvoux', 'Haute-Maurienne', 'Thabor', 'Queyras',
       'Parpaillon', 'Ubaye', 'Haut_Var-Haut_Verdon', 'Mercantour', 'other']
    options2 = ['hiking', 'off-piste ski or snowboard', 'cross_country ski, snowboard or snowshoes', 
            'alpinist activity', 'other']
    return render_template('questions.html', options = options, options2 = options2)

@app.route("/result",methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
      result = request.form
      aval_index = make_aval_index(request.form)
      return render_template('result.html', result = result, aval_index = aval_index)
    else:
      render_template('index.html')

if __name__ == "__main__":
    app.run()

