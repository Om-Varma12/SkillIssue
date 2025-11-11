"use client"

import { useState } from "react"
import Navigation from "@/components/navigation"
import HeroSection from "@/components/hero-section"
import InputInterface from "@/components/input-interface"
import ResultsDashboard from "@/components/results-dashboard"
import FeaturesGrid from "@/components/features-grid"
import HowItWorks from "@/components/how-it-works"
import Footer from "@/components/footer"

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

function AboutSection() {
  return (
    <section id="about" className="py-20 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-foreground mb-4">About SkillIssue</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            We're revolutionizing the hiring process with AI-powered resume screening that saves time and finds the best
            candidates.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="p-6 bg-background rounded-lg border border-border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Our Mission</h3>
            <p className="text-muted-foreground">
              To empower recruiters and hiring managers with intelligent tools that streamline the candidate screening
              process.
            </p>
          </div>
          <div className="p-6 bg-background rounded-lg border border-border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Our Vision</h3>
            <p className="text-muted-foreground">
              A world where hiring is faster, fairer, and more efficient through the power of artificial intelligence.
            </p>
          </div>
          <div className="p-6 bg-background rounded-lg border border-border">
            <h3 className="text-xl font-semibold text-foreground mb-3">Our Values</h3>
            <p className="text-muted-foreground">
              We believe in transparency, innovation, and creating tools that make a real difference in people's
              careers.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

export default function Home() {
  const [showResults, setShowResults] = useState(false)
  const [analysisData, setAnalysisData] = useState<AnalysisResult | null>(null)

  const handleAnalyze = (data: AnalysisResult) => {
    setAnalysisData(data)
    setShowResults(true)
  }

  return (
    <main className="min-h-screen bg-background">
      <Navigation />

      {!showResults ? (
        <>
          <div id="hero">
            <HeroSection onGetStarted={() => window.scrollTo({ top: 800, behavior: "smooth" })} />
          </div>
          <AboutSection />
          <div id="how-it-works">
            <HowItWorks />
          </div>
          <div id="features">
            <FeaturesGrid />
          </div>
          <InputInterface onAnalyze={handleAnalyze} />
        </>
      ) : (
        <ResultsDashboard 
          analysisData={analysisData!} 
          onNewAnalysis={() => setShowResults(false)} 
        />
      )}

      <Footer />
    </main>
  )
}