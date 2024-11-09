"use client";
import { useState } from "react";
import { Score } from "./components/score";

export default function Home() {
  const [message, setMessage] = useState('2102 Hummingbird St Princeton, TX 75407');
  const [response, setResponse] = useState<{ message?: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:6969/?location=${message}`);
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <form onSubmit={handleSubmit} className="mb-8 flex flex-col gap-4">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          placeholder="Enter your message"
        />
        <button 
          type="submit"
          className="px-4 py-2 bg-blue-500 rounded hover:bg-blue-600 transition-colors text-black"
        >
          Get Response
        </button>
      </form>

      {response && (
        <div className="p-4 bg-gray-100 rounded-lg text-black">
          <Score score={(response as any).risk_score || 0} />
        </div>
      )}
    </div>
  );
}
