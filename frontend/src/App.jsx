import { useEffect, useState } from 'react';
// import api from './api';
import Login from './components/Login';
import TopPostsPage from './pages/analytics/top-posts';

// Simple Nav Item Component
const NavItem = ({ label, icon }) => (
  <div className="flex items-center space-x-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition">
    <span className="text-xl">{icon}</span>
    <span className="font-medium text-gray-700">{label}</span>
  </div>
);

function App() {
  // State to track if the user is logged in
  const [token, setToken] = useState(localStorage.getItem('token'));

  // This function will be passed to the Login component
  const handleLoginSuccess = () => {
    setToken(localStorage.getItem('token'));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  // CONDITIONAL RENDERING:
  // If there's no token, show the Login screen
  if (!token) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  // If there's a token, show the Social Network Feed
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="p-4 bg-white shadow flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">Connectly</h1>
        <button 
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm"
        >
          Logout
        </button>
      </nav>

      <main className="p-8">
        <h2 className="text-2xl font-bold">Welcome back!</h2>
        <p>You are now authenticated with a JWT token.</p>
        {/* Your Feed/Analytics components go here */}
        <TopPostsPage />
      </main>
    </div>
  );
}

export default App;