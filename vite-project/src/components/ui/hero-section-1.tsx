import React from 'react'
import { ArrowRight, ChevronRight, Menu, X } from 'lucide-react'
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
                                                        <ArrowRight className="m-auto size-3" />
                                                    </span>
                                                    <span className="flex size-6">
                                                        <ArrowRight className="m-auto size-3" />
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
                                    <div className="w-full h-full ml-190 -mt-140">
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
                <section className="bg-background pb-16 pt-16 md:pb-32">
                    <div className="group relative m-auto max-w-5xl px-6">
                        
                        <div className="mx-auto mt-12  w-full">
                            <div className="marquee-container mt-20 marquee-mask relative z-20 min-h-[124px]  border-muted/40 bg-muted/10 py-3">
                                <div className=" marquee">
                                    {customerLogos.concat(customerLogos).map((logo, index) => {
                                        // Map logo names to their SVG file names in public/logos
                                        const logoMap: Record<string, string> = {
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
                                        const logoMap: Record<string, string> = {
                                            
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
                                                    className="h-30 w-50"
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

const menuItems: Array<{ name: string; href: string }> = []

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
                                <Menu className="in-data-[state=active]:rotate-180 group-data-[state=active]:scale-0 group-data-[state=active]:opacity-0 m-auto size-6 duration-200" />
                                <X className="group-data-[state=active]:rotate-0 group-data-[state=active]:scale-100 group-data-[state=active]:opacity-100 absolute inset-0 m-auto size-6 -rotate-180 scale-0 opacity-0 duration-200" />
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
                                    <a href="#">
                                        <span>Dashboard</span>
                                    </a>
                                </Button>

                                <Button
                                    asChild
                                    size="sm"
                                    className={cn(isScrolled ? 'lg:inline-flex' : 'hidden')}>
                                    <a href="#">
                                        <span>Get Started</span>
                                    </a>
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </header>
    )
}

const Logo = ({ className }: { className?: string }) => {
    return (
        <svg
            viewBox="0 0 78 18"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={cn('h-5 w-auto', className)}>
            <path
                d="M3 0H5V18H3V0ZM13 0H15V18H13V0ZM18 3V5H0V3H18ZM0 15V13H18V15H0Z"
                fill="url(#logo-gradient)"
            />
            <path
                d="M27.06 7.054V12.239C27.06 12.5903 27.1393 12.8453 27.298 13.004C27.468 13.1513 27.7513 13.225 28.148 13.225H29.338V14.84H27.808C26.9353 14.84 26.2667 14.636 25.802 14.228C25.3373 13.82 25.105 13.157 25.105 12.239V7.054H24V5.473H25.105V3.144H27.06V5.473H29.338V7.054H27.06ZM30.4782 10.114C30.4782 9.17333 30.6709 8.34033 31.0562 7.615C31.4529 6.88967 31.9855 6.32867 32.6542 5.932C33.3342 5.524 34.0822 5.32 34.8982 5.32C35.6349 5.32 36.2752 5.46733 36.8192 5.762C37.3745 6.04533 37.8165 6.40233 38.1452 6.833V5.473H40.1002V14.84H38.1452V13.446C37.8165 13.888 37.3689 14.2563 36.8022 14.551C36.2355 14.8457 35.5895 14.993 34.8642 14.993C34.0595 14.993 33.3229 14.789 32.6542 14.381C31.9855 13.9617 31.4529 13.3837 31.0562 12.647C30.6709 11.899 30.4782 11.0547 30.4782 10.114ZM38.1452 10.148C38.1452 9.502 38.0092 8.941 37.7372 8.465C37.4765 7.989 37.1309 7.62633 36.7002 7.377C36.2695 7.12767 35.8049 7.003 35.3062 7.003C34.8075 7.003 34.3429 7.12767 33.9122 7.377C33.4815 7.615 33.1302 7.972 32.8582 8.448C32.5975 8.91267 32.4672 9.468 32.4672 10.114C32.4672 10.76 32.5975 11.3267 32.8582 11.814C33.1302 12.3013 33.4815 12.6753 33.9122 12.936C34.3542 13.1853 34.8189 13.31 35.3062 13.31C35.8049 13.31 36.2695 13.1853 36.7002 12.936C37.1309 12.6867 37.4765 12.324 37.7372 11.848C38.0092 11.3607 38.1452 10.794 38.1452 10.148ZM43.6317 4.232C43.2803 4.232 42.9857 4.113 42.7477 3.875C42.5097 3.637 42.3907 3.34233 42.3907 2.991C42.3907 2.63967 42.5097 2.345 42.7477 2.107C42.9857 1.869 43.2803 1.75 43.6317 1.75C43.9717 1.75 44.2607 1.869 44.4987 2.107C44.7367 2.345 44.8557 2.63967 44.8557 2.991C44.8557 3.34233 44.7367 3.637 44.4987 3.875C44.2607 4.113 43.9717 4.232 43.6317 4.232ZM44.5837 5.473V14.84H42.6457V5.473H44.5837ZM49.0661 2.26V14.84H47.1281V2.26H49.0661ZM50.9645 10.114C50.9645 9.17333 51.1572 8.34033 51.5425 7.615C51.9392 6.88967 52.4719 6.32867 53.1405 5.932C53.8205 5.524 54.5685 5.32 55.3845 5.32C56.1212 5.32 56.7615 5.46733 57.3055 5.762C57.8609 6.04533 58.3029 6.40233 58.6315 6.833V5.473H60.5865V14.84H58.6315V13.446C58.3029 13.888 57.8552 14.2563 57.2885 14.551C56.7219 14.8457 56.0759 14.993 55.3505 14.993C54.5459 14.993 53.8092 14.789 53.1405 14.381C52.4719 13.9617 51.9392 13.3837 51.5425 12.647C51.1572 11.899 50.9645 11.0547 50.9645 10.114ZM58.6315 10.148C58.6315 9.502 58.4955 8.941 58.2235 8.465C57.9629 7.989 57.6172 7.62633 57.1865 7.377C56.7559 7.12767 56.2912 7.003 55.7925 7.003C55.2939 7.003 54.8292 7.12767 54.3985 7.377C53.9679 7.615 53.6165 7.972 53.3445 8.448C53.0839 8.91267 52.9535 9.468 52.9535 10.114C52.9535 10.76 53.0839 11.3267 53.3445 11.814C53.6165 12.3013 53.9679 12.6753 54.3985 12.936C54.8405 13.1853 55.3052 13.31 55.7925 13.31C56.2912 13.31 56.7559 13.1853 57.1865 12.936C57.6172 12.6867 57.9629 12.324 58.2235 11.848C58.4955 11.3607 58.6315 10.794 58.6315 10.148ZM65.07 6.833C65.3533 6.357 65.7273 5.98867 66.192 5.728C66.668 5.456 67.229 5.32 67.875 5.32V7.326H67.382C66.6227 7.326 66.0447 7.51867 65.648 7.904C65.2627 8.28933 65.07 8.958 65.07 9.91V14.84H63.132V5.473H65.07V6.833ZM73.3624 10.165L77.6804 14.84H75.0624L71.5944 10.811V14.84H69.6564V2.26H71.5944V9.57L74.9944 5.473H77.6804L73.3624 10.165Z"
                fill="currentColor"
            />
            <defs>
                <linearGradient
                    id="logo-gradient"
                    x1="10"
                    y1="0"
                    x2="10"
                    y2="20"
                    gradientUnits="userSpaceOnUse">
                    <stop stopColor="#9B99FE" />
                    <stop
                        offset="1"
                        stopColor="#2BC8B7"
                    />
                </linearGradient>
            </defs>
        </svg>
    )
}