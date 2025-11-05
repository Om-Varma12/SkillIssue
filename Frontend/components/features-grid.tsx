import { Zap, Target, Brain, TrendingUp, Search, FileText } from "lucide-react"

export default function FeaturesGrid() {
  const features = [
    {
      icon: Zap,
      title: "Real-time Analysis",
      description: "Get instant results with our lightning-fast AI engine",
    },
    {
      icon: Target,
      title: "ATS Optimization",
      description: "Ensure your resume passes ATS systems with flying colors",
    },
    {
      icon: Brain,
      title: "Skill Gap Identification",
      description: "Identify missing skills and get improvement recommendations",
    },
    {
      icon: TrendingUp,
      title: "Experience Matching",
      description: "Detailed analysis of experience alignment with job requirements",
    },
    {
      icon: Search,
      title: "Keyword Extraction",
      description: "Advanced keyword analysis for better job matching",
    },
    {
      icon: FileText,
      title: "Detailed Reports",
      description: "Export comprehensive PDF reports for your records",
    },
  ]

  return (
    <section className="py-16 sm:py-24 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">Powerful Features</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Everything you need to make informed hiring decisions
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div
                key={index}
                className="group p-6 border border-border rounded-xl hover:border-primary hover:shadow-lg hover:shadow-primary/10 transition-all duration-300 hover:scale-105 animate-slide-up"
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors duration-300">
                  <Icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
