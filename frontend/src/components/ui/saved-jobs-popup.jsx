"use client";
import React from "react";
import { cn } from "@/lib/utils";

export default function SavedJobsPopup({ isOpen, onClose, company, savedJobs }) {
  if (!isOpen || !company) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleApply = (jobId) => {
    console.log(`Applying to job ${jobId} at ${company.name}`);
    // Here you would implement the actual apply logic
    // For now, just log the action
  };

  const removeJob = (job) => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      const saved = raw ? JSON.parse(raw) : {};
      const companyName = company.name;
      const key = `${companyName}__${job.title}`;
      if (saved[companyName] && saved[companyName][key]) {
        delete saved[companyName][key];
        localStorage.setItem('wb_saved_jobs', JSON.stringify(saved));
        // Notify others and refresh this modal by closing and reopening state from parent
        window.dispatchEvent(new CustomEvent('wb:saved-jobs-updated'));
      }
    } catch (e) {
      console.error('Failed to remove saved job', e);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-2 sm:p-4"
      onClick={handleBackdropClick}
    >
      <div className="relative w-full max-w-4xl mx-auto bg-black text-white rounded-xl sm:rounded-2xl shadow-2xl max-h-[90vh] sm:max-h-[80vh] overflow-hidden border border-gray-800">
        {/* Header */}
        <div className="flex items-center justify-between p-4 sm:p-6 border-b border-gray-800">
          <div className="flex items-center gap-3 sm:gap-4">
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-black border border-gray-700 rounded-full flex items-center justify-center">
              <img
                src={company.logo}
                alt={`${company.name} logo`}
                className="w-6 h-6 sm:w-8 sm:h-8 object-contain invert"
                onError={(e) => {
                  const img = e.currentTarget;
                  if (img.src.includes('-only')) {
                    img.src = img.src.replace('-only', '');
                  }
                }}
              />
            </div>
            <div>
              <h2 className="text-lg sm:text-2xl font-bold">
                {company.name}
              </h2>
              <p className="text-sm sm:text-base text-gray-300">
                {savedJobs.length} saved job{savedJobs.length !== 1 ? 's' : ''}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 bg-white/10 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors"
          >
            <svg
              className="w-5 h-5 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Jobs List */}
        <div className="overflow-y-auto no-scrollbar max-h-[70vh] sm:max-h-[60vh] p-3 sm:p-6">
          {savedJobs.length === 0 ? (
            <div className="text-center py-8 sm:py-12">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4">
                <svg
                  className="w-6 h-6 sm:w-8 sm:h-8 text-gray-300"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6"
                  />
                </svg>
              </div>
              <h3 className="text-base sm:text-lg font-semibold mb-2">
                No saved jobs yet
              </h3>
              <p className="text-sm sm:text-base text-gray-300">
                Start saving jobs from {company.name} to see them here
              </p>
            </div>
          ) : (
            <div className="space-y-3 sm:space-y-4">
              {savedJobs.map((job) => (
                <div
                  key={job.id}
                  className="bg-black rounded-lg sm:rounded-xl p-3 sm:p-4 border border-gray-800 hover:shadow-md transition-shadow"
                >
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-4">
                    <div className="flex-1">
                      <h3 className="text-base sm:text-lg font-semibold mb-2">
                        {job.title}
                      </h3>
                      <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-xs sm:text-sm text-gray-300 mb-2 sm:mb-3">
                        <div className="flex items-center gap-1">
                          <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                          </svg>
                          <span className="truncate">{job.location}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                          </svg>
                          {job.level}
                        </div>
                      </div>
                      <p className="text-xs sm:text-sm text-white line-clamp-2">
                        {job.description}
                      </p>
                    </div>
                    <div className="flex sm:flex-col gap-2">
                      <button
                        onClick={() => handleApply(job.id)}
                        className="flex-1 sm:flex-none px-3 sm:px-4 py-2 glassmorphic-base apply-button text-white rounded-lg sm:rounded-2xl font-medium text-xs sm:text-sm"
                      >
                        Apply
                      </button>
                      <button
                        onClick={() => removeJob(job)}
                        className="flex-1 sm:flex-none px-3 sm:px-4 py-2 remove-button glassmorphic-remove-btn text-white rounded-lg font-medium transition-colors text-xs sm:text-sm"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
