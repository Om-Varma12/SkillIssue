"use client"

import { useEffect, useState } from "react"

interface AnalysisResult {
  overall_match_percent: number
  skill_match_score_percent: number
  experience_match_score_percent: number
  keywords: {
    matched: string[]
    missing: string[]
  }
  experience: {
    required_years: number
    candidate_years: number
  }
  relevant_experience_highlights: string[]
  ats: {
    score_percent: number
    label: string
  }
  top_resume_keywords: string[]
  section_match_analysis: {
    education: string
    certifications: string
    skills: string
    experience: string
    soft_skills: string
  }
}

export default function MatchScoreCard({ analysisData }: { analysisData: AnalysisResult }) {
  const [displayScore, setDisplayScore] = useState(0)
  const score = Math.round(analysisData.overall_match_percent)

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

  // Calculate keyword match percentage
  const totalKeywords = analysisData.keywords.matched.length + analysisData.keywords.missing.length
  const keywordMatchPercent = totalKeywords > 0 
    ? Math.round((analysisData.keywords.matched.length / totalKeywords) * 100) 
    : 0

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
                <span className="text-sm font-semibold text-primary">
                  {Math.round(analysisData.skill_match_score_percent)}%
                </span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                  style={{ width: `${analysisData.skill_match_score_percent}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-foreground">Experience Match</span>
                <span className="text-sm font-semibold text-primary">
                  {Math.round(analysisData.experience_match_score_percent)}%
                </span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                  style={{ width: `${analysisData.experience_match_score_percent}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-foreground">Keywords Match</span>
                <span className="text-sm font-semibold text-primary">{keywordMatchPercent}%</span>
              </div>
              <div className="w-full bg-border rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full"
                  style={{ width: `${keywordMatchPercent}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}