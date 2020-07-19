# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:50:50 2020

@author: vbhoj
"""

#pip install flask
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('rf_model.pkl','rb'))


@app.route('/')

def home():
    return render_template('cars.html')
        # return "<h1>Welcome to homepage</h1>"


@app.route('/predict', methods=['POST','GET'])

def predict():
    
    # print('preditcion page here')
    # Year = int(request.form['year'])
    # print("year is this ...............",Year)
    if request.method == 'POST':
        # year
        Year = int(request.form['year'])
        no_of_years_old = 2020-Year
        print('years_old=',no_of_years_old)
        
        if no_of_years_old > 15:
            return("Sorry you can't sell this year")
        
        # price
        Present_Price = int(request.form['price'])
        print('showroom price=',Present_Price)
        
        
        # # Kms_Driven
        Kms_Driven = int(request.form['kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        print('km driven=',Kms_Driven2)
        
        
        # owner
        Owner = int(request.form['owner'])
        print('ownership=',Owner)
        
        
        # Fuel_Type_Diesel
        Fuel_Type_Diesel = request.form['fuel']
        if Fuel_Type_Diesel == 'diesel':
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
            print(Fuel_Type_Diesel,"dessssss")
        
        elif request.form['fuel'] == 'cng':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
            print('CNG............')
        
            
        else:
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
            print(Fuel_Type_Petrol,'petrol............')
        
            
        # Seller_Type_Individual
        if request.form['sell'] == 'individual':
            Seller_Type_Individual = 1
            print(Seller_Type_Individual)
        else:
            Seller_Type_Individual = 0
            print(Seller_Type_Individual)
            
        if request.form['trans'] == 'automatic':
            Transmission_Mannual = 1
            print(Transmission_Mannual)
        else:
            Transmission_Mannual = 0
            print(Transmission_Mannual)
            
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        
        
        if output<0:
            return render_template('cars.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('cars.html',prediction_text="You Can Sell The Car at {} lakhs".format(output))
    
    else:
        return render_template('cars.html')



if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
       
    
    