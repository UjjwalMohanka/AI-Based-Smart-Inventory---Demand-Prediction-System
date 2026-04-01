import React, { useState, useEffect } from "react";
import api from "../api/axios";
import PredictionForm from "../components/PredictionForm";
import DemandChart from "../components/DemandChart";

const Predictions = () => {
  const [products, setProducts] = useState([]);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get("/api/products");
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handlePredict = async (productId, monthsAhead) => {
    setLoading(true);
    setPredictionResult(null);
    setChartData([]);

    try {
      const response = await api.post("/api/predict", {
        product_id: productId,
        months_ahead: monthsAhead,
      });

      setPredictionResult(response.data);

      // Format data for chart
      const formatted = response.data.predictions.map((pred, idx) => ({
        month: `Month ${idx + 1}`,
        predicted: pred.predicted_qty,
      }));

      setChartData(formatted);
    } catch (error) {
      console.error("Error generating prediction:", error);
      alert(error.response?.data?.error || "Failed to generate prediction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">
          Demand Predictions
        </h1>
        <p className="text-gray-400">
          AI-powered demand forecasting using machine learning
        </p>
      </div>

      {/* Info Banner */}
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
            <h3 className="text-indigo-300 font-semibold mb-1">How it works</h3>
            <p className="text-gray-300 text-sm">
              Our ML model analyzes historical sales data including trends,
              seasonality, and patterns to predict future demand. The prediction
              accuracy (R² score) shows how well the model fits your historical
              data.
            </p>
          </div>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Prediction Form */}
        <PredictionForm
          products={products}
          onPredict={handlePredict}
          result={predictionResult}
          loading={loading}
        />

        {/* Prediction Chart */}
        {chartData.length > 0 ? (
          <DemandChart
            data={chartData}
            type="area"
            title="Predicted Demand Trend"
          />
        ) : (
          <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 flex items-center justify-center">
            <div className="text-center">
              <svg
                className="w-16 h-16 text-gray-600 mx-auto mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
              <p className="text-gray-400">
                Select a product and generate prediction to see the chart
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Model Information */}
      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4">
          📊 Model Details
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="text-gray-400 text-sm mb-2">Algorithm</h4>
            <p className="text-white font-medium">Linear Regression</p>
            <p className="text-xs text-gray-500 mt-1">
              Scikit-learn implementation
            </p>
          </div>

          <div>
            <h4 className="text-gray-400 text-sm mb-2">Features Used</h4>
            <ul className="text-sm text-gray-300 space-y-1">
              <li>• Time index & seasonality</li>
              <li>• Rolling averages</li>
              <li>• Lag features (1-2 months)</li>
              <li>• Trend component</li>
            </ul>
          </div>

          <div>
            <h4 className="text-gray-400 text-sm mb-2">Accuracy Metric</h4>
            <p className="text-white font-medium">R² Score</p>
            <p className="text-xs text-gray-500 mt-1">
              Closer to 1.0 = better predictions
              <br />
              0.7+ is considered good
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predictions;
