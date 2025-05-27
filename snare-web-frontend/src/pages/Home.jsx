import { useState } from 'react'

const Home = () => {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setResult('Checking the listing...')

    try {
      const response = await fetch('http://127.0.0.1:8000/check_listing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
      })

      if (response.ok) {
        const data = await response.json()
        setResult(`The listing for '${data.name}' is ${data.is_suspicious ? 'suspicious' : 'not suspicious'}.`)
      } else {
        setResult('Error: Could not check the listing. Please try again.')
      }
    } catch (error) {
      setResult(`Error: ${error.message}. Please try again.`)
    }
    
    setIsLoading(false)
  }

  return (
    <>
      {/* Background glow effects */}
      <div className="absolute top-[20%] left-[10%] w-[300px] h-[300px] rounded-full bg-gradient-radial from-primary/20 to-transparent blur-[30px] -z-10"></div>
      <div className="absolute bottom-[10%] right-[15%] w-[300px] h-[300px] rounded-full bg-gradient-radial from-primary/20 to-transparent blur-[30px] -z-10"></div>
      
      <main>
        {/* <div className="w-[90%] max-w-[1200px] mx-auto px-5"> */}
        <div>
          <div className="py-20 text-center flex flex-col items-center justify-center min-h-[calc(100vh-200px)]">
            <h1 className="text-5xl mb-5 font-normal bg-gradient-to-r from-primary to-purple-accent bg-clip-text text-transparent">
              Detect Apartment Scams with AI
            </h1>
            <p className="text-lg mb-10 max-w-[600px] leading-relaxed opacity-80">
              Don't fall victim to rental scams. Use our advanced AI technology to analyze listings and identify potential fraud before it's too late.
            </p>
            
            <div className="w-full max-w-[600px] mx-auto my-5 relative">
              <form onSubmit={handleSubmit}>
                <input 
                  type="text" 
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full py-4 px-5 rounded-full border border-primary bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_25px_rgba(138,43,226,0.5)] focus:border-primary-light"
                  style={{ boxShadow: '0 0 20px rgba(138, 43, 226, 0.3)' }}
                  placeholder="Enter listing URL here..."
                  disabled={isLoading}
                />
                <button 
                  type="submit"
                  disabled={isLoading || !url.trim()}
                  className="absolute right-[5px] top-[5px] py-[10px] px-6 rounded-[25px] bg-gradient-to-br from-primary to-purple-darker text-white border-none cursor-pointer font-medium transition-all duration-300 hover:-translate-y-0.5 hover:shadow-purple-button disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Analyzing...' : 'Analyze'}
                </button>
              </form>
            </div>
            
            <div className="my-8 text-center relative">
              <div className="before:content-[''] before:absolute before:w-[45%] before:h-px before:bg-white/20 before:top-1/2 before:left-0 after:content-[''] after:absolute after:w-[45%] after:h-px after:bg-white/20 after:top-1/2 after:right-0">
                <span className="bg-darker px-4 relative text-sm opacity-70">OR</span>
              </div>
            </div>
            
            <button className="bg-transparent text-light border border-primary py-3 px-8 rounded-[25px] text-base cursor-pointer transition-all duration-300 hover:bg-primary/10 hover:shadow-[0_0_15px_rgba(138,43,226,0.3)]">
              Enter Details Manually
            </button>

            {result && (
              <div className="mt-8 p-4 rounded-lg bg-black/40 border border-primary/30 max-w-2xl">
                <p className="text-light">{result}</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  )
}

export default Home
