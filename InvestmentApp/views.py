from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
import pymysql
import io
import base64
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import google.generativeai as genai

genai.configure(api_key="AIzaSyCSrdHqh7wkS7TiOhA8NebxDFiQO41gCJ4")
global model

def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        if data.empty:
            print(f"No data found for {ticker} over the last {period}.")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# --- 2. Financial Analysis (Basic Example: Simple Moving Average) ---
def calculate_technical_indicators(data, window=20):
    """Calculates a simple moving average."""
    if data is None:
        return None
    data['SMA'] = data['Close'].rolling(window=window).mean()
    return data

# --- 3. Gemini Model Interaction ---
def get_investment_suggestion(financial_data_summary):
    global model
    """
    Sends financial data summary to Gemini and gets investment suggestions.
    """
    prompt = f"""
    Based on the following financial data for a stock, provide a concise investment suggestion (Buy, Sell, Hold) and a brief justification.
    Focus on key trends and indicators.

    **Financial Data Summary:**
    {financial_data_summary}

    Consider the following for your suggestion:
    - Recent price performance (last few days/weeks)
    - Relationship between closing price and moving average (if provided)
    - Overall trend

    Investment Suggestion:
    Justification:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini model: {e}"


def LoadModel(request):
    if request.method == 'GET':
        global model
        model = genai.GenerativeModel('gemini-1.5-flash')
        output = "<font size=3 color=blue>Gemini Financial Advisor Ai Model Loaded</font><br/>"
        context= {'data': output}
        return render(request, 'UserScreen.html', context)

def Suggestion(request):
    if request.method == 'GET':
       return render(request, 'Suggestion.html', {})  

def SuggestionAction(request):
    if request.method == 'POST':
        global model
        ticker = request.POST.get('t1', False)
        period = "1y"
        stock_data = get_stock_data(ticker, period)
        if stock_data is not None:
            print("Calculating technical indicators...")
            stock_data = calculate_technical_indicators(stock_data)
            # Display a simple plot
            plt.figure(figsize=(12, 6))
            plt.plot(stock_data['Close'], label='Close Price')
            if 'SMA' in stock_data.columns:
                plt.plot(stock_data['SMA'], label='20-Day SMA')
            plt.title(f'{ticker} Stock Price and 20-Day SMA (Last {period})')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            plt.grid(True)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            plt.clf()
            plt.cla()
            recent_data = stock_data.tail(5)  # Get last 5 days of data
            financial_summary = f"""
                Recent 5 days of {ticker} data:
                {recent_data[['Close', 'SMA']].to_string()}
                Current Close Price: {stock_data['Close'].iloc[-1]:.2f}
                Current 20-Day SMA: {stock_data['SMA'].iloc[-1]:.2f} (if available)
            """
            print("\nSending data to Gemini for investment suggestion...")
            investment_suggestion = get_investment_suggestion(financial_summary)
            investment_suggestion = investment_suggestion.replace('"',"")
            arr = investment_suggestion.split(" ")
            output = arr[0]+" "+arr[1]+" "+arr[2]
            output1 = investment_suggestion.replace(output,"")
            data = "<font size=3 color=red>"+output+"</font><br/>"
            data += "<font size=3 color=blue>"+output1.strip()+"</font><br/><br/>"
            context= {'data':data, 'img': img_b64}
            return render(request, 'UserScreen.html', context)
        else:
            output = "<font size=3 color=blue>Could not proceed with analysis due to data fetching issues.</font>"
            context= {'data':output}
            return render(request, 'UserScreen.html', context)       

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})   

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'investment',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)        
    
def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'investment',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'investment',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup process completed"
        context= {'data': status}
        return render(request, 'Register.html', context)

