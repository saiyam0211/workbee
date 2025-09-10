import React, { useState, useEffect, useMemo } from 'react';
import GlassFooter from '@/components/ui/GlassFooter';
import SavedJobsPopup from '@/components/ui/saved-jobs-popup';
import { storageUtils } from '../utils/storage';

// Sample saved jobs data - this would come from your backend/API
const generateSavedJobs = (companyName, count, titlesOverride) => {
  const jobTitles = titlesOverride && titlesOverride.length > 0 ? titlesOverride : [
    'Software Engineer',
    'Frontend Developer',
    'Backend Developer',
    'Full Stack Developer',
    'DevOps Engineer',
    'Product Manager',
    'UI/UX Designer',
    'Data Scientist',
    'Machine Learning Engineer',
    'Cloud Architect'
  ];

  const locations = [
    'Seattle, Washington, USA',
    'San Francisco, California, USA',
    'New York, New York, USA',
    'London, UK',
    'Berlin, Germany',
    'Bangalore, Karnataka, India',
    'Mumbai, Maharashtra, India',
    'Stockholm, Sweden',
    'Sydney, Australia',
    'Toronto, Canada'
  ];

  const levels = ['Entry', 'Mid', 'Senior', 'Lead', 'Principal'];

  const jobs = [];
  for (let i = 0; i < count; i++) {
    jobs.push({
      id: `${companyName.toLowerCase()}-job-${i + 1}`,
      title: jobTitles[Math.floor(Math.random() * jobTitles.length)],
      location: locations[Math.floor(Math.random() * locations.length)],
      level: levels[Math.floor(Math.random() * levels.length)],
      postedDate: `${Math.floor(Math.random() * 30) + 1} days ago`,
      description: `Join ${companyName} as a talented professional to work on cutting-edge projects and help shape the future of technology. This role offers excellent growth opportunities and competitive compensation.`
    });
  }
  return jobs;
};

// Roles per company (from user request)
const companyRoles = {
  Google: ['Software Engineer', 'Data Scientist', 'SRE', 'ML Engineer'],
  Amazon: ['SDE', 'Product Manager', 'Data Engineer'],
  Apple: ['iOS Developer', 'Hardware Engineer', 'Software Engineer'],
  Microsoft: ['Software Engineer', 'Cloud Engineer', 'Security Engineer'],
  Meta: ['Frontend Engineer', 'Data Engineer', 'AR/VR Engineer'],
  AMD: ['Hardware Engineer', 'Software Engineer', 'Verification Engineer'],
  NVIDIA: ['AI Engineer', 'Graphics Engineer', 'Systems Engineer'],
  Yahoo: ['Full Stack Developer', 'Frontend Developer'],
  Stripe: ['Backend Engineer', 'Infrastructure Engineer'],
  Tesla: ['Autopilot Engineer', 'Battery Engineer', 'Software Engineer'],
  Airbnb: ['Frontend Engineer', 'Full Stack Engineer'],
  Spotify: ['Backend Engineer', 'Data Engineer']
};

const companies = [
  { name: 'Google', logo: '/logos/google-only.svg' },
  { name: 'Amazon', logo: '/logos/amazon.png' },
  { name: 'Apple', logo: '/logos/apple-logo.svg' },
  { name: 'Microsoft', logo: '/logos/microsoft-only.svg' },
  { name: 'Meta', logo: '/logos/meta-only.svg' },
  { name: 'AMD', logo: '/logos/amd.png' },
  { name: 'NVIDIA', logo: '/logos/nvidia-only.svg' },
  { name: 'Yahoo', logo: '/logos/yahoo.png' },
  { name: 'Stripe', logo: '/logos/stripe-logo.svg' },
  { name: 'Tesla', logo: '/logos/tesla-logo.svg' },
  { name: 'Airbnb', logo: '/logos/airbnb-only.svg' },
  { name: 'Spotify', logo: '/logos/spotify-only.svg' }
];

export default function FavCompanies() {
  const [activeTab, setActiveTab] = useState('saved');
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [modalSavedJobs, setModalSavedJobs] = useState([]);
  const [savedCounts, setSavedCounts] = useState(() => {
    return storageUtils.getAllJobCounts();
  });

  // Listen for updates from dashboard when user saves/unsaves jobs
  React.useEffect(() => {
    const updateCounts = () => {
      const counts = storageUtils.getAllJobCounts();
      setSavedCounts(counts);
      console.log('Updated saved counts:', counts);
    };

    updateCounts();
    window.addEventListener('wb:saved-jobs-updated', updateCounts);
    return () => window.removeEventListener('wb:saved-jobs-updated', updateCounts);
  }, []);

  const getSavedJobsFor = (companyName) => {
    return storageUtils.getCompanyJobs(companyName);
  };

  const handleCompanyClick = (company) => {
    setSelectedCompany(company);
    setIsPopupOpen(true);
  };

  const handleClosePopup = () => {
    setIsPopupOpen(false);
    setSelectedCompany(null);
  };

  // Dummy function for search modal (not used in fav-companies page)
  const handleJobSelect = () => {};

  // Filter companies to only show those with saved jobs
  const companiesWithSavedJobs = useMemo(() => {
    return companies.filter(company => (savedCounts[company.name] || 0) > 0);
  }, [savedCounts]);

  return (
    <div className="min-h-screen bg-[#09090b] text-foreground relative ">
      <div className="px-4 sm:px-6 max-w-6xl mx-auto min-h-[80vh] flex flex-col items-center justify-start pt-8 pb-40">
        <h1 className="text-center text-3xl sm:text-5xl md:text-6xl font-extrabold notification-text tracking-tight opacity-90"
        >
          Your Dream Companies
        </h1>
        {companiesWithSavedJobs.length === 0 ? (
          <div className="flex flex-col items-center justify-center mt-20 text-center">
            <div className="text-6xl mb-4">💼</div>
            <h2 className="text-2xl sm:text-3xl font-bold text-white/80 mb-2">No Saved Jobs Yet</h2>
            <p className="text-white/60 text-lg">Start exploring jobs and save your favorites to see them here!</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 sm:gap-8 mt-8 sm:mt-20 w-full ">
            {companiesWithSavedJobs.map((c) => (
            <div 
              key={c.name} 
              className="relative rounded-3xl sm:rounded-[50px] bg-gradient-to-b from-[#D9D9D9] to-[#8A8A8A] p-3 sm:p-4 shadow-2xl border border-white/20 aspect-square flex flex-col cursor-pointer hover:scale-105 transition-transform duration-200"
              onClick={() => handleCompanyClick(c)}
            >
              <div className="absolute right-3 sm:right-4 top-3 sm:top-4 w-8 h-8 sm:w-10 sm:h-10 bg-white/40 backdrop-blur-sm rounded-full flex items-center justify-center shadow-md border border-white/30">
                <img
                  src={c.logo}
                  alt={`${c.name} logo`}
                  className="w-6 h-6 sm:w-8 sm:h-8 object-contain"
                  onError={(e) => {
                    const img = e.currentTarget;
                    if (img.src.includes('-only')) {
                      img.src = img.src.replace('-only', '');
                    }
                  }}
                />
              </div>
              <div className="flex-1 flex items-start justify-center">
                <div
                  className="fav-companies-text mt-4 sm:mt-8 text-center"
                  style={{
                    background: 'linear-gradient(270deg, rgba(102, 102, 102, 0.25) 23.08%, rgba(0, 0, 0, 0.25) 60.1%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    color: 'transparent',
                    fontFamily: "SF Pro, SF Pro Display, SF Pro Text, -apple-system, 'Helvetica Neue', Arial, sans-serif",
                    fontStyle: 'normal',
                    fontWeight: 510,
                    fontSize: 'clamp(18px, 6vw, 44px)',
                    lineHeight: 1.1,
                    display: 'flex',
                    alignItems: 'center',
                    textAlign: 'center',
                  }}
                >
                  {c.name}
                </div>
              </div>
              <div className="flex items-end gap-2 text-black/70">
                <div className="text-3xl sm:text-4xl md:text-5xl font-extrabold leading-none">{savedCounts[c.name] || 0}</div>
                <div className="flex flex-col leading-tight">
                  <span className="text-xs sm:text-sm">View</span>
                  <span className="text-[10px] md:text-xs text-black/60">Saved Jobs</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        )}
      </div>

      {/* Saved Jobs Popup */}
      <SavedJobsPopup
        isOpen={isPopupOpen}
        onClose={handleClosePopup}
        company={selectedCompany}
        savedJobs={selectedCompany ? getSavedJobsFor(selectedCompany.name) : []}
      />

      <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} onJobSelect={handleJobSelect} />
    </div>
  );
}


