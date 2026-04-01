import React, { useState, useEffect } from "react";
import api from "../api/axios";

const Reports = () => {
  const [inventory, setInventory] = useState([]);
  const [salesSummary, setSalesSummary] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [invRes, salesRes] = await Promise.all([
        api.get("/api/inventory"),
        api.get("/api/sales/summary"),
      ]);

      setInventory(invRes.data);
      setSalesSummary(salesRes.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  const exportInventoryReport = () => {
    const headers = [
      "Product ID",
      "Product Name",
      "Category",
      "Stock",
      "Reorder Point",
      "Status",
      "Location",
      "Last Updated",
    ];
    const rows = inventory.map((item) => [
      item.product_id,
      item.product_name,
      item.category,
      item.quantity_in_stock,
      item.reorder_point,
      item.stock_status,
      item.warehouse_location || "N/A",
      new Date(item.last_updated).toLocaleDateString(),
    ]);

    downloadCSV("inventory-report", headers, rows);
  };

  const exportSalesReport = () => {
    const headers = [
      "Product ID",
      "Product Name",
      "Year",
      "Month",
      "Total Sold",
    ];
    const rows = salesSummary.map((item) => [
      item.product_id,
      item.product_name,
      item.year,
      item.month,
      item.total_sold,
    ]);

    downloadCSV("sales-report", headers, rows);
  };

  const exportLowStockReport = () => {
    const lowStock = inventory.filter((item) => item.stock_status === "low");
    const headers = [
      "Product ID",
      "Product Name",
      "Current Stock",
      "Reorder Point",
      "Deficit",
      "Location",
    ];
    const rows = lowStock.map((item) => [
      item.product_id,
      item.product_name,
      item.quantity_in_stock,
      item.reorder_point,
      item.reorder_point - item.quantity_in_stock,
      item.warehouse_location || "N/A",
    ]);

    downloadCSV("low-stock-alert", headers, rows);
  };

  const downloadCSV = (filename, headers, rows) => {
    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.map((cell) => `"${cell}"`).join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${filename}-${new Date().toISOString().split("T")[0]}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Loading reports...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">
          Reports & Analytics
        </h1>
        <p className="text-gray-400">Export and analyze your inventory data</p>
      </div>

      {/* Report Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Inventory Report */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                />
              </svg>
            </div>
            <div>
              <h3 className="text-white font-semibold">Inventory Report</h3>
              <p className="text-xs text-gray-400">
                {inventory.length} products
              </p>
            </div>
          </div>

          <p className="text-gray-300 text-sm mb-4">
            Complete inventory snapshot with stock levels, reorder points, and
            warehouse locations.
          </p>

          <button
            onClick={exportInventoryReport}
            className="w-full px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>Download CSV</span>
          </button>
        </div>

        {/* Sales Report */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                />
              </svg>
            </div>
            <div>
              <h3 className="text-white font-semibold">Sales Report</h3>
              <p className="text-xs text-gray-400">
                {salesSummary.length} records
              </p>
            </div>
          </div>

          <p className="text-gray-300 text-sm mb-4">
            Monthly sales summary by product with total quantities sold.
          </p>

          <button
            onClick={exportSalesReport}
            className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>Download CSV</span>
          </button>
        </div>

        {/* Low Stock Alert Report */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-pink-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <div>
              <h3 className="text-white font-semibold">Low Stock Alerts</h3>
              <p className="text-xs text-gray-400">
                {inventory.filter((item) => item.stock_status === "low").length}{" "}
                alerts
              </p>
            </div>
          </div>

          <p className="text-gray-300 text-sm mb-4">
            Products below reorder point requiring immediate attention.
          </p>

          <button
            onClick={exportLowStockReport}
            className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <span>Download CSV</span>
          </button>
        </div>
      </div>

      {/* Summary Statistics */}
      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-6">
          Summary Statistics
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <p className="text-gray-400 text-sm mb-1">Total Products</p>
            <p className="text-3xl font-bold text-white">{inventory.length}</p>
          </div>

          <div>
            <p className="text-gray-400 text-sm mb-1">Total Stock Units</p>
            <p className="text-3xl font-bold text-white">
              {inventory.reduce((sum, item) => sum + item.quantity_in_stock, 0)}
            </p>
          </div>

          <div>
            <p className="text-gray-400 text-sm mb-1">Low Stock Items</p>
            <p className="text-3xl font-bold text-red-400">
              {inventory.filter((item) => item.stock_status === "low").length}
            </p>
          </div>

          <div>
            <p className="text-gray-400 text-sm mb-1">Good Stock Items</p>
            <p className="text-3xl font-bold text-green-400">
              {inventory.filter((item) => item.stock_status === "good").length}
            </p>
          </div>
        </div>
      </div>

      {/* Report Info */}
      <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
        <div className="flex items-start space-x-3">
          <svg
            className="w-6 h-6 text-indigo-400 mt-0.5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div>
            <h3 className="text-indigo-300 font-semibold mb-1">
              About Reports
            </h3>
            <p className="text-gray-300 text-sm">
              All reports are exported in CSV format and include timestamps. You
              can open them in Excel, Google Sheets, or any spreadsheet
              application for further analysis.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
