# 📄 Resume & Cover Letter Builder

**Land your dream internship with AI-powered application materials!**

Stop staring at a blank page. This tool helps you create compelling resumes and cover letters tailored to specific job postings. The AI version uses Claude to transform your experiences into impactful bullet points and generate customized cover letters.

## 🎯 What This App Does

- **Build your resume**: Add experiences, education, skills, and projects
- **Generate bullet points**: Transform experience descriptions into achievement-focused bullets
- **Create cover letters**: Auto-generate tailored cover letters from job descriptions
- **ATS optimization**: Get tips to pass Applicant Tracking Systems
- **Multiple formats**: Export to PDF or text
- **Job-specific tailoring**: Customize resume for different roles

## 🚀 Quick Start

```bash
cd template-6-resume-builder
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key_here" > .env  # For advanced version
streamlit run app.py  # Beginner version
streamlit run app_advanced.py  # AI-powered version
```

## 📁 File Structure

```
template-6-resume-builder/
├── README.md           # This file
├── app.py             # Beginner version
├── app_advanced.py    # AI-powered version
├── requirements.txt   # Dependencies
└── data/             # Your resume data
```

## 🎓 What You'll Learn

### Beginner Version
- Form-based data collection
- Resume template formatting
- PDF generation basics
- Data persistence
- Professional document structure

### Advanced Version
- Claude AI for content generation
- Job description analysis
- Keyword extraction and optimization
- Dynamic content tailoring
- Advanced text generation
- ATS optimization strategies

## 🔧 Customization Ideas

### Easy
- Add more resume templates
- Custom color schemes
- Additional sections (Certifications, Publications)
- Different formatting styles

### Medium
- LinkedIn profile import
- Multiple resume versions
- Export to Google Docs
- Custom branding/themes

### Advanced
- Job posting scraper (automatic JD analysis)
- Resume scoring system
- A/B testing different versions
- Portfolio website integration
- Video resume script generator

## 💡 Features Breakdown

### Beginner Version
- ✅ Add work experience, education, skills
- ✅ Pre-built resume template
- ✅ Export to text format
- ✅ Save/load resume data

### Advanced Version (AI-Powered)
- ✨ **Transform experiences**: "I helped customers" → "Delivered exceptional customer service to 50+ daily clients, achieving 95% satisfaction rating"
- ✨ **Job-tailored bullets**: Paste job description, get customized resume bullets
- ✨ **Cover letter generation**: Auto-generate personalized cover letters
- ✨ **ATS keyword analysis**: Identify missing keywords from job posting
- ✨ **Resume critique**: Get AI feedback on your resume
- ✨ **Action verb suggestions**: Strengthen weak bullet points

## 📝 Tips for Success

### Resume Best Practices
- Use action verbs (Led, Developed, Increased, etc.)
- Quantify achievements (50% increase, $10K saved)
- Tailor to each job posting
- Keep to 1 page (students) or 2 pages (experienced)
- Use consistent formatting

### Cover Letter Tips
- Address specific job requirements
- Show enthusiasm for the role
- Connect your experience to their needs
- Keep to 3-4 paragraphs
- Proofread carefully

### ATS Optimization
- Use standard section headers
- Avoid tables, images, headers/footers
- Include relevant keywords from job description
- Use common file formats (PDF or .docx)
- Spell out acronyms first time

## 🎯 Example Use Cases

**Use Case 1: First Resume**
1. Add your education and any experience (clubs, projects, coursework)
2. Use AI to generate professional bullet points
3. Export and review

**Use Case 2: Internship Application**
1. Paste the job description
2. AI analyzes required skills
3. Get tailored resume bullets highlighting relevant experience
4. Generate customized cover letter
5. Export both documents

**Use Case 3: Multiple Applications**
1. Save your master resume
2. For each job, create a tailored version
3. Track which version was sent where

## 🐛 Troubleshooting

**PDF generation issues**: Install reportlab: `pip install reportlab`

**API errors**: Verify your `.env` file has valid API key

**Formatting problems**: Check that all required fields are filled

## 📚 Resources

- [Harvard Resume Guide](https://hwpi.harvard.edu/files/ocs/files/hes-resume-cover-letter-guide.pdf)
- [Action Verb List](https://www.themuse.com/advice/185-powerful-verbs-that-will-make-your-resume-awesome)
- [ATS Guide](https://www.jobscan.co/blog/ats-resume/)

---

**Build a resume that gets you interviews!**

Questions? Check the main repository README or visit [Anthropic's docs](https://docs.anthropic.com/).
