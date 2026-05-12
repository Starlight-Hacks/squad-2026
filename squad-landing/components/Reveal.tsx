import { useEffect, useRef, useState } from "react";

const useScrollReveal = (options: IntersectionObserverInit = { threshold: 0.1, rootMargin: '0px' }) => {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const currentRef = ref.current;
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true);
        if (currentRef) observer.unobserve(currentRef); 
      }
    }, options);

    if (currentRef) observer.observe(currentRef); // TS now knows this is an Element, not 'null'
    return () => { if (currentRef) observer.unobserve(currentRef); };
  }, [options]);
  return [ref, isVisible] as const; 
};

interface RevealProps {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}

export const Reveal = ({ children, delay = 0, className = "" }: RevealProps) => {
  const [ref, isVisible] = useScrollReveal();
  
  return (
    <div 
      ref={ref}
      className={`transition-all duration-1000 ease-[cubic-bezier(0.16,1,0.3,1)] ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'
      } ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
};