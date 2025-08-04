import React, {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";

function ReparaturApp() {
    const [question, setQuestion] = useState("");
    const [file, setFile] = useState(null);
    const [uploadedPdf, setUploadedPdf] = useState(null);
    const [history, setHistory] = useState([]);
    const [userId, setUserId] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("not_uploaded");
    const navigate = useNavigate();

    useEffect(() => {
        const storedUser = localStorage.getItem("user");
        if (!storedUser) {
            navigate("/");
            return;
        }
        try {
            const parsed = JSON.parse(storedUser);
            setUserId(parsed.id);
        } catch {
            navigate("/");
        }
    }, [navigate]);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setUploadedPdf(null);
        setUploadStatus("not_uploaded");
    };

    const handleUploadPdf = async () => {
        if (!file) {
            alert("Please select a PDF file before uploading.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setUploadStatus("uploading");

            const response = await fetch(
                `http://localhost:8000/uploadedPdfs/?user_id=${userId}`,
                {
                    method: "POST",
                    body: formData,
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.error("Upload error:", error.detail);
                setUploadStatus("error");
                return;
            }

            const result = await response.json();
            setUploadedPdf(result);
            setUploadStatus("uploaded");
        } catch (error) {
            console.error("Error uploading PDF:", error);
            setUploadStatus("error");
        }
    };

    const handleSend = async (e) => {
        e.preventDefault();

        if (!question.trim()) return;

        const newEntry = {type: "user", content: question};
        setHistory((prev) => [...prev, newEntry]);
        setQuestion("");
    };

    const handleSignOut = () => {
        localStorage.removeItem("user");
        navigate("/");
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center">
            <div className="w-full bg-blue-500 text-white text-3xl font-bold text-center p-4 relative rounded-b-lg">
                🤖 Reparatur
                <button
                    onClick={handleSignOut}
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm"
                >
                    Logout
                </button>
            </div>

            <div className="bg-white shadow-md rounded p-6 mt-8 w-full max-w-2xl text-center">
                <img
                    src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
                    alt="Robot"
                    className="w-24 mx-auto mb-6"
                />

                {/* Upload PDF Section */}
                <div className="mb-6 text-left">
                    <h2 className="text-xl font-semibold mb-4">📄 Upload PDF</h2>
                    <div className="flex items-center justify-between space-x-2">
                        <input type="file" accept="application/pdf" onChange={handleFileChange}/>
                        <button
                            onClick={handleUploadPdf}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            Upload PDF
                        </button>
                    </div>

                    <div className="mt-2 text-sm">
                        {uploadStatus === "uploaded" && uploadedPdf && (
                            <span className="text-green-600">
                ✅ Uploaded: {uploadedPdf.original_filename || file.name}
              </span>
                        )}
                        {uploadStatus === "uploading" && (
                            <span className="text-blue-600">⏳ Uploading...</span>
                        )}
                        {uploadStatus === "error" && (
                            <span className="text-red-600">❌ Upload failed</span>
                        )}
                        {uploadStatus === "not_uploaded" && file && (
                            <span className="text-gray-600">⚠️ Not uploaded yet</span>
                        )}
                    </div>
                </div>

                {/* Ask Question */}
                <div className="text-left">
                    <h2 className="text-xl font-semibold mb-4">🤖 Ask a Question</h2>
                    <form onSubmit={handleSend} className="flex">
                        <input
                            type="text"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            placeholder="How can I help you..."
                            className="flex-1 border p-2 rounded-l focus:outline-none"
                            required
                            onKeyDown={(e) => {
                                if (e.key === "Enter" && !e.shiftKey) {
                                    handleSend(e);
                                }
                            }}
                        />
                        <button
                            type="submit"
                            className="bg-blue-500 hover:bg-blue-600 text-white px-4 rounded-r"
                        >
                            Send
                        </button>
                    </form>
                </div>

                {/* Chat History */}
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
                                        msg.type === "user"
                                            ? "bg-blue-100 text-right"
                                            : "bg-gray-200 text-left"
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
