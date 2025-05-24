import { Link } from 'react-router-dom'

const Why = () => {
  const stats = [
    {
      number: '5.2M',
      description: 'Americans affected by rental scams annually'
    },
    {
      number: '$5.8B',
      description: 'Financial losses from rental scams each year'
    },
    {
      number: '43%',
      description: 'Of renters have encountered a rental scam'
    },
    {
      number: '36%',
      description: 'Of victims lost over $1,000 to scammers'
    }
  ]

  return (
    <div className="container w-[90%] max-w-6xl mx-auto px-5">
      <div className="text-center my-12">
        <h1 className="text-4xl mb-4 gradient-text">
          Why We Built SNARE WEB
        </h1>
        <p className="text-lg opacity-80 max-w-2xl mx-auto">
          The growing epidemic of rental scams in America and how we're fighting back
        </p>
      </div>
      
      <div className="bg-black bg-opacity-60 p-10 rounded-2xl my-8 border border-primary border-opacity-30 shadow-card">
        <h2 className="text-3xl mb-5 text-primary-light">
          The Crisis of Rental Scams
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          Apartment rental scams have reached epidemic proportions across the United States, causing financial devastation, emotional trauma, and housing insecurity for countless victims. These sophisticated scams target vulnerable populations—students, first-time renters, low-income families, and individuals relocating under time pressure—who are often unfamiliar with rental processes or desperate to secure housing in competitive markets.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          Scammers manipulate this urgency by creating fake listings with below-market prices, stealing photos from legitimate properties, and fabricating entire rental histories. They use high-pressure tactics to extract security deposits, application fees, and even first month's rent—only for victims to discover that the property doesn't exist, isn't actually available, or was never owned by the "landlord" they've been communicating with.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          By the time the fraud is discovered, the scammer has disappeared with the victim's money, leaving them not only financially damaged but potentially homeless. The psychological toll is equally severe, with victims reporting increased anxiety, depression, and a lasting distrust of housing providers that can impact their ability to secure legitimate housing in the future.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 my-10">
          {stats.map((stat, index) => (
            <div 
              key={index}
              className="bg-card-bg p-6 rounded-xl text-center border border-primary border-opacity-30 transition-all duration-300 hover:-translate-y-2 hover:shadow-card-hover relative overflow-hidden group"
            >
              <div className="absolute inset-0 rounded-xl p-0.5 bg-gradient-button opacity-60 group-hover:opacity-100 transition-opacity duration-300" style={{
                WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
                WebkitMaskComposite: 'xor',
                maskComposite: 'exclude'
              }}></div>
              
              <div className="text-5xl font-bold mb-3 gradient-text relative z-10">
                {stat.number}
              </div>
              <div className="text-base opacity-80 relative z-10">
                {stat.description}
              </div>
            </div>
          ))}
        </div>
        
        <h2 className="text-3xl mb-5 text-primary-light">
          Beyond Financial Loss
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          The impact of rental scams extends far beyond immediate financial losses. Victims often face emergency housing crises when they discover their "new apartment" doesn't exist. This can lead to temporary homelessness, forced stays in expensive hotels, or rushed decisions to accept substandard housing alternatives. For families with children, this instability can disrupt education and development. For working adults, it can threaten employment if they cannot commute to their workplace.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          Communities suffer as well. High rates of rental fraud damage neighborhood trust and cohesion. Legitimate property owners and managers face increased skepticism from potential renters. Local economies experience ripple effects as victims' financial losses impact their spending power and economic mobility. Housing markets become less efficient as legitimate listings receive fewer inquiries due to renter wariness.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          Law enforcement resources are strained by the volume of rental fraud cases, which are often complex and time-consuming to investigate, especially when scammers operate across jurisdictional boundaries or from overseas. Many victims never recover their lost funds, creating lasting financial hardship that can take years to overcome.
        </p>
        
        <h2 className="text-3xl mb-5 text-primary-light">
          Our Mission
        </h2>
        <p className="leading-relaxed mb-5 opacity-90">
          SNARE WEB was developed in response to this growing crisis. We believe that technology that enables scammers should be countered with technology that protects consumers. Our AI-powered platform gives renters the tools to identify potential fraud before they become victims—analyzing listings for the subtle patterns and red flags that might escape human detection.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          By combining machine learning algorithms like Isolation Forest and DBSCAN with our comprehensive database of known scam patterns, we're creating a shield for vulnerable renters. Our goal is to dramatically reduce successful rental scams, protect consumers' financial security, and restore trust to the rental marketplace.
        </p>
        
        <p className="leading-relaxed mb-5 opacity-90">
          We believe everyone deserves safe access to housing without fear of fraud or deception. SNARE WEB represents our commitment to that vision—a future where technology empowers rather than endangers renters in their search for a place to call home.
        </p>
      </div>
      
      <div className="text-center my-16">
        <Link 
          to="/" 
          className="bg-gradient-button text-white border-none py-4 px-10 text-lg rounded-full cursor-pointer transition-all duration-300 hover:-translate-y-1 hover:shadow-purple-hover no-underline inline-block"
        >
          Start Checking Listings Now
        </Link>
      </div>
    </div>
  )
}

export default Why