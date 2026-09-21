\# AI Usage



\## Overview



AI tools were used as a development assistant during the implementation of the Sales CSV Analyzer project.



AI was used to help with understanding requirements, planning the application structure, generating and reviewing code, debugging issues, improving validation logic, and preparing project documentation.



All generated code was reviewed, tested, and modified as needed before being included in the project.



\## How AI Was Used



\### 1. Project Planning



AI was used to:



\- Break the project requirements into smaller development tasks.

\- Decide on a suitable frontend and backend structure.

\- Plan the React frontend and FastAPI backend integration.

\- Identify the main features required for the assessment.



\### 2. Frontend Development



AI assistance was used for:



\- Setting up the React + TypeScript project.

\- Implementing CSV upload functionality.

\- Implementing filtering by date, retailer, and product.

\- Calculating and displaying sales metrics.

\- Creating the sales data table.

\- Creating the sales value chart using Recharts.

\- Implementing filtered CSV download functionality.

\- Improving frontend styling and user interface behavior.



\### 3. Backend Development



AI assistance was used for:



\- Setting up the FastAPI backend.

\- Implementing the CSV upload endpoint.

\- Parsing CSV files using Python.

\- Validating required CSV columns.

\- Validating missing and invalid values.

\- Handling invalid file types and empty files.

\- Handling UTF-8 decoding errors.

\- Calculating sales metrics.

\- Connecting the React frontend to the FastAPI backend.

\- Configuring CORS for local frontend-backend communication.



\### 4. Debugging



AI was used to help investigate and resolve development issues, including:



\- CORS errors between the React frontend and FastAPI backend.

\- FastAPI/Uvicorn startup issues.

\- Git tracking of Python cache files.

\- Project structure and environment setup issues.



The issues were reproduced locally and the proposed solutions were tested before being accepted.



\### 5. Documentation



AI assistance was used to structure and improve:



\- `README.md`

\- `AI\_USAGE.md`

\- Git commit messages

\- Project setup instructions



\## Human Review and Testing



AI-generated suggestions were not accepted blindly.



The application was tested locally after implementation, including:



\- Valid CSV upload

\- Invalid CSV rows

\- Missing CSV columns

\- Empty CSV files

\- Invalid file types

\- Negative numeric values

\- Missing text values

\- Frontend filtering

\- Sales metric calculations

\- Chart rendering

\- Filtered CSV download

\- React-to-FastAPI communication



The developer reviewed the code and made implementation decisions based on the project requirements.



\## AI Tools



AI assistance was provided through ChatGPT.



AI was used as a development assistant and learning resource rather than as a replacement for understanding the submitted code.



The developer is expected to be able to explain the architecture, functionality, validation logic, calculations, and implementation decisions during the technical assessment.

