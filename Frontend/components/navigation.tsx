"use client"

import { useState } from "react"
import { Menu, X } from "lucide-react"
import Link from "next/link"

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
      setIsOpen(false)
    }
  }

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">SI</span>
            </div>
            <span className="font-bold text-lg text-foreground hidden sm:inline">SkillIssue</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-8">
            <button
              onClick={() => scrollToSection("hero")}
              className="text-sm text-muted-foreground hover:text-foreground transition cursor-pointer"
            >
              Home
            </button>
            <button
              onClick={() => scrollToSection("about")}
              className="text-sm text-muted-foreground hover:text-foreground transition cursor-pointer"
            >
              About
            </button>
            <button
              onClick={() => scrollToSection("how-it-works")}
              className="text-sm text-muted-foreground hover:text-foreground transition cursor-pointer"
            >
              How It Works
            </button>
            <button
              onClick={() => scrollToSection("features")}
              className="text-sm text-muted-foreground hover:text-foreground transition cursor-pointer"
            >
              Features
            </button>
            <Link href="/docs" className="text-sm text-muted-foreground hover:text-foreground transition cursor-pointer">
              Docs
            </Link>
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-4">
            <Link href="/docs">
              <button className="px-6 py-2 rounded-lg bg-primary text-primary-foreground font-medium hover:shadow-lg hover:shadow-primary/20 transition-all duration-300 cursor-pointer">
                Get Started
              </button>
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button onClick={() => setIsOpen(!isOpen)} className="md:hidden p-2 hover:bg-muted rounded-lg transition cursor-pointer">
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden pb-4 space-y-3 animate-slide-up">
            <button
              onClick={() => scrollToSection("hero")}
              className="block w-full text-left text-sm text-muted-foreground hover:text-foreground transition py-2 cursor-pointer"
            >
              Home
            </button>
            <button
              onClick={() => scrollToSection("about")}
              className="block w-full text-left text-sm text-muted-foreground hover:text-foreground transition py-2 cursor-pointer"
            >
              About
            </button>
            <button
              onClick={() => scrollToSection("how-it-works")}
              className="block w-full text-left text-sm text-muted-foreground hover:text-foreground transition py-2 cursor-pointer"
            >
              How It Works
            </button>
            <button
              onClick={() => scrollToSection("features")}
              className="block w-full text-left text-sm text-muted-foreground hover:text-foreground transition py-2 cursor-pointer"
            >
              Features
            </button>
            <Link
              href="/docs"
              className="block w-full text-left text-sm text-muted-foreground hover:text-foreground transition py-2 cursor-pointer"
            >
              Docs
            </Link>
            <Link href="/docs" className="block">
              <button className="w-full px-6 py-2 rounded-lg bg-primary text-primary-foreground font-medium hover:shadow-lg transition-all duration-300 cursor-pointer">
                Get Started
              </button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}