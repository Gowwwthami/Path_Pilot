import React, { useState } from "react";
import { API_URL } from "./config";

const FinancialInsights = () => {
  const [query, setQuery] = useState("");
  const [stockSymbol, setStockSymbol] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query) return alert("Please enter a query");

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const response = await fetch(`${API_URL}/financial-insights`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          stock_symbol: stockSymbol || undefined
        })
      });

      if (!response.ok) throw new Error("Failed to get financial insights");

      const data = await response.json();
      setAnalysis(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Financial Insights AI
          </h1>
          <p className="text-gray-600">
            Get AI-powered market analysis and investment insights using RAG
          </p>
        </header>

        {/* Query Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Query
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., What are the best tech stocks to invest in for long-term growth?"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                rows="3"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Stock Symbol (Optional)
              </label>
              <input
                type="text"
                value={stockSymbol}
                onChange={(e) => setStockSymbol(e.target.value.toUpperCase())}
                placeholder="e.g., AAPL, MSFT, GOOGL"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition"
            >
              {loading ? "Analyzing..." : "Get Financial Insights"}
            </button>
          </form>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Analyzing market data...</p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Market Analysis */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Market Analysis
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-blue-900 mb-2">Summary</h3>
                  <p className="text-blue-800">{analysis.analysis?.summary}</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-green-900 mb-2">Market Trend</h3>
                  <p className="text-green-800 text-2xl font-bold">
                    {analysis.analysis?.market_trend}
                  </p>
                </div>
              </div>

              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 mb-2">Key Insights</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.analysis?.key_insights?.map((insight, idx) => (
                    <li key={idx} className="text-gray-700">{insight}</li>
                  ))}
                </ul>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg">
                <h3 className="font-semibold text-yellow-900 mb-2">Risk Factors</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.risk_factors?.map((risk, idx) => (
                    <li key={idx} className="text-yellow-800">{risk}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Stock Analysis */}
            {analysis.stock_analysis && analysis.stock_analysis.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  Stock Analysis
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {analysis.stock_analysis.map((stock, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-lg">{stock.symbol}</h3>
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          stock.trend === 'Bullish' ? 'bg-green-100 text-green-800' :
                          stock.trend === 'Bearish' ? 'bg-red-100 text-red-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {stock.trend}
                        </span>
                      </div>
                      <p className="text-gray-600 mb-2">{stock.name}</p>
                      <p className="text-2xl font-bold text-gray-900 mb-2">
                        ${stock.current_price}
                      </p>
                      <div className="mb-2">
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          stock.recommendation === 'Buy' ? 'bg-green-100 text-green-800' :
                          stock.recommendation === 'Sell' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {stock.recommendation}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">{stock.reasoning}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Investment Strategy */}
            {analysis.investment_strategy && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  Recommended Strategy
                </h2>
                <div className="bg-indigo-50 p-4 rounded-lg mb-4">
                  <h3 className="font-semibold text-indigo-900 mb-2">
                    {analysis.investment_strategy.recommended_approach}
                  </h3>
                  <p className="text-indigo-800 mb-2">
                    Time Horizon: {analysis.investment_strategy.time_horizon}
                  </p>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.investment_strategy.key_considerations?.map((consideration, idx) => (
                      <li key={idx} className="text-indigo-800">{consideration}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Recommended Actions */}
            {analysis.recommended_actions && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  Recommended Actions
                </h2>
                <ul className="space-y-2">
                  {analysis.recommended_actions.map((action, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-indigo-600 mr-2">✓</span>
                      <span className="text-gray-700">{action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Disclaimer */}
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              <p className="text-sm text-gray-600">
                <strong>Disclaimer:</strong> {analysis.disclaimer}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FinancialInsights;
