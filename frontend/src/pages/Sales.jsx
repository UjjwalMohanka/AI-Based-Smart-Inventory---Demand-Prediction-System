import React, { useState, useEffect } from "react";
import api from "../api/axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const Sales = () => {
  const [products, setProducts] = useState([]);
  const [recentSales, setRecentSales] = useState([]);
  const [salesSummary, setSalesSummary] = useState([]);
  const [loading, setLoading] = useState(false);

  // Form state
  const [selectedProduct, setSelectedProduct] = useState("");
  const [quantity, setQuantity] = useState("");
  const [saleDate, setSaleDate] = useState(
    new Date().toISOString().split("T")[0],
  );

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [productsRes, salesRes, summaryRes] = await Promise.all([
        api.get("/api/products"),
        api.get("/api/sales/recent?limit=20"),
        api.get("/api/sales/summary"),
      ]);

      setProducts(productsRes.data);
      setRecentSales(salesRes.data);
      setSalesSummary(summaryRes.data);

      if (productsRes.data.length > 0) {
        setSelectedProduct(productsRes.data[0].id.toString());
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post("/api/sales", {
        product_id: parseInt(selectedProduct),
        quantity_sold: parseInt(quantity),
        sale_date: saleDate,
      });

      // Reset form
      setQuantity("");
      setSaleDate(new Date().toISOString().split("T")[0]);

      // Refresh data
      fetchData();

      alert("Sale recorded successfully!");
    } catch (error) {
      console.error("Error recording sale:", error);
      alert("Failed to record sale");
    } finally {
      setLoading(false);
    }
  };

  // Prepare chart data (monthly totals for current year)
  const currentYear = new Date().getFullYear();
  const chartData = salesSummary
    .filter((item) => item.year === currentYear)
    .reduce((acc, item) => {
      const monthKey = `${item.year}-${String(item.month).padStart(2, "0")}`;
      const existing = acc.find((d) => d.month === monthKey);

      if (existing) {
        existing[item.product_name] = item.total_sold;
      } else {
        acc.push({
          month: monthKey,
          [item.product_name]: item.total_sold,
        });
      }

      return acc;
    }, [])
    .sort((a, b) => a.month.localeCompare(b.month))
    .slice(-6); // Last 6 months

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Sales Management</h1>
        <p className="text-gray-400">Record and analyze sales transactions</p>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Log Sale Form */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Log New Sale
          </h3>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Product
              </label>
              <select
                value={selectedProduct}
                onChange={(e) => setSelectedProduct(e.target.value)}
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              >
                {products.map((product) => (
                  <option
                    key={product.id}
                    value={product.id}
                    className="bg-gray-900"
                  >
                    {product.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Quantity Sold
              </label>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter quantity"
                min="1"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Sale Date
              </label>
              <input
                type="date"
                value={saleDate}
                onChange={(e) => setSaleDate(e.target.value)}
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-lg transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Recording..." : "Record Sale"}
            </button>
          </form>
        </div>

        {/* Recent Sales */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Recent Sales
          </h3>

          <div className="space-y-3 max-h-96 overflow-y-auto">
            {recentSales.map((sale) => (
              <div
                key={sale.id}
                className="p-3 bg-white/5 border border-white/10 rounded-lg"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-white font-medium">
                    {sale.product_name}
                  </span>
                  <span className="text-indigo-400 font-semibold">
                    {sale.quantity_sold} units
                  </span>
                </div>
                <p className="text-xs text-gray-400">
                  {new Date(sale.sale_date).toLocaleDateString()}
                </p>
              </div>
            ))}

            {recentSales.length === 0 && (
              <p className="text-gray-400 text-center py-8">
                No sales recorded yet
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Sales Chart */}
      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">
          Monthly Sales Volume ({currentYear})
        </h3>

        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="month" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1f2937",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: "8px",
                }}
              />
              <Legend />
              {products.slice(0, 5).map((product, idx) => (
                <Bar
                  key={product.id}
                  dataKey={product.name}
                  fill={
                    ["#6366f1", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"][
                      idx % 5
                    ]
                  }
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-400 text-center py-8">
            No sales data available for chart
          </p>
        )}
      </div>
    </div>
  );
};

export default Sales;
