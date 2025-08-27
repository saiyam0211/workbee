import React, { useState } from 'react';
import GlassFooter from '@/components/ui/GlassFooter';

const companies = [
  { name: 'Microsoft', logo: '/logos/microsoft.svg', views: 10 },
  { name: 'Spotify', logo: '/logos/spotify.svg', views: 2 },
  { name: 'Slack', logo: '/logos/slack.svg', views: 6 },
  { name: 'Adobe', logo: '/logos/adobe.svg', views: 19 },
  { name: 'WhatsApp', logo: '/logos/whatsapp.svg', views: 8 },
  { name: 'Atlassian', logo: '/logos/atlassian.svg', views: 5 },
  { name: 'Razorpay', logo: '/logos/razorpay.svg', views: 12 },
  { name: 'Loom', logo: '/logos/lom.svg', views: 3 },
];

export default function FavCompanies() {
  const [activeTab, setActiveTab] = useState('jobs');
  return (
    <div className="min-h-screen bg-[#09090b] text-foreground relative">
      <div className="px-6 max-w-6xl mx-auto min-h-[80vh] flex flex-col items-center justify-end pb-10 pt-[200px]">
        <h1 className="text-center text-5xl md:text-6xl font-extrabold notification-text tracking-tight opacity-90"
        >
          Your Dream Companies
        </h1>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-8 mt-4">
          {companies.map((c) => (
            <div key={c.name} className="relative rounded-[50px] bg-gradient-to-b from-[#D9D9D9] to-[#8A8A8A] p-5 shadow-2xl border border-white/20 aspect-square flex flex-col">
              <div className="absolute right-4 top-4 w-10 h-10 bg-white/40 backdrop-blur-sm rounded-full flex items-center justify-center shadow-md border border-white/30">
                <img src={c.logo} alt={`${c.name} logo`} className="w-6 h-6 object-contain opacity-80" />
              </div>
              <div className="flex-1 flex items-start justify-center">
                <div className="text-4xl md:text-4xl fav-companies-text font-semibold text-black/50 mt-8 text-center">{c.name}</div>
              </div>
              <div className="flex items-end gap-2 text-black/70">
                <div className="text-4xl md:text-5xl font-extrabold leading-none">{c.views}</div>
                <div className="flex flex-col leading-tight">
                  <span className="text-sm">View</span>
                  <span className="text-[10px] md:text-xs text-black/60">Saved Jobs</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  );
}


