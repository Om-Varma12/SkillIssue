"use client"
import { ArrowLeft, Download, Share2, Save } from "lucide-react"
import MatchScoreCard from "./match-score-card"
import AnalysisTabs from "./analysis-tabs"

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

export default function ResultsDashboard({ analysisData, onNewAnalysis }: { 
  analysisData: AnalysisResult; 
  onNewAnalysis: () => void 
}) {
  return (
    <section className="py-16 sm:py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Button */}
        <button
          onClick={onNewAnalysis}
          className="flex items-center gap-2 text-primary hover:text-secondary transition mb-8"
        >
          <ArrowLeft size={20} />
          <span className="font-medium">New Analysis</span>
        </button>

        {/* Match Score Card */}
        <div className="mb-12 animate-slide-up">
          <MatchScoreCard analysisData={analysisData} />
        </div>

        {/* Analysis Tabs */}
        <div className="mb-12 animate-slide-up" style={{ animationDelay: "0.2s" }}>
          <AnalysisTabs analysisData={analysisData} />
        </div>

        {/* Action Cards */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 animate-slide-up" style={{ animationDelay: "0.3s" }}>
          <button className="p-4 border border-border rounded-lg hover:border-primary hover:bg-primary/5 transition-all duration-300 flex items-center gap-3 group">
            <Download className="w-5 h-5 text-primary group-hover:scale-110 transition" />
            <span className="font-medium text-foreground">Export Report</span>
          </button>
          <button className="p-4 border border-border rounded-lg hover:border-primary hover:bg-primary/5 transition-all duration-300 flex items-center gap-3 group">
            <Share2 className="w-5 h-5 text-primary group-hover:scale-110 transition" />
            <span className="font-medium text-foreground">Share Results</span>
          </button>
          <button className="p-4 border border-border rounded-lg hover:border-primary hover:bg-primary/5 transition-all duration-300 flex items-center gap-3 group">
            <Save className="w-5 h-5 text-primary group-hover:scale-110 transition" />
            <span className="font-medium text-foreground">Save Results</span>
          </button>
          <button className="p-4 border border-border rounded-lg hover:border-primary hover:bg-primary/5 transition-all duration-300 flex items-center gap-3 group">
            <span className="font-medium text-foreground">Compare Job</span>
          </button>
        </div>
      </div>
    </section>
  )
}