import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';


function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
const navigate = useNavigate();
  const handlelogin = (e) => {
    e.preventDefault();
    console.log('Email:', email);
    console.log('Password:', password);
    navigate('/chat');
    // هنا هنربط لاحقًا بـ API
  };

  return (
     <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handlelogin} className="bg-white p-8 rounded-lg shadow-lg w-800 space-y-4">
  <h2 className="text-3xl font-bold text-center text-blue-600">Login</h2>

  <input
    type="email"
    placeholder="Email"
    className="w-full border p-2 rounded"
    value={email}
    onChange={(e) => setEmail(e.target.value)}
    required
  />

  <input
    type="password"
    placeholder="Password"
    className="w-full border p-2 rounded"
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    required
  />

  <button type="submit" className="w-full bg-blue-600 text-whit px-6 py-4 rounded hover:bg-blue-700">
    Login
  </button>

  {/* ✅ رابط التسجيل */}
  <p className="text-sm text-center">
    Don't have an account?{" "}
    <Link to="/signup" className="text-blue-600 hover:underline">
      Sign up
    </Link>
  </p>
</form>
     
    </div>
    
  );
}

export default Login;
