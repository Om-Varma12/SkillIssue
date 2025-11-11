"use client"

import { useState, useRef } from "react"
import { Upload, FileText, Loader2, X } from "lucide-react"

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

export default function InputInterface({ onAnalyze }: { onAnalyze: (data: AnalysisResult) => void }) {
  const [isLoading, setIsLoading] = useState(false)
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [jobDescription, setJobDescription] = useState("")
  const [showPopup, setShowPopup] = useState(false)
  const [popupMessage, setPopupMessage] = useState("")
  const [popupType, setPopupType] = useState<"success" | "error">("success")
  const fileInputRef = useRef<HTMLInputElement>(null)

  const showNotification = (message: string, type: "success" | "error") => {
    setPopupMessage(message)
    setPopupType(type)
    setShowPopup(true)
    setTimeout(() => setShowPopup(false), 3000)
  }

  const handleFileSelect = (file: File | null) => {
    if (!file) return

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    const maxSize = 5 * 1024 * 1024 // 5MB

    if (!allowedTypes.includes(file.type)) {
      showNotification("Please upload a PDF, DOC, or DOCX file", "error")
      return
    }

    if (file.size > maxSize) {
      showNotification("File size must be less than 5MB", "error")
      return
    }

    setResumeFile(file)
    showNotification(`File "${file.name}" uploaded successfully!`, "success")
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    handleFileSelect(file)
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null
    handleFileSelect(file)
  }

  const handleAnalyze = async () => {
    if (!resumeFile || !jobDescription) {
      showNotification("Please upload a resume and add job description", "error")
      return
    }

    setIsLoading(true)

    try {
      // Create FormData to send file and job description
      const formData = new FormData()
      formData.append("resume", resumeFile)
      formData.append("jobDescription", jobDescription)

      // Send to backend API to save files
      const uploadResponse = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      if (!uploadResponse.ok) {
        throw new Error("Failed to upload files")
      }

      // Now call Flask backend for analysis
      const flaskResponse = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!flaskResponse.ok) {
        throw new Error("Failed to analyze resume")
      }

      const analysisData: AnalysisResult = await flaskResponse.json()
      
      showNotification("Analysis completed successfully!", "success")
      
      setTimeout(() => {
        setIsLoading(false)
        onAnalyze(analysisData)
      }, 500)
    } catch (error) {
      setIsLoading(false)
      showNotification("Error analyzing resume. Please try again.", "error")
      console.error("Analysis error:", error)
    }
  }

  return (
    <section id="match" className="py-16 sm:py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Popup Notification */}
        {showPopup && (
          <div
            className={`fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 animate-slide-up ${
              popupType === "success"
                ? "bg-accent text-accent-foreground"
                : "bg-destructive text-destructive-foreground"
            }`}
          >
            <span className="text-sm font-medium">{popupMessage}</span>
            <button onClick={() => setShowPopup(false)} className="hover:opacity-70 transition">
              <X size={18} />
            </button>
          </div>
        )}

        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">Start Your Analysis</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Upload your resume and job description to get instant AI-powered matching insights
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-8 items-start">
          {/* Resume Upload */}
          <div className="space-y-4 animate-slide-up">
            <h3 className="text-lg font-semibold text-foreground">Upload Resume</h3>
            <div
              className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-primary hover:bg-primary/5 transition-all duration-300 cursor-pointer flex flex-col items-center justify-center h-[264px]"
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-sm font-medium text-foreground mb-1">Drag and drop your resume</p>
              <p className="text-xs text-muted-foreground mb-4">or click to browse</p>
              <p className="text-xs text-muted-foreground">PDF, DOC, DOCX (Max 5MB)</p>
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept=".pdf,.doc,.docx"
                onChange={handleFileInputChange}
              />
            </div>
            {resumeFile && (
              <div className="flex items-center gap-3 p-3 bg-accent/10 border border-accent/20 rounded-lg">
                <FileText className="w-5 h-5 text-accent" />
                <span className="text-sm text-foreground">{resumeFile.name}</span>
                <button
                  onClick={() => setResumeFile(null)}
                  className="ml-auto text-destructive hover:text-destructive/80 transition"
                >
                  <X size={18} />
                </button>
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
              className="w-full h-[264px] p-4 border border-border rounded-xl bg-card text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
            />
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>Characters: {jobDescription.length}</span>
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