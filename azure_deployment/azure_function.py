import azure.functions as func
import logging
import json
import urllib.request
import os

API_KEY = os.environ["API_KEY"]
app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="samples-workitems",
                               connection="buzzhirecvs_STORAGE") 
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name} "
                f"Blob Size: {myblob.length} bytes")
    cv_text = "# John Smith\\n## Software Engineer\\n### Contact\\n- Email: john.smith@example.com\\n- Phone: +1 (123) 456-7890\\n- LinkedIn: https://www.linkedin.com/in/john-smith\\n### Summary\\n- A passionate and skilled software engineer with 5 years of experience in developing web and mobile applications using various technologies and frameworks.\\n- Proficient in Java, Python, C#, JavaScript, HTML, CSS, React, Angular, Node.js, MongoDB, SQL, Firebase, AWS, Azure, Git, and Agile methodologies.\\n- Experienced in working on full-stack projects, from design and development to deployment and testing.\\n- A team player who can collaborate effectively with other developers, designers, testers, and clients.\\n- A lifelong learner who is always eager to explore new technologies and improve existing skills.\\n### Education\\n- Bachelor of Science in Computer Science, University of Toronto, 2018 - 2022\\n    - GPA: 3.8/4.0\\n    - Relevant courses: Data Structures and Algorithms, Software Engineering, Web Development, Mobile Development, Database Systems, Artificial Intelligence, Machine Learning, Cloud Computing, Security, and Ethics.\\n### Work Experience\\n- Software Engineer, ABC Inc., Toronto, ON, Jan 2023 - Present\\n    - Developed and maintained various web and mobile applications for clients in different domains, such as e-commerce, education, health, and entertainment.\\n    - Used Java, Python, C#, JavaScript, HTML, CSS, React, Angular, Node.js, MongoDB, SQL, Firebase, AWS, Azure, Git, and Agile methodologies.\\n    - Implemented features such as user authentication, payment integration, data visualization, chat functionality, push notifications, and geolocation services.\\n    - Ensured code quality, performance, security, and scalability by following best practices and standards.\\n    - Conducted code reviews, debugging, testing, and documentation.\\n    - Collaborated with other developers, designers, testers, and clients throughout the software development lifecycle.\\n- Software Engineer Intern, XYZ Ltd., Vancouver, BC, May 2021 - Aug 2021\\n    - Worked on a web application that allows users to create, share, and discover interactive quizzes and surveys.\\n    - Used JavaScript, HTML, CSS, React, Node.js, MongoDB, Firebase, Git, and Agile methodologies.\\n    - Designed and developed the front-end and back-end of the application using React and Node.js.\\n    - Integrated Firebase for user authentication, database, storage, and hosting.\\n    - Added features such as quiz creation, quiz taking, quiz sharing, quiz analytics, and feedback collection.\\n    - Tested and deployed the application using Firebase Hosting and GitHub Pages.\\n    - Received positive feedback from the supervisor and the users for the functionality and usability of the application.\\n### Projects\\n- Todo App: A web application that allows users to create and manage their personal tasks and goals.\\n    - Used JavaScript, HTML, CSS, React, Node.js, MongoDB, and Git.\\n    - Implemented features such as task creation, task editing, task deletion, task filtering, task sorting, task prioritization, and task completion.\\n    - Applied the CRUD (Create, Read, Update, Delete) operations using Node.js and MongoDB.\\n    - Hosted the application on Heroku and GitHub Pages.\\n- Chat App: A mobile application that allows users to communicate with each other in real-time using text, voice, and video messages.\\n    - Used Java, Android Studio, Firebase, and Git.\\n    - Implemented features such as user registration, user login, user profile, contact list, chat list, chat room, text messaging, voice messaging, video messaging, and push notifications.\\n    - Integrated Firebase for user authentication, database, storage, and messaging.\\n    - Used the Firebase Cloud Messaging (FCM) service to send and receive push notifications.\\n    - Used the WebRTC (Web Real-Time Communication) technology to enable voice and video communication.\\n### Skills\\n- Programming Languages: Java, Python, C#, JavaScript, HTML, CSS\\n- Frameworks and Libraries: React, Angular, Node.js, MongoDB, SQL, Firebase, AWS, Azure\\n- Tools and Platforms: Git, Android Studio, Visual Studio Code, Heroku, GitHub Pages\\n- Methodologies and Concepts: Agile, Scrum, Object-Oriented Programming, Data Structures and Algorithms, Software Engineering, Web Development, Mobile Development, Database Systems, Artificial Intelligence, Machine Learning, Cloud Computing, Security, and Ethics.\\n### Awards and Achievements\\n- Dean's List, University of Toronto, 2018 - 2022\\n- First Place, Hackathon XYZ, 2021\\n- Second Place, Coding Challenge ABC, 2020\\n- Certificate of Completion, Coursera Course on Machine Learning, 2019\\n### Interests and Hobbies\\n- Reading, writing, blogging, podcasting, gaming, traveling, hiking, biking, swimming, and volunteering.\\n"
    url = "https://buzzhire.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-07-01-preview&api-key={API_KEY}"
    data = {
      "messages": [
        {
          "role": "system",
          "content": "You are an AI HR that creates a valid json with the following attributes in brief- name, email, contact_number, linkedin_profile, all_skills(all the skills should be in 1 list. no subattributes), education(degree, university, start_year, end_year, gpa), roles(title, company, location, start_date, end_date, responsibilities). Strictly stick to the given attributes and sub-attributes only. If information is absent, say NA."
        },
        {
          "role": "user",
          "content": cv_text
        }
      ],
      "temperature": 0.5,
      "top_p": 0.95,
      "frequency_penalty": 0,
      "presence_penalty": 0,
      "max_tokens": 4000
    }
    data = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST", headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)

    # Process the response
    response = response.read().decode("utf-8")
    result = json.loads(response)

    result = json.loads(result['choices'][0]['message']['content'].replace("\n", ""))
    logging.info(str(result))
