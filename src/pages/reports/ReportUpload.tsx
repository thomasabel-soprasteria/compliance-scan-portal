
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { toast } from "sonner";
import { FileUp, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import AppHeader from "@/components/layout/AppHeader";
import PageContainer from "@/components/layout/PageContainer";

const formSchema = z.object({
  file: z.instanceof(FileList).refine((files) => files.length === 1, "Please select a file"),
  company_name: z.string().optional(),
  fiscal_year: z.string().optional().refine((val) => !val || /^\d{4}$/.test(val), {
    message: "Fiscal year must be a 4-digit number",
  }),
});

type FormValues = z.infer<typeof formSchema>;

const ReportUpload = () => {
  const navigate = useNavigate();
  const [isUploading, setIsUploading] = useState(false);

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      company_name: "",
      fiscal_year: "",
    },
  });

  const onSubmit = async (data: FormValues) => {
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", data.file[0]);
      
      if (data.company_name) {
        formData.append("company_name", data.company_name);
      }
      
      if (data.fiscal_year) {
        formData.append("fiscal_year", data.fiscal_year);
      }

      const response = await fetch("http://localhost:8000/api/v1/reports", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to upload report");
      }

      const result = await response.json();
      
      toast.success("Report uploaded successfully", {
        description: "Your report has been uploaded and is being processed.",
      });
      
      navigate("/reports");
    } catch (error) {
      if (error instanceof Error) {
        toast.error("Upload failed", {
          description: error.message,
        });
      } else {
        toast.error("Upload failed", {
          description: "An unknown error occurred. Please try again.",
        });
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <AppHeader />
      <PageContainer title="Upload Report" description="Upload a PDF report for compliance analysis">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Upload Compliance Report</CardTitle>
              <CardDescription>
                Upload a PDF file of your annual report for compliance analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                  <FormField
                    control={form.control}
                    name="file"
                    render={({ field: { onChange, value, ...field } }) => (
                      <FormItem>
                        <FormLabel>PDF Report File</FormLabel>
                        <FormControl>
                          <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center bg-muted/50">
                            <FileUp className="h-10 w-10 text-muted-foreground mb-2" />
                            <div className="text-center mb-4">
                              <p className="font-medium">Drag and drop or click to upload</p>
                              <p className="text-sm text-muted-foreground">PDF files only (max 20MB)</p>
                            </div>
                            {value && value[0] ? (
                              <div className="text-sm bg-secondary p-2 rounded w-full text-center">
                                {value[0].name} ({(value[0].size / 1024 / 1024).toFixed(2)} MB)
                              </div>
                            ) : null}
                            <Input
                              type="file"
                              accept=".pdf"
                              {...field}
                              onChange={(event) => {
                                onChange(event.target.files);
                              }}
                              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                            />
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="company_name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Company Name (Optional)</FormLabel>
                        <FormControl>
                          <Input placeholder="Enter company name" {...field} />
                        </FormControl>
                        <FormDescription>
                          The name of the company the report belongs to
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="fiscal_year"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Fiscal Year (Optional)</FormLabel>
                        <FormControl>
                          <Input placeholder="YYYY" {...field} />
                        </FormControl>
                        <FormDescription>
                          The fiscal year the report covers (e.g., 2023)
                        </FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <div className="flex justify-end">
                    <Button type="button" variant="outline" className="mr-2" onClick={() => navigate("/reports")}>
                      Cancel
                    </Button>
                    <Button type="submit" disabled={isUploading}>
                      {isUploading ? (
                        <>
                          <Upload className="mr-2 h-4 w-4 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>Upload Report</>
                      )}
                    </Button>
                  </div>
                </form>
              </Form>
            </CardContent>
          </Card>
        </div>
      </PageContainer>
    </div>
  );
};

export default ReportUpload;
