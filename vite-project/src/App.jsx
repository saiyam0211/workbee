import React, { useEffect } from 'react';
import './App.css';

function App() {
    useEffect(() => {
        document.body.classList.add('dark');
    }, []);

    return (
        <div className="App">
            {/* Header */}
            <header className="header">
                <div className="header-container">
                    <div className="logo">WorkBee</div>
                    <div className="dashboard-button-container">
                        <div className="dashboard-button-bg">
                            <div className="dashboard-button-blur"></div>
                            <div className="dashboard-button-mask"></div>
                            <div className="dashboard-button-shape"></div>
                            <div className="dashboard-button-blur-inner"></div>
                            <div className="dashboard-button-fill"></div>
                            <div className="dashboard-button-glass"></div>
                        </div>
                        <div className="dashboard-button-text">Dashboard</div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="main-content">
                <div className="content-container">
        
                    <div className="text-content">
                        <div className="joble hover:bg-background dark:hover:border-t-border bg-muted group mx-auto flex w-fit items-center gap-4 rounded-full border p-1 pl-4 shadow-md shadow-black/5 transition-all duration-300 dark:border-t-white/5 dark:shadow-zinc-950 mb-8">
                            <span className="text-foreground text-sm">Introducing WorkBee</span>
                            <span className="dark:border-background block h-4 w-0.5 border-l bg-white dark:bg-zinc-700"></span>
                        </div>

                        <h1 className="main-heading">
                            DON'T LET YOUR DREAMS

                        </h1>
                        <h1 className="main-heading2"> FALL THROUGH THE HOURGLASS</h1>

                        <p className="supporting-text">
                            Just like sand through an hourglass, career opportunities slip away. Secure yours before time runs out
                            <span ><svg className="clock-icon"  width="30" height="30" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M17 31.1667C15.2291 31.1667 13.5705 30.8302 12.0239 30.1573C10.4774 29.4844 9.13157 28.5753 7.98643 27.4302C6.8413 26.2851 5.93227 24.9392 5.25935 23.3927C4.58643 21.8462 4.24998 20.1875 4.24998 18.4167C4.24998 16.6458 4.58643 14.9871 5.25935 13.4406C5.93227 11.8941 6.8413 10.5483 7.98643 9.40312C9.13157 8.25798 10.4774 7.34895 12.0239 6.67604C13.5705 6.00312 15.2291 5.66666 17 5.66666C18.7708 5.66666 20.4295 6.00312 21.976 6.67604C23.5225 7.34895 24.8684 8.25798 26.0135 9.40312C27.1587 10.5483 28.0677 11.8941 28.7406 13.4406C29.4135 14.9871 29.75 16.6458 29.75 18.4167C29.75 20.1875 29.4135 21.8462 28.7406 23.3927C28.0677 24.9392 27.1587 26.2851 26.0135 27.4302C24.8684 28.5753 23.5225 29.4844 21.976 30.1573C20.4295 30.8302 18.7708 31.1667 17 31.1667ZM20.9666 24.3667L22.95 22.3833L18.4166 17.85V11.3333H15.5833V18.9833L20.9666 24.3667ZM7.93331 3.32916L9.91664 5.3125L3.89581 11.3333L1.91248 9.35L7.93331 3.32916ZM26.0666 3.32916L32.0875 9.35L30.1041 11.3333L24.0833 5.3125L26.0666 3.32916Z" fill="#FEF7FF" />
                            </svg>
                            </span>
                        </p>
                    </div>

                    <div className="visual-content">
                        <div className="blank-space">
                            <div className="placeholder-text">
                                
                                <h3>3D Model Space</h3>
                                
                            </div>
                        </div>

                       
                    </div>
                </div>
            </main>

            <div className='hero2'>

                 <div className='blank_hero2'>
                    

                 </div>


            </div>
        </div>
    );
}

export default App;
