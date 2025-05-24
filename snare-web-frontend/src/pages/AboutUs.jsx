const AboutUs = () => {
  const teamMembers = [
    {
      name: 'Elias Missa',
      title: 'Founder & Lead Data Scientist',
      bio: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec ultricies. Nullam auctor, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec ultricies. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed euismod, nisl nec ultricies lacinia.',
      image: '/EliasPic.JPG',
      socialLinks: [
        { name: 'LinkedIn', url: '#' },
        { name: 'Twitter', url: '#' },
        { name: 'GitHub', url: '#' }
      ]
    },
    {
      name: 'Ann Ubaka',
      title: 'CTO & Algorithm Architect',
      bio: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec ultricies. Nullam auctor, nisl nec ultricies lacinia, nisl nisl aliquam nisl, nec ultricies nisl nisl nec ultricies. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed euismod, nisl nec ultricies lacinia.',
      image: null,
      socialLinks: [
        { name: 'LinkedIn', url: '#' },
        { name: 'Twitter', url: '#' },
        { name: 'GitHub', url: '#' }
      ]
    }
  ]

  return (
    <div className="container w-[90%] max-w-6xl mx-auto px-5">
      <div className="text-center my-12">
        <h1 className="text-4xl mb-4 gradient-text">
          About Us
        </h1>
        <p className="text-lg opacity-80 max-w-2xl mx-auto">
          Meet the team behind SNARE WEB
        </p>
      </div>
      
      <div className="bg-black bg-opacity-60 p-10 rounded-2xl my-12 border border-primary border-opacity-30 shadow-card">
        <h2 className="text-3xl mb-5 text-primary-light">
          Our Mission
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          At SNARE WEB, we're committed to creating a safer rental marketplace through innovative technology. Our mission is to empower renters with the tools they need to protect themselves from increasingly sophisticated scams that have devastated communities across America.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          Founded in 2024, SNARE WEB was born from our own experiences with rental fraud and our recognition that traditional approaches were failing to address this growing problem. We've combined expertise in machine learning, data science, and consumer protection to build an accessible solution that serves as a shield between vulnerable renters and would-be scammers.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          We believe that technology should enhance security, not compromise it. That's why we've built SNARE WEB as a transparent, user-focused platform that puts power back in the hands of renters. Our commitment extends beyond our technology—we regularly partner with consumer advocacy groups, housing organizations, and law enforcement to advance the broader fight against rental fraud.
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