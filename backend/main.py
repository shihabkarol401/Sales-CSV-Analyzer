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
    content = await file.read()

    # Convert the uploaded file into text
    text = content.decode("utf-8-sig")

    # Read the CSV
    reader = csv.DictReader(io.StringIO(text))

    # Get column names
    headers = reader.fieldnames or []

    # Check for missing columns
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
            "errors": [],
            "data": [],
            "metrics": {},
        }

    errors = []
    sales_data = []

    # Validate and parse every row
    for row_number, row in enumerate(reader, start=2):

        date = (row.get("Date") or "").strip()
        retailer = (row.get("Retailer") or "").strip()
        product = (row.get("Product") or "").strip()

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
            errors.append(
                f"Row {row_number}: Date is missing."
            )

        if not retailer:
            errors.append(
                f"Row {row_number}: Retailer is missing."
            )

        if not product:
            errors.append(
                f"Row {row_number}: Product is missing."
            )

        # Convert Quantity
        try:
            quantity = float(quantity_value)

            if quantity < 0:
                errors.append(
                    f"Row {row_number}: Quantity must be non-negative."
                )

        except ValueError:
            quantity = 0

            errors.append(
                f"Row {row_number}: Quantity must be a valid number."
            )

        # Convert Regular Price
        try:
            regular_price = float(
                regular_price_value
            )

            if regular_price < 0:
                errors.append(
                    f"Row {row_number}: Regular Price must be non-negative."
                )

        except ValueError:
            regular_price = 0

            errors.append(
                f"Row {row_number}: Regular Price must be a valid number."
            )

        # Convert Promotion Price
        try:
            promotion_price = float(
                promotion_price_value
            )

            if promotion_price < 0:
                errors.append(
                    f"Row {row_number}: Promotion Price must be non-negative."
                )

        except ValueError:
            promotion_price = 0

            errors.append(
                f"Row {row_number}: Promotion Price must be a valid number."
            )

        # Only add the row if its text fields are present
        # and its numeric values are valid
        if (
            date
            and retailer
            and product
            and quantity_value
            and regular_price_value
            and promotion_price_value
            and not any(
                error.startswith(
                    f"Row {row_number}:"
                )
                for error in errors
            )
        ):
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

    # Return validation errors if any exist
    if errors:
        return {
            "valid": False,
            "message": f"CSV contains {len(errors)} validation error(s).",
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
        row["quantity"] * row["promotionPrice"]
        for row in sales_data
    )

    # Calculate average selling price
    average_selling_price = (
        total_sales_value / total_quantity
        if total_quantity > 0
        else 0
    )

    # Count rows where promotion price is lower
    # than regular price
    promoted_rows = sum(
        1
        for row in sales_data
        if row["promotionPrice"] < row["regularPrice"]
    )

    # Calculate promotion percentage
    promotion_percentage = (
        promoted_rows / len(sales_data) * 100
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
            "averageSellingPrice": average_selling_price,
            "promotionPercentage": promotion_percentage,
        },
    }