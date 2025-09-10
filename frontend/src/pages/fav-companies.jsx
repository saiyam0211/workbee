import React, { useEffect, useMemo, useState } from 'react';
import GlassFooter from '@/components/ui/GlassFooter';
import SavedJobsPopup from '@/components/ui/saved-jobs-popup';

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
  { name: 'Google', logo: '/logos/google-only.svg', views: 14, savedJobs: generateSavedJobs('Google', 8, companyRoles.Google) },
  { name: 'Amazon', logo: '/logos/amazon.png', views: 12, savedJobs: generateSavedJobs('Amazon', 8, companyRoles.Amazon) },
  { name: 'Apple', logo: '/logos/apple-logo.svg', views: 11, savedJobs: generateSavedJobs('Apple', 8, companyRoles.Apple) },
  { name: 'Microsoft', logo: '/logos/microsoft-only.svg', views: 16, savedJobs: generateSavedJobs('Microsoft', 10, companyRoles.Microsoft) },
  { name: 'Meta', logo: '/logos/meta-only.svg', views: 9, savedJobs: generateSavedJobs('Meta', 8, companyRoles.Meta) },
  { name: 'AMD', logo: '/logos/amd.png', views: 7, savedJobs: generateSavedJobs('AMD', 6, companyRoles.AMD) },
  { name: 'NVIDIA', logo: '/logos/nvidia-only.svg', views: 18, savedJobs: generateSavedJobs('NVIDIA', 12, companyRoles.NVIDIA) },
  { name: 'Yahoo', logo: '/logos/yahoo.png', views: 4, savedJobs: generateSavedJobs('Yahoo', 4, companyRoles.Yahoo) },
  { name: 'Stripe', logo: '/logos/stripe-logo.svg', views: 5, savedJobs: generateSavedJobs('Stripe', 5, companyRoles.Stripe) },
  { name: 'Tesla', logo: '/logos/tesla-logo.svg', views: 8, savedJobs: generateSavedJobs('Tesla', 6, companyRoles.Tesla) },
  { name: 'Airbnb', logo: '/logos/airbnb-logo.svg', views: 6, savedJobs: generateSavedJobs('Airbnb', 5, companyRoles.Airbnb) },
  { name: 'Spotify', logo: '/logos/spotify-only.svg', views: 10, savedJobs: generateSavedJobs('Spotify', 6, companyRoles.Spotify) }
];

export default function FavCompanies() {
  const [activeTab, setActiveTab] = useState('saved');
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [modalSavedJobs, setModalSavedJobs] = useState([]);
  const [savedCounts, setSavedCounts] = useState(() => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      const saved = raw ? JSON.parse(raw) : {};
      const counts = {};
      Object.keys(saved).forEach((company) => {
        counts[company] = Object.keys(saved[company] || {}).length;
      });
      return counts;
    } catch {
      return {};
    }
  });

  // Listen for updates from dashboard when user saves/unsaves jobs
  React.useEffect(() => {
    const handler = () => {
      try {
        const raw = localStorage.getItem('wb_saved_jobs');
        const saved = raw ? JSON.parse(raw) : {};
        const counts = {};
        Object.keys(saved).forEach((company) => {
          counts[company] = Object.keys(saved[company] || {}).length;
        });
        setSavedCounts(counts);
      } catch {}
    };
    window.addEventListener('wb:saved-jobs-updated', handler);
    // Also refresh when page becomes visible again
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) handler();
    });
    return () => window.removeEventListener('wb:saved-jobs-updated', handler);
  }, []);

  const getSavedJobsFor = (companyName) => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      const saved = raw ? JSON.parse(raw) : {};
      const companyMap = saved[companyName] || {};
      return Object.values(companyMap);
    } catch {
      return [];
    }
  };

  const handleCompanyClick = (company) => {
    setSelectedCompany(company);
    setModalSavedJobs(getSavedJobsFor(company.name));
    setIsPopupOpen(true);
  };

  // When saved jobs change, update selected company job list shown in modal
  React.useEffect(() => {
    const syncSelected = () => {
      if (!selectedCompany) return;
      setModalSavedJobs(getSavedJobsFor(selectedCompany.name));
    };
    const listener = () => syncSelected();
    window.addEventListener('wb:saved-jobs-updated', listener);
    if (isPopupOpen) syncSelected();
    return () => window.removeEventListener('wb:saved-jobs-updated', listener);
  }, [isPopupOpen, selectedCompany?.name]);

  const handleClosePopup = () => {
    setIsPopupOpen(false);
    setSelectedCompany(null);
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-foreground relative ">
      <div className="px-4 sm:px-6 max-w-6xl mx-auto min-h-[80vh] flex flex-col items-center justify-start pb-20 pt-8 pb-40">
        <h1 className="text-center text-3xl sm:text-5xl md:text-6xl font-extrabold notification-text tracking-tight opacity-90"
        >
          Your Dream Companies
        </h1>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 sm:gap-8 mt-8 sm:mt-20 w-full ">
          {companies.map((c) => (
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
      </div>

      {/* Saved Jobs Popup */}
      <SavedJobsPopup
        isOpen={isPopupOpen}
        onClose={handleClosePopup}
        company={selectedCompany}
        savedJobs={modalSavedJobs}
      />

      <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
}


