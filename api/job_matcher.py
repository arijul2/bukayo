import os
import openai
from typing import Dict, Any, List
import json
import re
from datetime import datetime

class JobMatcher:
    """AI-powered job matching using OpenAI directly"""
    
    def __init__(self, openai_api_key: str):
        """Initialize the job matcher with OpenAI API key"""
        self.client = openai.OpenAI(api_key=openai_api_key)
    
    def analyze_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze how well a resume matches a job description
        
        Args:
            resume_text: Extracted text from resume
            job_description: Extracted text from job posting
            
        Returns:
            Structured analysis with recommendation and detailed insights
        """
        try:
            prompt = f"""
You are an expert career counselor and recruiter with 20+ years of experience. 
Analyze how well this resume matches the job description and provide actionable insights.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

ANALYSIS INSTRUCTIONS:
1. Carefully compare the resume against job requirements
2. Look for matching skills, experience, education, and qualifications
3. Identify gaps and missing requirements
4. Consider experience level (junior, mid, senior) compatibility
5. Evaluate education requirements vs candidate background

RECOMMENDATION CRITERIA:
- APPLY: 70%+ match, most requirements met, good fit
- DECENT_CHANCE: 40-69% match, some gaps but worth trying
- AVOID: <40% match, major gaps, poor fit or overqualified

Please provide your analysis in this exact JSON format:
{{
    "recommendation": "APPLY/AVOID/DECENT_CHANCE",
    "match_score": 85,
    "confidence_score": 90,
    "strengths": ["List of matching qualifications", "Strong Python skills", "Relevant experience"],
    "weaknesses": ["Missing requirements", "Limited experience in X"],
    "missing_skills": ["Specific skills from job not in resume"],
    "experience_match": "How experience level matches requirements",
    "education_match": "How education matches requirements",
    "detailed_reasoning": "Detailed explanation of the recommendation with specific examples"
}}

ANALYSIS:
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career counselor. Always respond with valid JSON in the exact format requested."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                # Extract JSON from response if it's wrapped in markdown
                if "```json" in analysis_text:
                    json_start = analysis_text.find("```json") + 7
                    json_end = analysis_text.find("```", json_start)
                    analysis_text = analysis_text[json_start:json_end].strip()
                elif "```" in analysis_text:
                    json_start = analysis_text.find("```") + 3
                    json_end = analysis_text.rfind("```")
                    analysis_text = analysis_text[json_start:json_end].strip()
                
                analysis_result = json.loads(analysis_text)
                
                # Add metadata
                analysis_result.update({
                    "analysis_timestamp": datetime.now().isoformat(),
                    "ai_model": "gpt-3.5-turbo",
                    "processing_status": "success"
                })
                
                return analysis_result
                
            except json.JSONDecodeError as e:
                # Fallback parsing if JSON fails
                return self._fallback_parse(analysis_text, str(e))
                
        except Exception as e:
            return {
                "processing_status": "error",
                "error_message": str(e),
                "recommendation": "AVOID",
                "match_score": 0,
                "confidence_score": 0,
                "strengths": [],
                "weaknesses": ["Analysis failed"],
                "missing_skills": [],
                "experience_match": "Could not analyze",
                "education_match": "Could not analyze",
                "detailed_reasoning": f"Analysis failed due to error: {str(e)}",
                "analysis_timestamp": datetime.now().isoformat()
            }
    
    def _fallback_parse(self, raw_response: str, parse_error: str) -> Dict[str, Any]:
        """Fallback parsing when JSON parsing fails"""
        
        # Extract recommendation using regex
        recommendation = "DECENT_CHANCE"  # default
        rec_match = re.search(r'"recommendation":\s*"(APPLY|AVOID|DECENT_CHANCE)"', raw_response, re.IGNORECASE)
        if rec_match:
            recommendation = rec_match.group(1).upper()
        
        # Extract match score
        match_score = 50  # default
        score_match = re.search(r'"match_score":\s*(\d+)', raw_response)
        if score_match:
            match_score = int(score_match.group(1))
        
        return {
            "recommendation": recommendation,
            "match_score": match_score,
            "confidence_score": 70,
            "strengths": ["Analysis completed with fallback parsing"],
            "weaknesses": ["Structured parsing failed"],
            "missing_skills": ["Could not extract detailed skills"],
            "experience_match": "Could not fully analyze experience match",
            "education_match": "Could not fully analyze education match", 
            "detailed_reasoning": raw_response,
            "processing_status": "partial_success",
            "parse_error": parse_error,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def batch_analyze(self, resume_text: str, job_descriptions: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Analyze one resume against multiple job descriptions
        
        Args:
            resume_text: The candidate's resume text
            job_descriptions: List of job descriptions with metadata
            
        Returns:
            List of analysis results, sorted by match score
        """
        results = []
        
        for job_data in job_descriptions:
            job_text = job_data.get("text", "")
            job_title = job_data.get("title", "Unknown Position")
            
            analysis = self.analyze_job_match(resume_text, job_text)
            
            # Add job metadata to result
            analysis.update({
                "job_title": job_title,
                "job_filename": job_data.get("filename", ""),
                "company": job_data.get("company", "Not specified")
            })
            
            results.append(analysis)
        
        # Sort by match score (highest first)
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return results