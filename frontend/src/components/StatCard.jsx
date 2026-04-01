import React from "react";

const StatCard = ({ title, value, icon, trend, color = "indigo" }) => {
  const colorClasses = {
    indigo: "from-indigo-500 to-purple-600",
    green: "from-green-500 to-emerald-600",
    yellow: "from-yellow-500 to-orange-600",
    red: "from-red-500 to-pink-600",
  };

  return (
    <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:bg-white/10 transition-all duration-200">
      <div className="flex items-center justify-between mb-4">
        <div
          className={`w-12 h-12 bg-gradient-to-br ${colorClasses[color]} rounded-lg flex items-center justify-center`}
        >
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
              d={icon}
            />
          </svg>
        </div>
        {trend && (
          <span
            className={`text-sm font-medium ${trend > 0 ? "text-green-400" : "text-red-400"}`}
          >
            {trend > 0 ? "↑" : "↓"} {Math.abs(trend)}%
          </span>
        )}
      </div>
      <h3 className="text-gray-400 text-sm font-medium mb-1">{title}</h3>
      <p className="text-3xl font-bold text-white">{value}</p>
    </div>
  );
};

export default StatCard;
