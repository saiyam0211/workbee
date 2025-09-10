import React from 'react';

const JobDetailsModal = ({ isOpen, job, onClose, onApply }) => {
  if (!isOpen || !job) return null;

  const companyName = job.company || job.company_name || 'Company';
  const logo = job.logo || `/logos/${(companyName || '').toLowerCase().replace(/\s+/g, '-')}.svg`;

  return (
    <div className="fixed inset-0 z-[999999] flex items-center justify-center bg-black/70 backdrop-blur-sm p-2 sm:p-4" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="relative w-full max-w-4xl mx-auto bg-black text-white rounded-xl sm:rounded-2xl shadow-2xl max-h-[90vh] sm:max-h-[80vh] overflow-hidden border border-gray-800">
        <div className="sticky top-0 z-10 flex items-start justify-between p-4 sm:p-6 border-b border-gray-800 bg-black">
          <div className="flex items-start gap-3 sm:gap-4">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-black border border-gray-700 rounded-full flex items-center justify-center">
              <img
                src={logo}
                alt={`${companyName} logo`}
                className="w-6 h-6 sm:w-8 sm:h-8 object-contain invert"
                onError={(e) => {
                  const img = e.currentTarget;
                  if (img.src.includes('-only')) {
                    img.src = img.src.replace('-only', '');
                  }
                }}
              />
            </div>
            <div className="min-w-0">
              <div className="text-xl sm:text-2xl font-bold truncate">{job.title}</div>
              {job.location && (
                <div className="mt-1 text-xs sm:text-sm text-gray-300 truncate">{job.location}</div>
              )}
              {job.posted_date && (
                <p className="mt-1 text-xs sm:text-sm text-gray-400">{job.posted_date}</p>
              )}
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 sm:w-12 sm:h-12 self-center bg-white/10 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors"
            aria-label="Close"
          >
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="overflow-y-auto no-scrollbar max-h-[70vh] sm:max-h-[60vh] p-3 sm:p-6 overflow-x-hidden">
          {(job.job_description || job.description) && (
            <p className="text-sm sm:text-base text-white whitespace-pre-wrap break-words leading-relaxed">{job.job_description || job.description}</p>
          )}

        </div>

        {/* Bottom Action Bar */}
        <div className="sticky bottom-0 p-4 sm:p-6 border-t border-gray-800 bg-black">
          <div className="flex gap-3 sm:gap-4">
            {job.job_link ? (
              <a
                href={job.job_link}
                target="_blank"
                rel="noreferrer"
                className="flex-1 px-4 py-3 bg-white text-black rounded-xl hover:bg-gray-200 transition-colors font-medium text-center"
                onClick={(e) => e.stopPropagation()}
              >
                Apply Now
              </a>
            ) : (
              <button
                onClick={onClose}
                className="flex-1 px-4 py-3 bg-white text-black rounded-xl hover:bg-gray-200 transition-colors font-medium"
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


