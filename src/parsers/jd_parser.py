import re
import json
from typing import Dict, List, Optional, Any
import spacy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobDescriptionParser:
    def __init__(self):
        """Initialize the job description parser with spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize job description text"""
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove common job posting headers/footers
        headers_to_remove = [
            r'job description',
            r'job posting',
            r'career opportunity',
            r'we are hiring',
            r'join our team'
        ]
        
        for header in headers_to_remove:
            text = re.sub(header, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def extract_job_title(self, text: str) -> str:
        """Extract job title from job description"""
        # Common patterns for job titles
        title_patterns = [
            r'(?:position|role|title|job):\s*([^\n]+)',
            r'(?:we are looking for|seeking|hiring)\s+(?:a|an)?\s*([^\n]+?)(?:\s+to|$|\n)',
            r'^([A-Z][^.\n]{5,50})(?:\n|$)',
            r'(?:software|data|web|mobile|devops|cloud|ai|ml)\s+(?:engineer|developer|analyst|scientist|architect|consultant)',
            r'(?:senior|junior|lead|principal)\s+(?:software|data|web|mobile|devops|cloud|ai|ml)\s+(?:engineer|developer|analyst|scientist|architect|consultant)'
        ]
        
        text_lower = text.lower()
        for pattern in title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                return matches[0].strip()
        
        # Fallback: look for common job titles in the first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in 
                  ['engineer', 'developer', 'analyst', 'scientist', 'architect', 'consultant', 'manager']):
                return line
        
        return "Software Engineer"  # Default fallback
    
    def extract_company_info(self, text: str) -> Dict[str, str]:
        """Extract company information"""
        company_info = {
            "name": "",
            "location": "",
            "industry": ""
        }
        
        # Company name patterns
        company_patterns = [
            r'(?:at|company|organization):\s*([^\n]+)',
            r'(?:join|work with)\s+([A-Z][^.\n]+)',
            r'^([A-Z][^.\n]{2,30})(?:\s+is|\s+seeks|\s+hiring)'
        ]
        
        for pattern in company_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                company_info["name"] = matches[0].strip()
                break
        
        # Location patterns
        location_patterns = [
            r'(?:location|based in|office in):\s*([^\n]+)',
            r'(?:hyderabad|bangalore|pune|delhi|mumbai|chennai|kolkata|gurgaon|noida)',
            r'(?:remote|hybrid|onsite)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                company_info["location"] = matches[0].strip()
                break
        
        return company_info
    
    def extract_required_skills(self, text: str) -> List[str]:
        """Extract must-have/required skills"""
        required_skills = []
        
        # Look for required skills sections
        required_sections = [
            r'(?:required|must have|mandatory|essential|core)\s+(?:skills|qualifications|requirements?):?\s*([^.]*)',
            r'(?:candidate must have|candidates should have|you must have):?\s*([^.]*)',
            r'(?:minimum|basic)\s+(?:requirements?|qualifications?):?\s*([^.]*)'
        ]
        
        text_lower = text.lower()
        for pattern in required_sections:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Extract skills from the matched text
                skills = self._extract_skills_from_text(match)
                required_skills.extend(skills)
        
        # Also look for technical skills mentioned throughout the document
        all_skills = self._extract_skills_from_text(text)
        required_skills.extend(all_skills)
        
        return list(set(skill.lower() for skill in required_skills))
    
    def extract_preferred_skills(self, text: str) -> List[str]:
        """Extract good-to-have/preferred skills"""
        preferred_skills = []
        
        # Look for preferred skills sections
        preferred_sections = [
            r'(?:preferred|good to have|nice to have|bonus|plus|advantage):?\s*([^.]*)',
            r'(?:additional|extra|optional)\s+(?:skills|qualifications?):?\s*([^.]*)',
            r'(?:would be great|ideal candidate):?\s*([^.]*)'
        ]
        
        text_lower = text.lower()
        for pattern in preferred_sections:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skills = self._extract_skills_from_text(match)
                preferred_skills.extend(skills)
        
        return list(set(skill.lower() for skill in preferred_skills))
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from a given text"""
        skills = []
        
        # Technical skills patterns
        skill_patterns = [
            r'\b(python|java|javascript|react|angular|vue|node\.?js|express|django|flask|fastapi)\b',
            r'\b(sql|mysql|postgresql|mongodb|redis|docker|kubernetes)\b',
            r'\b(aws|azure|gcp|git|github|gitlab)\b',
            r'\b(machine learning|deep learning|tensorflow|pytorch|scikit-learn)\b',
            r'\b(pandas|numpy|matplotlib|seaborn|jupyter)\b',
            r'\b(html|css|bootstrap|tailwind|sass|less|typescript)\b',
            r'\b(rest api|graphql|microservices|agile|scrum|devops)\b',
            r'\b(spring|hibernate|jpa|junit|maven|gradle)\b',
            r'\b(ios|android|swift|kotlin|flutter|react native)\b',
            r'\b(linux|unix|bash|shell|powershell)\b',
            r'\b(jenkins|ci/cd|terraform|ansible|prometheus|grafana)\b'
        ]
        
        text_lower = text.lower()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.extend(matches)
        
        return skills
    
    def extract_qualifications(self, text: str) -> List[str]:
        """Extract educational qualifications"""
        qualifications = []
        
        # Education patterns
        education_patterns = [
            r'(?:bachelor|master|phd|doctorate|diploma|certificate).*?(?:in|of|,).*?(?:computer science|engineering|technology|it|software)',
            r'(?:b\.?s\.?|m\.?s\.?|ph\.?d\.?|m\.?b\.?a\.?).*?(?:in|of|,).*?(?:computer science|engineering|technology|it|software)',
            r'(?:degree|graduation).*?(?:in|of|,).*?(?:computer science|engineering|technology|it|software)',
            r'(?:years? of experience|experience level):?\s*(\d+[\+\-\s]*(?:years?|yrs?))',
            r'(?:minimum|at least)\s+(\d+)\s+(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)'
        ]
        
        text_lower = text.lower()
        for pattern in education_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            qualifications.extend(matches)
        
        return qualifications
    
    def extract_experience_requirements(self, text: str) -> Dict[str, Any]:
        """Extract experience requirements"""
        experience_req = {
            "min_years": 0,
            "max_years": None,
            "level": "",
            "description": ""
        }
        
        # Experience level patterns
        level_patterns = [
            r'(?:entry level|junior|fresher|0-2\s*years?)',
            r'(?:mid level|intermediate|2-5\s*years?)',
            r'(?:senior|lead|5-8\s*years?)',
            r'(?:principal|architect|8\+\s*years?)'
        ]
        
        text_lower = text.lower()
        for pattern in level_patterns:
            if re.search(pattern, text_lower):
                experience_req["level"] = re.search(pattern, text_lower).group(0)
                break
        
        # Years of experience patterns
        years_patterns = [
            r'(\d+)\s*[-+]\s*(\d+)\s*(?:years?|yrs?)',
            r'(?:minimum|at least)\s+(\d+)\s+(?:years?|yrs?)',
            r'(\d+)\+\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)'
        ]
        
        for pattern in years_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                if isinstance(matches[0], tuple):
                    if len(matches[0]) == 2:
                        experience_req["min_years"] = int(matches[0][0])
                        experience_req["max_years"] = int(matches[0][1])
                    else:
                        experience_req["min_years"] = int(matches[0][0])
                else:
                    experience_req["min_years"] = int(matches[0])
                break
        
        return experience_req
    
    def extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        
        # Look for responsibilities sections
        resp_sections = [
            r'(?:responsibilities|duties|what you will do|key responsibilities?):?\s*([^.]*)',
            r'(?:role and responsibilities?|job responsibilities?):?\s*([^.]*)'
        ]
        
        text_lower = text.lower()
        for pattern in resp_sections:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by bullet points or line breaks
                points = re.split(r'[•\-\*\n]', match)
                for point in points:
                    point = point.strip()
                    if len(point) > 10:
                        responsibilities.append(point)
        
        return responsibilities
    
    def extract_benefits(self, text: str) -> List[str]:
        """Extract benefits and perks"""
        benefits = []
        
        # Benefits patterns
        benefit_patterns = [
            r'(?:benefits|perks|compensation|package):?\s*([^.]*)',
            r'(?:we offer|what we offer):?\s*([^.]*)',
            r'(?:competitive|attractive)\s+(?:salary|package|compensation)'
        ]
        
        text_lower = text.lower()
        for pattern in benefit_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by bullet points or line breaks
                points = re.split(r'[•\-\*\n]', match)
                for point in points:
                    point = point.strip()
                    if len(point) > 5:
                        benefits.append(point)
        
        return benefits
    
    def parse_job_description(self, text: str) -> Dict[str, Any]:
        """Main method to parse job description and extract all information"""
        try:
            # Clean text
            cleaned_text = self.clean_text(text)
            
            # Extract various components
            job_title = self.extract_job_title(cleaned_text)
            company_info = self.extract_company_info(cleaned_text)
            required_skills = self.extract_required_skills(cleaned_text)
            preferred_skills = self.extract_preferred_skills(cleaned_text)
            qualifications = self.extract_qualifications(cleaned_text)
            experience_req = self.extract_experience_requirements(cleaned_text)
            responsibilities = self.extract_responsibilities(cleaned_text)
            benefits = self.extract_benefits(cleaned_text)
            
            return {
                "raw_text": text,
                "cleaned_text": cleaned_text,
                "job_title": job_title,
                "company_info": company_info,
                "required_skills": required_skills,
                "preferred_skills": preferred_skills,
                "qualifications": qualifications,
                "experience_requirements": experience_req,
                "responsibilities": responsibilities,
                "benefits": benefits
            }
            
        except Exception as e:
            logger.error(f"Error parsing job description: {e}")
            return {
                "raw_text": text,
                "cleaned_text": "",
                "job_title": "",
                "company_info": {},
                "required_skills": [],
                "preferred_skills": [],
                "qualifications": [],
                "experience_requirements": {},
                "responsibilities": [],
                "benefits": [],
                "error": str(e)
            }
