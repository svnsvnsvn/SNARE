import { useState, useEffect } from 'react'
import apiService from '../services/apiService'
import Config from '../config/config'

const Home = () => {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState('')
  const [detailedResults, setDetailedResults] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [backendStatus, setBackendStatus] = useState('checking')
  const [showManualEntry, setShowManualEntry] = useState(false)
  const [manualData, setManualData] = useState({
    listing_name: '',
    price: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    bedrooms: '',
    bathrooms: '',
    square_footage: '',
    description: ''
  })

  // Check backend connectivity on component mount
  useEffect(() => {
    Config.logConfig(); // Log configuration in development
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await apiService.healthCheck();
      setBackendStatus('connected');
    } catch (error) {
      setBackendStatus('disconnected');
      console.warn('Backend health check failed:', error.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setResult('Processing listing data...')
    setDetailedResults(null)

    try {
      const data = await apiService.checkListing(url);
      
      // Basic result message
      const suspiciousText = data.is_suspicious ? 'FLAGGED AS ANOMALY' : 'APPEARS NORMAL';
      const confidenceText = `(Model confidence: ${Math.round(data.confidence_score * 100)}%)`;
      setResult(`Analysis of '${data.name}': ${suspiciousText} ${confidenceText}`);
      
      // Store detailed results for enhanced display
      setDetailedResults(data);
      
    } catch (error) {
      setResult(`Error: ${error.message}`)
      setDetailedResults(null);
      console.error('API Error:', error);
    }
    
    setIsLoading(false)
  }

  const handleManualSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setResult('Running anomaly detection models...')
    setDetailedResults(null)

    try {
      // Create a manual listing data object with current timestamp
      const listingData = {
        ...manualData,
        source: 'manual',
        listing_id: `manual_${Date.now()}`,
        time_posted: new Date().toISOString(),
        latitude: null,
        longitude: null,
        price: parseFloat(manualData.price) || 0,
        bedrooms: parseInt(manualData.bedrooms) || 0,
        bathrooms: parseFloat(manualData.bathrooms) || 0,
        square_footage: parseFloat(manualData.square_footage) || null
      }

      // Call the backend to analyze the manual data
      const data = await apiService.checkManualListing(listingData);
      
      // Basic result message
      const suspiciousText = data.is_suspicious ? 'FLAGGED AS ANOMALY' : 'APPEARS NORMAL';
      const confidenceText = `(Model confidence: ${Math.round(data.confidence_score * 100)}%)`;
      setResult(`Analysis of '${data.name}': ${suspiciousText} ${confidenceText}`);
      
      // Store detailed results for enhanced display
      setDetailedResults(data);
      
    } catch (error) {
      setResult(`Error: ${error.message}`)
      setDetailedResults(null);
      console.error('API Error:', error);
    }
    
    setIsLoading(false)
  }

  const handleManualInputChange = (field, value) => {
    // Handle numeric field validation
    if (['price', 'bedrooms', 'bathrooms', 'square_footage'].includes(field)) {
      // Allow empty string for clearing field
      if (value === '') {
        setManualData(prev => ({
          ...prev,
          [field]: value
        }))
        return
      }
      
      // Convert to number and validate
      const numValue = parseFloat(value)
      if (isNaN(numValue) || numValue < 0) {
        return // Don't update state for invalid values
      }
      
      // For bedrooms, ensure it's an integer
      if (field === 'bedrooms' && !Number.isInteger(numValue)) {
        return
      }
    }
    
    // Handle postal code validation - only allow digits
    if (field === 'postal_code') {
      // Allow empty string for clearing field
      if (value === '') {
        setManualData(prev => ({
          ...prev,
          [field]: value
        }))
        return
      }
      
      // Only allow digits (0-9)
      if (!/^\d+$/.test(value)) {
        return // Don't update state for non-numeric values
      }
      
      // Limit to reasonable ZIP code length (5-10 digits)
      if (value.length > 10) {
        return
      }
    }
    
    // Handle description field - sanitize for XSS protection
    if (field === 'description') {
      // Basic XSS prevention - remove/escape dangerous characters
      const sanitizedValue = value
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
        .replace(/<[^>]*>/g, '') // Remove all HTML tags
        .replace(/javascript:/gi, '') // Remove javascript: protocol
        .replace(/on\w+=/gi, '') // Remove event handlers like onclick=
        .slice(0, 2000) // Limit description length
      
      setManualData(prev => ({
        ...prev,
        [field]: sanitizedValue
      }))
      return
    }
    
    // Handle text fields that should be sanitized (address, listing_name)
    if (['address', 'listing_name'].includes(field)) {
      // Basic sanitization for text fields
      const sanitizedValue = value
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
        .replace(/<[^>]*>/g, '') // Remove all HTML tags
        .replace(/javascript:/gi, '') // Remove javascript: protocol
        .slice(0, 500) // Reasonable length limit
      
      setManualData(prev => ({
        ...prev,
        [field]: sanitizedValue
      }))
      return
    }
    
    setManualData(prev => ({
      ...prev,
      [field]: value
    }))
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
              Rental Scam Detection Research Platform
            </h1>
            <p className="text-lg mb-10 max-w-[600px] leading-relaxed opacity-80">
              Explore machine learning approaches to identifying potential rental fraud. This experimental platform demonstrates anomaly detection techniques applied to apartment listings.
            </p>
            
            <div className="w-full max-w-[600px] mx-auto my-5 relative">
              {!showManualEntry ? (
                // URL Entry Form
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
                    {isLoading ? 'Processing...' : 'Analyze'}
                  </button>
                </form>
              ) : (
                // Manual Entry Form
                <div className="w-full max-w-[800px] mx-auto">
                  <form onSubmit={handleManualSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Listing Name */}
                      <div className="md:col-span-2">
                        <input
                          type="text"
                          value={manualData.listing_name}
                          onChange={(e) => handleManualInputChange('listing_name', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="Listing Title/Name *"
                          disabled={isLoading}
                          required
                          maxLength="500"
                        />
                      </div>

                      {/* Price */}
                      <div>
                        <input
                          type="number"
                          value={manualData.price}
                          onChange={(e) => handleManualInputChange('price', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="Monthly Rent ($) *"
                          disabled={isLoading}
                          min="0"
                          step="1"
                          required
                        />
                      </div>

                      {/* Square Footage */}
                      <div>
                        <input
                          type="number"
                          value={manualData.square_footage}
                          onChange={(e) => handleManualInputChange('square_footage', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="Square Footage"
                          disabled={isLoading}
                          min="0"
                          step="1"
                        />
                      </div>

                      {/* Bedrooms */}
                      <div>
                        <input
                          type="number"
                          value={manualData.bedrooms}
                          onChange={(e) => handleManualInputChange('bedrooms', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="Bedrooms"
                          disabled={isLoading}
                          min="0"
                          max="10"
                          step="1"
                        />
                      </div>

                      {/* Bathrooms */}
                      <div>
                        <input
                          type="number"
                          step="0.5"
                          value={manualData.bathrooms}
                          onChange={(e) => handleManualInputChange('bathrooms', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="Bathrooms (e.g., 1.5)"
                          disabled={isLoading}
                          min="0"
                          max="10"
                        />
                      </div>

                      {/* Address */}
                      <div className="md:col-span-2">
                        <input
                          type="text"
                          value={manualData.address}
                          onChange={(e) => handleManualInputChange('address', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="Street Address"
                          disabled={isLoading}
                          maxLength="500"
                        />
                      </div>

                      {/* City */}
                      <div>
                        <select
                          value={manualData.city}
                          onChange={(e) => handleManualInputChange('city', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          disabled={isLoading}
                          required
                        >
                          <option value="">Select City *</option>
                          {/* Florida Cities - Primary focus */}
                          <option value="Jacksonville">Jacksonville</option>
                          <option value="Miami">Miami</option>
                          <option value="Tampa">Tampa</option>
                          <option value="Orlando">Orlando</option>
                          <option value="Fort Lauderdale">Fort Lauderdale</option>
                          <option value="Pensacola">Pensacola</option>
                          <option value="Gainesville">Gainesville</option>
                          <option value="Melbourne">Melbourne</option>
                          <option value="Cape Coral">Cape Coral</option>
                          <option value="Fort Myers">Fort Myers</option>
                          <option value="Lakeland">Lakeland</option>
                          <option value="Clearwater">Clearwater</option>
                          <option value="Sarasota">Sarasota</option>
                          <option value="West Palm Beach">West Palm Beach</option>
                          <option value="Hollywood">Hollywood</option>
                          <option value="Pompano Beach">Pompano Beach</option>
                          <option value="Boca Raton">Boca Raton</option>
                          <option value="Brandon">Brandon</option>
                          <option value="Kissimmee">Kissimmee</option>
                          <option value="Daytona Beach">Daytona Beach</option>
                          <option value="Tallahassee">Tallahassee</option>
                          <option value="Port Saint Lucie">Port Saint Lucie</option>
                          <option value="Coral Springs">Coral Springs</option>
                          <option value="Naples">Naples</option>
                          <option value="Bonita Springs">Bonita Springs</option>
                          <option value="Bradenton">Bradenton</option>
                        </select>
                      </div>

                      {/* State */}
                      <div>
                        <select
                          value={manualData.state}
                          onChange={(e) => handleManualInputChange('state', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          disabled={isLoading}
                          required
                        >
                          <option value="">Select State *</option>
                          <option value="FL">Florida</option>
                          <option value="AL">Alabama</option>
                          <option value="GA">Georgia</option>
                          <option value="TX">Texas</option>
                          <option value="CA">California</option>
                          <option value="NY">New York</option>
                          <option value="NC">North Carolina</option>
                          <option value="SC">South Carolina</option>
                          <option value="TN">Tennessee</option>
                          <option value="VA">Virginia</option>
                        </select>
                      </div>

                      {/* Postal Code */}
                      <div>
                        <input
                          type="text"
                          inputMode="numeric"
                          pattern="[0-9]*"
                          value={manualData.postal_code}
                          onChange={(e) => handleManualInputChange('postal_code', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light"
                          placeholder="ZIP Code"
                          disabled={isLoading}
                          maxLength="10"
                        />
                      </div>

                      {/* Description */}
                      <div className="md:col-span-2">
                        <textarea
                          value={manualData.description}
                          onChange={(e) => handleManualInputChange('description', e.target.value)}
                          className="w-full py-3 px-4 rounded-lg border border-primary/50 bg-black/60 text-light text-base transition-all duration-300 focus:outline-none focus:shadow-[0_0_15px_rgba(138,43,226,0.3)] focus:border-primary-light resize-none"
                          placeholder="Property Description"
                          rows="4"
                          disabled={isLoading}
                          maxLength="2000"
                        />
                        <div className="text-xs text-gray-400 mt-1 text-right">
                          {manualData.description.length}/2000 characters
                        </div>
                      </div>
                    </div>

                    {/* Submit Button */}
                    <div className="text-center mt-6">
                      <button 
                        type="submit"
                        disabled={isLoading || !manualData.listing_name.trim() || !manualData.price || !manualData.city || !manualData.state}
                        className="py-3 px-8 rounded-[25px] bg-gradient-to-br from-primary to-purple-darker text-white border-none cursor-pointer font-medium transition-all duration-300 hover:-translate-y-0.5 hover:shadow-purple-button disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isLoading ? 'Processing...' : 'Run Analysis'}
                      </button>
                      {(!manualData.listing_name.trim() || !manualData.price || !manualData.city || !manualData.state) && (
                        <p className="text-sm text-gray-400 mt-2">Please fill in listing name, price, city, and state</p>
                      )}
                    </div>
                  </form>
                </div>
              )}
            </div>
            
            <div className="my-8 text-center relative">
              <div className="before:content-[''] before:absolute before:w-[45%] before:h-px before:bg-white/20 before:top-1/2 before:left-0 after:content-[''] after:absolute after:w-[45%] after:h-px after:bg-white/20 after:top-1/2 after:right-0">
                <span className="bg-darker px-4 relative text-sm opacity-70">OR</span>
              </div>
            </div>
            
            <button 
              onClick={() => setShowManualEntry(!showManualEntry)}
              className="bg-transparent text-light border border-primary py-3 px-8 rounded-[25px] text-base cursor-pointer transition-all duration-300 hover:bg-primary/10 hover:shadow-[0_0_15px_rgba(138,43,226,0.3)]"
            >
              {showManualEntry ? 'Back to URL Entry' : 'Enter Details Manually'}
            </button>

            {result && (
              <div className="mt-8 p-4 rounded-lg bg-black/40 border border-primary/30 max-w-2xl">
                <p className="text-light">{result}</p>
              </div>
            )}

            {/* Detailed Analysis Results */}
            {detailedResults && (
              <div className="mt-6 w-full max-w-4xl space-y-6">
                
                {/* Overall Analysis Card */}
                <div className={`p-6 rounded-lg border ${detailedResults.is_suspicious ? 'bg-red-900/20 border-red-500/30' : 'bg-green-900/20 border-green-500/30'}`}>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-light">Model Analysis Results</h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${detailedResults.is_suspicious ? 'bg-red-500/20 text-red-300' : 'bg-green-500/20 text-green-300'}`}>
                      {detailedResults.is_suspicious ? 'ANOMALY DETECTED' : 'NORMAL PATTERN'}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary">{Math.round(detailedResults.confidence_score * 100)}%</div>
                      <div className="text-sm text-gray-400">Model Confidence</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary">{detailedResults.anomaly_score?.toFixed(3) || 'N/A'}</div>
                      <div className="text-sm text-gray-400">Anomaly Score</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary">
                        {detailedResults.scraped_data?.price ? `$${detailedResults.scraped_data.price}` : 'N/A'}
                      </div>
                      <div className="text-sm text-gray-400">Listed Price</div>
                    </div>
                  </div>
                </div>

                {/* Model Predictions */}
                {detailedResults.model_predictions && (
                  <div className="p-6 rounded-lg bg-black/40 border border-primary/30">
                    <h3 className="text-xl font-semibold text-light mb-4">Machine Learning Model Outputs</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      
                      {/* Isolation Forest */}
                      {detailedResults.model_predictions.isolation_forest && (
                        <div className="p-4 rounded-lg bg-purple-900/20 border border-purple-500/30">
                          <h4 className="font-semibold text-purple-300 mb-2">Isolation Forest</h4>
                          <div className="space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-gray-400">Result:</span>
                              <span className={detailedResults.model_predictions.isolation_forest.is_anomaly ? 'text-red-300' : 'text-green-300'}>
                                {detailedResults.model_predictions.isolation_forest.is_anomaly ? 'Anomaly' : 'Normal'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Score:</span>
                              <span className="text-light">{detailedResults.model_predictions.isolation_forest.score?.toFixed(3)}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* DBSCAN */}
                      {detailedResults.model_predictions.dbscan && (
                        <div className="p-4 rounded-lg bg-blue-900/20 border border-blue-500/30">
                          <h4 className="font-semibold text-blue-300 mb-2">DBSCAN Clustering</h4>
                          <div className="space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-gray-400">Result:</span>
                              <span className={detailedResults.model_predictions.dbscan.is_anomaly ? 'text-red-300' : 'text-green-300'}>
                                {detailedResults.model_predictions.dbscan.is_noise ? 'Outlier' : 'Clustered'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Cluster:</span>
                              <span className="text-light">{detailedResults.model_predictions.dbscan.cluster}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* LOF */}
                      {detailedResults.model_predictions.lof && (
                        <div className="p-4 rounded-lg bg-orange-900/20 border border-orange-500/30">
                          <h4 className="font-semibold text-orange-300 mb-2">Local Outlier Factor</h4>
                          <div className="space-y-1 text-sm">
                            <div className="flex justify-between">
                              <span className="text-gray-400">Result:</span>
                              <span className={detailedResults.model_predictions.lof.is_anomaly ? 'text-red-300' : 'text-green-300'}>
                                {detailedResults.model_predictions.lof.is_anomaly ? 'Outlier' : 'Normal'}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Score:</span>
                              <span className="text-light">{detailedResults.model_predictions.lof.score?.toFixed(3)}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Feature Analysis */}
                {detailedResults.analysis && (
                  <div className="p-6 rounded-lg bg-black/40 border border-primary/30">
                    <h3 className="text-xl font-semibold text-light mb-4">Feature Analysis</h3>
                    
                    {/* Suspicious Indicators */}
                    {detailedResults.analysis.suspicious_indicators && detailedResults.analysis.suspicious_indicators.length > 0 && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-red-300 mb-2">Suspicious Indicators</h4>
                        <ul className="space-y-1">
                          {detailedResults.analysis.suspicious_indicators.map((indicator, index) => (
                            <li key={index} className="text-red-200 text-sm">• {indicator}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Key Features */}
                    {detailedResults.analysis.key_features && (
                      <div>
                        <h4 className="font-semibold text-light mb-2">Key Metrics</h4>
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-sm">
                          {Object.entries(detailedResults.analysis.key_features).map(([key, value]) => (
                            <div key={key} className="p-2 rounded bg-gray-800/50">
                              <div className="text-gray-400 text-xs capitalize">{key.replace(/_/g, ' ')}</div>
                              <div className="text-light font-medium">
                                {typeof value === 'number' ? 
                                  (key.includes('price') ? `$${value.toFixed(0)}` : value.toFixed(2)) : 
                                  value.toString()
                                }
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Listing Details */}
                {detailedResults.scraped_data && (
                  <div className="p-6 rounded-lg bg-black/40 border border-primary/30">
                    <h3 className="text-xl font-semibold text-light mb-4">Listing Details</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="space-y-2">
                          <div><span className="text-gray-400">Address:</span> <span className="text-light">{detailedResults.scraped_data.address || 'N/A'}</span></div>
                          <div><span className="text-gray-400">City:</span> <span className="text-light">{detailedResults.scraped_data.city || 'N/A'}</span></div>
                          <div><span className="text-gray-400">State:</span> <span className="text-light">{detailedResults.scraped_data.state || 'N/A'}</span></div>
                          <div><span className="text-gray-400">Bedrooms:</span> <span className="text-light">{detailedResults.scraped_data.bedrooms || 'N/A'}</span></div>
                          <div><span className="text-gray-400">Bathrooms:</span> <span className="text-light">{detailedResults.scraped_data.bathrooms || 'N/A'}</span></div>
                        </div>
                      </div>
                      <div>
                        <div className="space-y-2">
                          <div><span className="text-gray-400">Square Footage:</span> <span className="text-light">{detailedResults.scraped_data.square_footage || 'N/A'}</span></div>
                          <div><span className="text-gray-400">Posted:</span> <span className="text-light">{detailedResults.scraped_data.time_posted ? new Date(detailedResults.scraped_data.time_posted).toLocaleDateString() : 'N/A'}</span></div>
                          <div><span className="text-gray-400">Source:</span> <span className="text-light capitalize">{detailedResults.scraped_data.source || 'N/A'}</span></div>
                          <div><span className="text-gray-400">Listing ID:</span> <span className="text-light">{detailedResults.scraped_data.listing_id || 'N/A'}</span></div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Description Preview */}
                    {detailedResults.scraped_data.description && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-light mb-2">Description Preview</h4>
                        <div className="p-3 rounded bg-gray-800/50 text-sm text-gray-300 max-h-32 overflow-y-auto">
                          {detailedResults.scraped_data.description.slice(0, 300)}
                          {detailedResults.scraped_data.description.length > 300 && '...'}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  )
}

export default Home
