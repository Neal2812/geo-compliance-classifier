import { Header } from "./components/Header";
import { ComplianceForm } from "./components/ComplianceForm";
import { AgentStatusPanel } from "./components/AgentStatusPanel";
import { ResultsSection } from "./components/ResultsSection";

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Compliance Form */}
          <div className="lg:col-span-1">
            <ComplianceForm />
          </div>
          
          {/* Right Panel - Agent Status */}
          <div className="lg:col-span-2">
            <AgentStatusPanel />
          </div>
        </div>
        
        {/* Results Section */}
        <div className="mt-6">
          <ResultsSection />
        </div>
      </div>
    </div>
  );
}