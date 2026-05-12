import { ArrowRight } from "lucide-react";

export const Navbar = () => (
  <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 lg:px-12 backdrop-blur-xl bg-black/40 border-b border-white/5">
    <div className="flex items-center space-x-3">
      <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-[0_0_20px_rgba(37,99,235,0.4)]">
        <span className="text-white font-bold text-lg leading-none">S</span>
      </div>
      <span className="font-bold text-lg text-white tracking-tight">Identity<span className="text-blue-500">Layer</span></span>
    </div>
    <button className="group flex items-center space-x-2 bg-white text-black px-5 py-2.5 rounded-full font-semibold text-sm hover:bg-gray-200 transition-colors">
      <span>Launch Dashboard</span>
      <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
    </button>
  </nav>
);