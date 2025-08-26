import React, { useState, useEffect } from 'react';

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
    description: "Build payment solutions that power businesses across India. Work on fintech products that handle millions of transactions securely and efficiently.",
    postedDate: "2 days ago"
  }
];

const WorkBeeJobCard = () => {
  useEffect(() => {
    document.body.classList.add('dark');
    return () => document.body.classList.remove('dark');
  }, []);
  const [currentJobIndex, setCurrentJobIndex] = useState(0);
  const currentJob = jobData[currentJobIndex];

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
    <div className="min-h-screen bg-background text-foreground font-sans">
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
        <div className="flex items-center space-x-4">
         
          <div className="w-13 h-13 border mr-30 border-border rounded-lg flex items-center justify-center">
            <div className="w-4 h-4 border-l border-b border-border transform rotate-45"></div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-4 py-8 flex items-center justify-center relative z-10">
        <div className="relative max-w-md w-full">
          {/* Navigation Arrows */}
          <button 
            onClick={handlePrevious}
            className="absolute -left-16 top-1/2 transform -translate-y-1/2 w-16 h-16 bg-gray-800 border border-gray-600 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors -ml-95">
            <span className="text-3xl">‹</span>
          </button>
          
          <button 
            onClick={handleNext}
            className="absolute -right-16 top-1/2 transform -translate-y-1/2 w-16 h-16 bg-gray-800 border border-gray-600 rounded-full flex items-center justify-center hover:bg-gray-700 transition-colors -mr-95">
            <span className="text-3xl">›</span>
          </button>

          {/* Job Card */}
                     <div className="bg-gradient-to-br from-[#D9D9D9] to-[#737373] -ml-55 rounded-[60px] p-15 text-black shadow-2xl border-4  w-230 h-140">
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
            <div className="flex items-center text-lg ml-6 text-gray-600 mb-6">
              <span className="mr-1">📍</span>
              <span>{currentJob.location}</span>
              <div className="flex items-center ml-4">
                <span className="mr-1">📅</span>
                <span>{currentJob.level}</span>
              </div>
            </div>

            {/* Job Description Section */}
            <div className="mb-8">
              <h3 className="text-3xl ml-6 mt-10 font-bold mb-2">Job Description</h3>
              <div className="mb-2">
                <span className="font-semibold text-xl ml-6">About the job</span>
              </div>
              <p className="text-xl ml-6 text-gray-700 leading-relaxed">
                {currentJob.description}
              </p>
             
            </div>

             {/* Action Buttons */}
             <div className="flex ml-135 mt-20 items-center justify-center space-x-4">
               <button 
                 onClick={handleFavorite}
                 className="w-15 h-15 bg-gray-400 rounded-full flex items-center justify-center hover:bg-gray-500 transition-colors">
                 <span className="text-3xl">❤️</span>
               </button>
               <button 
                 onClick={handleApply}
                 className="px-8 w-45 h-15 py-3 bg-gray-700 text-white rounded-full font-semibold hover:bg-gray-600 transition-colors text-xl">
                 Apply Now
               </button>
             </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation - Glassmorphic */}
      <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2">
        <div className="bg-black/30 backdrop-blur-xl border border-white/10 rounded-full px-6 py-3 shadow-2xl">
          <div className="flex items-center space-x-8">
            <button className="flex flex-col items-center space-y-1 text-blue-400">
              <span className="text-2xl">🏠</span>
              <span className="text-xs underline">Home</span>
            </button>
            <button className="flex flex-col items-center space-y-1 text-gray-400 hover:text-white transition-colors">
              <span className="text-2xl">📄</span>
            </button>
            <button className="flex flex-col items-center space-y-1 text-gray-400 hover:text-white transition-colors">
              <span className="text-2xl">❤️</span>
            </button>
            <button className="flex flex-col items-center space-y-1 text-gray-400 hover:text-white transition-colors">
              <span className="text-2xl">🔔</span>
            </button>
            <button className="flex flex-col items-center space-y-1 text-gray-400 hover:text-white transition-colors">
              <span className="text-2xl">👤</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkBeeJobCard;