import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { ArrowRight } from "lucide-react";
import SaabiGlobe from "./SaabiGlobe";

interface HeroProps {
  onExplore: (page: "dashboard" | "investment") => void;
}

export default function Hero({ onExplore }: HeroProps) {
  const root = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    gsap.from(".hero-title", {
      y: 60,
      opacity: 0,
      duration: 1.2,
      ease: "power4.out",
      stagger: 0.1
    });
    
    gsap.from(".hero-desc", {
      y: 40,
      opacity: 0,
      duration: 1,
      delay: 0.5,
      ease: "power3.out"
    });

    gsap.from(".hero-btns", {
      y: 30,
      opacity: 0,
      duration: 1,
      delay: 0.8,
      ease: "power3.out"
    });
  }, { scope: root });

  return (
    <section ref={root} className="relative min-h-screen pt-32 pb-20 px-6 flex flex-col items-center justify-center text-center overflow-hidden">
      <SaabiGlobe />
      
      <div className="relative z-10 w-full max-w-6xl">
        <div className="flex justify-center mb-8">
            <div className="px-4 py-1 rounded-lg border border-white/10 bg-white/5 text-[10px] tracking-[0.3em] font-black uppercase text-white/40">
                 FOR SAABI PEOPLE, BY SAABI PEOPLE
            </div>
        </div>
        
        <h1 className="hero-title text-4xl md:text-7xl font-bold leading-[0.95] mb-10 tracking-tighter mix-blend-difference uppercase">
          THE <span className="text-gt-orange text-glow brightness-125">REAL</span> ENGINE <br className="hidden md:block" /> OF COMMERCE
        </h1>
        
        <p className="hero-desc text-white/50 text-sm md:text-lg max-w-2xl mb-14 leading-relaxed font-light mx-auto">
          Scale your business with distributed WhatsApp payments and state-wide service discovery. Built for West Africa's economic powerhouse.
        </p>
        
        <div className="hero-btns flex flex-col sm:flex-row items-center justify-center gap-6">
          <button 
            onClick={() => onExplore("dashboard")}
            className="group relative bg-white text-black px-10 py-5 rounded-full font-bold text-base flex items-center gap-3 transition-all hover:scale-105 active:scale-95 shadow-2xl hover:bg-gt-orange hover:text-white"
          >
            JOIN TODAY
            <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
          </button>
          <button 
          onClick={() => onExplore("investment")}
          className="px-10 py-5 rounded-full border border-white/10 font-bold text-base text-white/70 hover:text-white hover:bg-white/5 transition-all">
            INVEST NOW
          </button>
        </div>
      </div>

      {/* Aesthetic strokes */}
      <div className="absolute inset-0 -z-10 pointer-events-none opacity-20">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1px] h-full bg-gradient-to-b from-white/20 via-transparent to-transparent" />
        <div className="absolute top-1/2 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>

      <div className="absolute inset-0 bg-gradient-to-t from-dark-bg via-transparent to-transparent -z-10" />
    </section>
  );
}
