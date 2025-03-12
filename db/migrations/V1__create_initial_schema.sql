
-- Create initial database schema

-- Create enum type for report status
CREATE TYPE report_status AS ENUM ('pending', 'processing', 'completed', 'failed');

-- Reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size INTEGER NOT NULL,
    upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status report_status NOT NULL DEFAULT 'pending',
    company_name VARCHAR(255),
    fiscal_year INTEGER,
    processed_text TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Regulatory requirements table
CREATE TABLE regulatory_requirements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Compliance results table
CREATE TABLE compliance_results (
    id SERIAL PRIMARY KEY,
    report_id INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    requirement_id INTEGER NOT NULL REFERENCES regulatory_requirements(id) ON DELETE CASCADE,
    is_compliant BOOLEAN,
    confidence_score FLOAT,
    extracted_evidence TEXT,
    analysis_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(report_id, requirement_id)
);

-- Insert some default regulatory requirements
INSERT INTO regulatory_requirements (name, description, category) VALUES
('Risk Factors Disclosure', 'The report must include a comprehensive discussion of risk factors facing the company.', 'SEC'),
('Management Discussion and Analysis', 'The report must contain MD&A section analyzing financial condition and results of operations.', 'SEC'),
('Financial Statements', 'The report must include audited financial statements compliant with GAAP.', 'Accounting'),
('Executive Compensation', 'The report must disclose compensation for top executives and board members.', 'Governance'),
('Corporate Governance', 'The report must include information about the company''s corporate governance structure.', 'Governance');

-- Create function to update timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at timestamps
CREATE TRIGGER update_reports_modtime
    BEFORE UPDATE ON reports
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_regulatory_requirements_modtime
    BEFORE UPDATE ON regulatory_requirements
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();

CREATE TRIGGER update_compliance_results_modtime
    BEFORE UPDATE ON compliance_results
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();
