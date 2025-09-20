import os
import numpy as np
from typing import Dict, List, Any, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticMatching:
    def __init__(self):
        """Initialize semantic matching with embedding model and Gemini client"""
        # Initialize Gemini client
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.gemini_model = genai.GenerativeModel(os.getenv("DEFAULT_MODEL", "gemini-pro"))
        
        # Initialize sentence transformer model
        model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        try:
            self.embedding_model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            self.embedding_model = None
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        if not self.embedding_model:
            logger.error("Embedding model not available")
            return np.array([])
        
        try:
            embeddings = self.embedding_model.encode(texts)
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return np.array([])
    
    def calculate_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """Calculate semantic similarity between resume and job description"""
        try:
            # Generate embeddings
            embeddings = self.generate_embeddings([resume_text, jd_text])
            
            if embeddings.size == 0:
                return 0.0
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def extract_semantic_skills(self, resume_text: str, jd_skills: List[str]) -> Dict[str, Any]:
        """Extract semantically similar skills from resume"""
        try:
            # Split resume into sentences for better matching
            resume_sentences = resume_text.split('. ')
            
            # Generate embeddings for resume sentences and JD skills
            all_texts = resume_sentences + jd_skills
            embeddings = self.generate_embeddings(all_texts)
            
            if embeddings.size == 0:
                return {"semantic_matches": [], "semantic_score": 0.0}
            
            resume_embeddings = embeddings[:len(resume_sentences)]
            jd_skill_embeddings = embeddings[len(resume_sentences):]
            
            semantic_matches = []
            total_similarity = 0
            
            for i, jd_skill in enumerate(jd_skills):
                jd_embedding = jd_skill_embeddings[i].reshape(1, -1)
                
                # Find best matching resume sentence
                similarities = cosine_similarity(jd_embedding, resume_embeddings)[0]
                best_match_idx = np.argmax(similarities)
                best_similarity = similarities[best_match_idx]
                
                if best_similarity > 0.3:  # Threshold for semantic match
                    semantic_matches.append({
                        "jd_skill": jd_skill,
                        "resume_context": resume_sentences[best_match_idx],
                        "similarity_score": float(best_similarity)
                    })
                    total_similarity += best_similarity
            
            semantic_score = total_similarity / len(jd_skills) if jd_skills else 0.0
            
            return {
                "semantic_matches": semantic_matches,
                "semantic_score": semantic_score,
                "total_skills": len(jd_skills),
                "matched_skills": len(semantic_matches)
            }
            
        except Exception as e:
            logger.error(f"Error in semantic skill extraction: {e}")
            return {"semantic_matches": [], "semantic_score": 0.0, "error": str(e)}
    
    def llm_semantic_analysis(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Use LLM for advanced semantic analysis"""
        try:
            prompt = f"""
            You are an expert resume evaluator. Analyze the following resume against the job description and provide a detailed assessment.

            JOB DESCRIPTION:
            {jd_text[:2000]}

            RESUME:
            {resume_text[:2000]}

            Please provide:
            1. Overall fit score (0-100)
            2. Key strengths that match the job requirements
            3. Missing skills or qualifications
            4. Experience level assessment
            5. Specific recommendations for improvement

            Format your response as JSON with the following structure:
            {{
                "fit_score": <number>,
                "strengths": ["strength1", "strength2", ...],
                "missing_skills": ["skill1", "skill2", ...],
                "experience_assessment": "<assessment>",
                "recommendations": ["rec1", "rec2", ...]
            }}
            """
            
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.3
                )
            )
            
            # Parse the response
            response_text = response.text
            
            # Try to extract JSON from response
            import json
            try:
                # Find JSON in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                else:
                    # Fallback parsing
                    analysis = self._parse_llm_response(response_text)
            except json.JSONDecodeError:
                analysis = self._parse_llm_response(response_text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in LLM semantic analysis: {e}")
            return {
                "fit_score": 0,
                "strengths": [],
                "missing_skills": [],
                "experience_assessment": "Unable to assess",
                "recommendations": ["Error in analysis"],
                "error": str(e)
            }
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response when JSON parsing fails"""
        analysis = {
            "fit_score": 0,
            "strengths": [],
            "missing_skills": [],
            "experience_assessment": "Unable to assess",
            "recommendations": []
        }
        
        # Extract fit score
        import re
        score_match = re.search(r'(\d+)', response_text)
        if score_match:
            analysis["fit_score"] = int(score_match.group(1))
        
        # Extract strengths
        if "strengths" in response_text.lower():
            strengths_section = response_text.lower().split("strengths")[1].split("missing")[0]
            strengths = re.findall(r'[•\-\*]\s*([^\n]+)', strengths_section)
            analysis["strengths"] = [s.strip() for s in strengths]
        
        # Extract missing skills
        if "missing" in response_text.lower():
            missing_section = response_text.lower().split("missing")[1].split("experience")[0]
            missing = re.findall(r'[•\-\*]\s*([^\n]+)', missing_section)
            analysis["missing_skills"] = [s.strip() for s in missing]
        
        return analysis
    
    def generate_improvement_suggestions(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any], analysis: Dict[str, Any]) -> List[str]:
        """Generate personalized improvement suggestions"""
        suggestions = []
        
        # Skills-based suggestions
        missing_skills = analysis.get("missing_skills", [])
        if missing_skills:
            suggestions.append(f"Consider learning or gaining experience with: {', '.join(missing_skills[:3])}")
        
        # Experience-based suggestions
        resume_experience = resume_data.get("experience", [])
        jd_experience_req = jd_data.get("experience_requirements", {})
        
        if jd_experience_req.get("min_years", 0) > 0:
            suggestions.append(f"Gain more experience in relevant technologies to meet the {jd_experience_req['min_years']}+ years requirement")
        
        # Project suggestions
        resume_projects = resume_data.get("projects", [])
        if len(resume_projects) < 2:
            suggestions.append("Add more relevant projects to showcase your technical skills")
        
        # Certification suggestions
        jd_skills = jd_data.get("required_skills", [])
        cert_keywords = ['aws', 'azure', 'gcp', 'certified', 'certification']
        cert_requirements = [skill for skill in jd_skills if any(keyword in skill.lower() for keyword in cert_keywords)]
        
        if cert_requirements:
            suggestions.append(f"Consider obtaining certifications in: {', '.join(cert_requirements[:2])}")
        
        # General suggestions
        suggestions.extend([
            "Tailor your resume to highlight relevant experience for this specific role",
            "Include quantifiable achievements and metrics in your experience descriptions",
            "Ensure your contact information and professional summary are up to date"
        ])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def calculate_semantic_match_score(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall semantic match score"""
        try:
            resume_text = resume_data.get("cleaned_text", "")
            jd_text = jd_data.get("cleaned_text", "")
            jd_skills = jd_data.get("required_skills", [])
            
            # Calculate different semantic metrics
            overall_similarity = self.calculate_semantic_similarity(resume_text, jd_text)
            semantic_skills = self.extract_semantic_skills(resume_text, jd_skills)
            llm_analysis = self.llm_semantic_analysis(resume_text, jd_text)
            
            # Generate improvement suggestions
            suggestions = self.generate_improvement_suggestions(resume_data, jd_data, llm_analysis)
            
            # Calculate weighted semantic score
            weights = {
                "overall_similarity": 0.3,
                "semantic_skills": 0.4,
                "llm_analysis": 0.3
            }
            
            semantic_score = (
                overall_similarity * weights["overall_similarity"] +
                semantic_skills["semantic_score"] * weights["semantic_skills"] +
                (llm_analysis.get("fit_score", 0) / 100) * weights["llm_analysis"]
            )
            
            return {
                "semantic_score": semantic_score,
                "overall_similarity": overall_similarity,
                "semantic_skills": semantic_skills,
                "llm_analysis": llm_analysis,
                "improvement_suggestions": suggestions,
                "weights": weights
            }
            
        except Exception as e:
            logger.error(f"Error calculating semantic match score: {e}")
            return {
                "semantic_score": 0.0,
                "error": str(e)
            }
