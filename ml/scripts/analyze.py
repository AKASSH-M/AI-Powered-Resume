from resume_analyzer import ResumeAnalyzer
from resume_parser import UniversalResumeParser 
import os

def resume_analysis(pdf_path = "AI-Powered-Resume\ml\data\sample_resume.pdf", printer = False):

    try :

        parser = UniversalResumeParser(pdf_path )
        parser.extract_text()
        parser.print_all_objects()

        analyzer = ResumeAnalyzer.from_parser(parser, "AI-Powered-Resume\ml\data\domains_skills.json" , score_threshold= 8)

        analyzer_text = f'{analyzer.get_summary()} \n {analyzer.suggest_missing_skills()}'
        if printer:
            print(analyzer_text)

        analyzer.plot_domain_scores()
        result = f'''~~~~~~~~~~~~~~~~~~~~~ Resume Analysis ~~~~~~~~~~~~~~~~~~~~~
{parser.personal_info_text}
{analyzer_text}'''

        if os.path.exists('__pycache__'):
            os.remove('__pycache__')
        return result

    except Exception as e:
        print(f"Error during resume analysis: {str(e)}")
        return "Error during resume analysis: {str(e)}"
    
if __name__ == "__main__":
    resume_analysis("C:/Users/Akassh/Desktop/resume.pdf", True)