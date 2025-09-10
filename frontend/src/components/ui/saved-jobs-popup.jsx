"use client";
import React, { useState } from "react";
import { cn } from "@/lib/utils";
import JobDetailsModal from "./JobDetailsModal";
import { storageUtils } from "../../utils/storage";

export default function SavedJobsPopup({ isOpen, onClose, company, savedJobs }) {
  const [isJobModalOpen, setIsJobModalOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);

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
      className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm p-2 sm:p-4"
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
                        {job.location && (
                          <div className="flex items-center gap-1">
                            <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <span className="truncate">{job.location}</span>
                          </div>
                        )}
                        {job.level && (
                          <div className="flex items-center gap-1">
                            <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                            </svg>
                            <span>{job.level}</span>
                          </div>
                        )}
                        {job.posted_date && (
                          <div className="flex items-center gap-1">
                            <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span>{job.posted_date}</span>
                          </div>
                        )}
                        {job.experience_required && (
                          <div className="flex items-center gap-1">
                            <svg className="w-3 h-3 sm:w-4 sm:h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                            </svg>
                            <span>{job.experience_required}</span>
                          </div>
                        )}
                      </div>
                      <p className="text-xs sm:text-sm text-white line-clamp-2">
                        {job.description}
                      </p>
                    </div>
                    <div className="flex sm:flex-col gap-2">
                      <button
                        onClick={() => handleViewMore(job)}
                        className="flex-1 sm:flex-none px-3 sm:px-4 py-2 glassmorphic-base apply-button text-white rounded-lg sm:rounded-2xl font-medium text-xs sm:text-sm"
                      >
                        View More
                      </button>
                      <button
                        onClick={() => removeJob(job)}
                        className="flex-1 sm:flex-none px-3 sm:px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors text-xs sm:text-sm flex items-center justify-center gap-1"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
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
