import React, { useState } from "react";

const StockTable = ({ inventory, onUpdateStock }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editValue, setEditValue] = useState("");

  const getStatusColor = (status) => {
    switch (status) {
      case "low":
        return "bg-red-500/10 text-red-400 border-red-500/20";
      case "warning":
        return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20";
      default:
        return "bg-green-500/10 text-green-400 border-green-500/20";
    }
  };

  const getRowColor = (item) => {
    if (item.quantity_in_stock < item.reorder_point) {
      return "bg-red-500/5 border-red-500/20";
    } else if (item.quantity_in_stock < item.reorder_point * 2) {
      return "bg-yellow-500/5 border-yellow-500/20";
    }
    return "bg-white/5 border-white/10";
  };

  const filteredInventory = inventory.filter(
    (item) =>
      item.product_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.category?.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  const handleEdit = (item) => {
    setEditingId(item.product_id);
    setEditValue(item.quantity_in_stock.toString());
  };

  const handleSave = async (productId) => {
    await onUpdateStock(productId, parseInt(editValue));
    setEditingId(null);
  };

  const exportToCSV = () => {
    const headers = [
      "Product",
      "Category",
      "Stock",
      "Reorder Point",
      "Status",
      "Location",
    ];
    const rows = filteredInventory.map((item) => [
      item.product_name,
      item.category,
      item.quantity_in_stock,
      item.reorder_point,
      item.stock_status,
      item.warehouse_location || "N/A",
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.join(",")),
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `inventory-${new Date().toISOString().split("T")[0]}.csv`;
    a.click();
  };

  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">Inventory Status</h3>
        <div className="flex items-center space-x-3">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            onClick={exportToCSV}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors duration-200 flex items-center space-x-2"
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
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/10">
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Product
              </th>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Category
              </th>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Stock
              </th>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Reorder Point
              </th>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Status
              </th>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Location
              </th>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredInventory.map((item) => (
              <tr
                key={item.product_id}
                className={`border-b border-white/5 hover:bg-white/5 transition-colors ${getRowColor(item)}`}
              >
                <td className="py-3 px-4 text-white font-medium">
                  {item.product_name}
                </td>
                <td className="py-3 px-4 text-gray-300">{item.category}</td>
                <td className="py-3 px-4">
                  {editingId === item.product_id ? (
                    <input
                      type="number"
                      value={editValue}
                      onChange={(e) => setEditValue(e.target.value)}
                      className="w-20 px-2 py-1 bg-white/10 border border-white/20 rounded text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  ) : (
                    <span className="text-white">{item.quantity_in_stock}</span>
                  )}
                </td>
                <td className="py-3 px-4 text-gray-300">
                  {item.reorder_point}
                </td>
                <td className="py-3 px-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(item.stock_status)}`}
                  >
                    {item.stock_status}
                  </span>
                </td>
                <td className="py-3 px-4 text-gray-300">
                  {item.warehouse_location || "N/A"}
                </td>
                <td className="py-3 px-4">
                  {editingId === item.product_id ? (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleSave(item.product_id)}
                        className="text-green-400 hover:text-green-300"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => setEditingId(null)}
                        className="text-red-400 hover:text-red-300"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleEdit(item)}
                      className="text-indigo-400 hover:text-indigo-300"
                    >
                      Edit
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StockTable;
