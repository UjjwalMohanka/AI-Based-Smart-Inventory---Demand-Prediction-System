import React, { useState, useEffect } from "react";
import api from "../api/axios";
import StockTable from "../components/StockTable";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      const response = await api.get("/api/inventory");
      setInventory(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching inventory:", error);
      setLoading(false);
    }
  };

  const handleUpdateStock = async (productId, newQuantity) => {
    try {
      await api.put(`/api/inventory/${productId}`, {
        quantity_in_stock: newQuantity,
      });

      // Refresh inventory
      fetchInventory();

      // Show success message (you could use a toast library here)
      alert("Stock updated successfully!");
    } catch (error) {
      console.error("Error updating stock:", error);
      alert("Failed to update stock");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Loading inventory...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">
          Inventory Management
        </h1>
        <p className="text-gray-400">Monitor and update your stock levels</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
          <h3 className="text-gray-400 text-sm font-medium mb-2">
            Total Items
          </h3>
          <p className="text-3xl font-bold text-white">{inventory.length}</p>
        </div>

        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
          <h3 className="text-gray-400 text-sm font-medium mb-2">
            Low Stock Items
          </h3>
          <p className="text-3xl font-bold text-red-400">
            {inventory.filter((item) => item.stock_status === "low").length}
          </p>
        </div>

        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
          <h3 className="text-gray-400 text-sm font-medium mb-2">
            Warning Items
          </h3>
          <p className="text-3xl font-bold text-yellow-400">
            {inventory.filter((item) => item.stock_status === "warning").length}
          </p>
        </div>
      </div>

      {/* Inventory Table */}
      <StockTable inventory={inventory} onUpdateStock={handleUpdateStock} />
    </div>
  );
};

export default Inventory;
