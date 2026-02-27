import React, { useState } from 'react';
import api from '../api';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      const response = await api.post('/login', formData);
      localStorage.setItem('token', response.data.access_token);
      onLoginSuccess();
    } catch (err) { alert("Login failed"); }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-blue-600">
      <form onSubmit={handleSubmit} className="bg-white p-10 rounded-xl shadow-2xl">
        <h2 className="text-2xl font-bold mb-5">Login to Connectly</h2>
        <input 
          type="text" 
          placeholder="Username" 
          className="w-full p-2 border mb-4" 
          onChange={e => setUsername(e.target.value)} 
        />
        <input 
          type="password" 
          placeholder="Password" 
          className="w-full p-2 border mb-4" 
          onChange={e => setPassword(e.target.value)} 
        />
        <button className="w-full bg-blue-500 text-white p-2 rounded">Sign In</button>
      </form>
    </div>
  );
};

export default Login;