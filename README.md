\# Sales CSV Analyzer



A full-stack web application for uploading, validating, filtering, analyzing, and exporting retail sales data from CSV files.



\## Features



\- Upload CSV sales data

\- Validate CSV structure and row values

\- Report invalid rows and missing columns

\- Filter data by:

&#x20; - Date

&#x20; - Retailer

&#x20; - Product

\- Display sales metrics:

&#x20; - Total Quantity

&#x20; - Total Sales Value

&#x20; - Average Selling Price

&#x20; - Promotion Percentage

\- Display sales data in a table

\- Visualize sales value by product

\- Download filtered data as CSV

\- FastAPI backend for CSV processing and validation

\- React frontend for the user interface



\## Tech Stack



\### Frontend



\- React

\- TypeScript

\- Vite

\- Recharts

\- Papa Parse

\- CSS



\### Backend



\- Python

\- FastAPI

\- Uvicorn

\- Python CSV module



\## Project Structure



```text

sales-csv-analyzer/

│

├── backend/

│   ├── main.py

│   ├── requirements.txt

│   └── venv/

│

├── src/

│   ├── App.tsx

│   ├── App.css

│   └── main.tsx

│

├── public/

├── .gitignore

├── package.json

├── package-lock.json

├── README.md

└── AI\_USAGE.md



\## CSV Format-

The uploaded CSV must contain the following columns:



Date

Retailer

Product

Quantity

Regular Price

Promotion Price



Example:



Date,Retailer,Product,Quantity,Regular Price,Promotion Price

01-01-2025,Retailer A,Product X,10,100,90

02-01-2025,Retailer B,Product Y,5,200,180

03-01-2025,Retailer A,Product Z,8,150,150



\## Validation

The backend validates:



File type

Empty files

UTF-8 encoding

Required CSV columns

Missing text values

Numeric values

Negative quantities

Negative prices



Invalid files are rejected and the application displays the validation errors.



\## Calculated Metrics

Total Quantity



Sum of the Quantity column.



Total Sales Value Calculated using:

Quantity × Promotion Price

for each row.



Average Selling Price Calculated using:

Total Sales Value ÷ Total Quantity



Promotion Percentage-

Percentage of rows where:

Promotion Price < Regular Price



\## Running the Application:

1\. Start the Backend.

Open a terminal and navigate to the backend:

cd backend



Create the virtual environment if it does not already exist:

python -m venv venv



Activate it:

venv\\Scripts\\activate



Install dependencies:

pip install -r requirements.txt



Start FastAPI:

uvicorn main:app --reload



The backend will run at:

http://127.0.0.1:8000



FastAPI documentation is available at:

http://127.0.0.1:8000/docs



2\. Start the Frontend.

Open another terminal and navigate to the project root:

cd C:\\Users\\shiha\\Desktop\\sales-csv-analyzer



Install frontend dependencies:

npm install



Start the development server:

npm run dev



The frontend will run at:

http://localhost:5173



Usage:

1. Open the application.

2\. Upload a CSV file using the file picker.

3\. The backend validates the uploaded CSV.

4\. If valid, the sales data and metrics are displayed.

5\. Use the filters to narrow the data.

6\. Review the table and chart.

7\. Click Download Filtered CSV to export the filtered results.



API-

Health Check:

GET /



Returns:

{

&#x20; "message": "Sales CSV Analyzer API is running"

}



Upload CSV-

POST /upload



Accepts a CSV file and returns:

Validation status

Validation errors

Parsed sales data

Calculated metrics



Development:

The project uses separate frontend and backend applications.



React + TypeScript

&#x20;       ↓

HTTP POST

&#x20;       ↓

FastAPI

&#x20;       ↓

CSV validation + processing

&#x20;       ↓

JSON response

&#x20;       ↓

React dashboard



The frontend handles the user interface, filtering, visualization, and CSV export.

The backend handles CSV validation, data parsing, and calculation of the initial sales metrics.



License:

This project was created as a technical assessment project.



