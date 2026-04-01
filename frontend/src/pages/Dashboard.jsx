import React, { useState, useEffect } from "react";
import api from "../api/axios";
import StatCard from "../components/StatCard";
import DemandChart from "../components/DemandChart";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get("/api/dashboard/stats");
      setStats(response.data);

      // If there's a top predicted product, fetch its predictions for chart
      if (response.data.top_predicted_demand) {
        const predResponse = await api.get(
          `/api/predict/history/${response.data.top_predicted_demand.product_id}`,
        );

        // Format data for chart
        const formatted = predResponse.data
          .slice(0, 6)
          .reverse()
          .map((pred) => ({
            month: `${pred.prediction_year}-${String(pred.prediction_month).padStart(2, "0")}`,
            predicted: pred.predicted_quantity,
          }));

        setChartData(formatted);
      }

      setLoading(false);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">
          Overview of your inventory and predictions
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Products"
          value={stats?.total_products || 0}
          icon="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
          color="indigo"
        />
        <StatCard
          title="Low Stock Alerts"
          value={stats?.low_stock_alerts || 0}
          icon="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          color="red"
        />
        <StatCard
          title="Total Stock Units"
          value={stats?.total_stock_value || 0}
          icon="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
          color="green"
        />
        <StatCard
          title="Prediction Accuracy"
          value={`${(stats?.prediction_accuracy_avg * 100 || 0).toFixed(1)}%`}
          icon="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          color="yellow"
        />
      </div>

      {/* Charts and Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Demand Chart */}
        <DemandChart
          data={chartData}
          type="line"
          title={`Demand Forecast - ${stats?.top_predicted_demand?.product_name || "N/A"}`}
        />

        {/* Top Predicted Demand */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">
            Top Predicted Demand
          </h3>
          {stats?.top_predicted_demand ? (
            <div className="space-y-4">
              <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-lg">
                <h4 className="text-indigo-400 font-semibold mb-2">
                  {stats.top_predicted_demand.product_name}
                </h4>
                <p className="text-3xl font-bold text-white mb-1">
                  {stats.top_predicted_demand.predicted_qty}{" "}
                  <span className="text-lg text-gray-400">units</span>
                </p>
                <p className="text-sm text-gray-400">
                  Predicted demand for upcoming months
                </p>
              </div>

              <div className="text-sm text-gray-400">
                This product has the highest forecasted demand. Consider
                reviewing stock levels and placing orders in advance.
              </div>
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">
              No predictions available yet
            </p>
          )}
        </div>
      </div>

      {/* Low Stock Alerts Table */}
      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">
          🚨 Low Stock Alerts ({stats?.low_stock_alerts || 0})
        </h3>

        {stats?.low_stock_items && stats.low_stock_items.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">
                    Product
                  </th>
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">
                    Current Stock
                  </th>
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">
                    Reorder Point
                  </th>
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">
                    Deficit
                  </th>
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">
                    Location
                  </th>
                </tr>
              </thead>
              <tbody>
                {stats.low_stock_items.map((item) => (
                  <tr
                    key={item.product_id}
                    className="border-b border-white/5 bg-red-500/5 hover:bg-red-500/10 transition-colors"
                  >
                    <td className="py-3 px-4 text-white font-medium">
                      {item.product_name}
                    </td>
                    <td className="py-3 px-4 text-red-400 font-semibold">
                      {item.quantity_in_stock}
                    </td>
                    <td className="py-3 px-4 text-gray-300">
                      {item.reorder_point}
                    </td>
                    <td className="py-3 px-4 text-red-400">
                      -{item.reorder_point - item.quantity_in_stock}
                    </td>
                    <td className="py-3 px-4 text-gray-300">
                      {item.warehouse_location || "N/A"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-green-400 text-center py-8">
            ✓ All products are adequately stocked!
          </p>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <a
          href="/predictions"
          className="block p-6 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl hover:shadow-xl hover:shadow-indigo-500/50 transition-all duration-200"
        >
          <h3 className="text-white font-semibold mb-2">Run Predictions</h3>
          <p className="text-indigo-100 text-sm">
            Generate demand forecasts for your products
          </p>
        </a>

        <a
          href="/inventory"
          className="block p-6 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl hover:shadow-xl hover:shadow-green-500/50 transition-all duration-200"
        >
          <h3 className="text-white font-semibold mb-2">Manage Inventory</h3>
          <p className="text-green-100 text-sm">
            Update stock levels and view details
          </p>
        </a>

        <a
          href="/sales"
          className="block p-6 bg-gradient-to-br from-yellow-600 to-orange-600 rounded-xl hover:shadow-xl hover:shadow-yellow-500/50 transition-all duration-200"
        >
          <h3 className="text-white font-semibold mb-2">Log Sales</h3>
          <p className="text-yellow-100 text-sm">
            Record new sales transactions
          </p>
        </a>
      </div>
    </div>
  );
};

export default Dashboard;
