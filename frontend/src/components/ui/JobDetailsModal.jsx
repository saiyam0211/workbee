import React, { useEffect, useRef, useState } from 'react';

const JobDetailsModal = ({ isOpen, job, onClose, onApply }) => {
  const [touchStart, setTouchStart] = useState(null);
  const [touchEnd, setTouchEnd] = useState(null);
  const modalRef = useRef(null);

  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      return () => {
        document.body.style.overflow = 'unset';
      };
    }
  }, [isOpen]);

  // Handle swipe to close on mobile
  const handleTouchStart = (e) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientY);
  };

  const handleTouchMove = (e) => {
    setTouchEnd(e.targetTouches[0].clientY);
  };

  const handleTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isUpSwipe = distance > 50;
    
    // Only close on upward swipe from the top of the modal
    if (isUpSwipe && modalRef.current && modalRef.current.scrollTop === 0) {
      onClose();
    }
  };

  if (!isOpen || !job) return null;

  const companyName = job.company || job.company_name || 'Company';
  const logo = job.logo || `/logos/${(companyName || '').toLowerCase().replace(/\s+/g, '-')}.svg`;

  return (
    <div 
      className="fixed inset-0 z-[999999] flex items-end sm:items-center justify-center bg-black/80 backdrop-blur-sm" 
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      {/* Mobile: Full height modal, Desktop: Centered modal */}
      <div 
        ref={modalRef}
        className="relative w-full h-full sm:h-auto sm:max-h-[85vh] sm:max-w-4xl mx-auto bg-black text-white rounded-t-3xl sm:rounded-2xl shadow-2xl overflow-hidden border border-gray-800 flex flex-col"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Mobile Swipe Indicator */}
        <div className="sm:hidden flex justify-center pt-2 pb-1">
          <div className="w-8 h-1 bg-gray-600 rounded-full"></div>
        </div>

        {/* Header - Fixed */}
        <div className="flex-shrink-0 flex items-start justify-between p-4 sm:p-6 border-b border-gray-800 bg-black">
          <div className="flex items-start gap-3 sm:gap-4 flex-1 min-w-0">
            <div className="w-12 h-12 sm:w-14 sm:h-14 bg-white/10 border border-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
              <img
                src={logo}
                alt={`${companyName} logo`}
                className="w-7 h-7 sm:w-9 sm:h-9 object-contain"
                onError={(e) => {
                  const img = e.currentTarget;
                  if (img.src.includes('-only')) {
                    img.src = img.src.replace('-only', '');
                  }
                }}
              />
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-lg sm:text-2xl font-bold leading-tight break-words">{job.title}</div>
              <div className="text-sm sm:text-base text-gray-300 mt-1">{companyName}</div>
              {job.location && (
                <div className="mt-1 text-xs sm:text-sm text-gray-400 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                  {job.location}
                </div>
              )}
              {job.posted_date && (
                <div className="mt-1 text-xs sm:text-sm text-gray-500 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {job.posted_date}
                </div>
              )}
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 sm:w-12 sm:h-12 bg-white/10 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors flex-shrink-0 ml-2"
            aria-label="Close"
          >
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content - Scrollable */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          {/* Job Details Section */}
          <div className="space-y-4 sm:space-y-6">
            {/* Experience Level */}
            {job.level && job.level !== 'Not specified' && (
              <div className="bg-white/5 rounded-lg p-3 sm:p-4">
                <h3 className="text-sm font-semibold text-gray-300 mb-2">Experience Level</h3>
                <p className="text-sm text-white">{job.level}</p>
              </div>
            )}

            {/* Job Description */}
            {(job.job_description || job.description) && (
              <div className="bg-white/5 rounded-lg p-3 sm:p-4">
                <h3 className="text-sm font-semibold text-gray-300 mb-3">Job Description</h3>
                <div className="text-sm sm:text-base text-white leading-relaxed whitespace-pre-wrap break-words prose prose-invert max-w-none">
                  <div className="space-y-3">
                    {(job.job_description || job.description).split('\n').map((paragraph, index) => (
                      <p key={index} className="text-sm sm:text-base leading-6">
                        {paragraph.trim()}
                      </p>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Additional Info */}
            <div className="bg-white/5 rounded-lg p-3 sm:p-4">
              <h3 className="text-sm font-semibold text-gray-300 mb-3">About This Role</h3>
              <div className="space-y-2 text-sm text-white">
                <div className="flex items-center">
                  <svg className="w-4 h-4 mr-2 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                  <span>Location: {job.location || 'Not specified'}</span>
                </div>
                <div className="flex items-center">
                  <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                  </svg>
                  <span>Level: {job.level || 'Not specified'}</span>
                </div>
                {job.posted_date && (
                  <div className="flex items-center">
                    <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>Posted: {job.posted_date}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Action Bar - Fixed */}
        <div className="flex-shrink-0 p-4 sm:p-6 border-t border-gray-800 bg-black">
          <div className="flex flex-col sm:flex-row gap-3">
            {job.job_link ? (
              <>
                <a
                  href={job.job_link}
                  target="_blank"
                  rel="noreferrer"
                  className="flex-1 px-6 py-4 bg-white text-black rounded-xl hover:bg-gray-200 transition-colors font-semibold text-center text-base sm:text-lg flex items-center justify-center gap-2"
                  onClick={(e) => e.stopPropagation()}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Apply Now
                </a>
                <button
                  onClick={onClose}
                  className="px-6 py-4 bg-white/10 text-white rounded-xl hover:bg-white/20 transition-colors font-medium text-center sm:w-auto"
                >
                  Cancel
                </button>
              </>
            ) : (
              <button
                onClick={onClose}
                className="flex-1 px-6 py-4 bg-white text-black rounded-xl hover:bg-gray-200 transition-colors font-semibold text-base sm:text-lg"
              >
                Close
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetailsModal;


