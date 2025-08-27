import React, { useState, useEffect } from 'react';
import { Heart } from 'lucide-react';
import GlassFooter from './GlassFooter';



// Sample job data - this will be replaced with API calls
const jobData = [
  {
    id: 1,
    company: "Microsoft",
    logo: "/logos/microsoft.svg",
    title: "Software Engineer - Azure",
    location: "Seattle, Washington, USA",
    level: "Mid",
    description: "Join Microsoft's Azure team to build cloud infrastructure that powers millions of applications worldwide. Work on cutting-edge technologies and help shape the future of cloud computing.",
    postedDate: "2 days ago"
  },
  {
    id: 2,
    company: "Spotify",
    logo: "/logos/spotify.svg",
    title: "Frontend Developer - Music Platform",
    location: "Stockholm, Sweden",
    level: "Senior",
    description: "Create amazing user experiences for music lovers around the world. Work with React, TypeScript, and modern web technologies to build the next generation of music streaming.",
    postedDate: "1 week ago"
  },
  {
    id: 3,
    company: "Slack",
    logo: "/logos/slack.svg",
    title: "Product Designer - Collaboration Tools",
    location: "San Francisco, California, USA",
    level: "Mid",
    description: "Design intuitive collaboration experiences that help teams work better together. Focus on user research, prototyping, and creating delightful product experiences.",
    postedDate: "3 days ago"
  },
  {
    id: 4,
    company: "Adobe",
    logo: "/logos/adobe.svg",
    title: "Creative Cloud Developer",
    location: "San Jose, California, USA",
    level: "Senior",
    description: "Build creative tools that empower artists and designers worldwide. Work on Creative Cloud applications and help shape the future of digital creativity.",
    postedDate: "5 days ago"
  },
  {
    id: 5,
    company: "WhatsApp",
    logo: "/logos/whatsapp.svg",
    title: "Mobile Engineer - Messaging",
    location: "Menlo Park, California, USA",
    level: "Mid",
    description: "Develop features for WhatsApp's mobile applications used by billions of users. Focus on performance, security, and user experience on mobile platforms.",
    postedDate: "1 day ago"
  },
  {
    id: 6,
    company: "Loom",
    logo: "/logos/lom.svg",
    title: "Video Platform Engineer",
    location: "San Francisco, California, USA",
    level: "Mid",
    description: "Build video recording and sharing tools that help teams communicate more effectively. Work on video processing, streaming, and collaboration features.",
    postedDate: "4 days ago"
  },
  {
    id: 7,
    company: "Atlassian",
    logo: "/logos/atlassian.svg",
    title: "DevOps Engineer - Jira",
    location: "Sydney, Australia",
    level: "Senior",
    description: "Scale Jira's infrastructure to support millions of developers worldwide. Focus on reliability, performance, and developer productivity tools.",
    postedDate: "6 days ago"
  },
  {
    id: 8,
    company: "Razorpay",
    logo: "/logos/razorpay.svg",
    title: "Full Stack Developer - Payments",
    location: "Bangalore, Karnataka, India",
    level: "Mid",
    description: "Build payment solutions that power businesses across India. Work on fintech products that handle millions of transactions securely and efficiently jkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.",
    postedDate: "2 days ago"
  }
];

const WorkBeeJobCard = () => {
  useEffect(() => {
    document.body.classList.add('dark');
    return () => document.body.classList.remove('dark');
  }, []);
  const [currentJobIndex, setCurrentJobIndex] = useState(0);
  const [activeTab, setActiveTab] = useState('home');
  const currentJob = jobData[currentJobIndex];
  const [isExpanded, setIsExpanded] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);
  const handlePrevious = () => {
    setCurrentJobIndex((prev) => (prev === 0 ? jobData.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setCurrentJobIndex((prev) => (prev === jobData.length - 1 ? 0 : prev + 1));
  };

  // TODO: Replace with API call
  const handleApply = () => {
    console.log(`Applying to ${currentJob.company} - ${currentJob.title}`);
    // API call will go here
  };

  const handleFavorite = () => {

    console.log(`Favoriting ${currentJob.company} - ${currentJob.title}`);

    // API call will go here
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
      <div className="flex items-center justify-between p-4 relative z-10">
        <h1 className="text-4xl ml-20 font-bold text-foreground">WorkBee</h1>

        <button>
          <img className='w-25 h-25 mr-25' src="./public/images/image.png" alt="" />

        </button>


      </div>

      {/* Main Content */}
      <div className="px-4 py-8 flex items-center justify-center relative z-10">
        <div className="relative max-w-md w-full">
          {/* Navigation Arrows */}
          <button
            onClick={handlePrevious}
            className="absolute -left-16 glassmorphic-base cursor-pointer top-1/2 transform -translate-y-1/2 w-16 h-16  border  rounded-full flex items-center justify-center transition-colors -ml-95">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M63.5413 50H36.458M36.458 50L46.8747 39.5833M36.458 50L46.8747 60.4167" stroke="#CDCDCD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M70.8333 18.8148C64.8746 14.8261 57.7089 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 70.7107 29.2893 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 43.1696 85.6739 36.7657 82.4832 31.25" stroke="#CDCDCD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            </svg>

          </button>

          <button
            onClick={handleNext}
            className="absolute cursor-pointer -right-16 top-1/2 transform -translate-y-1/2 w-16 h-16 glassmorphic-base border border-gray-600 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors -mr-95">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M36.4587 50H63.542M63.542 50L53.1253 60.4167M63.542 50L53.1253 39.5833" stroke="#CDCDCD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M29.1667 81.1852C35.1254 85.1739 42.2911 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 29.2893 70.7107 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 56.8304 14.3261 63.2343 17.5168 68.75" stroke="#CDCDCD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            </svg>

          </button>

          {/* Job Card */}
          <div className="bg-gradient-to-br from-[#D9D9D9] to-[#737373] -ml-55 rounded-[60px] p-15 text-black shadow-2xl border-4 -mt-17  w-230 h-140">
            {/* Company Logo */}
            <div className="flex justify-end mb-4">
              <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center p-2">
                <img
                  src={currentJob.logo}
                  alt={`${currentJob.company} logo`}
                  className="w-8 h-8 object-contain"
                />
              </div>
            </div>

            {/* Job Title */}
            <h2 className="text-4xl -mt-22 ml-6 font-bold mb-2">
              {currentJob.title}
            </h2>



            {/* Location and Level */}
            <div className="flex items-center text-lg ml-6 text-gray-900 mb-6">
              <span className="mr-1"><svg width="19" height="19" viewBox="0 0 19 19" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9.49967 17.1346C9.31495 17.1346 9.15662 17.0827 9.02467 16.9788C8.89273 16.875 8.79377 16.7387 8.7278 16.57C8.47711 15.843 8.16044 15.1615 7.7778 14.5255C7.40835 13.8894 6.88717 13.143 6.21426 12.2863C5.54134 11.4296 4.99377 10.6118 4.57155 9.83293C4.16252 9.05409 3.95801 8.11298 3.95801 7.00962C3.95801 5.49087 4.49238 4.20577 5.56113 3.15433C6.64308 2.0899 7.95592 1.55769 9.49967 1.55769C11.0434 1.55769 12.3497 2.0899 13.4184 3.15433C14.5004 4.20577 15.0413 5.49087 15.0413 7.00962C15.0413 8.19087 14.8104 9.1774 14.3486 9.96923C13.9 10.7481 13.3788 11.5204 12.7851 12.2863C12.0726 13.2209 11.5316 13.9998 11.1622 14.6228C10.8059 15.2329 10.509 15.882 10.2715 16.57C10.2056 16.7517 10.1 16.8945 9.95488 16.9983C9.82294 17.0892 9.6712 17.1346 9.49967 17.1346ZM9.49967 8.95673C10.0538 8.95673 10.5222 8.76851 10.9049 8.39207C11.2875 8.01563 11.4788 7.55481 11.4788 7.00962C11.4788 6.46442 11.2875 6.00361 10.9049 5.62716C10.5222 5.25072 10.0538 5.0625 9.49967 5.0625C8.94551 5.0625 8.47711 5.25072 8.09447 5.62716C7.71183 6.00361 7.52051 6.46442 7.52051 7.00962C7.52051 7.55481 7.71183 8.01563 8.09447 8.39207C8.47711 8.76851 8.94551 8.95673 9.49967 8.95673Z" fill="#1D1B20" />
              </svg>
              </span>
              <span>{currentJob.location}</span>
              <div className="flex items-center ml-4">
                <span className="mr-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 22H21" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M5.59998 8.38H4C3.45 8.38 3 8.83 3 9.38V18C3 18.55 3.45 19 4 19H5.59998C6.14998 19 6.59998 18.55 6.59998 18V9.38C6.59998 8.83 6.14998 8.38 5.59998 8.38Z" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M12.8002 5.19H11.2002C10.6502 5.19 10.2002 5.64 10.2002 6.19V18C10.2002 18.55 10.6502 19 11.2002 19H12.8002C13.3502 19 13.8002 18.55 13.8002 18V6.19C13.8002 5.64 13.3502 5.19 12.8002 5.19Z" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M20.0004 2H18.4004C17.8504 2 17.4004 2.45 17.4004 3V18C17.4004 18.55 17.8504 19 18.4004 19H20.0004C20.5504 19 21.0004 18.55 21.0004 18V3C21.0004 2.45 20.5504 2 20.0004 2Z" stroke="#292D32" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                </span>
                <span>{currentJob.level}</span>
              </div>
            </div>

            {/* Job Description Section */}
            <div className="mb-8 h-40">
              <h3 className="text-3xl ml-6 mt-10 font-bold mb-2">Job Description</h3>
              <div className="mb-2">
                <span className="font-semibold text-xl ml-6">About the job</span>
              </div>
              <p className={`text-xl ml-6 text-gray-700 leading-relaxed ${isExpanded ? '' : 'clamp-3'}`}>
                {currentJob.description}
              </p>
             

            </div>

            {/* Action Buttons */}
            {/*
              Add isFavorited state to control the button fill.
              Place this near the other useState hooks:
              const [isFavorited, setIsFavorited] = useState(false);
            */}
            <div className="flex ml-135 mt-24 items-center justify-center space-x-4 ">
              <button
                onClick={() => {
                  handleFavorite();
                  setIsFavorited((prev) => !prev);
                }}
                className={`w-15 h-15 cursor-pointer apply-button rounded-full flex items-center justify-center glassmorphic-base transition-colors ${isFavorited ? 'bg-red-600' : ''}`}
                style={isFavorited ? { backgroundColor: '#ef4444' } : {}}
              >
                <span className="text-3xl">
                  <Heart className={isFavorited ? 'text-white fill-white' : 'text-white'} fill={isFavorited ? '#fff' : 'none'} />
                </span>
              </button>
              <button
                onClick={handleApply}
                className="px-8 -45 h-15 py-3 apply-button glassmorphic-base text-white rounded-full font-semibold hover:bg-gray-600 transition-colors text-xl">
                Apply Now
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Glass Footer Navigation */}
      <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
};

export default WorkBeeJobCard;