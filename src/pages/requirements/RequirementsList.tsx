
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { 
  ClipboardList, 
  Plus, 
  Search, 
  Filter,
  Edit,
  Trash2,
  CheckCircle,
  XCircle 
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/hooks/use-toast";
import AppHeader from "@/components/layout/AppHeader";
import PageContainer from "@/components/layout/PageContainer";
import RequirementForm from "@/components/requirements/RequirementForm";

interface Requirement {
  id: number;
  name: string;
  description: string;
  category: string | null;
  active: boolean;
  created_at: string;
  updated_at: string;
}

const fetchRequirements = async (): Promise<Requirement[]> => {
  const response = await fetch("http://localhost:8000/api/v1/requirements");
  if (!response.ok) {
    throw new Error("Failed to fetch requirements");
  }
  return response.json();
};

const RequirementsList = () => {
  const { toast } = useToast();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [showOnlyActive, setShowOnlyActive] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingRequirement, setEditingRequirement] = useState<Requirement | null>(null);

  const { 
    data: requirements = [], 
    isLoading,
    refetch 
  } = useQuery({
    queryKey: ["requirements"],
    queryFn: fetchRequirements,
  });

  // Get unique categories
  const categories = Array.from(
    new Set(
      requirements
        .map((req) => req.category)
        .filter((cat): cat is string => cat !== null)
    )
  );

  // Filter requirements
  const filteredRequirements = requirements.filter((req) => {
    const matchesSearch = 
      req.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      req.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = 
      selectedCategory === null || req.category === selectedCategory;
    
    const matchesActive = 
      !showOnlyActive || req.active;
    
    return matchesSearch && matchesCategory && matchesActive;
  });

  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/requirements/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete requirement");
      }

      toast({
        title: "Requirement deleted",
        description: "The requirement has been successfully deleted.",
      });

      refetch();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to delete requirement",
      });
    }
  };

  const handleFormSuccess = () => {
    refetch();
    setShowAddForm(false);
    setEditingRequirement(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <AppHeader />
      <PageContainer 
        title="Regulatory Requirements" 
        description="Manage compliance requirements"
      >
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <div className="flex flex-1 w-full md:w-auto">
            <div className="relative flex-1">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search requirements..."
                className="pl-8"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="gap-1">
                  <Filter className="h-4 w-4" />
                  Filter
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <div className="p-2">
                  <div className="font-medium mb-1">Category</div>
                  <DropdownMenuItem onClick={() => setSelectedCategory(null)}>
                    All Categories
                  </DropdownMenuItem>
                  {categories.map((category) => (
                    <DropdownMenuItem 
                      key={category} 
                      onClick={() => setSelectedCategory(category)}
                    >
                      {category}
                    </DropdownMenuItem>
                  ))}
                  <div className="my-1 border-t"></div>
                  <div className="font-medium my-1">Status</div>
                  <DropdownMenuItem onClick={() => setShowOnlyActive(!showOnlyActive)}>
                    {showOnlyActive ? "Show All" : "Show Only Active"}
                  </DropdownMenuItem>
                </div>
              </DropdownMenuContent>
            </DropdownMenu>

            <Button onClick={() => setShowAddForm(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Requirement
            </Button>
          </div>
        </div>

        {showAddForm && (
          <div className="mb-6">
            <Card className="p-6">
              <h3 className="text-lg font-medium mb-4">Add New Requirement</h3>
              <RequirementForm onSuccess={handleFormSuccess} onCancel={() => setShowAddForm(false)} />
            </Card>
          </div>
        )}

        {editingRequirement && (
          <div className="mb-6">
            <Card className="p-6">
              <h3 className="text-lg font-medium mb-4">Edit Requirement</h3>
              <RequirementForm 
                requirement={editingRequirement}
                onSuccess={handleFormSuccess} 
                onCancel={() => setEditingRequirement(null)} 
              />
            </Card>
          </div>
        )}

        {selectedCategory && (
          <div className="mb-4 flex items-center">
            <Badge className="mr-2">{selectedCategory}</Badge>
            <Button variant="ghost" size="sm" onClick={() => setSelectedCategory(null)}>
              Clear filter
            </Button>
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p>Loading requirements...</p>
          </div>
        ) : filteredRequirements.length === 0 ? (
          <Card className="p-12 text-center">
            <ClipboardList className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium mb-2">No Requirements Found</h3>
            <p className="text-muted-foreground mb-6">
              {searchTerm
                ? "No requirements match your search criteria"
                : "No regulatory requirements have been added yet"}
            </p>
            <Button onClick={() => setShowAddForm(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Requirement
            </Button>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredRequirements.map((requirement) => (
              <Card key={requirement.id} className="p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-1">
                      <h3 className="font-medium">{requirement.name}</h3>
                      {requirement.active ? (
                        <Badge className="ml-2 bg-green-500">
                          <CheckCircle className="h-3 w-3 mr-1" /> Active
                        </Badge>
                      ) : (
                        <Badge variant="outline" className="ml-2">
                          <XCircle className="h-3 w-3 mr-1" /> Inactive
                        </Badge>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">
                      {requirement.description}
                    </p>
                    {requirement.category && (
                      <Badge variant="outline">{requirement.category}</Badge>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => setEditingRequirement(requirement)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="icon"
                      className="text-destructive"
                      onClick={() => handleDelete(requirement.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </PageContainer>
    </div>
  );
};

export default RequirementsList;
