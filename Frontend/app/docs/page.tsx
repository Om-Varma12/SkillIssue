"use client"

import { ArrowLeft } from "lucide-react"
import Link from "next/link"

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-40 backdrop-blur-md bg-background/80 border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition"
          >
            <ArrowLeft size={16} />
            Back to Home
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Title */}
        <div className="mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-4">Documentation</h1>
          <p className="text-lg text-muted-foreground">
            Learn how to use ResumeMatch to analyze resumes and match candidates with job opportunities.
          </p>
        </div>

        {/* Theory Section */}
        <div className="space-y-12">
          {/* Getting Started */}
          <section className="space-y-4">
            <h2 className="text-3xl font-bold text-foreground">Getting Started</h2>
            <p className="text-muted-foreground leading-relaxed">
              ResumeMatch is an AI-powered resume screening tool that helps you quickly identify the best candidates for
              your job openings. Our advanced NLP algorithms analyze resumes against job descriptions to provide
              detailed insights on candidate fit.
            </p>
          </section>

          {/* How It Works */}
          <section className="space-y-4">
            <h2 className="text-3xl font-bold text-foreground">How It Works</h2>
            <div className="space-y-3 text-muted-foreground">
              <div>
                <h3 className="font-semibold text-foreground mb-2">1. Upload Resume</h3>
                <p>
                  Start by uploading a candidate's resume in PDF or text format. Our system will extract and analyze the
                  key information including skills, experience, education, and certifications.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">2. Enter Job Description</h3>
                <p>
                  Paste the job description for the position you're hiring for. This helps our AI understand the
                  specific requirements, skills, and experience level needed for the role.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">3. Get Analysis</h3>
                <p>
                  Our AI engine analyzes the resume against the job description and provides a comprehensive match score
                  along with detailed breakdowns of skills alignment, experience fit, and ATS compatibility.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">4. Review Insights</h3>
                <p>
                  Examine the detailed analysis including matched skills, missing skills, experience alignment, and
                  recommendations for improving the candidate's profile or job description.
                </p>
              </div>
            </div>
          </section>

          {/* Key Features */}
          <section className="space-y-4">
            <h2 className="text-3xl font-bold text-foreground">Key Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-lg bg-muted border border-border">
                <h3 className="font-semibold text-foreground mb-2">Skills Matching</h3>
                <p className="text-sm text-muted-foreground">
                  Automatically identifies and matches technical and soft skills from the resume with job requirements.
                </p>
              </div>
              <div className="p-4 rounded-lg bg-muted border border-border">
                <h3 className="font-semibold text-foreground mb-2">Experience Analysis</h3>
                <p className="text-sm text-muted-foreground">
                  Evaluates years of experience, relevant work history, and career progression against job expectations.
                </p>
              </div>
              <div className="p-4 rounded-lg bg-muted border border-border">
                <h3 className="font-semibold text-foreground mb-2">ATS Optimization</h3>
                <p className="text-sm text-muted-foreground">
                  Checks resume formatting and content for ATS (Applicant Tracking System) compatibility.
                </p>
              </div>
              <div className="p-4 rounded-lg bg-muted border border-border">
                <h3 className="font-semibold text-foreground mb-2">Detailed Insights</h3>
                <p className="text-sm text-muted-foreground">
                  Provides actionable recommendations and detailed breakdowns of candidate fit and alignment.
                </p>
              </div>
            </div>
          </section>

          {/* Video Tutorial */}
          <section className="space-y-4">
            <h2 className="text-3xl font-bold text-foreground">Video Tutorial</h2>
            <p className="text-muted-foreground mb-6">
              Watch this video to see ResumeMatch in action and learn how to get the most out of the platform.
            </p>
            <div className="relative w-full bg-muted rounded-lg overflow-hidden border border-border">
              <div className="aspect-video flex items-center justify-center bg-gradient-to-br from-primary/20 to-secondary/20">
                <video
                  width="100%"
                  height="100%"
                  controls
                  className="w-full h-full"
                  poster="/video-thumbnail.png"
                >
                  <source src="https://example.com/resumematch-tutorial.mp4" type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
            </div>
            <p className="text-sm text-muted-foreground mt-4">
              Note: Replace the video source URL with your actual tutorial video link.
            </p>
          </section>

          {/* Best Practices */}
          <section className="space-y-4">
            <h2 className="text-3xl font-bold text-foreground">Best Practices</h2>
            <ul className="space-y-2 text-muted-foreground">
              <li className="flex gap-3">
                <span className="text-accent font-bold">•</span>
                <span>Use clear, well-formatted job descriptions for better analysis accuracy</span>
              </li>
              <li className="flex gap-3">
                <span className="text-accent font-bold">•</span>
                <span>Ensure resumes are in standard formats (PDF or text) for optimal parsing</span>
              </li>
              <li className="flex gap-3">
                <span className="text-accent font-bold">•</span>
                <span>Review the detailed insights to understand candidate strengths and gaps</span>
              </li>
              <li className="flex gap-3">
                <span className="text-accent font-bold">•</span>
                <span>Use the match score as one factor among many in your hiring decision</span>
              </li>
              <li className="flex gap-3">
                <span className="text-accent font-bold">•</span>
                <span>Regularly update job descriptions to reflect current market requirements</span>
              </li>
            </ul>
          </section>

          {/* CTA */}
          <section className="mt-16 p-8 rounded-lg bg-gradient-to-r from-primary/10 to-secondary/10 border border-primary/20">
            <h2 className="text-2xl font-bold text-foreground mb-4">Ready to Get Started?</h2>
            <p className="text-muted-foreground mb-6">
              Start analyzing resumes and matching candidates with opportunities today.
            </p>
            <Link
              href="/"
              className="inline-block px-8 py-3 rounded-lg bg-primary text-primary-foreground font-semibold hover:shadow-lg hover:shadow-primary/20 transition-all duration-300"
            >
              Go to ResumeMatch
            </Link>
          </section>
        </div>
      </div>
    </div>
  )
}
