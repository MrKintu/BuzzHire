🐝 # BuzzHire

BuzzHire is an AI-powered hiring portal built with Django and PostgreSQL. It automates PDF resume parsing, MBTI-style personality quizzes, and applicant–job matching using machine learning (Random Forest). Recruiting has never been sweeter! 🍯

⸻

🚀 Features
	•	Resume Parsing: Extracts structured data (skills, education, contact info) from uploaded PDFs using NLP.
	•	MBTI Quiz + Prediction: Applicants take a quiz; a trained Random Forest classifier predicts their Myers–Briggs Type Indicator.
	•	Job & Personality Matching: Matches applicants to job postings based on parsed resume insights and MBTI compatibility.
	•	Personality Visualization: Generates radar/bar charts of MBTI traits via Matplotlib.
	•	User Roles: Supports recruiters (post jobs) and applicants (submit resumes + take quizzes).
	•	Dockerized Deployment: Includes Dockerfile and docker-compose for easy setup.

⸻

🧩 Architecture Overview
	1.	Frontend
Django templates deliver clean, responsive UI for job applicants and recruiters.
	2.	Backend
	•	Resume App: Handles PDF uploads and NLP-based parsing.
	•	Quiz App: Manages MBTI quiz questions.
	•	Random Forest Model: Lives in app/quiz/RandomForest/predictModel.py; predicts personality type.
	•	Personality Charts: Generated via plotGraph.py and saved to /media/personalities/.
	3.	Data Storage
PostgreSQL database for users, resumes, quiz answers, and job postings.
	4.	Deployment
Docker containers run Django, Postgres, and other services.

⸻

🧠 ML Model Details
	•	Uses scikit-learn RandomForestClassifier.
	•	Trained on MBTI-labeled personality quiz data.
	•	Model file and label encoder saved as random_forest.pkl.
	•	When an applicant completes the quiz, predictions are generated on the fly.
	•	Personality trait charts improve visibility and recruiter insight.

⸻

🏗️ Getting Started

Requirements
	•	Docker & Docker Compose
	•	Python 3.10+ (for local dev)

Quick Start (via Docker)
	1.	git clone https://github.com/MrKintu/BuzzHire.git
	2.	cd BuzzHire
	3.	docker-compose up --build

	•	Backend available at http://localhost:8000/
	•	Auth with /app/users/
	•	Upload resumes at /app/resume/
	•	Quiz: /app/quiz/
	•	Generated personality visuals in /app/media/personalities/

Local Dev (No Docker)
	1.	python -m venv venv
	2.	source venv/bin/activate
	3.	pip install -r requirements.txt
	4.	python manage.py migrate
	5.	python manage.py runserver

⸻

🔧 Configuration & Settings
	•	Resume storage path: MEDIA_ROOT/personalities/
	•	ML model location: configured in predictModel.py
	•	Adjust in settings.py for production/local setups (avoid hard-coded paths)

⸻

🏆 Highlights & Future Enhancements

Pros
	•	Automates recruiter workflows via resume parsing and MBTI-based matching.
	•	Strong modular design—each app handles discrete responsibilities.
	•	Personality prediction enhances candidate insights dramatically.

To Do
	•	Path Config: Refactor absolute media paths to use Django settings.
	•	Asynchrony: Use Celery to parse uploads and generate MBTI charts.
	•	Model Updates: Integrate dynamic retraining or a lighter ML model.
	•	Bias Mitigation: Consider gender-neutral parsing for resumes.
	•	UI Improvements: More interactive quiz and recruiter panels.

⸻

🤝 Contribute & Deploy

Contributions welcome! Here’s how to get involved:
	1.	Fork the repo
	2.	Create a feature branch: git checkout -b feature/your-feature
	3.	Make your changes & commit with clear messages
	4.	Push your branch and open a pull request

Deploying
	•	Recommended using Heroku, AWS ECS/EKS, or Azure Web Apps.
	•	Update settings.py for production (DEBUG=false, ALLOWED_HOSTS).
	•	Use Postgres in production, set secure SECRET_KEY, and configure SSL.

⸻

📚 References
	•	Résumé parsing accuracy & utility
	•	Bias mitigation in resumes via gender-neutral approaches
	•	MBTI prediction via tree-based models

⸻

🧁 License

Licensed under Apache License 2.0. See the LICENSE file for details.

⸻

🤝 Contact

For questions or support, open an issue or reach out to the maintainers. Let’s make hiring smarter—and sweeter!