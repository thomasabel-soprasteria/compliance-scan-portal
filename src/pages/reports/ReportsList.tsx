
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { FileText, Download, ChevronRight, CheckCircle, AlertTriangle, Clock } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import AppHeader from "@/components/layout/AppHeader";
import PageContainer from "@/components/layout/PageContainer";

interface Report {
  id: number;
  file_name: string;
  company_name: string | null;
  fiscal_year: number | null;
  status: "pending" | "processing" | "completed" | "failed";
  upload_date: string;
  file_size: number;
}

const fetchReports = async (): Promise<Report[]> => {
  const response = await fetch("http://localhost:8000/api/v1/reports");
  if (!response.ok) {
    throw new Error("Failed to fetch reports");
  }
  return response.json();
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
};

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString() + " " + date.toLocaleTimeString();
};

const ReportsList = () => {
  const { data: reports = [], isLoading, error } = useQuery({
    queryKey: ["reports"],
    queryFn: fetchReports,
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge className="bg-green-500"><CheckCircle className="w-3 h-3 mr-1" /> Completed</Badge>;
      case "pending":
        return <Badge variant="outline"><Clock className="w-3 h-3 mr-1" /> Pending</Badge>;
      case "processing":
        return <Badge variant="secondary"><Clock className="w-3 h-3 mr-1" /> Processing</Badge>;
      case "failed":
        return <Badge variant="destructive"><AlertTriangle className="w-3 h-3 mr-1" /> Failed</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <AppHeader />
      <PageContainer 
        title="Reports" 
        description="View and manage uploaded compliance reports"
      >
        <div className="flex justify-between items-center mb-6">
          <div></div>
          <Button asChild>
            <Link to="/reports/upload">Upload New Report</Link>
          </Button>
        </div>

        {isLoading ? (
          <div className="text-center py-12">Loading reports...</div>
        ) : error ? (
          <div className="text-center py-12 text-red-500">
            Error loading reports. Please try again.
          </div>
        ) : reports.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <FileText className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium">No reports uploaded yet</h3>
              <p className="text-muted-foreground mb-4">Upload your first report to get started</p>
              <Button asChild>
                <Link to="/reports/upload">Upload Report</Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {reports.map((report) => (
              <Card key={report.id} className="overflow-hidden">
                <div className="flex items-center border-b p-4">
                  <div className="mr-4">
                    <div className="h-10 w-10 bg-primary/10 rounded-full flex items-center justify-center">
                      <FileText className="h-5 w-5 text-primary" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium">
                      {report.company_name || "Unnamed Company"} 
                      {report.fiscal_year ? ` (${report.fiscal_year})` : ""}
                    </h3>
                    <p className="text-sm text-muted-foreground">{report.file_name}</p>
                  </div>
                  <div className="hidden md:block">
                    {getStatusBadge(report.status)}
                  </div>
                  <div className="hidden md:block text-sm text-muted-foreground mx-4">
                    {formatDate(report.upload_date)}
                  </div>
                  <div className="hidden md:block text-sm text-muted-foreground mr-4">
                    {formatFileSize(report.file_size)}
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="icon" asChild>
                      <a href={`http://localhost:8000/api/v1/reports/${report.id}/download`} download>
                        <Download className="h-4 w-4" />
                      </a>
                    </Button>
                    <Button variant="ghost" size="icon" asChild>
                      <Link to={`/reports/${report.id}`}>
                        <ChevronRight className="h-4 w-4" />
                      </Link>
                    </Button>
                  </div>
                </div>
                <div className="md:hidden p-4 pt-0 flex justify-between text-sm">
                  <div>{getStatusBadge(report.status)}</div>
                  <div className="text-muted-foreground">{formatDate(report.upload_date)}</div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </PageContainer>
    </div>
  );
};

export default ReportsList;
