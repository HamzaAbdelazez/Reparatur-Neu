import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function ReparaturApp() {
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [history, setHistory] = useState([]); // ✅ جديد
  const navigate = useNavigate();

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSend = () => {
    if (!question.trim()) return;

    // أضف السؤال إلى السجل
    const newEntry = { type: "user", content: question };
    setHistory((prev) => [...prev, newEntry]);

    console.log("Sending question:", question);
    setQuestion("");

    // في المستقبل: أضف الرد من الـ backend هنا
    // const botResponse = "إجابة تجريبية من الروبوت";
    // setHistory((prev) => [...prev, { type: "bot", content: botResponse }]);
  };

  const handleSignOut = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      {/* Header */}
      <div className="w-full bg-blue-500 text-white text-3xl font-bold text-center p-4 relative rounded-b-lg">
        <span role="img" aria-label="bot">🤖</span> Reparatur
        <button
          onClick={handleSignOut}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
        >
          Logout
        </button>
      </div>

      {/* Main Content */}
      <div className="bg-white shadow-md rounded p-6 mt-8 w-full max-w-2xl text-center">
        <img
          src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
          alt="Robot"
          className="w-24 mx-auto mb-6"
        />

        <div className="mb-6 text-left">
          <h2 className="text-xl font-semibold mb-10">📄 Add PDF</h2>
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
        </div>

        <div className="text-left">
          <h2 className="text-xl font-semibold mb-10">🤖 Ask question</h2>
          <div className="flex">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="How can I help you..."
              className="flex-1 border p-2 rounded-l focus:outline-none"
            />
            <button
              onClick={handleSend}
              className="bg-blue-500 text-white px-4 rounded-r hover:bg-blue-600"
            >
              Send
            </button>
          </div>
        </div>

        {/* History Section */}
        <div className="mt-8 text-left max-h-60 overflow-y-auto border-t pt-4">
          <h3 className="text-lg font-semibold mb-2">🕘 History</h3>
          {history.length === 0 ? (
            <p className="text-gray-500 italic">No messages yet.</p>
          ) : (
            <ul className="space-y-2">
              {history.map((msg, index) => (
                <li
                  key={index}
                  className={`p-2 rounded ${
                    msg.type === "user" ? "bg-blue-100 text-right" : "bg-gray-200 text-left"
                  }`}
                >
                  {msg.content}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default ReparaturApp;
