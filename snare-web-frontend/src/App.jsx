import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './pages/Home'
import HowItWorks from './pages/HowItWorks'
import Why from './pages/Why'
import AboutUs from './pages/AboutUs'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-darker to-purple-end text-light relative">
        <Header />
        
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/why" element={<Why />} />
            <Route path="/about-us" element={<AboutUs />} />
          </Routes>
        </main>
        
        <Footer />
      </div>
    </Router>
  )
}

export default App