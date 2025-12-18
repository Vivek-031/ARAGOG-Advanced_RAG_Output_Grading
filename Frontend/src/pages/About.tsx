import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { 
  Activity, 
  MessageSquare, 
  Upload, 
  History, 
  Settings, 
  Zap, 
  Shield, 
  Brain, 
  Heart,
  Sparkles,
  TrendingUp,
  Users,
  FileText,
  BarChart3,
  Database,
  ArrowRight,
  CheckCircle2,
  Phone,
  Mail,
  MapPin,
  Award,
  Target,
  Workflow
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TypewriterText from "@/components/TypewriterText";
import "../customStyles.css";

const About = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const dashboardCards = [
    {
      icon: MessageSquare,
      title: "Start New Chat",
      description: "Ask medical questions and get AI-powered answers instantly",
      color: "from-shade-3 to-shade-5",
      action: "/main",
    },
    {
      icon: Upload,
      title: "Upload Document",
      description: "Upload medical reports and documents for analysis",
      color: "from-shade-2 to-shade-4",
      action: "/main",
    },
    {
      icon: History,
      title: "View History",
      description: "Access your past conversations and medical queries",
      color: "from-shade-4 to-shade-3",
      action: "/main",
    },
    {
      icon: Settings,
      title: "Settings",
      description: "Customize your experience and manage preferences",
      color: "from-shade-3 to-shade-2",
      action: "/main",
    },
  ];

  const statsCards = [
    {
      icon: Users,
      title: "Active Users",
      value: "12,458",
      change: "+12.5%",
      iconBg: "bg-primary"
    },
    {
      icon: FileText,
      title: "Documents Analyzed",
      value: "48,692",
      change: "+18.2%",
      iconBg: "bg-success"
    },
    {
      icon: BarChart3,
      title: "Accuracy Rate",
      value: "98.5%",
      change: "+2.1%",
      iconBg: "bg-shade-4"
    },
    {
      icon: TrendingUp,
      title: "Success Rate",
      value: "96.8%",
      change: "+5.3%",
      iconBg: "bg-warning"
    }
  ];

  const features = [
    {
      icon: Shield,
      title: "AI-Powered Grading",
      description: "Advanced transformers evaluate RAG outputs for trustworthiness and accuracy",
      gradient: "from-shade-3 to-shade-5",
    },
    {
      icon: Activity,
      title: "Knowledge + Reasoning",
      description: "Combines retrieval accuracy with interpretive reasoning for clarity",
      gradient: "from-shade-2 to-shade-4",
    },
    {
      icon: Sparkles,
      title: "Trust & Transparency",
      description: "Ethical AI that prioritizes human safety and explainable decisions",
      gradient: "from-shade-4 to-shade-3",
    },
  ];

  const services = [
    {
      icon: Brain,
      title: "AI Medical Analysis",
      description: "Advanced AI algorithms analyze medical data with 98% accuracy, providing reliable insights for healthcare professionals.",
      features: ["Deep Learning Models", "Real-time Processing", "Multi-format Support"]
    },
    {
      icon: Shield,
      title: "Secure & Compliant",
      description: "HIPAA-compliant infrastructure ensuring your medical data is protected with enterprise-grade security.",
      features: ["End-to-end Encryption", "HIPAA Compliance", "Regular Audits"]
    },
    {
      icon: Workflow,
      title: "Smart Workflow",
      description: "Streamline your medical documentation workflow with intelligent automation and seamless integrations.",
      features: ["Automated Reports", "API Integration", "Custom Workflows"]
    }
  ];

  const faqs = [
    {
      question: "How accurate is the AI medical analysis?",
      answer: "Our AI models achieve 98.5% accuracy rate, validated against peer-reviewed medical literature and continuously improved through machine learning."
    },
    {
      question: "Is my medical data secure?",
      answer: "Yes, we use enterprise-grade encryption and are fully HIPAA compliant. Your data is never shared with third parties."
    },
    {
      question: "Can I integrate MediRAG with my existing systems?",
      answer: "Absolutely! We provide REST APIs and SDKs for seamless integration with EHR systems and custom applications."
    },
    {
      question: "What types of medical documents can I analyze?",
      answer: "MediRAG supports PDFs, images, text files, DICOM files, and most common medical document formats."
    }
  ];

  return (
    <div className="min-h-screen relative overflow-hidden">
      <Navbar />
      
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-96 h-96 bg-shade-3/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.15, 0.3, 0.15],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-[500px] h-[500px] bg-shade-2/15 rounded-full blur-3xl"
          animate={{
            scale: [1.3, 1, 1.3],
            opacity: [0.15, 0.3, 0.15],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute top-1/2 left-1/2 w-[600px] h-[600px] bg-shade-4/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2"
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      </div>

      {/* Hero Section */}
      <div className="relative z-10 pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <motion.div 
              className="flex justify-center mb-8"
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, type: "spring", bounce: 0.4 }}
            >
              <div className="relative">
                <motion.div
                  className="absolute inset-0 bg-gradient-to-br from-shade-3 to-shade-5 rounded-3xl blur-2xl opacity-30"
                  animate={{
                    scale: [1, 1.15, 1],
                    opacity: [0.3, 0.5, 0.3],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                />
                <div className="relative w-24 h-24 bg-primary rounded-2xl flex items-center justify-center shadow-lg">
                  <Sparkles className="w-12 h-12 text-white" />
                </div>
              </div>
            </motion.div>
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 text-foreground"
            >
              <TypewriterText 
                text="AI-Powered Medical Insights" 
                speed={80}
                showCursor={true}
              />
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed"
            >
              AI-powered medical query platform with reliable, structured answers.
              <br />
              Advanced RAG Output Grading for trusted medical insights.
            </motion.p>
          </motion.div>

          {/* Stats Cards */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16"
          >
            {statsCards.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.5 + index * 0.1 }}
                  whileHover={{ 
                    y: -8,
                    transition: { duration: 0.2 }
                  }}
                  className="group"
                >
                  <div className="relative bg-card rounded-xl shadow-sm hover:shadow-lg transition-all duration-200 p-6 border border-border">
                    <div className="flex items-start justify-between mb-4">
                      <div className={`p-3 rounded-lg ${stat.iconBg}`}>
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {stat.change}
                      </Badge>
                    </div>
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">{stat.title}</p>
                      <h3 className="text-3xl font-bold text-foreground">{stat.value}</h3>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>

          {/* Dashboard Cards Grid */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20"
          >
            {dashboardCards.map((card, index) => {
              const Icon = card.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.5 + index * 0.1 }}
                  whileHover={{ 
                    y: -12, 
                    transition: { duration: 0.3, type: "spring", stiffness: 300 } 
                  }}
                  onClick={() => navigate(card.action)}
                  className="group cursor-pointer"
                >
                  <div className="relative h-full">
                    <div className="absolute inset-0 bg-gradient-to-br from-shade-3/15 to-shade-2/15 rounded-3xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                    <div className="relative bg-card/80 backdrop-blur-md rounded-2xl shadow-lg hover:shadow-xl transition-all duration-500 p-8 h-full border border-border">
                      <div className="w-20 h-20 mb-6 mx-auto rounded-2xl bg-primary flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
                        <Icon className="w-8 h-8 text-white" />
                      </div>
                      <h3 className="text-lg font-bold text-foreground mb-3 group-hover:text-primary transition-colors">
                        {card.title}
                      </h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {card.description}
                      </p>
                      <motion.div
                        className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                        initial={{ x: -10 }}
                        whileHover={{ x: 0 }}
                      >
                        <ArrowRight className="w-5 h-5 text-primary" />
                      </motion.div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </motion.div>

          {/* Features Section */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.9 }}
            className="mb-20"
          >
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1, duration: 0.6 }}
              className="text-4xl md:text-5xl font-bold text-center mb-16 text-foreground"
            >
              Why Choose MediRAG?
            </motion.h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {features.map((feature, index) => {
                const Icon = feature.icon;
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 1.1 + index * 0.15 }}
                    whileHover={{ 
                      scale: 1.05,
                      y: -8,
                      transition: { duration: 0.3 }
                    }}
                    className="relative group"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-shade-3/10 to-shade-2/10 rounded-3xl blur-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                    <div className="relative bg-card/80 backdrop-blur-md rounded-2xl shadow-lg hover:shadow-xl transition-all duration-500 p-10 border border-border">
                      <motion.div 
                        className={`w-16 h-16 bg-gradient-to-br ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 shadow-lg`}
                        whileHover={{ 
                          rotate: [0, -10, 10, -10, 0],
                          scale: 1.1
                        }}
                        transition={{ duration: 0.5 }}
                      >
                        <Icon className="w-8 h-8 text-white" />
                      </motion.div>
                      <h3 className="text-2xl font-bold text-foreground mb-4 group-hover:text-primary transition-colors">
                        {feature.title}
                      </h3>
                      <p className="text-muted-foreground leading-relaxed text-base">
                        {feature.description}
                      </p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>

          {/* CTA Section */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.5 }}
            className="text-center"
          >
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              {/* Sign Up Button */}
              <motion.button
                onClick={() => navigate("/signup")}
                className="button-submit inline-flex items-center gap-3 text-lg px-10 py-5 shadow-lg hover:shadow-xl"
                whileHover={{ 
                  scale: 1.05
                }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2, ease: "easeInOut" }}
              >
                Sign Up <ArrowRight className="w-5 h-5" />
              </motion.button>

              {/* Login Button */}
              <motion.button
                onClick={() => navigate("/login")}
                className="button-white inline-flex items-center gap-3 text-lg px-10 py-5"
                whileHover={{ 
                  scale: 1.05
                }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2, ease: "easeInOut" }}
              >
                Login
              </motion.button>
            </div>
            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.7, duration: 0.5 }}
              className="text-sm text-muted-foreground mt-6"
            >
              Join thousands of healthcare professionals using MediRAG
            </motion.p>
          </motion.div>
        </div>
      </div>

      {/* Services Section */}
      <section id="services" className="relative z-10 py-16 px-4 sm:px-6 lg:px-8 bg-shade-1/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">Our Services</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Comprehensive AI-powered solutions for modern healthcare
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {services.map((service, index) => {
              const Icon = service.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.15 }}
                  viewport={{ once: true }}
                  whileHover={{ y: -8, transition: { duration: 0.2 } }}
                  className="group"
                >
                  <div className="relative bg-card rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 p-8 border border-border h-full">
                    <div className="w-16 h-16 bg-primary rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-foreground mb-4">{service.title}</h3>
                    <p className="text-muted-foreground leading-relaxed mb-6">{service.description}</p>
                    <ul className="space-y-2">
                      {service.features.map((feature, idx) => (
                        <li key={idx} className="flex items-center gap-2 text-sm text-muted-foreground">
                          <CheckCircle2 className="w-4 h-4 text-primary flex-shrink-0" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="relative z-10 py-16 px-4 sm:px-6 lg:px-8 bg-shade-1/30">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">Frequently Asked Questions</h2>
            <p className="text-xl text-muted-foreground">
              Everything you need to know about MediRAG
            </p>
          </motion.div>

          <div className="space-y-6">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-card rounded-xl shadow-sm hover:shadow-md transition-all duration-200 p-6 border border-border"
              >
                <h3 className="text-lg font-semibold text-foreground mb-3">{faq.question}</h3>
                <p className="text-muted-foreground leading-relaxed">{faq.answer}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="relative z-10 py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-4">Get In Touch</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Have questions? We'd love to hear from you
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { icon: Phone, title: "Phone", content: "+1 (555) 123-4567", link: "tel:+15551234567" },
              { icon: Mail, title: "Email", content: "support@medirag.ai", link: "mailto:support@medirag.ai" },
              { icon: MapPin, title: "Address", content: "123 Medical Plaza, San Francisco, CA 94102", link: "#" }
            ].map((contact, index) => {
              const Icon = contact.icon;
              return (
                <motion.a
                  key={index}
                  href={contact.link}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.15 }}
                  viewport={{ once: true }}
                  whileHover={{ y: -8, transition: { duration: 0.2 } }}
                  className="group block"
                >
                  <div className="relative bg-card rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 p-8 border border-border text-center">
                    <div className="w-16 h-16 bg-primary rounded-xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-foreground mb-2">{contact.title}</h3>
                    <p className="text-muted-foreground">{contact.content}</p>
                  </div>
                </motion.a>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default About;
