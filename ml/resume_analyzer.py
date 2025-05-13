import re
import pdfplumber

class UniversalResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""
        self.sections = {}
        self.personal_info = {}

    def extract_text(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                self.text += page.extract_text() + "\n"
        return self.text

    def extract_personal_info(self):
        email = re.search(r'[\w\.-]+@[\w\.-]+', self.text)
        phone = re.search(r'(\+?\d{1,3}[\s-]?)?(\(?\d{3,4}\)?[\s-]?)?\d{3}[\s-]?\d{4}', self.text)
        linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_]+', self.text)
        github = re.search(r'(https?://)?(www\.)?github\.com/[A-Za-z0-9\-_]+', self.text)
        other_links = re.findall(r'(https?://[^\s]+)', self.text)
        other_links = [link for link in other_links if 'linkedin' not in link and 'github' not in link]
        address = re.search(r'\d+\s[A-Za-z]+\s[A-Za-z]+', self.text)
        if address:
            self.personal_info['address'] = address.group(0)

        lines = self.text.strip().splitlines()
        name = ""
        for line in lines[:10]:  
            line = line.strip()
            if len(line.split()) <= 3 and line.isupper():
                name = line
                break
            elif re.match(r'^[A-Z][a-z]+\s[A-Z][a-z]+$', line):
                name = line
                break

        self.personal_info = {
            'name': name,
            'email': email.group(0) if email else "",
            'phone': phone.group(0) if phone else "",
            'linkedin': linkedin.group(0) if linkedin else "",
            'github': github.group(0) if github else "",
            'other_links': other_links,
        }

        return self.personal_info

    def split_into_sections(self):
        headings = [
            r"(?i)education", r"(?i)experience", r"(?i)projects?", r"(?i)skills?",
            r"(?i)certifications?", r"(?i)achievements?", r"(?i)languages?",
            r"(?i)summary", r"(?i)objective", r"(?i)research", r"(?i)publications?"
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

    def print_all_objects(self):
        print("----- obj1: Personal Info -----")
        for k, v in self.extract_personal_info().items():
            print(f"{k}: {v}")

        print("\n----- Sectional Info (obj2 to objN) -----")
        section_map = self.split_into_sections()
        for i, (title, content) in enumerate(section_map.items(), start=2):
            print(f"\nobj{i}: [{title}]\n{content}...")  


if __name__ == "__main__":
    parser = UniversalResumeParser("AI-Powered-Resume\ml\data\sample_resume.pdf")
    parser.extract_text()
    parser.print_all_objects()
