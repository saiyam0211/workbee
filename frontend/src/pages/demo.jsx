import React from "react";
import { cn } from "@/lib/utils";
import { DIcons } from "dicons";
import { useAnimate } from "framer-motion";
import { Button, buttonVariants } from "@/components/ui/button";
import { HighlighterItem, HighlightGroup, Particles } from "@/components/ui/highlighter";
import { HeroSection } from "@/components/ui/hero-section-1";
import { FeatureCarousel } from "@/components/ui/animated-feature-carousel";

function Connect() {
  const [scope, animate] = useAnimate();

  React.useEffect(() => {
    animate(
      [
        ["#pointer", { left: 200, top: 60 }, { duration: 0 }],
        ["#javascript", { opacity: 1 }, { duration: 0.3 }],
        ["#pointer", { left: 50, top: 102 }, { at: "+0.5", duration: 0.5, ease: "easeInOut" }],
        ["#javascript", { opacity: 0.4 }, { at: "-0.3", duration: 0.1 }],
        ["#react-js", { opacity: 1 }, { duration: 0.3 }],
        ["#pointer", { left: 224, top: 170 }, { at: "+0.5", duration: 0.5, ease: "easeInOut" }],
        ["#react-js", { opacity: 0.4 }, { at: "-0.3", duration: 0.1 }],
        ["#typescript", { opacity: 1 }, { duration: 0.3 }],
        ["#pointer", { left: 88, top: 198 }, { at: "+0.5", duration: 0.5, ease: "easeInOut" }],
        ["#typescript", { opacity: 0.4 }, { at: "-0.3", duration: 0.1 }],
        ["#next-js", { opacity: 1 }, { duration: 0.3 }],
        ["#pointer", { left: 200, top: 60 }, { at: "+0.5", duration: 0.5, ease: "easeInOut" }],
        ["#next-js", { opacity: 0.5 }, { at: "-0.3", duration: 0.1 }],
      ],
      { repeat: Number.POSITIVE_INFINITY }
    );
  }, [animate]);

  return (
    <section id="contact" className="relative mx-auto mb-20 mt-30 w-6xl">
      <HighlightGroup className="group h-full">
        <div className="group/item h-full md:col-span-6 lg:col-span-12">
          <HighlighterItem className="rounded-3xl p-6">
            <div className="relative z-20 overflow-hidden rounded-3xl border border-slate-200 bg-[#000000] dark:border-slate-800">
              <Particles
                className="absolute inset-0 -z-10 opacity-10 transition-opacity duration-1000 ease-in-out group-hover/item:opacity-100"
                quantity={200}
                color="#555555"
                vy={-0.2}
              />
              <div className="flex justify-center">
                <div className="flex h-full flex-col justify-center gap-10 p-4 md:h-[300px] md:flex-row">
                  <div className="relative mx-auto h-[270px] w-[300px]" ref={scope}>
                    <DIcons.Designali className="absolute left-1/2 top-1/2 h-6 w-6 -translate-x-1/2 -translate-y-1/2" />
                    <div id="next-js" className="absolute bottom-12 left-14 rounded-3xl border border-slate-400 bg-gray-800 px-2 py-1.5 text-xs text-white">
                      Resume Building
                    </div>
                    <div id="react-js" className="absolute left-2 top-20 rounded-3xl border border-slate-400 bg-gray-800 px-2 py-1.5 text-xs text-white">
                      Job Alerts
                    </div>
                    <div id="typescript" className="absolute bottom-20 right-1 rounded-3xl border border-slate-400 bg-gray-800 px-2 py-1.5 text-xs text-white">
                      Career Counseling
                    </div>
                    <div id="javascript" className="absolute right-12 top-10 rounded-3xl border border-slate-400 bg-gray-800 px-2 py-1.5 text-xs text-white">
                      Internships
                    </div>
                    <div id="pointer" className="absolute">
                      <svg width="16.8" height="18.2" viewBox="0 0 12 13" className="fill-red-500" stroke="white" strokeWidth="1">
                        <path fillRule="evenodd" clipRule="evenodd" d="M12 5.50676L0 0L2.83818 13L6.30623 7.86537L12 5.50676V5.50676Z" />
                      </svg>
                      <span className="bg-ali relative -top-1 left-3 rounded-3xl px-2 py-1 text-xs text-white">Bee</span>
                    </div>
                  </div>
                  <div className="-mt-20 flex h-full flex-col justify-center p-2 md:-mt-4 md:ml-10 md:w-[400px]">
                    <div className="flex flex-col items-center">
                      <h3 className="mt-6 pb-1 font-bold text-white">
                        <span className="text-2xl md:text-4xl">Ready to unlock your dream career?</span>
                      </h3>
                    </div>
                    <p className="mb-4 text-white">Feel free to reach out to Us!</p>
                    <div className="flex flex-wrap gap-2">
                      <a href="https://cal.com/aliimam/designali" target="_blank" rel="noopener noreferrer">
                        <Button>Book a call</Button>
                      </a>
                      <a href="mailto:saiyamkumar2007+git@gmail.com" target="_blank" rel="noopener noreferrer" className={cn(buttonVariants({ variant: "outline", size: "icon" }))}>
                        <span className="flex items-center gap-1">
                          <DIcons.Mail strokeWidth={1} className="h-5 w-5" />
                        </span>
                      </a>
                      <a href="https://wa.me/918901825390" target="_blank" rel="noopener noreferrer" className={cn(buttonVariants({ variant: "outline", size: "icon" }))}>
                        <span className="flex items-center gap-1">
                          <DIcons.WhatsApp strokeWidth={1} className="h-4 w-4" />
                        </span>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </HighlighterItem>
        </div>
      </HighlightGroup>
    </section>
  );
}

export function Demo() {
  const images = {
    alt: "Feature screenshot",
    step1img1: "https://images.unsplash.com/photo-1618761714954-0b8cd0026356?q=80&w=1740&auto=format&fit=crop",
    step1img2: "https://images.unsplash.com/photo-1607705703571-c5a8695f18f6?q=80&w=1740&auto=format&fit=crop",
    step2img1: "https://images.unsplash.com/photo-1542393545-10f5cde2c810?q=80&w=1661&auto=format&fit=crop",
    step2img2: "https://images.unsplash.com/photo-1504639725590-34d0984388bd?q=80&w=1674&auto=format&fit=crop",
    step3img: "https://images.unsplash.com/photo-1587620962725-abab7fe55159?q=80&w=1740&auto=format&fit=crop",
    step4img: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1742&auto=format&fit=crop",
  };

  return (
    <>
      <HeroSection />
      <FeatureCarousel image={images} />
      
      <section id="ourteam" className="mt-50 py-12">
        <h2 className="text-6xl font-bold text-center text-white mb-12">Meet Our Team</h2>
        <div className="flex mt-30 flex-wrap justify-center gap-45">
          <div className="flex flex-col items-center">
            <div className="bg-gray-400 rounded-full w-40 h-40 mb-4">
              <img className="rounded-full" src="/images/saiyam.png" alt="Saiyam Kumar" />
            </div>
            <div className="text-white text-2xl font-semibold">Saiyam Kumar</div>
            <div className="text-gray-300 text-m mb-2">Deadline Driver</div>
            <div className="flex mt-3 gap-8">
              <a href="https://www.instagram.com/fr_saiyam/">
                <img className="h-7" src="/logos/linkdin.png" alt="LinkedIn" />
              </a>
              <a href="https://www.linkedin.com/in/saiyam0211/">
                <img className="h-7" src="/logos/insta.png" alt="Instagram" />
              </a>
              <a href="https://github.com/saiyam0211">
                <img className="h-7" src="/logos/github.png" alt="GitHub" />
              </a>
            </div>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="rounded-full w-40 h-40 mb-4">
              <img className="rounded-full" src="/images/janvi.jpg" alt="Janvi Yadav" />
            </div>
            <div className="text-white text-2xl font-semibold">Janvi Yadav</div>
            <div className="text-gray-300 text-m mb-2">Frontend Developer</div>
            <div className="flex mt-3 gap-8">
              <a href="https://www.instagram.com/janvi__yadav1205/">
                <img className="h-7" src="/logos/linkdin.png" alt="LinkedIn" />
              </a>
              <a href="https://www.linkedin.com/in/janvi1205/">
                <img className="h-7" src="/logos/insta.png" alt="Instagram" />
              </a>
              <a href="https://github.com/Janvi1205">
                <img className="h-7" src="/logos/github.png" alt="GitHub" />
              </a>
            </div>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="bg-gray-400 rounded-full w-40 h-40 mb-4">
              <img className="rounded-full" src="/images/ronak.jpg" alt="Ronak Jain" />
            </div>
            <div className="text-white text-2xl font-semibold">Ronak Jain</div>
            <div className="text-gray-300 text-m mb-2">API Integrator</div>
            <div className="flex mt-3 gap-8">
              <a href="https://www.instagram.com/ronak_._jain/">
                <img className="h-7" src="/logos/linkdin.png" alt="LinkedIn" />
              </a>
              <a href="https://www.linkedin.com/in/reachronakofficial756/">
                <img className="h-7" src="/logos/insta.png" alt="Instagram" />
              </a>
              <a href="https://github.com/reachronakofficial756">
                <img className="h-7" src="/logos/github.png" alt="GitHub" />
              </a>
            </div>
          </div>
          
          <div className="flex flex-col items-center">
            <div className="bg-gray-400 rounded-full w-40 h-40 mb-4">
              <img className="rounded-full" src="/images/sonal.png" alt="Sonal Sonal" />
            </div>
            <div className="text-white text-2xl font-semibold">Sonal Sonal</div>
            <div className="text-gray-300 text-m mb-2">Presenter</div>
            <div className="flex mt-3 gap-8">
              <a href="https://www.instagram.com/sonal__2810/">
                <img className="h-7" src="/logos/linkdin.png" alt="LinkedIn" />
              </a>
              <a href="https://www.linkedin.com/in/sonal-singh28/">
                <img className="h-7" src="/logos/insta.png" alt="Instagram" />
              </a>
              <img className="h-7" src="/logos/github.png" alt="GitHub" />
            </div>
          </div>
        </div>
      </section>
      
      <Connect />
      
      <footer className="w-full py-12 flex flex-col items-center bg-background">
        <div className="w-40 h-32 mb-6">
          <img src="/logos/workbeelogo.svg" alt="WorkBee Logo" />
        </div>
        <nav className="flex flex-wrap justify-center gap-8 mb-4">
          <a href="#" className="font-bold text-white">Home</a>
          <a href="#howitworks" className="font-bold text-white">How it works?</a>
          <a href="#ourteam" className="font-bold text-white">Our Team</a>
          <a href="#contact" className="font-bold text-white">Contact us</a>
        </nav>
        <div className="flex mt-3 gap-8">
          <img className="h-7" src="/logos/linkdin.png" alt="LinkedIn" />
          <img className="h-7" src="/logos/insta.png" alt="Instagram" />
          <img className="h-7" src="/logos/github.png" alt="GitHub" />
        </div>
        <form className="flex items-center mb-6 mt-5">
          <input
            type="email"
            placeholder="Enter your email"
            className="rounded-full px-6 py-2 bg-gray-300 text-black focus:outline-none"
          />
          <button
            type="submit"
            className="ml-2 px-6 py-2 rounded-full border-2 border-white text-white bg-black hover:bg-white hover:text-black transition"
          >
            Subscribe
          </button>
        </form>
        <div className="text-white flex items-center gap-2">
          <span className="text-xl">&copy;</span>
          <span>2025 WorkBee. All rights reserved.</span>
        </div>
      </footer>
    </>
  );
}


export { Connect };
