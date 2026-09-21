import csv
import io

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
	"http://localhost:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


REQUIRED_COLUMNS = [
    "Date",
    "Retailer",
    "Product",
    "Quantity",
    "Regular Price",
    "Promotion Price",
]


@app.get("/")
def read_root():
    return {
        "message": "Sales CSV Analyzer API is running"
    }


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    # Check that a file was actually selected
    if not file.filename:
        return {
            "valid": False,
            "message": "No file was selected.",
            "missing_columns": [],
            "errors": ["Please select a CSV file."],
            "data": [],
            "metrics": {},
        }

    # Check file extension
    if not file.filename.lower().endswith(".csv"):
        return {
            "valid": False,
            "message": "Invalid file type.",
            "missing_columns": [],
            "errors": [
                "Please upload a file with a .csv extension."
            ],
            "data": [],
            "metrics": {},
        }

    try:
        # Read uploaded file
        content = await file.read()

        # Check for empty file
        if not content:
            return {
                "valid": False,
                "message": "The uploaded CSV file is empty.",
                "missing_columns": [],
                "errors": [
                    "The file does not contain any data."
                ],
                "data": [],
                "metrics": {},
            }

        # Convert uploaded bytes into text
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            return {
                "valid": False,
                "message": "The CSV file could not be read.",
                "missing_columns": [],
                "errors": [
                    "The file must use UTF-8 encoding."
                ],
                "data": [],
                "metrics": {},
            }

        # Read CSV
        reader = csv.DictReader(
            io.StringIO(text)
        )

        # Get column names
        headers = reader.fieldnames or []

        # Check if CSV has headers
        if not headers:
            return {
                "valid": False,
                "message": "CSV headers are missing.",
                "missing_columns": REQUIRED_COLUMNS,
                "errors": [
                    "The CSV file must contain a header row."
                ],
                "data": [],
                "metrics": {},
            }

        # Check for missing required columns
        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in headers
        ]

        if missing_columns:
            return {
                "valid": False,
                "message": "CSV is missing required columns.",
                "missing_columns": missing_columns,
                "errors": [
                    f"Missing column: {column}"
                    for column in missing_columns
                ],
                "data": [],
                "metrics": {},
            }

        errors = []
        sales_data = []

        # Validate and parse every row
        for row_number, row in enumerate(
            reader,
            start=2
        ):

            row_errors = []

            date = (row.get("Date") or "").strip()
            retailer = (
                row.get("Retailer") or ""
            ).strip()
            product = (
                row.get("Product") or ""
            ).strip()

            quantity_value = (
                row.get("Quantity") or ""
            ).strip()

            regular_price_value = (
                row.get("Regular Price") or ""
            ).strip()

            promotion_price_value = (
                row.get("Promotion Price") or ""
            ).strip()

            # Validate text fields
            if not date:
                row_errors.append(
                    f"Row {row_number}: Date is missing."
                )

            if not retailer:
                row_errors.append(
                    f"Row {row_number}: Retailer is missing."
                )

            if not product:
                row_errors.append(
                    f"Row {row_number}: Product is missing."
                )

            # Validate Quantity
            try:
                quantity = float(quantity_value)

                if quantity < 0:
                    row_errors.append(
                        f"Row {row_number}: "
                        "Quantity must be non-negative."
                    )

            except ValueError:
                quantity = 0

                row_errors.append(
                    f"Row {row_number}: "
                    "Quantity must be a valid number."
                )

            # Validate Regular Price
            try:
                regular_price = float(
                    regular_price_value
                )

                if regular_price < 0:
                    row_errors.append(
                        f"Row {row_number}: "
                        "Regular Price must be non-negative."
                    )

            except ValueError:
                regular_price = 0

                row_errors.append(
                    f"Row {row_number}: "
                    "Regular Price must be a valid number."
                )

            # Validate Promotion Price
            try:
                promotion_price = float(
                    promotion_price_value
                )

                if promotion_price < 0:
                    row_errors.append(
                        f"Row {row_number}: "
                        "Promotion Price must be non-negative."
                    )

            except ValueError:
                promotion_price = 0

                row_errors.append(
                    f"Row {row_number}: "
                    "Promotion Price must be a valid number."
                )

            # Add row errors to overall errors
            errors.extend(row_errors)

            # Add only completely valid rows
            if not row_errors:
                sales_data.append(
                    {
                        "date": date,
                        "retailer": retailer,
                        "product": product,
                        "quantity": quantity,
                        "regularPrice": regular_price,
                        "promotionPrice": promotion_price,
                    }
                )

        # Check if CSV contains no data rows
        if not sales_data and not errors:
            return {
                "valid": False,
                "message": "The CSV file contains no data rows.",
                "missing_columns": [],
                "errors": [
                    "Please add at least one data row."
                ],
                "data": [],
                "metrics": {},
            }

        # Return validation errors
        if errors:
            return {
                "valid": False,
                "message": (
                    f"CSV contains "
                    f"{len(errors)} validation error(s)."
                ),
                "missing_columns": [],
                "errors": errors,
                "data": [],
                "metrics": {},
            }

        # Calculate total quantity
        total_quantity = sum(
            row["quantity"]
            for row in sales_data
        )

        # Calculate total sales value
        total_sales_value = sum(
            row["quantity"]
            * row["promotionPrice"]
            for row in sales_data
        )

        # Calculate average selling price
        average_selling_price = (
            total_sales_value / total_quantity
            if total_quantity > 0
            else 0
        )

        # Count promoted rows
        promoted_rows = sum(
            1
            for row in sales_data
            if row["promotionPrice"]
            < row["regularPrice"]
        )

        # Calculate promotion percentage
        promotion_percentage = (
            promoted_rows
            / len(sales_data)
            * 100
            if sales_data
            else 0
        )

        return {
            "valid": True,
            "message": "CSV file is valid.",
            "missing_columns": [],
            "errors": [],
            "data": sales_data,
            "metrics": {
                "totalQuantity": total_quantity,
                "totalSalesValue": total_sales_value,
                "averageSellingPrice": (
                    average_selling_price
                ),
                "promotionPercentage": (
                    promotion_percentage
                ),
            },
        }

    except Exception as error:
        print(
            "Unexpected server error:",
            error
        )

        return {
            "valid": False,
            "message": (
                "An unexpected error occurred "
                "while processing the CSV."
            ),
            "missing_columns": [],
            "errors": [
                "Please check the CSV file and try again."
            ],
            "data": [],
            "metrics": {},
        }