import { Upload, Zap, BarChart3 } from "lucide-react"

export default function HowItWorks() {
  const steps = [
    {
      icon: Upload,
      title: "Upload Resume & Job Description",
      description: "Simply upload your resume and paste the job description to get started.",
    },
    {
      icon: Zap,
      title: "AI Analyzes with NLP",
      description: "Our advanced NLP engine analyzes skills, experience, and keywords in seconds.",
    },
    {
      icon: BarChart3,
      title: "Get Detailed Insights",
      description: "Receive comprehensive match analysis with actionable recommendations.",
    },
  ]

  return (
    <section className="py-16 sm:py-24 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">How It Works</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Three simple steps to match candidates with opportunities
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((step, index) => {
            const Icon = step.icon
            return (
              <div
                key={index}
                className="relative group animate-slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative p-8 border border-border rounded-2xl hover:border-primary transition-all duration-300">
                  <div className="w-14 h-14 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-3">{step.title}</h3>
                  <p className="text-muted-foreground">{step.description}</p>
                  {index < steps.length - 1 && (
                    <div className="hidden md:flex absolute -right-4 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-primary rounded-full items-center justify-center text-white font-bold text-center">
                      →
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
