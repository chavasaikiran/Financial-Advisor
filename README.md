# Financial Advisor using AI

## Overview

Financial Advisor is a Django-based web application that leverages AI and financial data analysis to provide users with investment suggestions. By integrating real-time stock data, technical indicators, and Google Gemini AI, the platform offers actionable insights (Buy, Sell, Hold) for selected stocks, along with visualizations and justifications for each recommendation.

## Features

- **User Registration & Login:** Secure user authentication and registration system.
- **Stock Data Analysis:** Fetches historical stock data using Yahoo Finance.
- **Technical Indicators:** Calculates and visualizes the Simple Moving Average (SMA) for selected stocks.
- **AI-Powered Suggestions:** Utilizes Google Gemini AI to generate investment suggestions based on recent trends and technical indicators.
- **Interactive Dashboard:** Clean user interface for viewing analysis results and AI recommendations.

## Technology Stack

- **Backend:** Python, Django 5.1.6
- **Frontend:** HTML, CSS (custom styles)
- **Database:** MySQL (for user registration), SQLite (default Django DB)
- **APIs & Libraries:** yfinance, pandas, matplotlib, google-generativeai, PyMySQL

