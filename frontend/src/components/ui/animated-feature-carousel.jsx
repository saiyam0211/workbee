"use client"

import {
  forwardRef,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react"
import {
  AnimatePresence,
  motion,
  useMotionTemplate,
  useMotionValue,
} from "framer-motion"

// --- Helper Functions and Fallbacks ---

// A simple utility for class names, similar to cn/clsx
const cn = (...classes) => {
  return classes.filter(Boolean).join(" ")
}

// Placeholder for image assets if they are not found.
const placeholderImage = (text = "Image") =>
  `https://placehold.co/600x400/1a1a1a/ffffff?text=${text}`

// --- Constants ---
const TOTAL_STEPS = 4

const steps = [
  {
    id: "1",
    name: "Step 1",
    title: "Get Started Instantly",
    description: "Sign up with your email or social accounts and unlock access to thousands of curated job opportunities. No lengthy forms, just quick access to your career path.",
  },
  {
    id: "2",
    name: "Step 2",
    title: "Personalize Your Experience",
    description: "Create a profile highlighting your skills, experience, and career goals. Our system uses this to tailor job recommendations just for you",
  },
  {
    id: "3",
    name: "Step 3",
    title: "Discover Curated Opportunities",
    description: "Navigate through a personalized job feed updated in real-time from company career pages. Use smart filters to zero in on roles that fit your aspirations.",
  },
  {
    id: "4",
    name: "Step 4",
    title: "Apply Directly & Securely",
    description:"When you find the right fit, apply directly through the company’s official job portal. Fast, secure, and trusted.",
  },
]

const ANIMATION_PRESETS = {
  fadeInScale: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.95 },
    transition: { type: "spring", stiffness: 300, damping: 25, mass: 0.5 },
  },
  slideInRight: {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -20 },
    transition: { type: "spring", stiffness: 300, damping: 25, mass: 0.5 },
  },
  slideInLeft: {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: 20 },
    transition: { type: "spring", stiffness: 300, damping: 25, mass: 0.5 },
  },
}

// --- Hooks ---
function useNumberCycler(totalSteps = TOTAL_STEPS, interval = 5000) {
  const [currentNumber, setCurrentNumber] = useState(0);

  // This effect handles the automatic cycling.
  // It depends on `currentNumber`, so every time the step changes,
  // it will clear the old timer and set a new one for the next step.
  useEffect(() => {
    const timerId = setTimeout(() => {
      setCurrentNumber((prev) => (prev + 1) % totalSteps);
    }, interval);

    // Cleanup function to clear the timer if the component unmounts
    // or if the dependencies of the effect change (e.g., user clicks a step).
    return () => clearTimeout(timerId);
  }, [currentNumber, totalSteps, interval]);

  // This function allows manual setting of the step.
  // When called, it updates `currentNumber`, which will trigger the useEffect
  // to reset the timer for the next cycle.
  const setStep = useCallback((stepIndex) => {
    setCurrentNumber(stepIndex % totalSteps);
  }, [totalSteps]);

  return { currentNumber, setStep };
}


function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false)
  useEffect(() => {
    const checkDevice = () => {
      setIsMobile(window.matchMedia("(max-width: 768px)").matches)
    }
    checkDevice()
    window.addEventListener("resize", checkDevice)
    return () => window.removeEventListener("resize", checkDevice)
  }, [])
  return isMobile
}

// --- Components ---
function IconCheck({ className, ...props }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor" className={cn("h-4 w-4", className)} {...props} >
      <path d="m229.66 77.66-128 128a8 8 0 0 1-11.32 0l-56-56a8 8 0 0 1 11.32-11.32L96 188.69 218.34 66.34a8 8 0 0 1 11.32 11.32Z" />
    </svg>
  )
}

const stepVariants = {
  inactive: { scale: 0.9, opacity: 0.7 },
  active: { scale: 1, opacity: 1 },
}

const StepImage = forwardRef(
  ({ src, alt, className, style, ...props }, ref) => {
    return (
      <img
        ref={ref}
        alt={alt}
        className={className}
        src={src}
        style={{ position: "absolute", userSelect: "none", maxWidth: "unset", ...style }}
        onError={(e) => (e.currentTarget.src = placeholderImage(alt))}
        {...props}
      />
    )
  }
)
StepImage.displayName = "StepImage"

const MotionStepImage = motion(StepImage)

const AnimatedStepImage = ({ preset = "fadeInScale", delay = 0, ...props }) => {
  const presetConfig = ANIMATION_PRESETS[preset]
  return <MotionStepImage {...props} {...presetConfig} transition={{ ...presetConfig.transition, delay }} />
}

function FeatureCard({ children, step }) {
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)
  const isMobile = useIsMobile()
  function handleMouseMove({ currentTarget, clientX, clientY }) {
    if (isMobile) return
    const { left, top } = currentTarget.getBoundingClientRect()
    mouseX.set(clientX - left)
    mouseY.set(clientY - top)
  }
  return (
    <motion.div id="howitworks"
      className="animated-cards group  w-[1100px] h-[600px] -ml-30 rounded-2xl"
      onMouseMove={handleMouseMove}
      style={{ "--x": useMotionTemplate`${mouseX}px`, "--y": useMotionTemplate`${mouseY}px` }}
    >
              <div  className="relative w-full overflow-hidden rounded-3xl border border-neutral-200 bg-[#000000] transition-colors duration-300 dark:border-neutral-800 dark:bg-[#000000]">
        <div className="m-10 min-h-[550px] w-full">
          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              className="flex w-full flex-col gap-4 md:w-3/5"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
            >
              <motion.div
                className="text-sm  font-semibold uppercase tracking-wider text-sky-600 dark:text-sky-500"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.05, duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              >
                {steps[step].name}
              </motion.div>
                             <motion.h2
                 className="text-2xl font-bold tracking-tight text-white md:text-3xl"
                 initial={{ opacity: 0, x: -20 }}
                 animate={{ opacity: 1, x: 0 }}
                 transition={{ delay: 0.1, duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
               >
                 {steps[step].title}
               </motion.h2>
               <motion.div
                 initial={{ opacity: 0, x: -20 }}
                 animate={{ opacity: 1, x: 0 }}
                 transition={{ delay: 0.15, duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
               >
                 <p className="text-base leading-relaxed text-gray-300">
                   {steps[step].description}
                 </p>
               </motion.div>
            </motion.div>
          </AnimatePresence>
          {children}
        </div>
      </div>
    </motion.div>
  )
}

function StepsNav({ steps: stepItems, current, onChange }) {
  return (
    <>
      <style jsx>{`
        .liquid-btn {
          /* Auto layout */
          display: flex;
          flex-direction: row;
          justify-content: center;
          align-items: center;
          padding: 6px 20px;
          gap: 4px;
          isolation: isolate;
          position: relative;
          width: 150px;
          height: 53px;
          border-radius: 1000px;
          border: none;
          cursor: pointer;
          transition: all 300ms ease;
          overflow: hidden;
        }

        /* Active state - Black button */
        .liquid-btn.active {
          background: rgba(0, 0, 0, 0.001);
        }

        .liquid-btn.active::before {
          content: "";
          position: absolute;
          left: 0px;
          right: 0px;
          top: 0px;
          bottom: 0px;
          background: linear-gradient(0deg, #000000, #000000), linear-gradient(0deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), #000000;
          background-blend-mode: plus-darker, normal, color-dodge;
          border-radius: 1000px;
          z-index: 0;
        }

        .liquid-btn.active::after {
          content: "";
          position: absolute;
          left: 0px;
          right: 0px;
          top: 0px;
          bottom: 0px;
          background: rgba(0, 0, 0, 0.001);
          border-radius: 1000px;
          backdrop-filter: blur(20px);
          z-index: 1;
        }

        /* Inactive state - Light gray button */
        .liquid-btn.inactive {
          background: rgba(0, 0, 0, 0.001);
        }

        .liquid-btn.inactive::before {
          content: "";
          position: absolute;
          left: 0px;
          right: 0px;
          top: 0px;
          bottom: 0px;
          background: linear-gradient(0deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), linear-gradient(0deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), rgba(247, 247, 247, 0.5);
          background-blend-mode: plus-darker, normal, color-dodge;
          border-radius: 1000px;
          z-index: 0;
        }

        .liquid-btn.inactive::after {
          content: "";
          position: absolute;
          left: 0px;
          right: 0px;
          top: 0px;
          bottom: 0px;
          background: rgba(0, 0, 0, 0.001);
          border-radius: 1000px;
          backdrop-filter: blur(20px);
          z-index: 1;
        }

        /* Text styling */
        .liquid-btn-text {
          position: relative;
          z-index: 2;
          font-family: 'SF Pro', -apple-system, BlinkMacSystemFont, sans-serif;
          font-style: normal;
          font-weight: 510;
          font-size: 24px;
          line-height: 29px;
          display: flex;
          align-items: center;
          text-align: center;
          font-feature-settings: 'ss16' on;
          transition: color 300ms ease;
        }

        .liquid-btn.active .liquid-btn-text {
          color: #D9D9D9;
        }

        .liquid-btn.inactive .liquid-btn-text {
          color: #000000;
        }

        /* Hover effects */
        .liquid-btn:hover {
          transform: scale(1.02);
        }

        .liquid-btn.active:hover::before {
          background: linear-gradient(0deg, #1a1a1a, #1a1a1a), linear-gradient(0deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), #1a1a1a;
          background-blend-mode: plus-darker, normal, color-dodge;
        }

        .liquid-btn.inactive:hover::before {
          background: linear-gradient(0deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), linear-gradient(0deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), rgba(240, 240, 240, 0.6);
          background-blend-mode: plus-darker, normal, color-dodge;
        }

        /* Responsive text size */
        @media (max-width: 640px) {
          .liquid-btn {
            width: 120px;
            height: 45px;
            padding: 4px 16px;
          }
          
          .liquid-btn-text {
            font-size: 18px;
            line-height: 22px;
          }
        }
      `}</style>
      <nav aria-label="Progress" className="flex justify-center px-4">
        <ol className="flex w-full mt-15 flex-wrap items-center justify-center gap-4" role="list">
          {stepItems.map((step, stepIdx) => {
            const isCurrent = current === stepIdx;
            return (
              <motion.li 
                key={step.name} 
                initial="inactive" 
                animate={isCurrent ? "active" : "inactive"} 
                variants={stepVariants} 
                transition={{ duration: 0.3 }} 
                className="relative"
              >
                <button
                  type="button"
                  className={`liquid-btn ${isCurrent ? 'active' : 'inactive'}`}
                  onClick={() => onChange(stepIdx)}
                >
                  <span className="liquid-btn-text">{step.name}</span>
                </button>
              </motion.li>
            );
          })}
        </ol>
      </nav>
    </>
  );
}

const defaultClasses = {
  img: "rounded-xl border border-neutral-200 dark:border-neutral-800 shadow-2xl shadow-black/10 dark:shadow-neutral-950/50",
  step1img1: "w-[50%] left-0 top-[15%]",
  step1img2: "w-[60%] left-[40%] top-[35%]",
  step2img1: "w-[50%] left-[5%] top-[20%]",
  step2img2: "w-[40%] left-[55%] top-[45%]",
  step3img: "w-[90%] left-[5%] top-[25%]",
  step4img: "w-[90%] left-[5%] top-[25%]",
}

export function FeatureCarousel({
  image,
  step1img1Class = defaultClasses.step1img1,
  step1img2Class = defaultClasses.step1img2,
  step2img1Class = defaultClasses.step2img1,
  step2img2Class = defaultClasses.step2img2,
  step3imgClass = defaultClasses.step3img,
  step4imgClass = defaultClasses.step4img,
  ...props
}) {
  const { currentNumber: step, setStep } = useNumberCycler()
  const renderStepContent = () => {
    switch (step) {
      case 0:
        return (
          <div className="relative w-full h-full">
            <AnimatedStepImage alt={image.alt} className={cn(defaultClasses.img, step1img1Class)} src={image.step1img1} preset="slideInLeft" />
            <AnimatedStepImage alt={image.alt} className={cn(defaultClasses.img, step1img2Class)} src={image.step1img2} preset="slideInRight" delay={0.1} />
          </div>
        )
      case 1:
        return (
          <div className="relative w-full h-full">
            <AnimatedStepImage alt={image.alt} className={cn(defaultClasses.img, step2img1Class)} src={image.step2img1} preset="fadeInScale" />
            <AnimatedStepImage alt={image.alt} className={cn(defaultClasses.img, step2img2Class)} src={image.step2img2} preset="fadeInScale" delay={0.1} />
          </div>
        )
      case 2:
        return <AnimatedStepImage alt={image.alt} className={cn(defaultClasses.img, step3imgClass)} src={image.step3img} preset="fadeInScale" />
      case 3:
        return <AnimatedStepImage alt={image.alt} className={cn(defaultClasses.img, step4imgClass)} src={image.step4img} preset="fadeInScale" />
      default: return null
    }
  }
  return (
    <div className="flex flex-col gap-12 w-full max-w-4xl mx-auto p-4">
      <FeatureCard {...props} step={step}>
        <AnimatePresence mode="wait">
          <motion.div key={step} {...ANIMATION_PRESETS.fadeInScale} className="w-full h-full absolute">
            {renderStepContent()}
          </motion.div>
        </AnimatePresence>
      </FeatureCard>
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <StepsNav current={step} onChange={setStep} steps={steps} />
      </motion.div>
    </div>
  )
}

// Demo usage
export default function App() {
  const demoImages = {
    step1img1: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop&crop=entropy&auto=format",
    step1img2: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop&crop=entropy&auto=format",
    step2img1: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop&crop=entropy&auto=format",
    step2img2: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=400&fit=crop&crop=entropy&auto=format",
    step3img: "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800&h=500&fit=crop&crop=entropy&auto=format",
    step4img: "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=800&h=500&fit=crop&crop=entropy&auto=format",
    alt: "Feature demonstration"
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-8">
      <FeatureCarousel image={demoImages} />
    </div>
  )
}
