import json
import re
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from resume_parser import UniversalResumeParser
import random

class ResumeAnalyzer:
    def __init__(self, resume_text: str, domain_file: str, score_threshold: int = 10):
        self.resume_text = resume_text
        self.domain_file = domain_file
        self.score_threshold = score_threshold
        self.domain_scores = defaultdict(int)
        self.matched_skills = defaultdict(list)
        self.missing_skills = {}
        try:
            with open(self.domain_file, 'r') as file:
                self.domain_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Domain file not found: {self.domain_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in domain file: {self.domain_file}")

    @classmethod
    def from_parser(cls, parser: UniversalResumeParser, domain_file: str, score_threshold: int = 10):
        """Initialize analyzer from a UniversalResumeParser instance."""
        resume_text = parser.extract_text()
        return cls(resume_text, domain_file, score_threshold)

    def score_domains(self) -> Dict[str, int]:
        """Score domains based on skill matches using word boundary regex."""
        for domain, skills in self.domain_data.items():
            for skill, weight in skills.items():
                if re.search(r'\b{}\b'.format(re.escape(skill.lower())), self.resume_text.lower()):
                    self.domain_scores[domain] += weight
                    self.matched_skills[domain].append(skill)
                else:
                    if domain not in self.missing_skills:
                        self.missing_skills[domain] = []
                    self.missing_skills[domain].append(skill)
        return dict(self.domain_scores)

    def suggest_improvements(self) -> Dict[str, str | int | List[str]]:
        """Provide feedback based on domain scores."""
        if not self.domain_scores:
            self.score_domains()

        sorted_domains = sorted(self.domain_scores.items(), key=lambda x: x[1], reverse=True)
        feedback = {}

        if not sorted_domains:
            messages = [
                "No domains matched. Consider adding relevant skills to your resume.",
                "Ensure your resume includes specific technologies and keywords related to your field.",
                "Use industry-standard terms to improve keyword matching.",
                "Try incorporating the skill or areas that define your professional interests."
                ,"Deepen your resume with focused experiences to highlight mastery in one or two domains."]
            
            feedback["message"] = (random.choice(messages))
            
            return feedback

        top_domain, top_score = sorted_domains[0]
        feedback['top_domain'] = top_domain
        feedback['score'] = top_score
        feedback['matched_skills'] = self.matched_skills[top_domain]
        feedback['missing_skills'] = self.missing_skills[top_domain][:5]

        if top_score < self.score_threshold:
            feedback['suggestions'] = (
                f"Your resume shows interest in {top_domain} but lacks depth. "
                f"Consider adding more relevant skills such as: {', '.join(self.missing_skills[top_domain][:3])}."
            )
        else:
            feedback['suggestions'] = (
                f"Your resume demonstrates strong alignment with {top_domain}. "
                f"Consider highlighting your experience with: {', '.join(self.matched_skills[top_domain][:3])}."
            )

        # Include all domains with non-zero scores (showing interest)
        interested_domains = [(d, s) for d, s in sorted_domains[1:] if s > 0]
        if interested_domains:
            feedback['interested_domains'] = [
                {
                    "domain": d,
                    "score": s,
                    "matched_skills": self.matched_skills[d][:5],  # Limit to 5 for brevity
                    "missing_skills": self.missing_skills[d][:5]   # Limit to 5 for brevity
                }
                for d, s in interested_domains
            ]

        return feedback

    def get_summary(self) -> str:
        """Generate a formatted summary of the analysis."""
        self.score_domains()
        feedback = self.suggest_improvements()

        interested_info = ""
        if feedback.get('interested_domains'):
            interested_info = "\nOther Domains Showing Interest:\n"
            for d in feedback['interested_domains']:
                interested_info += (
                    f"- {d['domain']} (Score: {d['score']}, "
                    f"Matched: {', '.join(d['matched_skills'] or ['None'])}, "
                    f"Missing: {', '.join(d['missing_skills'] or ['None'])})\n"
                )

        summary = f"""
========================== Resume Analysis Summary ==========================
Top Matching Domain: {feedback.get('top_domain', 'N/A')}
Score: {feedback.get('score', 'N/A')}
Matched Skills: {', '.join(feedback.get('matched_skills', ['None']))}
Missing High-Value Skills: {', '.join(feedback.get('missing_skills', ['None']))}
Suggestions: {feedback.get('suggestions', 'N/A')}
{interested_info}
==============================================================================
"""
        return summary

    def suggest_missing_skills(self) -> str:
        """Suggest missing skills for the top domain and other domains with non-zero scores."""
        if not self.domain_scores:
            self.score_domains()

        sorted_domains = sorted(self.domain_scores.items(), key=lambda x: x[1], reverse=True)
        if not sorted_domains:
            return "No domains matched. Consider adding relevant skills to your resume."

        suggestions = "Consider adding the following high-value skills to strengthen your resume:\n"

        # Top domain
        top_domain, top_score = sorted_domains[0]
        suggestions += f"\n{top_domain} (Top Match, Score: {top_score}):\n"
        top_skills = sorted(
            [(skill, self.domain_data[top_domain].get(skill, 1)) for skill in self.missing_skills[top_domain]],
            key=lambda x: x[1], reverse=True
        )[:5]  # Limit to top 5 by weight
        if top_skills:
            for skill, _ in top_skills:
                suggestions += f"- {skill}\n"
        else:
            suggestions += "- None (all key skills matched)\n"

        # Other domains with non-zero scores
        interested_domains = [(d, s) for d, s in sorted_domains[1:] if s > 0]
        if interested_domains:
            suggestions += "\nOther Domains Showing Interest:\n"
            for domain, score in interested_domains:
                suggestions += f"\n{domain} (Score: {score}):\n"
                domain_skills = sorted(
                    [(skill, self.domain_data[domain].get(skill, 1)) for skill in self.missing_skills[domain]],
                    key=lambda x: x[1], reverse=True
                )[:5]  # Limit to top 5 by weight
                if domain_skills:
                    for skill, _ in domain_skills:
                        suggestions += f"- {skill}\n"
                else:
                    suggestions += "- None (all key skills matched)\n"

        suggestions += "\nThese skills are relevant to domains where your resume shows interest and can enhance its alignment."
        return suggestions

    def plot_domain_scores(self):
        """Visualize domain scores using a bar chart."""
        scores = self.score_domains()
        if not scores:
            print("No domain scores to plot.")
            return
        # plt.figure(figsize=(10, 6))
        # plt.bar(scores.keys(), scores.values())
        # plt.xlabel("Domains")
        # plt.ylabel("Scores")
        # plt.title("Resume Domain Alignment")
        # plt.xticks(rotation=45, ha='right')
        # plt.tight_layout()
        # plt.show()