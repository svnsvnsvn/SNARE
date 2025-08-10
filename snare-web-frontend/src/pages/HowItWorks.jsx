const HowItWorks = () => {
  const features = [
    {
      title: 'Price Pattern Analysis',
      description: 'Examines pricing relative to market expectations',
      details: 'The model analyzes listing prices in relation to location, size, and amenities to identify potential outliers that may indicate below-market pricing patterns often associated with fraudulent listings.'
    },
    {
      title: 'Feature Extraction',
      description: 'Processes listing characteristics for analysis',
      details: 'Multiple property features are extracted and normalized, including spatial data, temporal patterns, and listing metadata to create a comprehensive feature vector for anomaly detection algorithms.'
    },
    {
      title: 'Text Analysis (Experimental)',
      description: 'Explores linguistic patterns in descriptions',
      details: 'Experimental natural language processing techniques examine listing descriptions for patterns that may correlate with fraudulent content, though this feature requires significant additional validation.'
    },
    {
      title: 'Geographic Clustering',
      description: 'Analyzes spatial distribution patterns',
      details: 'Location-based features are examined using density clustering to identify listings that appear geographically isolated or inconsistent with known neighborhood patterns.'
    },
    {
      title: 'Temporal Pattern Recognition',
      description: 'Studies listing timing and duration patterns',
      details: 'Research into posting times, listing durations, and update frequencies to identify potentially suspicious temporal behaviors in listing management.'
    },
    {
      title: 'Multi-Model Ensemble',
      description: 'Combines multiple detection approaches',
      details: 'Different machine learning models (Isolation Forest, DBSCAN, LOF) are combined to provide a more robust anomaly detection framework, though individual model performance varies significantly.'
    }
  ]

  return (
    <div className="container w-[90%] max-w-6xl mx-auto px-5">
      <div className="text-center my-12">
        <h1 className="text-4xl mb-4 gradient-text">
          Research Methodology
        </h1>
        <p className="text-lg opacity-80 max-w-2xl mx-auto">
          Exploring machine learning approaches for rental listing anomaly detection
        </p>
      </div>
      
      <div className="bg-black bg-opacity-60 p-8 rounded-2xl mb-10 border border-primary border-opacity-30 shadow-card">
        <h2 className="text-2xl mb-5 text-primary-light">
          Experimental Anomaly Detection Approach
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          This research platform experiments with three machine learning algorithms to identify potentially fraudulent apartment listings: Isolation Forest, DBSCAN (Density-Based Spatial Clustering of Applications with Noise), and LOF (Local Outlier Factor).
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          Isolation Forest works by isolating observations through random feature selection and split values. The algorithm builds trees where anomalous patterns require fewer splits to isolate, making them detectable through shorter path lengths. This approach is particularly effective for identifying outliers in rental pricing and property characteristics.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          DBSCAN identifies density-based clusters in the feature space, marking isolated points as outliers. This helps detect listings that deviate significantly from normal patterns in the multi-dimensional space of legitimate rental properties.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          LOF (Local Outlier Factor) measures the local density deviation of a data point with respect to its neighbors. It identifies anomalies as points that have a substantially lower density than their neighbors, making it effective for detecting local outliers that might be missed by global methods.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          <strong>Note:</strong> This is an experimental platform for research purposes. The models are trained on limited data and should not be used as the sole basis for rental decisions. Results are exploratory and require further validation.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-12">
        {features.map((feature, index) => (
          <div 
            key={index}
            className="bg-card-bg rounded-xl p-6 border border-primary border-opacity-30 transition-all duration-300 cursor-pointer relative overflow-hidden group hover:shadow-card-hover"
          >
            {/* Glow effect */}
            <div className="absolute inset-0 bg-gradient-radial from-primary/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            {/* Border glow effect */}
            <div className="absolute inset-0 rounded-xl p-0.5 bg-gradient-button opacity-60 group-hover:opacity-100 transition-opacity duration-300" style={{
              WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
              WebkitMaskComposite: 'xor',
              maskComposite: 'exclude'
            }}></div>
            
            {/* Content */}
            <div className="relative z-10">
              <h3 className="text-xl mb-4 text-primary-light transition-opacity duration-300 group-hover:opacity-0">
                {feature.title}
              </h3>
              <p className="transition-opacity duration-300 group-hover:opacity-0">
                {feature.description}
              </p>
            </div>
            
            {/* Hover content */}
            <div className="absolute inset-0 bg-black bg-opacity-95 flex items-center justify-center p-5 opacity-0 translate-y-3 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300 rounded-xl text-center z-20">
              <p className="text-sm leading-relaxed">
                {feature.details}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default HowItWorks