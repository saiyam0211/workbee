import React, { useState, useEffect } from 'react';
import GlassFooter from '@/components/ui/GlassFooter';
import SavedJobsPopup from '@/components/ui/saved-jobs-popup';

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
  const [savedCounts, setSavedCounts] = useState({});

  useEffect(() => {
    const updateCounts = () => {
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

    updateCounts();
    window.addEventListener('wb:saved-jobs-updated', updateCounts);
    return () => window.removeEventListener('wb:saved-jobs-updated', updateCounts);
  }, []);

  const getSavedJobsFor = (companyName) => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      const saved = raw ? JSON.parse(raw) : {};
      return Object.values(saved[companyName] || {});
    } catch {
      return [];
    }
  };

  const handleCompanyClick = (company) => {
    setSelectedCompany(company);
    setIsPopupOpen(true);
  };

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
        savedJobs={selectedCompany ? getSavedJobsFor(selectedCompany.name) : []}
      />

      <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
}


