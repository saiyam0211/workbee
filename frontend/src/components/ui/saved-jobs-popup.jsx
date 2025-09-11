"use client";
import React, { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import JobDetailsModal from "./JobDetailsModal";
import { storageUtils } from "../../utils/storage";

export default function SavedJobsPopup({ isOpen, onClose, company, savedJobs }) {
  const [isJobModalOpen, setIsJobModalOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [touchStart, setTouchStart] = useState(null);
  const [touchEnd, setTouchEnd] = useState(null);

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
    if (isUpSwipe) {
      onClose();
    }
  };

  if (!isOpen || !company) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleViewMore = (job) => {
    setSelectedJob(job);
    setIsJobModalOpen(true);
  };

  const handleJobModalClose = () => {
    setIsJobModalOpen(false);
    setSelectedJob(null);
  };

  const removeJob = (job) => {
    const success = storageUtils.removeJob(job, company.name);
    if (success) {
      console.log('Job removed successfully');
      // The storage utility already dispatches the update event
    } else {
      console.error('Failed to remove job');
    }
  };

  return (
    <div
      className="fixed inset-0 z-[9999] flex items-end sm:items-center justify-center bg-black/80 backdrop-blur-sm"
      onClick={handleBackdropClick}
    >
      {/* Mobile: Full height modal, Desktop: Centered modal */}
      <div 
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
        <div className="flex-shrink-0 flex items-center justify-between p-4 sm:p-6 border-b border-gray-800">
          <div className="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
            <div className="w-12 h-12 sm:w-14 sm:h-14 bg-white/10 border border-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
              <img
                src={company.logo}
                alt={`${company.name} logo`}
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
              <h2 className="text-lg sm:text-2xl font-bold truncate">
                {company.name}
              </h2>
              <p className="text-sm sm:text-base text-gray-300">
                {savedJobs.length} saved job{savedJobs.length !== 1 ? 's' : ''}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 sm:w-12 sm:h-12 bg-white/10 rounded-full flex items-center justify-center hover:bg-white/20 transition-colors flex-shrink-0 ml-2"
            aria-label="Close"
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

        {/* Jobs List - Scrollable */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          {savedJobs.length === 0 ? (
            <div className="text-center py-8 sm:py-12">
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4 sm:mb-6">
                <svg
                  className="w-8 h-8 sm:w-10 sm:h-10 text-gray-300"
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
              <h3 className="text-lg sm:text-xl font-semibold mb-2 text-white">
                No saved jobs yet
              </h3>
              <p className="text-sm sm:text-base text-gray-300">
                Start saving jobs from {company.name} to see them here
              </p>
            </div>
          ) : (
            <div className="space-y-4 sm:space-y-6">
              {savedJobs.map((job) => (
                <div
                  key={job.id}
                  className="bg-white/5 rounded-xl sm:rounded-2xl p-4 sm:p-6 border border-gray-800 hover:bg-white/10 transition-all duration-200"
                >
                  {/* Job Header */}
                  <div className="flex items-start justify-between mb-3 sm:mb-4">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg sm:text-xl font-bold text-white mb-2 leading-tight break-words">
                        {job.title}
                      </h3>
                      <div className="flex flex-wrap items-center gap-3 sm:gap-4 text-sm text-gray-300">
                        {job.location && (
                          <div className="flex items-center gap-1.5">
                            <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                            </svg>
                            <span className="truncate">{job.location}</span>
                          </div>
                        )}
                        {job.level && job.level !== 'Not specified' && (
                          <div className="flex items-center gap-1.5">
                            <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                            </svg>
                            <span>{job.level}</span>
                          </div>
                        )}
                        {job.posted_date && (
                          <div className="flex items-center gap-1.5">
                            <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span>{job.posted_date}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Job Description */}
                  <div className="mb-4 sm:mb-6">
                    <p className="text-sm sm:text-base text-gray-200 leading-relaxed line-clamp-3">
                      {job.description || job.job_description || 'Job description not available.'}
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-col sm:flex-row gap-3">
                    <button
                      onClick={() => handleViewMore(job)}
                      className="flex-1 px-4 sm:px-6 py-3 sm:py-4 bg-white text-black rounded-xl hover:bg-gray-200 transition-colors font-semibold text-sm sm:text-base flex items-center justify-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      View More
                    </button>
                    <button
                      onClick={() => removeJob(job)}
                      className="px-4 sm:px-6 py-3 sm:py-4 bg-red-600 hover:bg-red-700 text-white rounded-xl font-semibold transition-colors text-sm sm:text-base flex items-center justify-center gap-2 sm:w-auto"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Job Details Modal */}
      <JobDetailsModal
        isOpen={isJobModalOpen}
        job={selectedJob}
        onClose={handleJobModalClose}
      />
    </div>
  );
}
