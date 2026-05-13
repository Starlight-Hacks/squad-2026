import { ArrowRight, CheckCircle2 } from "lucide-react";
import { Reveal } from "./Reveal";

export const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex flex-col justify-center items-center overflow-hidden px-6 pt-20 bg-[#020202]">
      {/*Animated Mesh Background */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        <div className="absolute top-[20%] left-[20%] w-[40vw] h-[40vw] bg-blue-900/30 rounded-full blur-[120px] mix-blend-screen animate-pulse" style={{ animationDuration: '6s' }}></div>
        <div className="absolute bottom-[10%] right-[10%] w-[30vw] h-[30vw] bg-indigo-900/20 rounded-full blur-[100px] mix-blend-screen animate-pulse" style={{ animationDuration: '8s', animationDelay: '1s' }}></div>
      </div>

      <div className="relative z-10 max-w-5xl mx-auto text-center w-full mt-12">
        <Reveal>
          <div className="inline-flex items-center space-x-2 border border-white/10 bg-white/5 backdrop-blur-sm rounded-full px-4 py-1.5 mb-8">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
            <span className="text-xs font-medium text-gray-300 tracking-wider uppercase">Built for Squad Hackathon</span>
          </div>
        </Reveal>

        <Reveal delay={150}>
          <h1 className="text-5xl md:text-7xl lg:text-[5.5rem] font-extrabold text-white tracking-tighter leading-[1.05] mb-6">
            The transaction layer for <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-300 to-blue-500 animate-gradient-x">
              Africa's informal economy.
            </span>
          </h1>
        </Reveal>

        <Reveal delay={300}>
          <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto font-medium leading-relaxed mb-10">
            WhatsApp-native payments capture the cashflow data that's invisible today; AI turns that data into credit, jobs, and a verified marketplace.
          </p>
        </Reveal>

        <Reveal delay={450}>
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <button className="w-full sm:w-auto group relative inline-flex items-center justify-center px-8 py-4 font-bold text-white transition-all duration-200 bg-blue-600 border border-transparent rounded-full hover:bg-blue-500 shadow-[0_0_30px_rgba(37,99,235,0.3)]">
              <span>View Macro Intelligence</span>
              <ArrowRight size={18} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-4 font-bold text-white transition-all duration-200 bg-transparent border border-white/20 rounded-full hover:bg-white/5">
              Read the Thesis
            </button>
          </div>
        </Reveal>
      </div>

      {/* Floating Mockup - WhatsApp Interface */}
      <Reveal delay={600} className="relative z-10 mt-16 w-full max-w-2xl mx-auto">
        <div className="bg-[#0A0A0A] border border-white/10 rounded-t-2xl p-6 shadow-2xl backdrop-blur-xl relative overflow-hidden h-48 border-b-0">
           <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-1/3 h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50"></div>
           
           <div className="space-y-4">
             {/* Fake Chat Bubbles */}
             <div className="flex justify-end">
               <div className="bg-[#005C4B] text-white text-sm py-2 px-4 rounded-2xl rounded-tr-sm max-w-[80%] shadow-md">
                 Abeg pay Segun 5k for the transport
               </div>
             </div>
             <div className="flex justify-start">
               <div className="bg-[#202C33] text-gray-200 text-sm py-2 px-4 rounded-2xl rounded-tl-sm max-w-[80%] shadow-md flex items-center border border-white/5">
                 <div className="w-4 h-4 rounded-full bg-blue-500/20 flex items-center justify-center mr-2">
                   <CheckCircle2 size={10} className="text-blue-400" />
                 </div>
                 Parsed Intent: Transfer ₦5,000 to 'Segun'. Processing via Squad...
               </div>
             </div>
           </div>
           
           <div className="absolute bottom-0 left-0 w-full h-24 bg-gradient-to-t from-[#0A0A0A] to-transparent"></div>
        </div>
      </Reveal>
    </section>
  );
};
