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
            <section className="max-w-6xl mx-auto px-4 sm:px-6 pt-6 sm:pt-8 pb-28">
                <div className="relative flex items-center justify-center mb-4 sm:mb-6">
                    <h1 className="text-center text-3xl sm:text-5xl md:text-6xl font-extrabold notification-text tracking-tight opacity-90">Notifications</h1>
                </div>

                {loading ? (
                    <div className="text-center opacity-70">Loading…</div>
                ) : items.length === 0 ? (
                    <div className="text-center opacity-70">No notifications yet</div>
                ) : (
                    <div className="divide-y divide-border rounded-2xl sm:rounded-[2rem] overflow-hidden bg-transparent">
                        {items.map((n) => (
                            <div key={n.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between py-4 sm:py-6 gap-4">
                                <div className="flex items-center gap-3 sm:gap-4">
                                    <div className="w-12 h-12 sm:w-14 sm:h-14 notification-logo rounded-full  ring-1  flex items-center  justify-center">
                                        <img src={n.logo} alt="logo" className="w-7 h-7 sm:w-8 sm:h-8 object-contain" />
                                    </div>
                                    <div>
                                        <div className="text-base sm:text-lg font-semibold opacity-90">{n.company} <span className="font-normal">{n.title}</span></div>
                                        <div className="text-xs sm:text-sm opacity-70">{n.subtitle}</div>
                                    </div>
                                </div>
                                <button className="w-full sm:w-auto px-5 sm:px-6 py-2 h-11 sm:h-12 view-job-btn rounded-2xl sm:rounded-3xl view-job text-white ">View Job</button>
                            </div>
                        ))}
                    </div>
                )}
            </section>
            <GlassFooter activeTab={activeTab} setActiveTab={setActiveTab} />
        </main>
    )
}


