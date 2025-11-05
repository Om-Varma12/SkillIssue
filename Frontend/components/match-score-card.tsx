"use client"

import { useEffect, useState } from "react"

export default function MatchScoreCard({ score }: { score: number }) {
  const [displayScore, setDisplayScore] = useState(0)

  useEffect(() => {
    let current = 0
    const interval = setInterval(() => {
      current += Math.ceil(score / 30)
      if (current >= score) {
        setDisplayScore(score)
        clearInterval(interval)
      } else {
        setDisplayScore(current)
      }
    }, 30)
    return () => clearInterval(interval)
  }, [score])

  const getScoreColor = () => {
    if (score >= 80) return "from-accent to-accent/60"
    if (score >= 60) return "from-warning to-warning/60"
    return "from-destructive to-destructive/60"
  }

  const getScoreLabel = () => {
    if (score >= 80) return "Excellent Match"
    if (score >= 60) return "Good Match"
    return "Fair Match"
  }

  return (
    <div className="bg-card border border-border rounded-2xl p-8 sm:p-12">
      <div className="grid md:grid-cols-2 gap-8 items-center">
        {/* Circular Progress */}
        <div className="flex justify-center">
          <div className="relative w-48 h-48 sm:w-56 sm:h-56">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 200 200">
              {/* Background Circle */}
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="currentColor"
                strokeWidth="8"
                className="text-border"
              />
              {/* Progress Circle */}
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="url(#scoreGradient)"
                strokeWidth="8"
                strokeDasharray={`${(displayScore / 100) * 565.48} 565.48`}
                strokeLinecap="round"
                className="transition-all duration-500"
              />
              <defs>
                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="var(--color-primary)" />
                  <stop offset="100%" stopColor="var(--color-secondary)" />
                </linearGradient>
              </defs>
            </svg>
            {/* Center Text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-5xl sm:text-6xl font-bold text-foreground">{displayScore}%</span>
              <span className="text-sm text-muted-foreground mt-2">Match Score</span>
            </div>
          </div>
        </div>

        {/* Details */}
        <div className="space-y-6">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2">Overall Compatibility</h2>
            <p className="text-lg font-semibold text-primary">{getScoreLabel()}</p>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-foreground">Skills Match</span>
                <span className="text-sm font-semibold text-primary">85%</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                  style={{ width: "85%" }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-foreground">Experience Match</span>
                <span className="text-sm font-semibold text-primary">72%</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                  style={{ width: "72%" }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-foreground">Keywords Match</span>
                <span className="text-sm font-semibold text-primary">78%</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                  style={{ width: "78%" }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
