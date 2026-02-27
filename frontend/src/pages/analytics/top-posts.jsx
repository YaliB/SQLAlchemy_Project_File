import React, { useState, useEffect } from 'react';
// Correct relative paths based on your folder structure
import api from "../../api";           
import Login from "../../components/Login"; 
import Sidebar from "../../components/Sidebar"; 

// Sub-component for Sidebar Items
const NavItem = ({ label, icon }) => (
  <div className="flex items-center space-x-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition">
    <span className="text-xl">{icon}</span>
    <span className="font-medium text-gray-700">{label}</span>
  </div>
);

function TopPostsPage() {
  const [topPosts, setTopPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  // Check for existing token in localStorage
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Fetch data from the API
  useEffect(() => {
    if (token) {
      setLoading(true);
      api.get('/analytics/top-posts')
        .then(response => {
          setTopPosts(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching posts:", error);
          setLoading(false);
          // If token is invalid or expired, trigger logout
          if (error.response?.status === 401) handleLogout();
        });
    }
  }, [token]);

  const handleLoginSuccess = () => {
    setToken(localStorage.getItem('token'));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  // Render Login component if not authenticated
  if (!token) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar - Navigation */}
      <aside className="w-64 bg-white border-r border-gray-200 p-6 hidden md:block sticky top-0 h-screen">
        <h1 className="text-2xl font-bold text-blue-600 mb-8 px-3">Connectly</h1>
        <nav className="space-y-2">
          <NavItem label="Home" icon="🏠" />
          <NavItem label="Explore" icon="🔍" />
          <NavItem label="Analytics" icon="📊" />
          <NavItem label="Profile" icon="👤" />
        </nav>
        
        <div className="mt-auto pt-10">
          <button 
            onClick={handleLogout}
            className="w-full bg-red-50 text-red-600 p-2 rounded-lg font-medium hover:bg-red-100 transition"
          >
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 max-w-2xl mx-auto py-8 px-4">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold text-gray-800">Trending Dashboard</h2>
            <p className="text-sm text-gray-500">The most popular posts right now</p>
          </div>
        </header>

        {/* Loading Spinner */}
        {loading ? (
          <div className="flex justify-center py-10">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="space-y-6">
            {topPosts.length > 0 ? (
              topPosts.map((post) => (
                <div key={post.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition">
                  <div className="p-4 flex items-center space-x-3 border-b border-gray-50">
                     <div className="w-10 h-10 bg-gradient-to-tr from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        {post.user_name?.charAt(0) || 'U'}
                     </div>
                     <div>
                        <p className="font-semibold text-gray-900">{post.user_name || "Unknown User"}</p>
                        <p className="text-xs text-gray-400">Trending Post</p>
                     </div>
                  </div>
                  
                  <div className="p-4">
                    <p className="text-gray-800 text-lg leading-relaxed italic">
                      "{post.content}"
                    </p>
                  </div>

                  <div className="p-4 bg-gray-50 flex items-center justify-between">
                    <button className="flex items-center space-x-2 text-pink-600 font-semibold hover:bg-pink-100 px-3 py-1 rounded-full transition">
                      <span>❤️</span>
                      <span>{post.likes_count || 0} Likes</span>
                    </button>
                    <button className="text-gray-400 hover:text-blue-600 text-sm font-medium">
                      Share
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-center text-gray-500">No posts found.</p>
            )}
          </div>
        )}
      </main>

      {/* Right Sidebar - System Stats */}
      <aside className="w-80 p-8 hidden lg:block">
        <div className="bg-blue-600 rounded-2xl p-6 text-white shadow-lg shadow-blue-200 sticky top-8">
          <h3 className="font-bold text-lg mb-2">Network Status ⚡</h3>
          <p className="text-blue-100 text-sm mb-4">You are currently connected to the FastAPI SQLite production server.</p>
          <div className="text-2xl font-mono font-bold">{topPosts.length} Posts Loaded</div>
        </div>
      </aside>
    </div>
  );
}

export default TopPostsPage;