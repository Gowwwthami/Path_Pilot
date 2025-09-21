import React from 'react';

export default function TestTailwind() {
  return (
    <div className="min-h-screen bg-red-500 flex items-center justify-center">
      <div className="bg-blue-500 text-white p-8 rounded-lg shadow-lg">
        <h1 className="text-4xl font-bold mb-4">Tailwind Test</h1>
        <p className="text-lg">If you can see this styled properly, Tailwind is working!</p>
        <div className="mt-4 bg-green-500 p-4 rounded">
          <p className="text-white font-semibold">This should be green with white text</p>
        </div>
      </div>
    </div>
  );
}
