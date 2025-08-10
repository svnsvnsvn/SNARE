import { Link, useLocation } from 'react-router-dom'

const Header = () => {
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname === path
  }

  return (
    <header className="py-5 border-b border-primary/30">
      <div className="w-[90%] max-w-[1200px] mx-auto px-5">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <div className="w-[125px] h-[125px] mr-4 rounded-[10px] overflow-hidden flex items-center justify-center bg-gradient-to-br from-darker to-purple-end shadow-[0_4px_8px_rgba(0,0,0,0.3)]">
              <img 
                src="/SnareLogo.png" 
                alt="SNARE WEB Logo" 
                className="w-full h-full object-cover rounded-[10px]"
              />
            </div>
            <div className="flex flex-col">
              <div className="text-2xl font-bold bg-gradient-to-r from-primary to-purple-accent bg-clip-text text-transparent tracking-wide">
                SNARE WEB
              </div>
              <div className="text-xs opacity-70 max-w-[300px] whitespace-nowrap">
                (Scam Network Anomaly Recognition Engine - Research Platform)
              </div>
            </div>
          </div>
          
          <nav className="flex items-center gap-8">
            <Link 
              to="/" 
              className={`text-light no-underline font-medium relative py-1 transition-all duration-300 hover:text-primary-light whitespace-nowrap group ${
                isActive('/') ? 'text-primary-light' : ''
              }`}
            >
              Home
              <span className={`absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-primary to-purple-accent transition-all duration-300 ${
                isActive('/') ? 'w-full' : 'w-0 group-hover:w-full'
              }`}></span>
            </Link>
            <Link 
              to="/how-it-works" 
              className={`text-light no-underline font-medium relative py-1 transition-all duration-300 hover:text-primary-light whitespace-nowrap group ${
                isActive('/how-it-works') ? 'text-primary-light' : ''
              }`}
            >
              How it Works
              <span className={`absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-primary to-purple-accent transition-all duration-300 ${
                isActive('/how-it-works') ? 'w-full' : 'w-0 group-hover:w-full'
              }`}></span>
            </Link>
            <Link 
              to="/why" 
              className={`text-light no-underline font-medium relative py-1 transition-all duration-300 hover:text-primary-light whitespace-nowrap group ${
                isActive('/why') ? 'text-primary-light' : ''
              }`}
            >
              Why
              <span className={`absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-primary to-purple-accent transition-all duration-300 ${
                isActive('/why') ? 'w-full' : 'w-0 group-hover:w-full'
              }`}></span>
            </Link>
            <Link 
              to="/about-us" 
              className={`text-light no-underline font-medium relative py-1 transition-all duration-300 hover:text-primary-light whitespace-nowrap group ${
                isActive('/about-us') ? 'text-primary-light' : ''
              }`}
            >
              About Us
              <span className={`absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-primary to-purple-accent transition-all duration-300 ${
                isActive('/about-us') ? 'w-full' : 'w-0 group-hover:w-full'
              }`}></span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header