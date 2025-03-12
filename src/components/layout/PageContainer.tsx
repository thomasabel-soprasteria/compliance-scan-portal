
import { ReactNode } from "react";

interface PageContainerProps {
  children: ReactNode;
  title: string;
  description?: string;
}

const PageContainer = ({ children, title, description }: PageContainerProps) => {
  return (
    <div className="container mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold">{title}</h1>
        {description && <p className="text-muted-foreground mt-1">{description}</p>}
      </div>
      {children}
    </div>
  );
};

export default PageContainer;
