from typing import List, Any

from flask import Flask, request, render_template,jsonify
import cowin_api.api as myapi

app = Flask(__name__)

def do_somethings(text1):
    st_id = text1
    obj = myapi.CoWinAPI()
    dist_dict = obj.get_districts(st_id)
    district = dist_dict['districts']
    list_dict ={}
    for i in district:
        list_dict[i['district_id']] = i['district_name']

    return list_dict


def do_something(text1):
    obj=myapi.CoWinAPI()
    district_id=text1
    min_age="18"
    avail=obj.get_availability_by_district(district_id, min_age)
    centers=avail['centers']
    name=[]
    address=[]
    fee=[]
    vac=[]
    slot=[]
    for i in centers:
        name.append(i['name'])
        address.append(i['address'])
        fee.append(i['fee_type'])
        for j in i['sessions']:
            vac.append(j['vaccine'])
            slot.append(j['slots'])
    return name, address, fee, vac, slot

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/state', methods=['GET','POST'])
def my_form_posts():
    text1 = request.form['text1']
    word = request.args.get('text1')

    combine = do_somethings(text1)

    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    text1 = request.form['text1']
    word = request.args.get('text1')
    combine = do_something(text1)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)

