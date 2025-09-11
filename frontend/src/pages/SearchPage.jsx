import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import allJobs from '../../../mainScrapper/all_jobs.json';
import GlassFooter from '../components/ui/GlassFooter';
import JobDetailsModal from '../components/ui/JobDetailsModal';

const SearchPage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('search');

  // Company logos mapping
  const companyLogos = {
    'NVIDIA': '/logos/nvidia.svg',
    'Apple': '/logos/apple-only.svg',
    'Google': '/logos/google-only.svg',
    'Microsoft': '/logos/microsoft-only.svg',
    'MICROSOFT': '/logos/microsoft-only.svg', // Handle all caps version
    'Meta': '/logos/meta-only.svg',
    'Amazon': '/logos/amazon.png',
    'Netflix': '/logos/netflix-only.svg',
    'Spotify': '/logos/spotify-only.svg',
    'Tesla': '/logos/tesla-logo.svg',
    'Stripe': '/logos/stripe-logo.svg',
    'Airbnb': '/logos/airbnb-logo.svg',
    'AMD': '/logos/amd.png',
    'Atlassian': '/logos/Atlassian-only.svg',
    'Adobe': '/logos/adobe-only.svg',
    'Slack': '/logos/slack-only.svg',
    'Loom': '/logos/loom-only.svg',
    'WhatsApp': '/logos/whatsapp-only.svg',
    'Yahoo': '/logos/yahoo.png',
    'GitHub': '/logos/github.png',
    'LinkedIn': '/logos/linkdin.png',
    'Instagram': '/logos/insta.png'
  };

  // Process job data with company logos
  const jobData = allJobs.map(job => ({
    ...job,
    logo: companyLogos[job.company] || `/logos/${(job.company || '').toLowerCase().replace(/\s+/g, '-')}.svg`
  }));

  // Filter jobs based on search query
  useEffect(() => {
    if (searchQuery.trim()) {
      const filtered = jobData.filter(job =>
        job.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setSearchResults(filtered.slice(0, 20)); // Limit to 20 results
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  // Handle job selection
  const handleJobSelect = (job) => {
    setSelectedJob(job);
    setIsModalOpen(true);
  };

  // Handle modal close
  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedJob(null);
  };


  // Handle back navigation
  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-white">
      {/* Header */}
      <div className="px-4 sm:px-6 max-w-6xl mx-auto flex flex-col items-center justify-start pt-10 pb-20">
        <h1 id="search-page-title" className="text-center text-3xl sm:text-5xl md:text-6xl font-extrabold notification-text tracking-tight opacity-90">
          Search Jobs
        </h1>
        
      </div>

      {/* Search Section */}
      <div className="px-6 pb-6">
        <div className="max-w-2xl mx-auto">
          <div id="search-input-container" className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none z-100">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search job titles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent backdrop-blur-sm"
              autoFocus
            />
          </div>
        </div>
      </div>

      {/* Search Results */}
      <div className="px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          {searchQuery.trim() ? (
            searchResults.length > 0 ? (
              <div className="space-y-4">
                <h2 className="text-lg font-semibold text-gray-300 mb-4">
                  Found {searchResults.length} job{searchResults.length !== 1 ? 's' : ''}
                </h2>
                {searchResults.map((job, index) => (
                  <div
                    key={`${job.company}-${job.title}-${index}`}
                    className="bg-white/5 border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-colors cursor-pointer"
                    onClick={() => handleJobSelect(job)}
                  >
                    <div className="flex items-start gap-4">
                      {/* Company Logo */}
                      <div className="w-12 h-12 bg-white/10 border border-white/20 rounded-full flex items-center justify-center flex-shrink-0">
                        <img
                          src={job.logo}
                          alt={`${job.company} logo`}
                          className="w-8 h-8 object-contain"
                          onError={(e) => {
                            const img = e.currentTarget;
                            if (img.src.includes('-only')) {
                              img.src = img.src.replace('-only', '');
                            }
                          }}
                        />
                      </div>

                      {/* Job Details */}
                      <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-semibold text-white mb-1 line-clamp-2">
                          {job.title}
                        </h3>
                        <p className="text-gray-300 mb-2">{job.company}</p>
                        
                        <div className="flex flex-wrap gap-4 text-sm text-gray-400">
                          {job.location && (
                            <div className="flex items-center gap-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                              </svg>
                              <span>{job.location}</span>
                            </div>
                          )}
                          {job.level && (
                            <div className="flex items-center gap-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                              </svg>
                              <span>{job.level}</span>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* View Job Button */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleJobSelect(job);
                        }}
                        className="bg-black text-white px-4 py-2 rounded-xl hover:bg-gray-800 transition-colors flex items-center gap-2 flex-shrink-0"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        View Job
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <h3 className="text-xl font-semibold text-gray-300 mb-2">No jobs found</h3>
                <p className="text-gray-400">Try adjusting your search terms</p>
              </div>
            )
          ) : (
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <h3 className="text-xl font-semibold text-gray-300 mb-2">Search for jobs</h3>
              <p className="text-gray-400">Enter a job title to find relevant positions</p>
            </div>
          )}
        </div>
      </div>

      {/* Job Details Modal */}
      <JobDetailsModal
        isOpen={isModalOpen}
        job={selectedJob}
        onClose={handleModalClose}
      />

      {/* Footer */}
      <GlassFooter 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onJobSelect={handleJobSelect} 
      />
    </div>
  );
};

export default SearchPage;
