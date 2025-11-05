"use client"

import { useState } from "react"
import { Badge } from "@/components/ui/badge"

export default function AnalysisTabs() {
  const [activeTab, setActiveTab] = useState("skills")

  const tabs = [
    { id: "skills", label: "Skills Match" },
    { id: "experience", label: "Experience" },
    { id: "keywords", label: "Keywords & ATS" },
    { id: "breakdown", label: "Detailed Breakdown" },
  ]

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
                {["React", "TypeScript", "Node.js", "Next.js", "Tailwind CSS", "REST APIs"].map((skill) => (
                  <Badge key={skill} className="bg-accent/20 text-accent border-accent/30 hover:bg-accent/30">
                    ✓ {skill}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Missing Skills</h3>
              <div className="flex flex-wrap gap-2">
                {["GraphQL", "Docker", "Kubernetes"].map((skill) => (
                  <Badge
                    key={skill}
                    className="bg-destructive/20 text-destructive border-destructive/30 hover:bg-destructive/30"
                  >
                    ✗ {skill}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Additional Skills</h3>
              <div className="flex flex-wrap gap-2">
                {["Python", "PostgreSQL", "AWS"].map((skill) => (
                  <Badge key={skill} className="bg-primary/20 text-primary border-primary/30 hover:bg-primary/30">
                    + {skill}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "experience" && (
          <div className="space-y-6">
            <div className="grid sm:grid-cols-2 gap-6">
              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground mb-1">Required Experience</p>
                <p className="text-2xl font-bold text-foreground">5+ years</p>
              </div>
              <div className="p-4 bg-accent/10 border border-accent/20 rounded-lg">
                <p className="text-sm text-muted-foreground mb-1">Candidate Experience</p>
                <p className="text-2xl font-bold text-accent">6 years</p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Relevant Experience Highlights</h3>
              <ul className="space-y-3">
                <li className="flex gap-3 p-3 bg-muted rounded-lg">
                  <span className="text-accent font-bold">✓</span>
                  <span className="text-foreground">Led development of 3 full-stack applications</span>
                </li>
                <li className="flex gap-3 p-3 bg-muted rounded-lg">
                  <span className="text-accent font-bold">✓</span>
                  <span className="text-foreground">Managed teams of 2-5 developers</span>
                </li>
                <li className="flex gap-3 p-3 bg-muted rounded-lg">
                  <span className="text-warning font-bold">~</span>
                  <span className="text-foreground">Limited DevOps experience</span>
                </li>
              </ul>
            </div>
          </div>
        )}

        {activeTab === "keywords" && (
          <div className="space-y-6">
            <div className="p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">ATS Compatibility Score</p>
              <p className="text-3xl font-bold text-foreground">92%</p>
              <p className="text-xs text-muted-foreground mt-2">Excellent - Resume is well-optimized for ATS systems</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">Top Matched Keywords</h3>
              <div className="space-y-2">
                {[
                  { keyword: "Full-stack development", count: 8 },
                  { keyword: "React", count: 6 },
                  { keyword: "API design", count: 5 },
                  { keyword: "Database optimization", count: 4 },
                ].map((item) => (
                  <div key={item.keyword} className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span className="text-foreground">{item.keyword}</span>
                    <span className="text-sm font-semibold text-primary">{item.count}x</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "breakdown" && (
          <div className="space-y-4">
            {[
              { section: "Education", match: "Matches", status: "accent" },
              { section: "Certifications", match: "Partial Match", status: "warning" },
              { section: "Soft Skills", match: "Matches", status: "accent" },
              { section: "Technical Skills", match: "Strong Match", status: "accent" },
            ].map((item) => (
              <div key={item.section} className="flex justify-between items-center p-4 bg-muted rounded-lg">
                <span className="font-medium text-foreground">{item.section}</span>
                <Badge
                  className={
                    item.status === "accent"
                      ? "bg-accent/20 text-accent border-accent/30"
                      : "bg-warning/20 text-warning border-warning/30"
                  }
                >
                  {item.match}
                </Badge>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
