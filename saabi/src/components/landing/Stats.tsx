import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { ScrollTrigger } from "gsap/ScrollTrigger";

// Register the plugin
gsap.registerPlugin(ScrollTrigger);

const stats = [
  { label: "Daily Transactions", value: 200, suffix: "+" },
  { label: "Registered Traders", value: 50, suffix: "" },
  { label: "Discovery Queries", value: 80, suffix: "+" },
  { label: "LGA Coverage", value: 5, suffix: "/20" },
];

export default function Stats() {
  const root = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    gsap.from(".stat-item", {
      scrollTrigger: {
        trigger: root.current,
        start: "top 80%",
      },
      y: 30,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
    });

    // Simple counter animation
    stats.forEach((_, i) => {
      const target = { val: 0 };
      gsap.to(target, {
        val: stats[i].value,
        duration: 2,
        scrollTrigger: {
          trigger: root.current,
          start: "top 90%",
        },
        onUpdate: () => {
          const el = document.getElementById(`stat-val-${i}`);
          if (el) el.innerText = Math.round(target.val).toString();
        }
      });
    });
  }, { scope: root });

  return (
    <section ref={root} className="px-6 py-32 bg-[#080808] border-y border-white/5">
      <div className="max-w-7xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-24">
        {stats.map((stat, i) => (
          <div key={i} className="stat-item">
            <div className="text-6xl md:text-8xl font-bold text-white mb-4 inline-flex items-baseline gap-1 tracking-tighter">
              <span id={`stat-val-${i}`}>0</span>
              <span className="text-3xl text-white/20">{stat.suffix}</span>
            </div>
            <p className="text-gt-orange text-xs font-black uppercase tracking-[0.3em]">{stat.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
