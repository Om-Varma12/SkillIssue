"use client"

import { useState } from "react"
import { Upload, FileText, Loader2 } from "lucide-react"

export default function InputInterface({ onAnalyze }: { onAnalyze: () => void }) {
  const [isLoading, setIsLoading] = useState(false)
  const [resumeFile, setResumeFile] = useState<string | null>(null)
  const [jobDescription, setJobDescription] = useState("")

  const handleAnalyze = () => {
    if (resumeFile && jobDescription) {
      setIsLoading(true)
      setTimeout(() => {
        setIsLoading(false)
        onAnalyze()
      }, 2000)
    }
  }

  return (
    <section className="py-16 sm:py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Resume Upload */}
          <div className="space-y-4 animate-slide-up">
            <h3 className="text-lg font-semibold text-foreground">Upload Resume</h3>
            <div
              className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-primary hover:bg-primary/5 transition-all duration-300 cursor-pointer"
              onDragOver={(e) => e.preventDefault()}
            >
              <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-sm font-medium text-foreground mb-1">Drag and drop your resume</p>
              <p className="text-xs text-muted-foreground mb-4">or click to browse</p>
              <p className="text-xs text-muted-foreground">PDF, DOC, DOCX (Max 5MB)</p>
              <input
                type="file"
                className="hidden"
                onChange={(e) => setResumeFile(e.target.files?.[0]?.name || null)}
              />
            </div>
            {resumeFile && (
              <div className="flex items-center gap-3 p-3 bg-accent/10 border border-accent/20 rounded-lg">
                <FileText className="w-5 h-5 text-accent" />
                <span className="text-sm text-foreground">{resumeFile}</span>
              </div>
            )}
          </div>

          {/* Job Description */}
          <div className="space-y-4 animate-slide-up" style={{ animationDelay: "0.1s" }}>
            <h3 className="text-lg font-semibold text-foreground">Job Description</h3>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              className="w-full h-48 p-4 border border-border rounded-xl bg-card text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
            />
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>Characters: {jobDescription.length}</span>
              <button className="text-primary hover:underline">Upload file</button>
            </div>
          </div>
        </div>

        {/* Analyze Button */}
        <div className="flex justify-center pt-4">
          <button
            onClick={handleAnalyze}
            disabled={!resumeFile || !jobDescription || isLoading}
            className="px-12 py-3 rounded-lg bg-gradient-to-r from-primary to-secondary text-primary-foreground font-semibold hover:shadow-lg hover:shadow-primary/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              "Analyze Match"
            )}
          </button>
        </div>
      </div>
    </section>
  )
}
