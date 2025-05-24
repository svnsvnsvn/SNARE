const HowItWorks = () => {
  const features = [
    {
      title: 'Price Analysis',
      description: 'Evaluates if the listing price is within market expectations',
      details: 'Our algorithm analyzes the listing price relative to the location, size, amenities, and current market conditions to determine if it\'s suspiciously below market value—a common tactic in rental scams.'
    },
    {
      title: 'Image Analysis',
      description: 'Detects suspicious patterns in listing photos',
      details: 'SNARE WEB scans images for signs of manipulation, watermarks from other sites, inconsistent lighting, and other indicators that photos may have been stolen from legitimate listings.'
    },
    {
      title: 'Text Pattern Recognition',
      description: 'Identifies suspicious language and content',
      details: 'Our NLP algorithms detect common linguistic patterns found in fraudulent listings, including urgency tactics, grammar issues, inconsistent details, and vague descriptions designed to hide a property\'s non-existence.'
    },
    {
      title: 'Contact Info Verification',
      description: 'Evaluates legitimacy of provided contact details',
      details: 'SNARE WEB analyzes listing contact information against known patterns of scammer behavior, including use of temporary email services, inconsistent area codes, and missing local address information.'
    },
    {
      title: 'Cross-Listing Detection',
      description: 'Checks if the same property appears elsewhere',
      details: 'Our system searches for duplicate listings across multiple platforms to identify if the same property is being advertised with different details or by different supposed landlords—a red flag for potential scams.'
    },
    {
      title: 'Payment Method Analysis',
      description: 'Evaluates requested payment methods for risk',
      details: 'SNARE WEB identifies high-risk payment requests like wire transfers, cryptocurrency, gift cards, or cash apps that offer no fraud protection—payment methods frequently demanded by scammers.'
    }
  ]

  return (
    <div className="container w-[90%] max-w-6xl mx-auto px-5">
      <div className="text-center my-12">
        <h1 className="text-4xl mb-4 gradient-text">
          How SNARE WEB Works
        </h1>
        <p className="text-lg opacity-80 max-w-2xl mx-auto">
          Advanced AI technology to detect apartment listing scams
        </p>
      </div>
      
      <div className="bg-black bg-opacity-60 p-8 rounded-2xl mb-10 border border-primary border-opacity-30 shadow-card">
        <h2 className="text-2xl mb-5 text-primary-light">
          Our Anomaly Detection Technology
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          SNARE WEB utilizes two powerful machine learning algorithms to identify potentially fraudulent apartment listings: Isolation Forest and DBSCAN (Density-Based Spatial Clustering of Applications with Noise).
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          Isolation Forest works by isolating observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature. Since recursive partitioning can be represented by a tree structure, the number of splittings required to isolate a sample is equivalent to the path length from the root node to the terminating node. This path length, averaged over a forest of random trees, is a measure of normality and our decision function. Anomalies are more susceptible to isolation and thus have shorter paths.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          DBSCAN is a density-based clustering algorithm that groups together points that are closely packed together, marking as outliers points that lie alone in low-density regions. This allows SNARE WEB to identify listings that deviate from normal patterns in the high-dimensional feature space that represents legitimate listings.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          By combining these two powerful algorithms, SNARE WEB can identify subtle patterns that humans might miss, providing you with a reliable assessment of a listing's legitimacy.
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