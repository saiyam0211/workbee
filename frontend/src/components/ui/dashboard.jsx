import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, HelpCircle, Play } from 'lucide-react';
import { driver } from 'driver.js';
import 'driver.js/dist/driver.css';
import GlassFooter from './GlassFooter';
import JobDetailsModal from './JobDetailsModal';
import nvidiaJobs from '@/nvidia_jobs.json';
import { storageUtils } from '../../utils/storage';



// Company logo mapping
const companyLogos = {
  'NVIDIA': '/logos/nvidia.svg',
  'Microsoft': '/logos/microsoft.svg',
  'Google': '/logos/google-only.svg',
  'Apple': '/logos/apple-only.svg',
  'Amazon': '/logos/amazon.png',
  'Meta': '/logos/meta-only.svg',
  'AMD': '/logos/amd.png',
  'Yahoo': '/logos/yahoo.png',
  'Stripe': '/logos/stripe-logo.svg',
  'Tesla': '/logos/tesla-logo.svg',
  'Airbnb': '/logos/airbnb-logo.svg',
  'Spotify': '/logos/spotify-only.svg',
  'Netflix': '/logos/netflix-only.svg',
  'Slack': '/logos/slack-only.svg',
  'Atlassian': '/logos/atlassian.svg',
  'Adobe': '/logos/adobe-only.svg',
  'WhatsApp': '/logos/whatsapp-only.svg',
  'Loom': '/logos/loom-only.svg'
};

// Build job data from NVIDIA JSON
const jobData = (Array.isArray(nvidiaJobs) ? nvidiaJobs : []).map((job, idx) => ({
  id: idx + 1,
  company: job.company || 'NVIDIA',
  logo: companyLogos[job.company] || companyLogos['NVIDIA'],
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
    
    // Add custom CSS for Driver.js popover styling
    const style = document.createElement('style');
    style.textContent = `
      .driver-popover-custom {
        border-radius: 16px !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        background: rgba(17, 24, 39, 0.95) !important;
      }
      
      .driver-popover-custom .driver-popover-title {
        color: #f3f4f6 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.75rem !important;
      }
      
      .driver-popover-custom .driver-popover-description {
        color: #d1d5db !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
        margin-bottom: 1rem !important;
      }
      
      .driver-popover-custom .driver-popover-footer {
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding-top: 1rem !important;
      }
      
      .driver-popover-custom .driver-popover-progress-text {
        color: #9ca3af !important;
        font-size: 0.875rem !important;
      }
      
      .driver-popover-custom .driver-popover-btn {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
      }
      
      .driver-popover-custom .driver-popover-btn.driver-popover-btn-primary {
        background: #3b82f6 !important;
        border: 1px solid #3b82f6 !important;
        color: white !important;
      }
      
      .driver-popover-custom .driver-popover-btn.driver-popover-btn-primary:hover {
        background: #2563eb !important;
        border-color: #2563eb !important;
      }
      
      .driver-popover-custom .driver-popover-btn.driver-popover-btn-secondary {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #d1d5db !important;
      }
      
      .driver-popover-custom .driver-popover-btn.driver-popover-btn-secondary:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
      }
      
      /* Special styling for step 1 - larger size */
      .driver-popover-step-1 {
        min-width: 400px !important;
        max-width: 500px !important;
        width: auto !important;
        padding: 2rem !important;
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.98) 0%, rgba(31, 41, 55, 0.95) 100%) !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(59, 130, 246, 0.1) !important;
      }
      
      .driver-popover-step-1 .driver-popover-title {
        font-size: 1.5rem !important;
        text-align: center !important;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 1rem !important;
      }
      
      .driver-popover-step-1 .driver-popover-description {
        font-size: 1.125rem !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        color: #e5e7eb !important;
        line-height: 1.6 !important;
      }
      
      .driver-popover-step-1 .driver-popover-footer {
        margin-top: 1.5rem !important;
        padding-top: 1.5rem !important;
        border-top: 1px solid rgba(59, 130, 246, 0.2) !important;
      }
      
      /* Custom highlight styling for step 1 */
      .driver-popover-step-1 ~ .driver-highlighted-element {
        border-radius: 16px !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3), 0 0 20px rgba(59, 130, 246, 0.2) !important;
        background: rgba(59, 130, 246, 0.05) !important;
        transition: all 0.3s ease !important;
      }
      
      /* Enhanced highlight for the job card header */
      #job-card-header.driver-highlighted-element {
        background: rgba(59, 130, 246, 0.08) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        margin: -0.5rem !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4), 0 0 15px rgba(59, 130, 246, 0.3) !important;
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.body.classList.remove('dark');
      // Clean up the style element
      if (document.head.contains(style)) {
        document.head.removeChild(style);
      }
    };
  }, []);
  const [currentJobIndex, setCurrentJobIndex] = useState(0);
  const [savedVersion, setSavedVersion] = useState(0);
  const [activeTab, setActiveTab] = useState('home');
  const [navigatedFromFavorited, setNavigatedFromFavorited] = useState(false);
  const [showTourButton, setShowTourButton] = useState(false);
  const [showTooltip, setShowTooltip] = useState(null);

  // Driver.js configuration
  const driverObj = driver({
    showProgress: true,
    showButtons: ['next', 'previous', 'close'],
    nextBtnText: 'Next →',
    prevBtnText: '← Previous',
    doneBtnText: 'Got it!',
    closeBtnText: 'Skip tour',
    progressText: 'Step {{current}} of {{total}}',
    popoverClass: 'driver-popover-custom',
    steps: [
      {
        element: '#job-card',
        popover: {
          title: 'Welcome to WorkBee! 🐝',
          description: 'This is your job discovery platform. Here you can browse through available job opportunities from top companies.',
          side: 'bottom',
          align: 'center',
          popoverClass: 'driver-popover-custom driver-popover-step-1'
        }
      },
      {
        element: '#company-logo',
        popover: {
          title: 'Company Information',
          description: 'Each job card shows the company logo, making it easy to identify opportunities from your favorite companies.',
          side: 'right',
          align: 'center'
        }
      },
      {
        element: '#job-card-header',
        popover: {
          title: 'Job Title',
          description: 'Each job card shows the Job Title, making it easy to identify opportunities from your favorite companies.',
          side: 'right',
          align: 'center'
        }
      },
      {
        element: '#job-details',
        popover: {
          title: 'Job Details',
          description: 'View important information like location, experience level, and posting date to help you make informed decisions.',
          side: 'top',
          align: 'center'
        }
      },
      {
        element: '#job-description',
        popover: {
          title: 'Job Description',
          description: 'Read the full job description to understand the role requirements and responsibilities. Click "Read More" for the complete details.',
          side: 'top',
          align: 'center'
        }
      },
      {
        element: '#favorite-button',
        popover: {
          title: 'Save Jobs',
          description: 'Click the heart icon to save jobs you\'re interested in. Saved jobs will appear in your favorites section.',
          side: 'left',
          align: 'center'
        }
      },
      {
        element: '#apply-button',
        popover: {
          title: 'Apply Now',
          description: 'Ready to apply? Click this button to be taken directly to the company\'s application page.',
          side: 'left',
          align: 'center'
        }
      },
      {
        element: '#navigation-arrows',
        popover: {
          title: 'Browse Jobs',
          description: 'Use these arrows to navigate between different job opportunities. You can also use keyboard arrows.',
          side: 'top',
          align: 'center'
        }
      },
      {
        element: '#bottom-navigation',
        popover: {
          title: 'Navigation Menu',
          description: 'Access different sections of WorkBee: search for jobs, view your saved jobs, and manage notifications.',
          side: 'top',
          align: 'center'
        }
      },
      {
        element: '#nav-search',
        popover: {
          title: 'Search Feature',
          description: 'Click here to access the search page where you can find specific job opportunities.',
          side: 'top',
          align: 'center'
        }
      },
      {
        element: '#nav-saved',
        popover: {
          title: 'Saved Jobs',
          description: 'View all your saved job opportunities in one place.',
          side: 'top',
          align: 'center'
        }
      }
    ]
  });

  // Start the tour
  const startTour = () => {
    driverObj.drive();
    setShowTourButton(false);
  };

  // Check if user has completed the tour
  useEffect(() => {
    const hasCompletedTour = storageUtils.tourUtils.hasCompletedTour();
    if (!hasCompletedTour) {
      setShowTourButton(true);
    }
  }, []);

  // Mark tour as completed
  const onTourComplete = () => {
    storageUtils.tourUtils.markTourCompleted();
    setShowTourButton(false);
  };

  // Add event listener for tour completion
  useEffect(() => {
    const handleTourComplete = () => {
      onTourComplete();
    };

    // Listen for tour completion
    document.addEventListener('driver:completed', handleTourComplete);
    document.addEventListener('driver:closed', handleTourComplete);

    return () => {
      document.removeEventListener('driver:completed', handleTourComplete);
      document.removeEventListener('driver:closed', handleTourComplete);
    };
  }, []);

  // Tooltip component
  const Tooltip = ({ children, content, position = 'top' }) => {
    const [isVisible, setIsVisible] = useState(false);
    
    return (
      <div 
        className="relative inline-block"
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
      >
        {children}
        {isVisible && (
          <div className={`absolute z-50 px-3 py-2 text-sm text-white bg-gray-900 rounded-lg shadow-lg whitespace-nowrap ${
            position === 'top' ? 'bottom-full mb-2' : 
            position === 'bottom' ? 'top-full mt-2' :
            position === 'left' ? 'right-full mr-2' : 'left-full ml-2'
          }`}>
            {content}
            <div className={`absolute w-2 h-2 bg-gray-900 transform rotate-45 ${
              position === 'top' ? 'top-full -mt-1 left-1/2 -translate-x-1/2' :
              position === 'bottom' ? 'bottom-full -mb-1 left-1/2 -translate-x-1/2' :
              position === 'left' ? 'left-full -ml-1 top-1/2 -translate-y-1/2' :
              'right-full -mr-1 top-1/2 -translate-y-1/2'
            }`} />
          </div>
        )}
      </div>
    );
  };

  const getSavedMap = () => {
    return storageUtils.getSavedJobs();
  };
  const isJobSaved = (job) => {
    const saved = getSavedMap();
    const company = job.company || 'Unknown';
    const key = `${company}__${job.title}`;
    return Boolean(saved?.[company]?.[key]);
  };
  const visibleJobs = React.useMemo(() => {
    // If user hasn't navigated away from a favorited job, show all jobs
    if (!navigatedFromFavorited) {
      return jobData;
    }
    // If user has navigated away, filter out favorited jobs
    return jobData.filter((job) => !isJobSaved(job));
  }, [savedVersion, navigatedFromFavorited]);
  const currentJob = visibleJobs[currentJobIndex];
  const [isExpanded, setIsExpanded] = useState(false);
  const [isFavorited, setIsFavorited] = useState(null); // null = loading, true/false = loaded
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const touchStartXRef = useRef(null);
  const touchStartYRef = useRef(null);

  // Helper function to get next valid job index
  const getNextValidIndex = (currentIndex, direction) => {
    const totalJobs = visibleJobs.length;
    if (totalJobs === 0) return 0;
    
    return direction === 'next' 
      ? (currentIndex + 1) % totalJobs
      : (currentIndex - 1 + totalJobs) % totalJobs;
  };
  const handlePrevious = () => {
    if (visibleJobs.length === 0) return;
    // Check if current job is favorited before navigating away
    if (currentJob && isJobSaved(currentJob)) {
      setNavigatedFromFavorited(true);
    }
    setCurrentJobIndex((prev) => getNextValidIndex(prev, 'prev'));
  };

  const handleNext = () => {
    if (visibleJobs.length === 0) return;
    // Check if current job is favorited before navigating away
    if (currentJob && isJobSaved(currentJob)) {
      setNavigatedFromFavorited(true);
    }
    setCurrentJobIndex((prev) => getNextValidIndex(prev, 'next'));
  };

  // Initialize favorited state based on localStorage when job changes
  useEffect(() => {
    if (!currentJob) {
      setIsFavorited(false);
      return;
    }
    setIsFavorited(storageUtils.isJobSaved(currentJob));
  }, [currentJob]);

  // Debug: Log storage info on mount
  useEffect(() => {
    const storageInfo = storageUtils.getStorageInfo();
    console.log('Storage Info:', storageInfo);
    console.log('All saved jobs:', storageUtils.getSavedJobs());
  }, []);

  // TODO: Replace with API call
  const handleApply = () => {
    if (currentJob && currentJob.job_link) {
      window.open(currentJob.job_link, '_blank', 'noopener,noreferrer');
      return;
    }
    console.log(`Applying to ${currentJob.company} - ${currentJob.title}`);
    // API call will go here
  };

  // Handle job selection from search
  const handleJobSelect = (job) => {
    setSelectedJob(job);
    setIsModalOpen(true);
  };

  const handleFavorite = () => {
    if (!currentJob) return;
    
    const isCurrentlySaved = storageUtils.isJobSaved(currentJob);
    
    if (isCurrentlySaved) {
      // Remove the job
      const success = storageUtils.removeJob(currentJob, currentJob.company);
      if (success) {
        setIsFavorited(false);
        console.log('Job removed from favorites');
      } else {
        console.error('Failed to remove job from favorites');
      }
    } else {
      // Add the job
      const success = storageUtils.addJob(currentJob);
      if (success) {
        setIsFavorited(true);
        console.log('Job added to favorites');
      } else {
        console.error('Failed to add job to favorites');
      }
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
  // Set random initial job and keep index in bounds when list changes
  useEffect(() => {
    if (visibleJobs.length > 0) {
      // If this is the first load or if current index is out of bounds, set random index
      if (currentJobIndex >= visibleJobs.length || currentJobIndex === 0) {
        const randomIndex = Math.floor(Math.random() * visibleJobs.length);
        setCurrentJobIndex(randomIndex);
      }
    }
  }, [visibleJobs.length, currentJobIndex]);
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

      {/* Tour Control Buttons - Positioned absolutely to avoid layout interference */}
      <div className="fixed top-4 right-24 sm:right-32 z-50 flex flex-col gap-2 max-w-[180px] sm:max-w-none">
        {/* Tour Button */}
        {showTourButton && (
          <button
            onClick={startTour}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors shadow-lg text-xs sm:text-sm"
          >
            <Play className="w-3 h-3 sm:w-4 sm:h-4" />
            <span className="hidden sm:inline">Take a Tour</span>
            <span className="sm:hidden">Tour</span>
          </button>
        )}

        {/* Help Button - Always visible */}
        <button
          onClick={startTour}
          className="flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors shadow-lg text-xs sm:text-sm"
          title="Start product tour"
        >
          <HelpCircle className="w-3 h-3 sm:w-4 sm:h-4" />
          <span className="hidden sm:inline">Help</span>
        </button>

        {/* Debug: Reset Tour Button (only in development) */}
        {process.env.NODE_ENV === 'development' && (
          <button
            onClick={() => {
              storageUtils.tourUtils.resetTour();
              setShowTourButton(true);
              console.log('Tour reset for testing');
            }}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors shadow-lg text-xs sm:text-sm"
            title="Reset tour (dev only)"
          >
            <span className="hidden sm:inline">Reset Tour</span>
            <span className="sm:hidden">Reset</span>
          </button>
        )}
      </div>

      {/* Main Content */}
      <div className="px-4 py-8 flex items-center justify-center relative z-10" id="job-card">
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
            <div  className="hidden sm:flex">

              <button
                onClick={handlePrevious}
                className="absolute -left-16 glassmorphic-base cursor-pointer top-1/2 transform -translate-y-1/2 w-12 h-12 sm:w-16 sm:h-16 border rounded-full items-center justify-center transition-colors -ml-95">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M63.5413 50H36.458M36.458 50L46.8747 39.5833M36.458 50L46.8747 60.4167" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M70.8333 18.8148C64.8746 14.8261 57.7089 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 70.7107 29.2893 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 43.1696 85.6739 36.7657 82.4832 31.25" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>

              </button>
              <button
              id="navigation-arrows"
                onClick={handleNext}
                className="absolute cursor-pointer -right-16 top-1/2 transform -translate-y-1/2 w-12 h-12 sm:w-16 sm:h-16 glassmorphic-base border border-gray-600 rounded-full items-center justify-center hover:bg-gray-700 transition-colors -mr-95">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M36.4587 50H63.542M63.542 50L53.1253 60.4167M63.542 50L53.1253 39.5833" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M29.1667 81.1852C35.1254 85.1739 42.2911 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 29.2893 70.7107 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 56.8304 14.3261 63.2343 17.5168 68.75" stroke="#CDCDCD" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>

              </button>
          </div>

          {/* Job Card */}
          <div
            key={currentJob.id || currentJob.title}
            className="bg-gradient-to-br from-[#D9D9D9] to-[#737373] rounded-3xl sm:rounded-[60px] p-6 sm:p-8 text-black shadow-2xl border-4 w-full sm:w-230 h-auto sm:h-140 ml-0 sm:-ml-55 sm:-mt-17 select-none touch-pan-y"
          >
            {/* Header with Company Logo and Job Title */}
            <div className="flex items-start justify-between mb-6">
              {/* Company Logo */}
              <div id="company-logo" className="flex-shrink-0 w-16 h-16 sm:w-20 sm:h-20 bg-white rounded-2xl sm:rounded-3xl flex items-center justify-center p-3 sm:p-4 shadow-lg">
                <img
                  src={currentJob.logo}
                  alt={`${currentJob.company} logo`}
                  className="w-10 h-10 sm:w-12 sm:h-12 object-contain"
                  onError={(e) => {
                    const img = e.currentTarget;
                    if (img.src.includes('-only')) img.src = img.src.replace('-only','');
                  }}
                />
              </div>
              
              {/* Job Title */}
              <div className="flex-1 ml-4 sm:ml-6">
                <h2  id="job-card-header" className="text-xl sm:text-3xl font-bold leading-tight text-gray-900 break-words line-clamp-2">
                  {currentJob.title}
                </h2>
                <p className="text-sm sm:text-lg font-medium text-gray-700 mt-1">
                  {currentJob.company}
                </p>
              </div>
            </div>



            {/* Job Details */}
            <div id="job-details" className="flex flex-col sm:flex-row sm:items-center gap-4 mb-6">
              {/* Location - only render if available */}
              {currentJob.location && currentJob.location.trim() !== '' && (
                <div className="flex items-center text-sm sm:text-base text-gray-700">
                  <svg className="w-4 h-4 mr-2 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                  <span className="font-medium">{currentJob.location}</span>
                </div>
              )}
              
              {/* Experience Level - only render if available */}
              {currentJob.level && currentJob.level.trim() !== '' && currentJob.level !== 'Not specified' && (
                <div className="flex items-center text-sm sm:text-base text-gray-700">
                  <svg className="w-4 h-4 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                  </svg>
                  <span className="font-medium">{currentJob.level}</span>
                </div>
              )}

              {/* Posted Date - only render if available */}
              {currentJob.postedDate && currentJob.postedDate.trim() !== '' && (
                <div className="flex items-center text-sm sm:text-base text-gray-700">
                  <svg className="w-4 h-4 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span className="font-medium">{currentJob.postedDate}</span>
                </div>
              )}
            </div>

            {/* Job Description Section */}
            <div id="job-description" className="mb-6">
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 mb-3">Job Description</h3>
              {currentJob.description && currentJob.description.trim() !== '' ? (
                <div className="bg-white/20 rounded-xl p-4 backdrop-blur-sm">
                  <p className={`text-sm sm:text-base text-gray-800 leading-relaxed ${isExpanded ? '' : 'line-clamp-3'}`}>
                    {currentJob.description}
                  </p>
                  <button
                    className="mt-3 text-sm font-semibold text-blue-700 hover:text-blue-800 transition-colors cursor-pointer"
                    onClick={(e) => { e.stopPropagation(); setIsModalOpen(true); }}
                  >
                    Read More →
                  </button>
                </div>
              ) : (
                <div className="bg-white/20 rounded-xl p-4 backdrop-blur-sm">
                  <p className="text-sm sm:text-base text-gray-600 italic text-center py-4">
                    No job description available. Click Apply Now to learn more!
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center justify-end pt-10 border-t border-white/20">
              <Tooltip content={isFavorited ? "Remove from favorites" : "Save this job"} position="top">
                <button
                  id="favorite-button"
                  onClick={handleFavorite}
                  className={`w-12 h-12 sm:w-14 sm:h-14 rounded-full flex items-center justify-center transition-all duration-200 shadow-lg ${
                    isFavorited === true
                      ? 'bg-red-500 hover:bg-red-600 shadow-red-500/25' 
                      : 'bg-white/20 hover:bg-white/30 backdrop-blur-sm'
                  }`}
                >
                  <Heart 
                    className={`w-6 h-6 sm:w-7 sm:h-7 ${
                      isFavorited === true ? 'text-white fill-white' : 'text-gray-700'
                    }`} 
                    fill={isFavorited === true ? '#fff' : 'none'} 
                  />
                </button>
              </Tooltip>
              
              <Tooltip content="Apply to this job position" position="top">
                <button
                  id="apply-button"
                  onClick={(e) => { e.stopPropagation(); handleApply(); }}
                  className="flex-1 sm:flex-none sm:px-8 py-3 sm:py-4 bg-black hover:bg-gray-800 text-white rounded-xl sm:rounded-full font-semibold transition-all duration-200 shadow-lg hover:shadow-xl text-base sm:text-lg ml-3"
                >
                  Apply Now
                </button>
              </Tooltip>
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
      <div id="bottom-navigation">
        <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} onJobSelect={handleJobSelect} />
      </div>
      {/* Details Modal */}
      <JobDetailsModal
        isOpen={isModalOpen}
        job={selectedJob || currentJob}
        onClose={() => {
          setIsModalOpen(false);
          setSelectedJob(null);
        }}
        onApply={handleApply}
        onFavorite={() => setIsFavorited((prev) => !prev)}
        isFavorited={isFavorited}
      />
    </div>
  );
};

export default WorkBeeJobCard;