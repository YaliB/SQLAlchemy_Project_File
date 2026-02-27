import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

// import TopPostsPage from './pages/analytics/top-posts';

// // Render the specific page you just built
// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <TopPostsPage />
//   </React.StrictMode>
// )