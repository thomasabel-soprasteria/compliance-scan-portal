
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { FileUp, ClipboardList, CheckCircle } from "lucide-react";
import AppHeader from "@/components/layout/AppHeader";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <AppHeader />
      
      <main className="flex-1">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold mb-4">Compliance Scan Portal</h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Upload and analyze reports for regulatory compliance requirements
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <Card>
              <CardHeader className="space-y-1">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                  <FileUp className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Upload Reports</CardTitle>
                <CardDescription>
                  Upload annual reports to scan for compliance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button asChild className="w-full">
                  <Link to="/reports/upload">Upload New Report</Link>
                </Button>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="space-y-1">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                  <ClipboardList className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>View Requirements</CardTitle>
                <CardDescription>
                  Browse regulatory requirements
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button asChild className="w-full" variant="outline">
                  <Link to="/requirements">View Requirements</Link>
                </Button>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="space-y-1">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                  <CheckCircle className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Check Results</CardTitle>
                <CardDescription>
                  View compliance analysis results
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button asChild className="w-full" variant="outline">
                  <Link to="/reports">View Results</Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
