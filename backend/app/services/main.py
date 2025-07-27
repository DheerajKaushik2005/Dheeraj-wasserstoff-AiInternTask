import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        text = full_text.strip()
        return text
    except Exception as e:
        return f"[ERROR] Could not read PDF: {e}"
def answer_question_from_pdf(file_path: str, question: str) -> str:
    import re
    import os
    text = extract_text_from_pdf(file_path)
    if text.startswith('[ERROR]'):
        return text
    question_lower = question.lower()

    # File name
    if 'file name' in question_lower or 'name of file' in question_lower or 'filename' in question_lower:
        filename = os.path.basename(file_path)
        return f"File name: {filename}"

    # Email
    elif 'email' in question_lower:
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        return f"Email(s) found: {', '.join(emails)}" if emails else "No email found in the document."

    # Phone
    elif 'phone' in question_lower or 'mobile' in question_lower:
        phones = re.findall(r'(?:\+?\d{1,3}[\s-]?)?(?:\d{10})', text)
        return f"Phone number(s) found: {', '.join(phones)}" if phones else "No phone number found in the document."

    # LinkedIn
    elif 'linkedin' in question_lower:
        linkedin = re.findall(r'https?://www\.linkedin\.com/in/[\w\-]+', text)
        return f"LinkedIn profile(s) found: {', '.join(linkedin)}" if linkedin else "No LinkedIn profile found in the document."

    # CGPA
    elif 'cgpa' in question_lower:
        cgpa = re.findall(r'CGPA[:\s]*([\d\.]+)', text, re.IGNORECASE)
        return f"CGPA found: {', '.join(cgpa)}" if cgpa else "No CGPA found in the document."

    # University
    elif 'university' in question_lower:
        uni_match = re.search(r'(University[\w\s,\-]+)', text, re.IGNORECASE)
        if uni_match:
            return f"University details: {uni_match.group(1).strip()}"
        else:
            return "No university details found in the document."

    # Graduation year
    elif 'graduation' in question_lower or 'passout' in question_lower or 'year' in question_lower:
        years = re.findall(r'(20\d{2})', text)
        return f"Year(s) found: {', '.join(years)}" if years else "No graduation year found in the document."

    # Address
    elif 'address' in question_lower:
        addr_match = re.search(r'(Address[:\s]*.+)', text, re.IGNORECASE)
        if addr_match:
            return f"Address found: {addr_match.group(1).strip()}"
        else:
            return "No address found in the document."

    # Skills
    elif 'skill' in question_lower or 'skills' in question_lower:
        skills_match = re.search(r'Skills?[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if skills_match:
            return f"Skills found: {skills_match.group(1).strip()}"
        else:
            return "No skills found in the document."

    # Experience
    elif 'experience' in question_lower:
        exp_match = re.search(r'Experience[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if exp_match:
            return f"Experience found: {exp_match.group(1).strip()}"
        else:
            return "No experience found in the document."

    # Education
    elif 'education' in question_lower:
        edu_match = re.search(r'EDUCATION(.+?)(?:\n\n|$)', text, re.DOTALL | re.IGNORECASE)
        if edu_match:
            return f"Education details: {edu_match.group(1).strip()}"
        else:
            return "No education details found in the document."

    # Author
    elif 'author' in question_lower:
        if 'author' in text.lower():
            return 'The document mentions the author.'
        else:
            return 'No author information found in the document.'

    # Document type
    elif 'type of document' in question_lower or 'document type' in question_lower:
        if 'report' in text.lower():
            return "This document appears to be a report."
        elif 'policy' in text.lower():
            return "This document appears to be a policy."
        elif 'article' in text.lower():
            return "This document appears to be an article."
        else:
            return "Document type not explicitly mentioned, but it contains general information."

    # Key facts
    elif 'key facts' in question_lower or 'facts' in question_lower:
        facts = re.findall(r'Fact[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Key fact(s) found: {', '.join(facts)}" if facts else "No key facts found in the document."

    # Important terms
    elif 'important terms' in question_lower or 'define terms' in question_lower or 'define important terms' in question_lower:
        terms = re.findall(r'\b[A-Z][a-z]+\b', text)
        return f"Important term(s) found: {', '.join(set(terms))}" if terms else "No important terms found in the document."

    # Explanation of a concept
    elif 'explanation of' in question_lower or 'define' in question_lower:
        concept = question_lower.split('explanation of ')[-1].split('define ')[-1].strip()
        if concept:
            definition = re.search(rf'\b{re.escape(concept)}\b[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
            if definition:
                return f"Explanation of {concept}: {definition.group(1).strip()}"
            else:
                return f"No explanation found for {concept} in the document."
        else:
            return "No concept specified for explanation."

    # Solutions suggested
    elif 'solutions suggested' in question_lower or 'solutions' in question_lower:
        solutions = re.findall(r'Solution[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Solution(s) suggested: {', '.join(solutions)}" if solutions else "No solutions suggested in the document."

    # Recommendations made
    elif 'recommendations made' in question_lower or 'recommendations' in question_lower:
        recommendations = re.findall(r'Recommendation[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Recommendation(s) made: {', '.join(recommendations)}" if recommendations else "No recommendations made in the document."

    # Steps proposed
    elif 'steps proposed' in question_lower or 'steps' in question_lower:
        steps = re.findall(r'Step[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Step(s) proposed: {', '.join(steps)}" if steps else "No steps proposed in the document."

    # Main topics covered
    elif 'main topics' in question_lower or 'topics covered' in question_lower or 'major sections' in question_lower:
        topics = re.findall(r'Topic[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Main topic(s) covered: {', '.join(topics)}" if topics else "No main topics found in the document."

    # Major sections
    elif 'major sections' in question_lower or 'sections' in question_lower:
        sections = re.findall(r'Section[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Major section(s) found: {', '.join(sections)}" if sections else "No major sections found in the document."

    # Summary or conclusion section
    elif 'summary' in question_lower or 'conclusion' in question_lower:
        summary = re.search(r'Summary[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if summary:
            return f"Summary found: {summary.group(1).strip()}"
        else:
            conclusion = re.search(r'Conclusion[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
            if conclusion:
                return f"Conclusion found: {conclusion.group(1).strip()}"
            else:
                return "No summary or conclusion section found in the document."

    # Main theme / central idea / addressed problem
    elif 'main theme' in question_lower or 'central idea' in question_lower or 'purpose' in question_lower or 'problem' in question_lower or 'address' in question_lower:
        if 'environment' in text.lower():
            return "This document appears to be about environmental issues."
        elif 'health' in text.lower():
            return "This document appears to be about health-related topics."
        elif 'education' in text.lower():
            return "This document appears to be about education."
        elif 'technology' in text.lower():
            return "This document appears to be about technology."
        else:
            return f"This document appears to be about: {text[:500]}..." if len(text) > 500 else f"This document appears to be about: {text}"

    # Methodology
    elif 'methodology' in question_lower or 'methods used' in question_lower or 'approach' in question_lower:
        methodology = re.search(r'Methodology[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if methodology:
            return f"Methodology used: {methodology.group(1).strip()}"
        else:
            return "No specific methodology mentioned in the document."

    # Future directions or scope
    elif 'future directions' in question_lower or 'scope' in question_lower:
        future_directions = re.search(r'Future Directions[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if future_directions:
            return f"Future directions or scope: {future_directions.group(1).strip()}"
        else:
            return "No future directions or scope mentioned in the document."

    # Challenges or risks
    elif 'challenges' in question_lower or 'risks' in question_lower:
        challenges = re.findall(r'Challenge[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Challenges or risks mentioned: {', '.join(challenges)}" if challenges else "No challenges or risks mentioned in the document."

    # Advantages or benefits
    elif 'advantages' in question_lower or 'benefits' in question_lower:
        advantages = re.findall(r'Advantage[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Advantages or benefits mentioned: {', '.join(advantages)}" if advantages else "No advantages or benefits mentioned in the document."

    # Goals or objectives
    elif 'goals' in question_lower or 'objectives' in question_lower:
        goals = re.findall(r'Goal[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Goals or objectives mentioned: {', '.join(goals)}" if goals else "No goals or objectives mentioned in the document."

    # Key points
    elif 'key points' in question_lower or 'key takeaways' in question_lower:
        key_points = re.findall(r'Key Point[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Key point(s) found: {', '.join(key_points)}" if key_points else "No key points found in the document."

    # Requirements or needs
    elif 'requirements' in question_lower or 'needs' in question_lower:
        requirements = re.findall(r'Requirement[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Requirement(s) found: {', '.join(requirements)}" if requirements else "No requirements found in the document."

    # What should I remember after reading
    elif 'remember' in question_lower or 'takeaway' in question_lower or 'key takeaway' in question_lower:
        takeaway = re.search(r'Takeaway[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if takeaway:
            return f"Key takeaway: {takeaway.group(1).strip()}"
        else:
            return "No specific takeaway mentioned in the document."

    # Simple summary
    elif 'summarize in simple words' in question_lower or 'simple summary' in question_lower:
        return f"Simple Summary: {text[:300]}..." if len(text) > 300 else f"Simple Summary: {text}"

    # Certifications
    elif 'certifications' in question_lower or 'certification' in question_lower:
        certifications = re.findall(r'Certification[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Certification(s) found: {', '.join(certifications)}" if certifications else "No certifications found in the document."

    # Achievements
    elif 'achievements' in question_lower or 'achievement' in question_lower:
        achievements = re.findall(r'Achievement[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Achievement(s) found: {', '.join(achievements)}" if achievements else "No achievements found in the document."

    # Designation or role
    elif 'designation' in question_lower or 'role' in question_lower:
        designation = re.search(r'Designation[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if designation:
            return f"User's designation or role: {designation.group(1).strip()}"
        else:
            return "No designation or role found in the document."

    # Interests or hobbies
    elif 'interests' in question_lower or 'hobbies' in question_lower:
        interests = re.findall(r'Interest[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Interest(s) or hobby(hobbies) found: {', '.join(interests)}" if interests else "No interests or hobbies found in the document."

    # Company name
    elif 'company name' in question_lower or 'company' in question_lower:
        company = re.search(r'Company[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if company:
            return f"Company name: {company.group(1).strip()}"
        else:
            return "No company name found in the document."

    # Company address
    elif 'company address' in question_lower or 'company location' in question_lower:
        company_address = re.search(r'Company Address[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if company_address:
            return f"Company address: {company_address.group(1).strip()}"
        else:
            return "No company address found in the document."

    # Company contact number
    elif 'company contact number' in question_lower or 'company phone' in question_lower:
        company_phone = re.search(r'Company Phone[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if company_phone:
            return f"Company contact number: {company_phone.group(1).strip()}"
        else:
            return "No company contact number found in the document."

    # Company products or services
    elif 'company products' in question_lower or 'company services' in question_lower:
        products_services = re.findall(r'Product[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        return f"Company product(s) or service(s) found: {', '.join(products_services)}" if products_services else "No company products or services found in the document."

    # Main theme / summary fallback
    elif (
        'what is document about' in question_lower or
        'document about' in question_lower or
        'main theme' in question_lower or
        'central idea' in question_lower or
        'purpose' in question_lower or
        'problem' in question_lower or
        'address' in question_lower or
        'Give me a summary' in question_lower
    ):
        return f"This document appears to be about: {text[:500]}..." if len(text) > 500 else f"This document appears to be about: {text}"

    # Summary fallback
    elif 'summary' in question_lower:
        return f"Summary: {text[:300]}..." if len(text) > 300 else f"Summary: {text}"

    # Default: return first 300 chars
    else:
        return f"Extracted Text: {text[:300]}..." if len(text) > 300 else f"Extracted Text: {text}"