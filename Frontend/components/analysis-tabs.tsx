"use client"

import { useState } from "react"
import { Badge } from "@/components/ui/badge"

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

export default function AnalysisTabs({ analysisData }: { analysisData: AnalysisResult }) {
  const [activeTab, setActiveTab] = useState("skills")

  const tabs = [
    { id: "skills", label: "Skills Match" },
    { id: "experience", label: "Experience" },
    { id: "keywords", label: "Keywords & ATS" },
    { id: "breakdown", label: "Detailed Breakdown" },
  ]

  const getMatchStatus = (status: string) => {
    const normalized = status.toLowerCase()
    if (normalized.includes("strong") || normalized === "matches") {
      return "accent"
    } else if (normalized.includes("partial")) {
      return "warning"
    }
    return "accent"
  }

  const getMatchLabel = (status: string) => {
    const normalized = status.toLowerCase()
    if (normalized.includes("strong")) return "Strong Match"
    if (normalized.includes("partial")) return "Partial Match"
    if (normalized === "matches") return "Matches"
    return status
  }

  return (
    <div className="bg-card border border-border rounded-2xl overflow-hidden">
      {/* Tab Navigation */}
      <div className="flex border-b border-border overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-6 py-4 font-medium text-sm whitespace-nowrap transition-all duration-300 ${
              activeTab === tab.id
                ? "text-primary border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="p-8">
        {activeTab === "skills" && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Matched Skills</h3>
              <div className="flex flex-wrap gap-2">
                {analysisData.keywords.matched.length > 0 ? (
                  analysisData.keywords.matched.map((skill) => (
                    <Badge key={skill} className="bg-accent/20 text-accent border-accent/30 hover:bg-accent/30">
                      ✓ {skill}
                    </Badge>
                  ))
                ) : (
                  <p className="text-muted-foreground text-sm">No matched skills found</p>
                )}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Missing Skills</h3>
              <div className="flex flex-wrap gap-2">
                {analysisData.keywords.missing.length > 0 ? (
                  analysisData.keywords.missing.map((skill) => (
                    <Badge
                      key={skill}
                      className="bg-destructive/20 text-destructive border-destructive/30 hover:bg-destructive/30"
                    >
                      ✗ {skill}
                    </Badge>
                  ))
                ) : (
                  <p className="text-muted-foreground text-sm">No missing skills</p>
                )}
              </div>
            </div>

            {analysisData.top_resume_keywords.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-foreground mb-4">Additional Skills from Resume</h3>
                <div className="flex flex-wrap gap-2">
                  {analysisData.top_resume_keywords
                    .filter(skill => !analysisData.keywords.matched.includes(skill.toLowerCase()))
                    .slice(0, 10)
                    .map((skill) => (
                      <Badge key={skill} className="bg-primary/20 text-primary border-primary/30 hover:bg-primary/30">
                        + {skill}
                      </Badge>
                    ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "experience" && (
          <div className="space-y-6">
            <div className="grid sm:grid-cols-2 gap-6">
              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground mb-1">Required Experience</p>
                <p className="text-2xl font-bold text-foreground">
                  {analysisData.experience.required_years}+ years
                </p>
              </div>
              <div className={`p-4 rounded-lg border ${
                analysisData.experience.candidate_years >= analysisData.experience.required_years
                  ? 'bg-accent/10 border-accent/20'
                  : 'bg-warning/10 border-warning/20'
              }`}>
                <p className="text-sm text-muted-foreground mb-1">Candidate Experience</p>
                <p className={`text-2xl font-bold ${
                  analysisData.experience.candidate_years >= analysisData.experience.required_years
                    ? 'text-accent'
                    : 'text-warning'
                }`}>
                  {analysisData.experience.candidate_years} years
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Relevant Experience Highlights</h3>
              <ul className="space-y-3">
                {analysisData.relevant_experience_highlights.map((highlight, index) => (
                  <li key={index} className="flex gap-3 p-3 bg-muted rounded-lg">
                    <span className="text-accent font-bold">✓</span>
                    <span className="text-foreground">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeTab === "keywords" && (
          <div className="space-y-6">
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">ATS Compatibility Score</p>
              <p className="text-3xl font-bold text-foreground">
                {Math.round(analysisData.ats.score_percent)}%
              </p>
              <p className="text-xs text-muted-foreground mt-2">
                {analysisData.ats.label} - Resume is {analysisData.ats.label.toLowerCase()} for ATS systems
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Top Resume Keywords</h3>
              <div className="space-y-2">
                {analysisData.top_resume_keywords.slice(0, 10).map((keyword, index) => (
                  <div key={keyword} className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span className="text-foreground capitalize">{keyword}</span>
                    <span className="text-sm font-semibold text-primary">
                      #{index + 1}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "breakdown" && (
          <div className="space-y-4">
            {Object.entries(analysisData.section_match_analysis).map(([section, match]) => (
              <div key={section} className="flex justify-between items-center p-4 bg-muted rounded-lg">
                <span className="font-medium text-foreground capitalize">
                  {section.replace('_', ' ')}
                </span>
                <Badge
                  className={
                    getMatchStatus(match) === "accent"
                      ? "bg-accent/20 text-accent border-accent/30"
                      : "bg-warning/20 text-warning border-warning/30"
                  }
                >
                  {getMatchLabel(match)}
                </Badge>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}