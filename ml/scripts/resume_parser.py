import re
import pdfplumber
import spacy
from typing import Dict, List

class UniversalResumeParser:
    def __init__(self, pdf_path = "AI-Powered-Resume\ml\data\sample_resume.pdf"):
        self.pdf_path = pdf_path
        self.text = ""
        self.sections = {}
        self.personal_info = {}
        self.nlp = None
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])  # Load spacy for NER
        except Exception as e:
            print(f"Warning: Could not load spacy model for NER: {str(e)}. Falling back to regex.")

    def extract_text(self) -> str:
        """Extract text from the PDF with error handling."""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        self.text += page_text + "\n"
            if not self.text.strip():
                raise ValueError("No text extracted from the PDF.")
            return self.text
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

 
    def extract_personal_info(self) -> Dict[str, str | List[str]]:
        """Extract personal information using regex and optional spaCy NER."""
        
        # Regex patterns
        email = re.search(r'[\w\.-]+@[\w\.-]+', self.text)
        phone = re.search(r'(\+?\d{1,3}[\s-]?)?(\(?\d{3,4}\)?[\s-]?)?\d{3}[\s-]?\d{4}', self.text)
        linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_]+', self.text)
        github = re.search(r'(https?://)?(www\.)?github\.com/[A-Za-z0-9\-_]+', self.text)
        
        # Capture all links and exclude LinkedIn and GitHub
        other_links = re.findall(r'(https?://[^\s]+)', self.text)
        other_links = [link for link in other_links if 'linkedin' not in link.lower() and 'github' not in link.lower()]
        
        # Address regex (simple US-style address)
        address = re.search(r'\d+\s[A-Za-z\s]+,\s*[A-Za-z]+,\s*[A-Z]{2}\s*\d{5}', self.text)
        
        # Name and address extraction using spaCy
        name = ""
        address_from_ner = ""


        # Fallback: Heuristic name detection from first few lines
        if not name:
            lines = self.text.strip().splitlines()
            for line in lines[:10]:  # limit to top few lines
                line = line.strip()
                if not line or line.lower() in {"email", "e-mail", "contact", "phone", "address", "linkedin", "github" , "skills", "education", "experience", "projects", "certifications", "achievements", "languages", "summary", "objective"}:
                    continue
                if len(line.split()) <= 4 and line.isupper() and not re.search(r'\d', line):
                    name = line
                    break
                elif re.match(r'^[A-Z][a-z]+(\s[A-Z]\.)?\s[A-Z][a-z]+$', line):
                    name = line
                    break

        # Compile extracted information
        self.personal_info = {
            'name': name or "Not found",
            'email': email.group(0) if email else "",
            'phone': phone.group(0) if phone else "",
            'linkedin': linkedin.group(0) if linkedin else "",
            'github': github.group(0) if github else "",
            'other_links': other_links,
            'address': address.group(0) if address else address_from_ner or ""
        }
        
        return self.personal_info

    def split_into_sections(self) -> Dict[str, str]:
        """Split resume text into sections based on headings."""
        headings = [
            r"(?i)(education|academic)", r"(?i)(experience|work\s*history)", r"(?i)projects?",
            r"(?i)skills?", r"(?i)certifications?", r"(?i)achievements?",
            r"(?i)languages?", r"(?i)(summary|professional\s*summary)", r"(?i)objective",
            r"(?i)research", r"(?i)publications?"
        ]
        current_section = "General"
        self.sections[current_section] = ""
        for line in self.text.splitlines():
            matched = False
            for h in headings:
                if re.match(h, line.strip()):
                    current_section = re.sub(r'[^a-zA-Z ]', '', line.strip()).title()
                    self.sections[current_section] = ""
                    matched = True
                    break
            if not matched:
                self.sections[current_section] += line.strip() + "\n"
        return self.sections

    def print_all_objects(self,printer = False):
        """Print extracted personal info and sections."""
        # print("----- obj1: Personal Info -----")
        self.personal_info_text = ""
        self.personal_info_obj = self.extract_personal_info()
        for k, v in self.personal_info_obj.items():
                if v:
                    self.personal_info_text += f"{k}: {v}\n"
        if printer:
            print("\n----- Sectional Info (obj2 to objN) -----")
            section_map = self.split_into_sections()
            for i, (title, content) in enumerate(section_map.items(), start=2):
                print(f"\nobj{i}: [{title}]\n{content.rstrip() or 'No content'}")