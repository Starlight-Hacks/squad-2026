import { ArchitectureSection } from "@/components/ArchitectureSection";
import { Footer } from "@/components/footer";
import { HeroSection } from "@/components/HeroSection";
import { Navbar } from "@/components/NavBar";
import { PillarsSection } from "@/components/PillarSection";
import { ProblemSection } from "@/components/ProblemSection";
import { PitchSection } from "@/components/PitchSection";


export default function App() {
  return (
    <div className="bg-[#020202] min-h-screen font-sans selection:bg-blue-500/30 selection:text-blue-200">
      <Navbar/>
      <main>
        <HeroSection />
        <ProblemSection />
        <ArchitectureSection />
        <PillarsSection />
        <PitchSection />
      </main>
      <Footer />
      
      {/* Global Styles for Animations */}
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes gradient-x {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        .animate-gradient-x {
          background-size: 200% 200%;
          animation: gradient-x 4s ease infinite;
        }
        body { scroll-behavior: smooth; }
      `}} />
    </div>
  );
}