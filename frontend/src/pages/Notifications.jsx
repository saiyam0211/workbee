import React, { useEffect, useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import GlassFooter from '@/components/ui/GlassFooter'

export default function Notifications() {
    const [activeTab, setActiveTab] = useState('alerts')
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const pollRef = useRef(null)
    const navigate = useNavigate()

    useEffect(() => {
        document.body.classList.add('dark')
        return () => document.body.classList.remove('dark')
    }, [])

    // Helper to merge without duplicates by id
    const upsertMany = (list, incoming) => {
        const map = new Map(list.map((n) => [n.id, n]))
        for (const n of incoming) map.set(n.id, { ...map.get(n.id), ...n })
        // newest first
        return Array.from(map.values()).sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0))
    }

    const fetchOnce = async (signal) => {
        try {
            setError('')
            // Replace with your API endpoint
            const res = await fetch('/api/notifications', { signal })
            if (!res.ok) throw new Error('Failed to load notifications')
            const data = await res.json()
            setItems((prev) => upsertMany(prev, data))
        } catch (err) {
            if (err.name !== 'AbortError') {
                // Fallback demo content so the page is not empty during development
                const demo = new Array(6).fill(0).map((_, i) => ({
                    id: i + 1,
                    company: 'Company_Name',
                    logo: 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg',
                    title: 'has a Vacancy !!!',
                    subtitle: 'Job Title, Location,Experience',
                    createdAt: Date.now() - i * 1000,
                }))
                setItems((prev) => (prev.length ? prev : demo))
                setError('')
            }
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        const controller = new AbortController()
        fetchOnce(controller.signal)

        // Poll every 15s for new notifications
        pollRef.current = setInterval(() => fetchOnce(controller.signal), 15000)

        // Optional: live updates via SSE if your backend exposes it
        let es
        try {
            if ('EventSource' in window) {
                es = new EventSource('/api/notifications/stream')
                es.onmessage = (e) => {
                    try {
                        const payload = JSON.parse(e.data)
                        setItems((prev) => upsertMany(prev, Array.isArray(payload) ? payload : [payload]))
                    } catch { }
                }
            }
        } catch { }

        return () => {
            controller.abort()
            if (pollRef.current) clearInterval(pollRef.current)
            if (es) es.close()
        }
    }, [])

    return (
        <main className="min-h-dvh bg-background text-foreground">
            <section className="max-w-6xl mx-auto px-6 pt-8 pb-28">
                <div className="relative flex items-center justify-center mb-6">
                    <button
                        onClick={() => navigate('/dashboard')}
                        aria-label="Back to dashboard"
                        className="absolute left-0 w-17 h-17 rounded-full border border-white/10 bg-black/40 text-white flex items-center -ml-45 justify-center shadow-[0_8px_30px_rgba(0,0,0,.35)]"
                    >
                        <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M63.5413 50H36.458M36.458 50L46.8747 39.5833M36.458 50L46.8747 60.4167" stroke="#CDCDCD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M70.8333 18.8148C64.8746 14.8261 57.7089 12.5 50 12.5C29.2893 12.5 12.5 29.2893 12.5 50C12.5 70.7107 29.2893 87.5 50 87.5C70.7107 87.5 87.5 70.7107 87.5 50C87.5 43.1696 85.6739 36.7657 82.4832 31.25" stroke="#CDCDCD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                    </button>
                    <h1 className="text-center text-5xl md:text-6xl font-extrabold notification-text tracking-tight opacity-90">Notifications</h1>
                </div>

                {loading ? (
                    <div className="text-center opacity-70">Loading…</div>
                ) : items.length === 0 ? (
                    <div className="text-center opacity-70">No notifications yet</div>
                ) : (
                    <div className="divide-y divide-border rounded-[2rem] overflow-hidden bg-transparent">
                        {items.map((n) => (
                            <div key={n.id} className="flex items-center justify-between py-6">
                                <div className="flex items-center gap-4">
                                    <div className="w-14 h-14 notification-logo rounded-full  ring-1  flex items-center  justify-center">
                                        <img src={n.logo} alt="logo" className="w-8 h-8 object-contain" />
                                    </div>
                                    <div>
                                        <div className="text-lg font-semibold opacity-90">{n.company} <span className="font-normal">{n.title}</span></div>
                                        <div className="text-sm opacity-70">{n.subtitle}</div>
                                    </div>
                                </div>
                                <button className="px-6 py-2 h-12 view-job-btn rounded-3xl view-job text-white ">View Job</button>
                            </div>
                        ))}
                    </div>
                )}
            </section>
            <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
        </main>
    )
}


