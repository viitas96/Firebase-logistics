import pyrebase

firebaseConfig={
    "apiKey": "AIzaSyD6jsgVsHiD2vaGvDPR_4iCdTkXpbFQafo",
    "authDomain": "logistic-72ed4.firebaseapp.com",
    "databaseURL": "https://logistic-72ed4-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "logistic-72ed4",
    "storageBucket": "logistic-72ed4.appspot.com",
    "messagingSenderId": "185587951953",
    "appId": "1:185587951953:web:d08e84237e77ce2b5b4b70",
    "measurementId": "G-RMEB749QCT"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def produs_saver(name, barcode, departament):
    data = {
        "name" : name,
        "departament" : departament,
        "barcode" : barcode
    }
    db.push(data)
    return True

def all():
    resp = db.get()
    return resp

def delete_by_id(id):
    db.child(id).remove()

def get_one_row(id):
    resp = db.child(id).get()
    return resp

def update_row(name, departament, barcode, id):
    db.child(id).update({
        "name": name,
        "departament": departament,
        "barcode": barcode
        })