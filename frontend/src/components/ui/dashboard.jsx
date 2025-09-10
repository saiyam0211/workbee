import React, { useState, useEffect, useRef } from 'react';
import { Heart } from 'lucide-react';
import GlassFooter from './GlassFooter';
import JobDetailsModal from './JobDetailsModal';
import nvidiaJobs from '@/nvidia_jobs.json';



// Build job data from NVIDIA JSON
const jobData = (Array.isArray(nvidiaJobs) ? nvidiaJobs : []).map((job, idx) => ({
  id: idx + 1,
  company: job.company || 'NVIDIA',
  logo: '/logos/microsoft.svg',
  title: job.title || 'Untitled Role',
  location: job.location || 'Location not specified',
  level: job.experience_required || 'Not specified',
  description: job.job_description || job.description || '',
  job_link: job.job_link || '',
  postedDate: job.posted_date || ''
}));

const WorkBeeJobCard = () => {
  useEffect(() => {
    document.body.classList.add('dark');
    return () => document.body.classList.remove('dark');
  }, []);
  const [currentJobIndex, setCurrentJobIndex] = useState(0);
  const [savedVersion, setSavedVersion] = useState(0);
  const [activeTab, setActiveTab] = useState('home');
  const getSavedMap = () => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  };
  const isJobSaved = (job) => {
    const saved = getSavedMap();
    const company = job.company || 'Unknown';
    const key = `${company}__${job.title}`;
    return Boolean(saved?.[company]?.[key]);
  };
  const visibleJobs = React.useMemo(() => jobData.filter((j) => !isJobSaved(j)), [savedVersion]);
  const currentJob = visibleJobs[currentJobIndex];
  const [isExpanded, setIsExpanded] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const touchStartXRef = useRef(null);
  const touchStartYRef = useRef(null);
  const handlePrevious = () => {
    if (visibleJobs.length === 0) return;
    setCurrentJobIndex((prev) => (prev === 0 ? visibleJobs.length - 1 : prev - 1));
  };

  const handleNext = () => {
    if (visibleJobs.length === 0) return;
    setCurrentJobIndex((prev) => (prev === visibleJobs.length - 1 ? 0 : prev + 1));
  };

  // Initialize favorited state based on localStorage when job changes
  useEffect(() => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      const saved = raw ? JSON.parse(raw) : {};
      if (!currentJob) return;
      const jobKey = `${currentJob.company}__${currentJob.title}`;
      setIsFavorited(Boolean(saved?.[currentJob.company]?.[jobKey]));
    } catch (e) {
      setIsFavorited(false);
    }
  }, [currentJob]);

  // TODO: Replace with API call
  const handleApply = () => {
    if (currentJob && currentJob.job_link) {
      window.open(currentJob.job_link, '_blank', 'noopener,noreferrer');
      return;
    }
    console.log(`Applying to ${currentJob.company} - ${currentJob.title}`);
    // API call will go here
  };

  const handleFavorite = () => {
    try {
      const raw = localStorage.getItem('wb_saved_jobs');
      const saved = raw ? JSON.parse(raw) : {};
      const company = currentJob.company || 'Unknown';
      const jobKey = `${company}__${currentJob.title}`;
      const companyMap = saved[company] || {};
      let newFavorited;
      if (companyMap[jobKey]) {
        // Toggle off (remove)
        delete companyMap[jobKey];
        newFavorited = false;
      } else {
        companyMap[jobKey] = {
          id: currentJob.id,
          title: currentJob.title,
          location: currentJob.location,
          level: currentJob.level,
          description: currentJob.description,
          job_link: currentJob.job_link,
          company: company
        };
        newFavorited = true;
      }
      saved[company] = companyMap;
      localStorage.setItem('wb_saved_jobs', JSON.stringify(saved));
      setIsFavorited(newFavorited);
      // Notify other pages (fav-companies) to update counts
      window.dispatchEvent(new CustomEvent('wb:saved-jobs-updated'));
      // If saved, remove from current visible list
      if (newFavorited) {
        setSavedVersion((v) => v + 1);
        if (visibleJobs.length > 1) {
          setCurrentJobIndex((prev) => (prev >= visibleJobs.length - 1 ? 0 : prev));
        }
      }
    } catch (e) {
      console.error('Failed to update saved jobs', e);
    }
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === 'ArrowLeft') {
        handlePrevious();
      } else if (event.key === 'ArrowRight') {
        handleNext();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);
  // Keep index in bounds when list changes
  useEffect(() => {
    if (currentJobIndex >= visibleJobs.length) {
      setCurrentJobIndex(0);
    }
  }, [visibleJobs.length]);
  return (
    <div className="min-h-screen bg-background text-foreground font-sans pb-20">
      {/* Background Effects */}
      <div
        aria-hidden
        className="z-[2] absolute inset-0 pointer-events-none isolate opacity-50 contain-strict hidden lg:block">
        <div className="w-[35rem] h-[80rem] -translate-y-[350px] absolute left-0 top-0 -rotate-45 rounded-full bg-[radial-gradient(68.54%_68.72%_at_55.02%_31.46%,hsla(0,0%,85%,.08)_0,hsla(0,0%,55%,.02)_50%,hsla(0,0%,45%,0)_80%)]" />
        <div className="h-[80rem] absolute left-0 top-0 w-56 -rotate-45 rounded-full bg-[radial-gradient(50%_50%_at_50%_50%,hsla(0,0%,85%,.06)_0,hsla(0,0%,45%,.02)_80%,transparent_100%)] [translate:5%_-50%]" />
        <div className="h-[80rem] -translate-y-[350px] absolute left-0 top-0 w-56 -rotate-45 bg-[radial-gradient(50%_50%_at_50%_50%,hsla(0,0%,85%,.04)_0,hsla(0,0%,45%,.02)_80%,transparent_100%)]" />
      </div>
      <div aria-hidden className="absolute inset-0 -z-10 size-full [background:radial-gradient(125%_125%_at_50%_100%,transparent_0%,var(--background)_75%)]" />

      {/* Header */}
      <div className="flex items-center mb-10 justify-between p-4 relative z-10">
        <div className="ml-0 sm:ml-20 flex items-center" style={{ height: "100px", width: "200px" }}>
          <svg
            width="1000"
            height="1000"
            viewBox="0 0 440 581"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{ display: "block", height: "1000%", width: "1000%" }}
          >
            <g clipPath="url(#prefix__clip0_6029_35)">
              <path d="M15.17 242.18l8.29 27.09 8.74-26.36c1.11-1.13 11.11-1.22 12.5-.54 1.54.76 7.16 24.12 8.49 27.48 1.49.17.89-.03 1.14-.83 2.61-8.7 5.07-17.47 7.48-26.22.94-.97 10.19-.91 12.08-.73 4.66.46 2.95 3.41 2.1 6.69-3.76 14.48-9.44 28.59-13.71 42.92-.06 3.93-13.74 2.72-14.62 1.82l-8.92-25.36-9.01 24.97c-.63.84-1.29.99-2.28 1.12-1.98.25-10.55.31-11.67-.84L0 245.15c-.27-5.42 11.68-2.25 15.17-2.97z" fill="#fff"/>
              <path d="M90.5 243h31l7.5 7.5 4 8-3 6.5-1 8-7.5 7.5-4 8-6 8-10.5.5-10.5-15.5-7-8.5-1-6.5-3-8 3.5-7 7.5-8.5z" fill="#F5B03B"/>
              <path d="M241.52 220.58c2.18 2.22.82 4.77.82 7.06 0 5.58.05 11.16.03 16.73 16.21-7.01 33.97-.59 36.74 17.91 2.73 18.21-7.35 33.74-26.86 33.09-15.94-.54-24.37-11.81-25.2-26.9-.68-12.34-1.01-31.53 0-43.66.13-1.5.27-3.14 1.44-4.23h13.03zm10.92 34.68c-14.25 1.56-13.32 27.25 2.1 25.93 14.42-1.24 12.99-27.58-2.1-25.93zM191.39 257.96l2.01-.54 13.43-14.89c1.68-.68 11.05-.74 13.19-.46 1.45.19 2.71.75 2.45 2.45-.35 2.27-11.28 13.78-13.51 16.57-.82 1.03-3.97 4.72-3.97 5.65 1.76 4.97 19.84 21.39 19.87 24.92 0 .65-.07 1.26-.61 1.71-1.7 1.71-11.5.53-14.34.72l-17.1-18.03-1.42.87v15.86c0 1.01-2.24 1.37-3.08 1.45-1.83.18-11.64.48-11.64-1.45v-71.36l.85-.85h13.03l.85.85v36.53h-.01zM356.21 273.82c1.76 7.52 10.18 7.98 16.64 7.29 3.76-.4 11.23-4.61 13.78-1.47.97 1.2 1.07 8.07.62 9.63-1.1 3.76-15.84 6.12-19.42 6.12-37.44 0-35.1-55.75 1.16-53.88 11.74.6 21.33 9.44 22.37 21.24.21 2.36.83 11.06-2.57 11.06h-32.57l-.01.01zm20.95-11.33c-2.19-10.99-18.27-10.34-20.96 0h20.96z" fill="#fff"/>
              <path d="M300.14 273.82c1.76 7.65 10.14 8.03 16.65 7.3 3.5-.39 11.67-4.66 13.98-1.4.93 1.31.87 9.62-.21 10.93-1.98 2.4-15.42 4.73-18.81 4.73-36.02-.02-35.51-52.72-1.73-53.87 14.61-.5 25.19 10.1 25.28 24.66.01 1.99-.63 7.64-3.16 7.64h-32v.01zm20.95-11.33c-3.06-10.61-17.97-10.8-20.96 0h20.96zM154.58 292.79c-.59 1.95-10.16 1.64-12.14 1.36-2.46-.34-2.41-1.34-2.6-3.6-.6-7.07-.83-29.29.89-35.41 2.1-7.47 8.79-12.27 16.42-13.04 2.24-.22 8.72-.37 10.74 0 3.47.65 2.89 7.69 2.57 10.47-.64 5.57-7.5 1.69-12.11 4.31-2.09 1.19-3.76 5.38-3.76 7.57v28.32l-.01.02zM90.01 243.24l5.48-7.65-4.84-8.36 7.28-10.87c.04-1.6-3.17-5.42-4.56-6.2-2.48-1.39-5.51-.3-7.07-1.42-2.01-1.43-1.79-4.81 1.14-5.17 7.78-.96 13.73 4.79 15.7 11.83 7.15 1.36 5.55-1.58 8.5-5.75 2.63-3.72 6.84-6.43 11.54-6.09 3.73.28 5.07 3.77 1.73 5.19-2.41 1.02-4.31.02-7.1 1.97-9.43 6.58 5.2 12.54 3.06 18.34-.57 1.55-4.24 5.23-4.24 6.55l5.11 7.64H90.02l-.01-.01zM79.25 258.53c-.31-.27 3.42-7.04 3.7-7.34.61-.65 2.07-.86 2.97-1 8.54-1.33 29.2-.74 38.38-.18 1.59.1 3.13.33 4.66.72l4.1 7.8H79.25zM130.23 265.32l-1.24 7.82c-1.33.49-2.7.62-4.12.7-13.08.74-26.97-.5-40.13-.17-2.87-.54-2.5-5.97-2.66-8.36h48.14l.01.01zM121.73 280.62l-4.27 7.94-21.96.44-5.49-8.1 31.72-.28zM111.54 296.47l-3.87 9.44c-.85.56-.86 4.01-2.07 3.59-.62-.22-4.36-11-4.69-12.31-.11-.44-.19-.83-.12-1.29.21-.28.72.57.84.57h9.91z" fill="#fff"/>
            </g>
            <defs>
              <clipPath id="prefix__clip0_6029_35">
                <path fill="#fff" d="M0 0h440v581H0z"/>
              </clipPath>
            </defs>
          </svg>
        </div>
       

      </div>


      {/* Main Content */}
      <div className="px-4 -mt-12 py-8 flex items-center justify-center relative z-10">
        <div
          className="relative max-w-md w-full sm:max-w-lg"
          onTouchStart={(e) => {
            const touch = e.changedTouches[0];
            touchStartXRef.current = touch.clientX;
            touchStartYRef.current = touch.clientY;
          }}
          onTouchEnd={(e) => {

            const touch = e.changedTouches[0];
            const dx = touch.clientX - (touchStartXRef.current ?? 0);
            const dy = touch.clientY - (touchStartYRef.current ?? 0);
            const absDx = Math.abs(dx);
            const absDy = Math.abs(dy);
            const SWIPE_THRESHOLD = 40;
            if (absDx > SWIPE_THRESHOLD && absDx > absDy) {
              if (dx < 0) handleNext();
              else handlePrevious();
            }
          }}
        >
          {/* Navigation Arrows */}
          <button
            onClick={handlePrevious}
            className="hidden sm:flex absolute -left-16 glassmorphic-base cursor-pointer top-1/2 transform -translate-y-1/2 w-12 h-12 sm:w-16 sm:h-16 border rounded-full items-center justify-center transition-colors -ml-95">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M63.5413 50H36.458M36.458 50L46.8747 39.5833M36.458 50L46.8747 60.4167" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M70.8333 18.8148C64.8746 14.8261 57.7089 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 70.7107 29.2893 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 43.1696 85.6739 36.7657 82.4832 31.25" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>

          </button>

          <button
            onClick={handleNext}
            className="hidden sm:flex absolute cursor-pointer -right-16 top-1/2 transform -translate-y-1/2 w-12 h-12 sm:w-16 sm:h-16 glassmorphic-base border border-gray-600 rounded-full items-center justify-center hover:bg-gray-700 transition-colors -mr-95">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M36.4587 50H63.542M63.542 50L53.1253 60.4167M63.542 50L53.1253 39.5833" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M29.1667 81.1852C35.1254 85.1739 42.2911 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 29.2893 70.7107 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 56.8304 14.3261 63.2343 17.5168 68.75" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>

          </button>

          {/* Job Card */}
          <div
            key={currentJob.id || currentJob.title}
            className="bg-gradient-to-br from-[#D9D9D9] to-[#737373]    rounded-3xl sm:rounded-[60px] p-4 sm:p-15 text-black shadow-2xl border-4 w-full sm:w-230 h-auto sm:h-140 ml-0 sm:-ml-55  sm:-mt-17 select-none touch-pan-y"
          >
            {/* Company Logo (desktop only) */}
            <div className="hidden sm:flex justify-end mb-4">
              <div className="w-20  h-20 bg-white rounded-full flex items-center justify-center p-2">
                <img
                  src={currentJob.logo}
                  alt={`${currentJob.company} logo`}
                  className="w-8 h-8 object-contain"
                  onError={(e) => {
                    const img = e.currentTarget;
                    if (img.src.includes('-only')) img.src = img.src.replace('-only','');
                  }}
                />
              </div>
            </div>

            {/* Job Title with inline logo on mobile */}
            <div className="flex  items-center -mt-4 gap-3 ml-6 mb-2 sm:mb-0">
              <div className="sm:hidden  shrink-0 w-10 h-10 bg-white rounded-full flex items-center justify-center p-1.5">
                <img
                  src={currentJob.logo}
                  alt={`${currentJob.company} logo`}
                  className="w-6 h-6 object-contain"
                />
              </div>
              <h2 className="text-2xl sm:text-4xl mt-2 sm:-mt-22 font-bold leading-tight break-words line-clamp-2 pr-24 sm:pr-40">
              {currentJob.title}
            </h2>
            </div>



            {/* Location and Level */}
            <div className="flex items-start text-sm sm:text-lg ml-6 text-gray-900 mb-6">
              <span className="mr-1"><svg width="19" height="19" viewBox="0 0 19 19" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9.49967 17.1346C9.31495 17.1346 9.15662 17.0827 9.02467 16.9788C8.89273 16.875 8.79377 16.7387 8.7278 16.57C8.47711 15.843 8.16044 15.1615 7.7778 14.5255C7.40835 13.8894 6.88717 13.143 6.21426 12.2863C5.54134 11.4296 4.99377 10.6118 4.57155 9.83293C4.16252 9.05409 3.95801 8.11298 3.95801 7.00962C3.95801 5.49087 4.49238 4.20577 5.56113 3.15433C6.64308 2.0899 7.95592 1.55769 9.49967 1.55769C11.0434 1.55769 12.3497 2.0899 13.4184 3.15433C14.5004 4.20577 15.0413 5.49087 15.0413 7.00962C15.0413 8.19087 14.8104 9.1774 14.3486 9.96923C13.9 10.7481 13.3788 11.5204 12.7851 12.2863C12.0726 13.2209 11.5316 13.9998 11.1622 14.6228C10.8059 15.2329 10.509 15.882 10.2715 16.57C10.2056 16.7517 10.1 16.8945 9.95488 16.9983C9.82294 17.0892 9.6712 17.1346 9.49967 17.1346ZM9.49967 8.95673C10.0538 8.95673 10.5222 8.76851 10.9049 8.39207C11.2875 8.01563 11.4788 7.55481 11.4788 7.00962C11.4788 6.46442 11.2875 6.00361 10.9049 5.62716C10.5222 5.25072 10.0538 5.0625 9.49967 5.0625C8.94551 5.0625 8.47711 5.25072 8.09447 5.62716C7.71183 6.00361 7.52051 6.46442 7.52051 7.00962C7.52051 7.55481 7.71183 8.01563 8.09447 8.39207C8.47711 8.76851 8.94551 8.95673 9.49967 8.95673Z" fill="#1D1B20" />
              </svg>
              </span>
              <span className="line-clamp-2 break-words">{currentJob.location}</span>
              <div className="flex items-center ml-4">
                <span className="mr-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 22H21" stroke="#292D32" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M5.59998 8.38H4C3.45 8.38 3 8.83 3 9.38V18C3 18.55 3.45 19 4 19H5.59998C6.14998 19 6.59998 18.55 6.59998 18V9.38C6.59998 8.83 6.14998 8.38 5.59998 8.38Z" stroke="#292D32" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M12.8002 5.19H11.2002C10.6502 5.19 10.2002 5.64 10.2002 6.19V18C10.2002 18.55 10.6502 19 11.2002 19H12.8002C13.3502 19 13.8002 18.55 13.8002 18V6.19C13.8002 5.64 13.3502 5.19 12.8002 5.19Z" stroke="#292D32" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M20.0004 2H18.4004C17.8504 2 17.4004 2.45 17.4004 3V18C17.4004 18.55 17.8504 19 18.4004 19H20.0004C20.5504 19 21.0004 18.55 21.0004 18V3C21.0004 2.45 20.5504 2 20.0004 2Z" stroke="#292D32" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                </span>
                <span>{currentJob.level}</span>
              </div>
            </div>

            {/* Job Description Section */}
            <div className="mb-4 sm:mb-8 sm:h-40">
              <h3 className="text-xl sm:text-3xl ml-6 mt-4 sm:mt-10 font-bold mb-2">Job Description</h3>
              <div className="mb-2">
                <span className="font-semibold text-lg sm:text-xl ml-6">About the job</span>
              </div>
              <p className={`text-sm sm:text-xl ml-6 text-gray-700 leading-relaxed ${isExpanded ? '' : 'clamp-3'}`}>
                {currentJob.description}
              </p>
              <button
                className="ml-6 mt-2 text-sm sm:text-base font-semibold text-blue-700 hover:underline cursor-pointer"
                onClick={(e) => { e.stopPropagation(); setIsModalOpen(true); }}
              >
                Read More...
              </button>

            </div>

            {/* Action Buttons */}
            {/*
              Add isFavorited state to control the button fill. 
              Place this near the other useState hooks:
              const [isFavorited, setIsFavorited] = useState(false);
            */}
            <div className="flex flex-col sm:flex-row ml-0 sm:ml-135 mt-4 sm:mt-24 items-center justify-between sm:justify-center space-y-3 sm:space-y-0 sm:space-x-4 ">
              <button
                onClick={handleFavorite}
                onClick={() => {
                  handleFavorite();
                }}
                className={`w-14 h-14 sm:w-15 sm:h-15 cursor-pointer apply-button rounded-full flex items-center justify-center glassmorphic-base transition-colors ${isFavorited ? 'bg-red-600' : ''}`}
                style={isFavorited ? { backgroundColor: '#ef4444' } : {}}
              >
                <span className="text-3xl">
                  <Heart className={isFavorited ? 'text-white fill-white' : 'text-white'} fill={isFavorited ? '#fff' : 'none'} />
                </span>
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); handleApply(); }}
                className="w-full sm:w-auto px-8 h-15 py-3 apply-button glassmorphic-base text-white rounded-full font-semibold hover:bg-gray-600 transition-colors text-lg sm:text-xl">
                Apply Now
              </button>
            </div>
          </div>

          {/* Mobile Navigation Arrows - Only visible on mobile */}
          <div className="flex sm:hidden justify-center items-center mt-4 space-x-8">
            <button
              onClick={handlePrevious}
              className="w-14 h-14 glassmorphic-base border border-gray-600 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer"
              aria-label="Previous job"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 18L9 12L15 6" stroke="#CDCDCD" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            
            <button
              onClick={handleNext}
              className="w-14 h-14 glassmorphic-base border border-gray-600 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors cursor-pointer"
              aria-label="Next job"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 18L15 12L9 6" stroke="#CDCDCD" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>

          {/* Swipe hint for mobile */}
           
        </div>
      </div>

      {/* Glass Footer Navigation */}
      <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
      {/* Details Modal */}
      <JobDetailsModal
        isOpen={isModalOpen}
        job={currentJob}
        onClose={() => setIsModalOpen(false)}
        onApply={handleApply}
        onFavorite={() => setIsFavorited((prev) => !prev)}
        isFavorited={isFavorited}
      />
    </div>
  );
};

export default WorkBeeJobCard;