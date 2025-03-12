
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, Calendar, Building, Download, AlertTriangle, CheckCircle, Clock, ArrowLeft } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import AppHeader from "@/components/layout/AppHeader";
import PageContainer from "@/components/layout/PageContainer";

interface ReportDetail {
  id: number;
  file_name: string;
  file_size: number;
  upload_date: string;
  status: "pending" | "processing" | "completed" | "failed";
  company_name: string | null;
  fiscal_year: number | null;
  processed_text: string | null;
  created_at: string;
  updated_at: string;
}

interface RequirementResult {
  id: number;
  name: string;
  description: string;
  category: string | null;
  is_compliant: boolean | null;
  confidence_score: number | null;
  extracted_evidence: string | null;
}

interface ComplianceSummary {
  report_id: number;
  total_requirements: number;
  compliant_count: number;
  non_compliant_count: number;
  pending_count: number;
  overall_compliance_percentage: number;
  results: RequirementResult[];
}

const fetchReport = async (id: string): Promise<ReportDetail> => {
  const response = await fetch(`http://localhost:8000/api/v1/reports/${id}`);
  if (!response.ok) {
    throw new Error("Failed to fetch report");
  }
  return response.json();
};

const fetchComplianceSummary = async (id: string): Promise<ComplianceSummary> => {
  const response = await fetch(`http://localhost:8000/api/v1/compliance/reports/${id}/summary`);
  if (!response.ok) {
    throw new Error("Failed to fetch compliance summary");
  }
  return response.json();
};

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString();
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
};

const ReportDetail = () => {
  const { id = "" } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data: report, isLoading: isLoadingReport } = useQuery({
    queryKey: ["report", id],
    queryFn: () => fetchReport(id),
  });

  const { data: compliance, isLoading: isLoadingCompliance } = useQuery({
    queryKey: ["compliance", id],
    queryFn: () => fetchComplianceSummary(id),
    enabled: report?.status === "completed",
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

  if (isLoadingReport) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <AppHeader />
        <PageContainer title="Report Details" description="Loading report information...">
          <div className="flex justify-center items-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p>Loading report details...</p>
            </div>
          </div>
        </PageContainer>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="min-h-screen flex flex-col bg-gray-50">
        <AppHeader />
        <PageContainer title="Report Not Found" description="The requested report could not be found">
          <div className="text-center py-12">
            <AlertTriangle className="h-12 w-12 text-destructive mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">Report Not Found</h2>
            <p className="text-muted-foreground mb-6">The report you're looking for doesn't exist or has been removed.</p>
            <Button onClick={() => navigate("/reports")}>
              Back to Reports
            </Button>
          </div>
        </PageContainer>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <AppHeader />
      <PageContainer
        title="Report Details"
        description={report.company_name || "Unnamed Company"}
      >
        <Button 
          variant="outline" 
          className="mb-6" 
          onClick={() => navigate("/reports")}
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Reports
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Report Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-muted-foreground">
                    <FileText className="mr-2 h-4 w-4" />
                    <span>File Name</span>
                  </div>
                  <span className="font-medium text-sm">{report.file_name}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-muted-foreground">
                    <Building className="mr-2 h-4 w-4" />
                    <span>Company</span>
                  </div>
                  <span className="font-medium text-sm">{report.company_name || "Not specified"}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-muted-foreground">
                    <Calendar className="mr-2 h-4 w-4" />
                    <span>Fiscal Year</span>
                  </div>
                  <span className="font-medium text-sm">{report.fiscal_year || "Not specified"}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-muted-foreground">
                    <Clock className="mr-2 h-4 w-4" />
                    <span>Upload Date</span>
                  </div>
                  <span className="font-medium text-sm">{formatDate(report.upload_date)}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-muted-foreground">
                    <FileText className="mr-2 h-4 w-4" />
                    <span>File Size</span>
                  </div>
                  <span className="font-medium text-sm">{formatFileSize(report.file_size)}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-sm text-muted-foreground">
                    <Clock className="mr-2 h-4 w-4" />
                    <span>Status</span>
                  </div>
                  {getStatusBadge(report.status)}
                </div>
                
                <Button className="w-full" asChild>
                  <a href={`http://localhost:8000/api/v1/reports/${report.id}/download`} download>
                    <Download className="mr-2 h-4 w-4" /> Download Report
                  </a>
                </Button>
              </CardContent>
            </Card>
          </div>

          <div className="lg:col-span-2">
            {report.status === "pending" && (
              <Card>
                <CardHeader>
                  <CardTitle>Processing Status</CardTitle>
                  <CardDescription>This report is pending processing</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-center py-8">
                    <div className="text-center">
                      <Clock className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                      <h3 className="text-lg font-medium mb-2">Awaiting Processing</h3>
                      <p className="text-muted-foreground">The report is queued for processing. Please check back later.</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {report.status === "processing" && (
              <Card>
                <CardHeader>
                  <CardTitle>Processing Status</CardTitle>
                  <CardDescription>This report is currently being processed</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-center py-8">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                      <h3 className="text-lg font-medium mb-2">Processing in Progress</h3>
                      <p className="text-muted-foreground mb-4">The system is currently analyzing this report for compliance requirements.</p>
                      <Progress value={33} className="max-w-md mx-auto" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {report.status === "failed" && (
              <Card>
                <CardHeader>
                  <CardTitle>Processing Failed</CardTitle>
                  <CardDescription>There was an error processing this report</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-center py-8">
                    <div className="text-center">
                      <AlertTriangle className="h-16 w-16 text-destructive mx-auto mb-4" />
                      <h3 className="text-lg font-medium mb-2">Processing Error</h3>
                      <p className="text-muted-foreground">The system encountered an error while processing this report. Please try uploading again or contact support.</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {report.status === "completed" && isLoadingCompliance && (
              <Card>
                <CardHeader>
                  <CardTitle>Compliance Results</CardTitle>
                  <CardDescription>Loading compliance results...</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                  </div>
                </CardContent>
              </Card>
            )}

            {report.status === "completed" && compliance && (
              <>
                <Card className="mb-6">
                  <CardHeader>
                    <CardTitle>Compliance Summary</CardTitle>
                    <CardDescription>Overall compliance results for this report</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-6">
                      <div className="flex flex-col items-center justify-center py-4">
                        <div className="relative w-36 h-36 mb-4">
                          <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-3xl font-bold">{compliance.overall_compliance_percentage.toFixed(0)}%</span>
                          </div>
                          <svg className="w-full h-full" viewBox="0 0 100 100">
                            <circle
                              cx="50"
                              cy="50"
                              r="45"
                              fill="none"
                              stroke="#e2e8f0"
                              strokeWidth="10"
                            />
                            <circle
                              cx="50"
                              cy="50"
                              r="45"
                              fill="none"
                              stroke={compliance.overall_compliance_percentage > 80 ? "#10b981" : compliance.overall_compliance_percentage > 50 ? "#f59e0b" : "#ef4444"}
                              strokeWidth="10"
                              strokeDasharray={`${2 * Math.PI * 45 * compliance.overall_compliance_percentage / 100} ${2 * Math.PI * 45 * (1 - compliance.overall_compliance_percentage / 100)}`}
                              strokeDashoffset={2 * Math.PI * 45 * 0.25}
                            />
                          </svg>
                        </div>
                        <h3 className="text-lg font-medium">Overall Compliance Score</h3>
                      </div>

                      <div className="grid grid-cols-3 gap-4">
                        <div className="bg-green-50 p-4 rounded-lg text-center">
                          <div className="text-2xl font-bold text-green-600">{compliance.compliant_count}</div>
                          <div className="text-sm text-green-600">Compliant</div>
                        </div>
                        <div className="bg-red-50 p-4 rounded-lg text-center">
                          <div className="text-2xl font-bold text-red-600">{compliance.non_compliant_count}</div>
                          <div className="text-sm text-red-600">Non-Compliant</div>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg text-center">
                          <div className="text-2xl font-bold text-gray-600">{compliance.pending_count}</div>
                          <div className="text-sm text-gray-600">Pending</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Compliance Details</CardTitle>
                    <CardDescription>Detailed compliance results by requirement</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {compliance.results.map((result) => (
                        <div key={result.id} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start mb-2">
                            <h3 className="font-medium">{result.name}</h3>
                            {result.is_compliant === null ? (
                              <Badge variant="outline">Pending</Badge>
                            ) : result.is_compliant ? (
                              <Badge className="bg-green-500">Compliant</Badge>
                            ) : (
                              <Badge variant="destructive">Non-Compliant</Badge>
                            )}
                          </div>
                          <p className="text-sm text-muted-foreground mb-2">{result.description}</p>
                          
                          {result.category && (
                            <div className="flex items-center mb-2">
                              <span className="text-xs bg-secondary px-2 py-1 rounded">
                                {result.category}
                              </span>
                            </div>
                          )}
                          
                          {result.confidence_score !== null && (
                            <div className="mt-2">
                              <div className="flex justify-between items-center text-sm mb-1">
                                <span>Confidence</span>
                                <span>{(result.confidence_score * 100).toFixed(0)}%</span>
                              </div>
                              <Progress value={result.confidence_score * 100} />
                            </div>
                          )}
                          
                          {result.extracted_evidence && (
                            <div className="mt-4">
                              <p className="text-xs uppercase text-muted-foreground mb-1">Evidence</p>
                              <div className="bg-muted p-3 rounded text-sm">
                                {result.extracted_evidence}
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </div>
        </div>
      </PageContainer>
    </div>
  );
};

export default ReportDetail;
