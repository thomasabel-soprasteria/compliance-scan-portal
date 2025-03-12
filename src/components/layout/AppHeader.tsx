
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ClipboardList, FileText, Home, Settings } from "lucide-react";

const AppHeader = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-primary flex items-center gap-2">
          <ClipboardList className="h-6 w-6" />
          <span>Compliance Scan Portal</span>
        </Link>
        
        <nav className="hidden md:flex space-x-1">
          <Button variant="ghost" asChild>
            <Link to="/" className="flex items-center gap-2">
              <Home className="h-4 w-4" />
              <span>Home</span>
            </Link>
          </Button>
          <Button variant="ghost" asChild>
            <Link to="/reports" className="flex items-center gap-2">
              <FileText className="h-4 w-4" />
              <span>Reports</span>
            </Link>
          </Button>
          <Button variant="ghost" asChild>
            <Link to="/requirements" className="flex items-center gap-2">
              <ClipboardList className="h-4 w-4" />
              <span>Requirements</span>
            </Link>
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default AppHeader;
