import { useState } from "react";
import Papa from "papaparse";
import "./App.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type SalesRow = {
  date: string;
  retailer: string;
  product: string;
  quantity: number;
  regularPrice: number;
  promotionPrice: number;
};

function App() {
  const [fileName, setFileName] = useState("");
  const [validationMessage, setValidationMessage] = useState("");
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [salesData, setSalesData] = useState<SalesRow[]>([]);
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedRetailer, setSelectedRetailer] = useState("");
  const [selectedProduct, setSelectedProduct] = useState("");

  // Filter the sales data
  const filteredData = salesData.filter((row) => {
    const matchesDate =
      selectedDate === "" || row.date === selectedDate;

    const matchesRetailer =
      selectedRetailer === "" ||
      row.retailer === selectedRetailer;

    const matchesProduct =
      selectedProduct === "" ||
      row.product === selectedProduct;

    return matchesDate && matchesRetailer && matchesProduct;
  });

  // Calculate total quantity
  const totalQuantity = filteredData.reduce(
    (total, row) => total + row.quantity,
    0
  );

  // Calculate total sales value
  const totalSalesValue = filteredData.reduce(
    (total, row) => total + row.quantity * row.promotionPrice,
    0
  );

  // Calculate average selling price
  const averageSellingPrice =
    totalQuantity > 0
      ? totalSalesValue / totalQuantity
      : 0;

  // Calculate promotion percentage
  const promotedRows = filteredData.filter(
    (row) => row.promotionPrice < row.regularPrice
  ).length;

  const promotionPercentage =
    filteredData.length > 0
      ? (promotedRows / filteredData.length) * 100
      : 0;
  
  const chartData = filteredData.map((row) => ({
    product: row.product,
    salesValue: row.quantity * row.promotionPrice,
  }));

  function handleDownloadCSV() {
  if (filteredData.length === 0) {
    return;
  }

  const csv = Papa.unparse(
    filteredData.map((row) => ({
      Date: row.date,
      Retailer: row.retailer,
      Product: row.product,
      Quantity: row.quantity,
      "Regular Price": row.regularPrice,
      "Promotion Price": row.promotionPrice,
    }))
  );

  const blob = new Blob([csv], {
    type: "text/csv;charset=utf-8;",
  });

  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");

  link.href = url;
  link.download = "filtered_sales_data.csv";

  link.click();

  URL.revokeObjectURL(url);
}

  async function handleFileChange(
  event: React.ChangeEvent<HTMLInputElement>
) {
  const file = event.target.files?.[0];

  if (!file) {
    return;
  }
  setFileName(file.name);

  setValidationMessage("");
  setValidationErrors([]);

  const formData = new FormData();

  formData.append("file", file);

  try {
    const response = await fetch(
      "https://sales-csv-analyzer-api.onrender.com/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error(
        `Server error: ${response.status}`
      );
    }

    const result = await response.json();
    if (typeof result.valid !== "boolean") {
      throw new Error(
        "Invalid response received from backend."
      );
    }

    console.log("Backend response:", result);

    if (!result.valid) {
      setValidationMessage(
        result.message || "CSV validation failed."
      );

      setValidationErrors(
        result.errors || []
      );

      setSalesData([]);

      return;
    }

    setValidationMessage(
      result.message || "CSV file is valid."
    );

    setValidationErrors([]);

    setSalesData(result.data);

    setSelectedDate("");
    setSelectedRetailer("");
    setSelectedProduct("");
  } catch (error) {
    console.error(error);

    setValidationMessage(
      "Could not connect to the FastAPI backend."
    );

    setValidationErrors([]);

    setSalesData([]);
  }
}

  // Get unique filter values
  const uniqueDates = [
    ...new Set(salesData.map((row) => row.date)),
  ];

  const uniqueRetailers = [
    ...new Set(salesData.map((row) => row.retailer)),
  ];

  const uniqueProducts = [
    ...new Set(salesData.map((row) => row.product)),
  ];

  return (
    <div>
      <h1>Sales CSV Analyzer</h1>

      <p>
        Upload your sales CSV file to analyze retail sales data.
      </p>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
      />

      {fileName && <p>Selected file: {fileName}</p>}

      {validationMessage && (
        <p>{validationMessage}</p>
      )}

      {validationErrors.length > 0 && (
        <div>
          <h2>Validation Errors</h2>

          <ul>
            {validationErrors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </div>
      )}

      {salesData.length > 0 && (
        <div>
          <h2>Filters</h2>

          {/* Date Filter */}
          <div>
            <label htmlFor="date-filter">
              Date:
            </label>

            <select
              id="date-filter"
              value={selectedDate}
              onChange={(event) =>
                setSelectedDate(event.target.value)
              }
            >
              <option value="">All Dates</option>

              {uniqueDates.map((date) => (
                <option key={date} value={date}>
                  {date}
                </option>
              ))}
            </select>
          </div>

          {/* Retailer Filter */}
          <div>
            <label htmlFor="retailer-filter">
              Retailer:
            </label>

            <select
              id="retailer-filter"
              value={selectedRetailer}
              onChange={(event) =>
                setSelectedRetailer(event.target.value)
              }
            >
              <option value="">All Retailers</option>

              {uniqueRetailers.map((retailer) => (
                <option key={retailer} value={retailer}>
                  {retailer}
                </option>
              ))}
            </select>
          </div>

          {/* Product Filter */}
          <div>
            <label htmlFor="product-filter">
              Product:
            </label>

            <select
              id="product-filter"
              value={selectedProduct}
              onChange={(event) =>
                setSelectedProduct(event.target.value)
              }
            >
              <option value="">All Products</option>

              {uniqueProducts.map((product) => (
                <option key={product} value={product}>
                  {product}
                </option>
              ))}
            </select>
          </div>

          <button onClick={handleDownloadCSV}>
            Download Filtered CSV
          </button>
          
          <button
            onClick={() => {
              setSelectedDate("");
              setSelectedRetailer("");
              setSelectedProduct("");
            }}
          >
            Clear Filters
          </button>
        </div>
      )}

      {salesData.length > 0 && (
        <div>
          <h2>Sales Summary</h2>

          <div>
            <h3>Total Quantity</h3>
            <p>{totalQuantity}</p>
          </div>

          <div>
            <h3>Total Sales Value</h3>
            <p>₹{totalSalesValue.toFixed(2)}</p>
          </div>

          <div>
            <h3>Average Selling Price</h3>
            <p>₹{averageSellingPrice.toFixed(2)}</p>
          </div>

          <div>
            <h3>Promotion Percentage</h3>
            <p>{promotionPercentage.toFixed(2)}%</p>
          </div>
        </div>
      )}
      {filteredData.length > 0 && (
  <div>
    <h2>Sales Data</h2>

    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Retailer</th>
          <th>Product</th>
          <th>Quantity</th>
          <th>Regular Price</th>
          <th>Promotion Price</th>
        </tr>
      </thead>

      <tbody>
        {filteredData.map((row, index) => (
          <tr key={index}>
            <td>{row.date}</td>
            <td>{row.retailer}</td>
            <td>{row.product}</td>
            <td>{row.quantity}</td>
            <td>₹{row.regularPrice.toFixed(2)}</td>
            <td>₹{row.promotionPrice.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}

  {filteredData.length > 0 && (
  <div>
    <h2>Sales Value by Product</h2>

    <ResponsiveContainer width="100%" height={350}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="product" />

        <YAxis />

        <Tooltip />

        <Bar dataKey="salesValue" />
      </BarChart>
    </ResponsiveContainer>
  </div>
)}
      
    </div>
  );
}

export default App;