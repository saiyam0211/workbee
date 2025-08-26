import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'

import { Button } from '@/components/ui/button'
import { AnimatedGroup } from '@/components/ui/animated-group'
import { cn } from '@/lib/utils'
import Spline from '@splinetool/react-spline'
"use client"

const transitionVariants = {
    item: {
        hidden: {
            opacity: 0,
            filter: 'blur(12px)',
            y: 12,
        },
        visible: {
            opacity: 1,
            filter: 'blur(0px)',
            y: 0,
            transition: {
                type: 'spring',
                bounce: 0.3,
                duration: 1.5,
            },
        },
    },
}

const customerLogos = [
    // "Google",
    // "Netflix",
    "Microsoft",
    "Spotify",
    "Slack",
    "Adobe",
    "Whatsapp",
    "Loom",
    "Atlassian",
    "Razorpay",
    // "Github",
    // "Nike",
    // "Openai",
]

export function HeroSection() {
    useEffect(() => {
        const intervalId = setInterval(() => {
            try { window.focus?.(); } catch {}
            const eventOptions = { key: 'e', code: 'KeyE', keyCode: 69, which: 69, bubbles: true };
            const keydown = new KeyboardEvent('keydown', eventOptions);
            const keyup = new KeyboardEvent('keyup', eventOptions);
            window.dispatchEvent(keydown);
            document.dispatchEvent(keydown);
            window.dispatchEvent(keyup);
            document.dispatchEvent(keyup);
        }, 6000);

        return () => clearInterval(intervalId);
    }, []);

    return (
        <>
            <HeroHeader />
            <main className="overflow-hidden">
                <div
                    aria-hidden
                    className="z-[2] absolute inset-0 pointer-events-none isolate opacity-50 contain-strict hidden lg:block">
                    <div className="w-[35rem] h-[80rem] -translate-y-[350px] absolute left-0 top-0 -rotate-45 rounded-full bg-[radial-gradient(68.54%_68.72%_at_55.02%_31.46%,hsla(0,0%,85%,.08)_0,hsla(0,0%,55%,.02)_50%,hsla(0,0%,45%,0)_80%)]" />
                    <div className="h-[80rem] absolute left-0 top-0 w-56 -rotate-45 rounded-full bg-[radial-gradient(50%_50%_at_50%_50%,hsla(0,0%,85%,.06)_0,hsla(0,0%,45%,.02)_80%,transparent_100%)] [translate:5%_-50%]" />
                    <div className="h-[80rem] -translate-y-[350px] absolute left-0 top-0 w-56 -rotate-45 bg-[radial-gradient(50%_50%_at_50%_50%,hsla(0,0%,85%,.04)_0,hsla(0,0%,45%,.02)_80%,transparent_100%)]" />
                </div>
                <section>
                    <div className="relative pt-24 md:pt-36">
                        <AnimatedGroup
                            variants={{
                                container: {
                                    visible: {
                                        transition: {
                                            delayChildren: 1,
                                        },
                                    },
                                },
                                item: {
                                    hidden: {
                                        opacity: 0,
                                        y: 20,
                                    },
                                    visible: {
                                        opacity: 1,
                                        y: 0,
                                        transition: {
                                            type: 'spring',
                                            bounce: 0.3,
                                            duration: 2,
                                        },
                                    },
                                },
                            }}
                            className="absolute inset-0 -z-20">
                            <img
                                src="https://images.unsplash.com/photo-1527443224154-c4f2dff7ec4e?q=80&w=3276&auto=format&fit=crop"
                                alt="background"
                                className="absolute inset-x-0 top-56 -z-20 hidden lg:top-32 dark:block"
                                width={3276}
                                height={4095}
                            />
                        </AnimatedGroup>
                        <div aria-hidden className="absolute inset-0 -z-10 size-full [background:radial-gradient(125%_125%_at_50%_100%,transparent_0%,var(--background)_75%)]" />
                        <div className="max-w-7xl px-6 relative">
                            <div className="">
                                {/* Left side - Text content */}
                                <div className="text-center lg:text-left sm:mx-auto lg:mr-auto lg:mt-0">
                                    <AnimatedGroup variants={transitionVariants}>
                                        <a
                                            href="#link"
                                            className="mt-20 ml-115 hover:border-t-border bg-white group  flex w-fit  gap-4 rounded-full border p-1 pl-4 shadow-md shadow-black/5 transition-all duration-300 dark:border-t-white/5 dark:shadow-zinc-950">
                                            <span className="text-black text-sm font-bold">Introducing WorkBee</span>
                                            <span className="dark:border-background block h-4 w-0.5 border-l bg-white dark:bg-zinc-700"></span>

                                            <div className="bg-background group-hover:bg-muted size-6 overflow-hidden rounded-full duration-500">
                                                <div className="flex w-12 -translate-x-1/2 duration-500 ease-in-out group-hover:translate-x-0">
                                                    <span className="flex size-6">
                                                        <span className="m-auto text-xs">→</span>
                                                    </span>
                                                    <span className="flex size-6">
                                                        <span className="m-auto text-xs">→</span>
                                                    </span>
                                                </div>
                                            </div>
                                        </a>

                                        <h1
                                            className="julius-sans-one-regular ml-60 mt-10 text-[3.65rem] leading-tight" 
                                            style={{letterSpacing: '-0.05em'}}>
                                            Don't Let Your Dreams
                                        </h1>
                                        <h1
                                            className="julius-sans-one-regular ml-38 text-[3.65rem] leading-tight" 
                                            style={{letterSpacing: '-0.05em'}}>
                                            Fall Through The Hourglass
                                        </h1>
                                        <p className=" mr-30 mt-8 text-xl relative text-center">
                                            Just like sand through an hourglass, career opportunities slip <br className=" hidden lg:block" /> 
                                            away. Secure yours before time runs out
                                            
                                            
                                        </p>
                                        <span className="inline-block  ml-185 -mt-7 absolute ">
                                                <svg width="30" height="30" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <path d="M17 31.1667C15.2291 31.1667 13.5705 30.8302 12.0239 30.1573C10.4774 29.4844 9.13157 28.5753 7.98643 27.4302C6.8413 26.2851 5.93227 24.9392 5.25935 23.3927C4.58643 21.8462 4.24998 20.1875 4.24998 18.4167C4.24998 16.6458 4.58643 14.9871 5.25935 13.4406C5.93227 11.8941 6.8413 10.5483 7.98643 9.40312C9.13157 8.25798 10.4774 7.34895 12.0239 6.67604C13.5705 6.00312 15.2291 5.66666 17 5.66666C18.7708 5.66666 20.4295 6.00312 21.976 6.67604C23.5225 7.34895 24.8684 8.25798 26.0135 9.40312C27.1587 10.5483 28.0677 11.8941 28.7406 13.4406C29.4135 14.9871 29.75 16.6458 29.75 18.4167C29.75 20.1875 29.4135 21.8462 28.7406 23.3927C28.0677 24.9392 27.1587 26.2851 26.0135 27.4302C24.8684 28.5753 23.5225 29.4844 21.976 30.1573C20.4295 30.8302 18.7708 31.1667 17 31.1667ZM20.9666 24.3667L22.95 22.3833L18.4166 17.85V11.3333H15.5833V18.9833L20.9666 24.3667ZM7.93331 3.32916L9.91664 5.3125L3.89581 11.3333L1.91248 9.35L7.93331 3.32916ZM26.0666 3.32916L32.0875 9.35L30.1041 11.3333L24.0833 5.3125L26.0666 3.32916Z" fill="#FEF7FF" />
                                                </svg>
                                            </span>
                                    </AnimatedGroup>
                                </div>

                                {/* Right side - Spline 3D Object */}
                                {/* <div className=" h-[600px]  flex ml-1   pointer-events-none select-none"> */}
                                    <div className="w-[800px] h-[800px] ml-215 -mt-150 scale-160">
                                        <Spline
                                            scene="https://prod.spline.design/t4rmChduw5J8uhUi/scene.splinecode"
                                            className="w-full h-full pointer-events-none select-none"
                                        />
                                    </div>
                                {/* </div> */}
                            </div>
                        </div>

                        <AnimatedGroup
                            variants={{
                                container: {
                                    visible: {
                                        transition: {
                                            staggerChildren: 0.05,
                                            delayChildren: 0.75,
                                        },
                                    },
                                },
                                ...transitionVariants,
                            }}>
                            <div className="relative -mr-56 mt-8 overflow-hidden px-2 sm:mr-0 sm:mt-12 md:mt-20">
                                <div
                                    aria-hidden
                                    className="bg-gradient-to-b to-background absolute inset-0 z-10 from-transparent from-35%"
                                />
                                <div className="mt-30 inset-shadow-2xs ring-background dark:inset-shadow-white/20 bg-background relative mx-auto max-w-6xl overflow-hidden rounded-2xl border p-4 shadow-lg shadow-zinc-950/15 ring-1">
                                    <img
                                        className="bg-background aspect-15/8 relative hidden rounded-2xl dark:block"
                                        src="https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=2700&auto=format&fit=crop"
                                        alt="app screen"
                                        width={2700}
                                        height={1440}
                                    />
                                    <img
                                        className="z-2 border-border/25 aspect-15/8 relative rounded-2xl border dark:hidden"
                                        src="https://images.unsplash.com/photo-1603575449299-bb76a9369110?q=80&w=2700&auto=format&fit=crop"
                                        alt="app screen"
                                        width={2700}
                                        height={1440}
                                    />
                                </div>
                            </div>
                        </AnimatedGroup>
                    </div>
                </section>
                <section  className="bg-background pb-16 pt-16 md:pb-32">
                    <div className="group relative m-auto max-w-5xl px-6">
                        
                        <div className="mx-auto mt-12  w-full">
                            <div className="marquee-container mt-20 marquee-mask relative z-20 min-h-[124px]  border-muted/40 bg-muted/10 py-3">
                                <div className=" marquee">
                                    {customerLogos.concat(customerLogos).map((logo, index) => {
                                        // Map logo names to their SVG file names in public/logos
                                        const logoMap = {
                                            'Whatsapp': '/logos/whatsapp.svg',
                                            'Spotify': '/logos/spotify.svg',
                                            'Loom': '/logos/lom.svg',
                                            'Microsoft': '/logos/microsoft.svg',
                                            'Atlassian': '/logos/atlassian.svg',
                                            'Slack': '/logos/slack.svg',
                                            'Razorpay': '/logos/razorpay.svg',
                                            'Adobe': '/logos/adobe.svg',
                                        };
                                        const src = logoMap[logo];
                                        return (
                                            <div key={`${logo}-${index}`} className="flex  px-10 py-2 opacity-80 transition-opacity hover:opacity-100">
                                                <img
                                                    src={src}
                                                    alt={`${logo} logo`}
                                                    className="h-50 w-50"
                                                />
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>

                            <div className="marquee-container marquee-mask -mt-17 relative z-20 min-h-[124px]  border-muted/40 bg-muted/10 py-3">
                                <div className=" marquee-reverse">
                                    {customerLogos.concat(customerLogos).map((logo, index) => {
                                        // Map logo names to their SVG file names in public/logos
                                        const logoMap = {
                                            
                                            'Spotify': '/logos/spotify.svg',
                                            'Loom': '/logos/lom.svg',
                                           'Microsoft': '/logos/microsoft.svg',
                                            'Slack': '/logos/slack.svg',
                                            'Razorpay': '/logos/razorpay.svg',
                                            'Adobe': '/logos/adobe.svg',
                                            'Whatsapp': '/logos/whatsapp.svg',
                                           'Atlassian': '/logos/atlassian.svg',
                                        };
                                        const src = logoMap[logo];
                                        return (
                                            <div key={`${logo}-${index}`} className="flex  px-10 py-2 opacity-80 transition-opacity hover:opacity-100">
                                                <img
                                                    src={src}
                                                    alt={`${logo} logo`}
                                                    className="h-50 w-50"
                                                />
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </>
    )
}

const menuItems = []

const HeroHeader = () => {
    const [menuState, setMenuState] = React.useState(false)
    const [isScrolled, setIsScrolled] = React.useState(false)

    React.useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50)
        }
        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [])
    return (
        <header>
            <nav
                data-state={menuState && 'active'}
                className="fixed z-20 w-full px-2 group">
                <div className={cn('mx-auto mt-2 max-w-6xl px-6 transition-all duration-300 lg:px-12', isScrolled && 'bg-background/50 max-w-4xl rounded-2xl border backdrop-blur-lg lg:px-5')}>
                    <div className="relative flex flex-wrap items-center justify-between gap-6 py-3 lg:gap-0 lg:py-4">
                        <div className="flex w-full justify-between lg:w-auto">
                            <a
                                href="/"
                                aria-label="home"
                                className="flex items-center space-x-2">
                                <Logo />
                            </a>

                            <button
                                onClick={() => setMenuState(!menuState)}
                                aria-label={menuState == true ? 'Close Menu' : 'Open Menu'}
                                className="relative z-20 -m-2.5 -mr-4 block cursor-pointer p-2.5 lg:hidden">
                                <span className="in-data-[state=active]:rotate-180 group-data-[state=active]:scale-0 group-data-[state=active]:opacity-0 m-auto size-6 duration-200">☰</span>
                                <span className="group-data-[state=active]:rotate-0 group-data-[state=active]:scale-100 group-data-[state=active]:opacity-100 absolute inset-0 m-auto size-6 -rotate-180 scale-0 opacity-0 duration-200">✕</span>
                            </button>
                        </div>

                        <div className="absolute inset-0 m-auto hidden size-fit lg:block">
                            <ul className="flex gap-8 text-sm">
                                {menuItems.map((item, index) => (
                                    <li key={index}>
                                        <a
                                            href={item.href}
                                            className="text-muted-foreground hover:text-accent-foreground block duration-150">
                                            <span>{item.name}</span>
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="bg-background group-data-[state=active]:block lg:group-data-[state=active]:flex mb-6 hidden w-full flex-wrap items-center justify-end space-y-8 rounded-3xl border p-6 shadow-2xl shadow-zinc-300/20 md:flex-nowrap lg:m-0 lg:flex lg:w-fit lg:gap-6 lg:space-y-0 lg:border-transparent lg:bg-transparent lg:p-0 lg:shadow-none dark:shadow-none dark:lg:bg-transparent">
                            <div className="lg:hidden">
                                <ul className="space-y-6 text-base">
                                    {menuItems.map((item, index) => (
                                        <li key={index}>
                                            <a
                                                href={item.href}
                                                className="text-muted-foreground hover:text-accent-foreground block duration-150">
                                                <span>{item.name}</span>
                                            </a>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div className="flex w-full flex-col space-y-3 sm:flex-row sm:gap-3 sm:space-y-0 md:w-fit">
                                <Button
                                    asChild
                                    variant="outline"
                                    size="sm"
                                    className={cn(isScrolled && 'lg:hidden')}>
                                    <Link to="/dashboard">
                                        <span>Dashboard</span>
                                    </Link>
                                </Button>

                                <Button
                                    asChild
                                    size="sm"
                                    className={cn(isScrolled ? 'lg:inline-flex' : 'hidden')}>
                                    <Link to="/dashboard">
                                        <span>Get Started</span>
                                    </Link>
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </header>
    )
}

const Logo = ({ className }) => {
    return (
    <>
        <span className='text-2xl font-bold'>WorkBee</span>
        </>
    )
}
