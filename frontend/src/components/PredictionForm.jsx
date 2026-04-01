import React, { useState, useEffect } from "react";

const PredictionForm = ({ products, onPredict, result, loading }) => {
  const [selectedProduct, setSelectedProduct] = useState("");
  const [monthsAhead, setMonthsAhead] = useState(3);

  useEffect(() => {
    if (products && products.length > 0 && !selectedProduct) {
      setSelectedProduct(products[0].id.toString());
    }
  }, [products, selectedProduct]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedProduct) {
      onPredict(parseInt(selectedProduct), monthsAhead);
    }
  };

  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
      <h3 className="text-lg font-semibold text-white mb-4">
        Generate Prediction
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Select Product
          </label>
          <select
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
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
            Months Ahead: {monthsAhead}
          </label>
          <input
            type="range"
            min="1"
            max="6"
            value={monthsAhead}
            onChange={(e) => setMonthsAhead(parseInt(e.target.value))}
            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer slider"
          />
          <div className="flex justify-between text-xs text-gray-400 mt-1">
            <span>1 month</span>
            <span>6 months</span>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-lg transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Generating..." : "Generate Prediction"}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 bg-white/5 border border-white/10 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-white font-semibold">
              📦 {result.product_name}
            </h4>
            <span className="text-sm text-gray-400">
              Next {result.predictions.length} Months
            </span>
          </div>

          <div className="space-y-2 mb-4">
            {result.predictions.map((pred, idx) => {
              const change =
                idx > 0
                  ? (
                      ((pred.predicted_qty -
                        result.predictions[idx - 1].predicted_qty) /
                        result.predictions[idx - 1].predicted_qty) *
                      100
                    ).toFixed(1)
                  : 0;

              return (
                <div
                  key={idx}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="text-gray-300">Month {idx + 1}</span>
                  <div className="flex items-center space-x-2">
                    <span className="text-white font-medium">
                      {pred.predicted_qty} units
                    </span>
                    {idx > 0 && (
                      <span
                        className={`text-xs ${change > 0 ? "text-green-400" : "text-red-400"}`}
                      >
                        {change > 0 ? "↑" : "↓"} {Math.abs(change)}%
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="border-t border-white/10 pt-3 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Current Stock:</span>
              <span className="text-white font-medium">
                {result.current_stock} units
              </span>
            </div>

            {result.restock_needed && (
              <div className="p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                <p className="text-yellow-400 text-sm font-medium">
                  ⚠️ Restock Needed
                </p>
                <p className="text-gray-300 text-sm mt-1">
                  Order {result.suggested_order_qty} units
                </p>
              </div>
            )}

            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Model Accuracy (R²):</span>
              <span className="text-indigo-400 font-medium">
                {result.accuracy_score}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PredictionForm;
