const AboutUs = () => {
  const teamMembers = [
    {
      name: 'Elias Missa',
      image: '/EliasPic.JPG',
      socialLinks: [
        { name: 'GitHub', url: 'https://github.com/Elias-Missa?tab=repositories' }
      ]
    },
    {
      name: 'Ann Ubaka',
      image: null,
      socialLinks: [
        { name: 'GitHub', url: 'https://github.com/svnsvnsvn' }
      ]
    }
  ]

  return (
    <div className="container w-[90%] max-w-6xl mx-auto px-5">
      <div className="text-center my-12">
        <h1 className="text-4xl mb-4 gradient-text">
          About This Project
        </h1>
        <p className="text-lg opacity-80 max-w-2xl mx-auto">
          A machine learning research project exploring rental listing anomaly detection
        </p>
      </div>
      
      <div className="bg-black bg-opacity-60 p-10 rounded-2xl my-12 border border-primary border-opacity-30 shadow-card">
        <h2 className="text-3xl mb-5 text-primary-light">
          Project Background
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          SNARE WEB started as a hackathon project aimed at exploring machine learning approaches to detect potentially fraudulent rental listings. What began as a weekend experiment evolved into a comprehensive research study demonstrating anomaly detection techniques applied to real estate data.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          This project focuses on the technical challenges of data collection, feature engineering, and anomaly detection rather than creating a production-ready consumer tool. We collected rental listing data primarily from Florida markets, engineered features around pricing patterns, geographic characteristics, and listing metadata, then experimented with multiple ML algorithms.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          The web interface demonstrates our research process, technical implementation, and the challenges we encountered working with real-world data. While the models show interesting patterns, they require significant additional work and validation before being suitable for practical application. This project serves as a portfolio piece showcasing data science, machine learning, and full-stack development skills.
        </p>
      </div>
      
      <div className="my-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {teamMembers.map((member, index) => (
            <div 
              key={index}
              className="bg-black rounded-2xl overflow-hidden border border-primary border-opacity-30 transition-all duration-300 hover:-translate-y-3 hover:shadow-card-hover shadow-card"
            >
              <div className="w-full h-80 relative overflow-hidden">
                {member.image ? (
                  <img 
                    src={member.image} 
                    alt={member.name}
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-main flex items-center justify-center">
                    <div className="text-4xl gradient-text">
                      {member.name.split(' ').map(n => n[0]).join('')}
                    </div>
                  </div>
                )}
              </div>
              
              <div className="p-6">
                <h3 className="text-2xl mb-3 text-primary-light">
                  {member.name}
                </h3>
                <div className="text-base opacity-70 mb-5">
                  {member.title}
                </div>
                <p className="leading-relaxed opacity-90 mb-5">
                  {member.bio}
                </p>
                <div className="flex gap-4 opacity-70">
                  {member.socialLinks.map((link, linkIndex) => (
                    <a 
                      key={linkIndex}
                      href={link.url} 
                      className="text-light no-underline transition-colors duration-300 hover:text-primary-light"
                    >
                      {link.name}
                    </a>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default AboutUs