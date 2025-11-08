"use client"

import Link from "next/link"

export default function HeroSection({ onGetStarted }: { onGetStarted: () => void }) {
  const scrollToMatch = () => {
    const element = document.getElementById("match")
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <section className="relative overflow-hidden bg-gradient-to-br from-primary via-secondary to-primary/80 py-20 sm:py-32">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center space-y-8 animate-fade-in">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20">
            <span className="w-2 h-2 bg-accent rounded-full"></span>
            <span className="text-sm text-white/90">Powered by Advanced NLP</span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white leading-tight">
            Match Candidates to Opportunities with <span className="text-accent">AI Precision</span>
          </h1>

          {/* Subheadline */}
          <p className="text-lg sm:text-xl text-white/80 max-w-2xl mx-auto leading-relaxed">
            Analyze resumes against job descriptions in seconds. Get detailed insights on skills match, experience
            alignment, and ATS optimization.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <button
              onClick={scrollToMatch}
              className="px-8 py-3 rounded-lg bg-white text-primary font-semibold hover:shadow-2xl hover:shadow-white/20 transition-all duration-300 hover:scale-105 cursor-pointer"
            >
              Start Matching
            </button>
            <Link
              href="/docs"
              className="px-8 py-3 rounded-lg border-2 border-white text-white font-semibold hover:bg-white/10 transition-all duration-300 inline-block text-center cursor-pointer"
            >
              View Demo
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}