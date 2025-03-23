import random
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from lxpapiapp.models import (
    User, Subject, Chapter, Topic, Category, SubCategory, Course, CourseChapter,
    CourseType, Batch, BatchCourse, BatchTrainer, BatchLearner, McqQuestion, ShortQuestion,
    Exam, ExamQuestionDettails, McqResult
)
# How to Run
# py manage.py shell
# exec(open('createdemo.py').read())
# Helper function to create users
def create_users():
    user_roles = ["TRAINER", "LEARNER", "CTO", "CFO", "MENTOR", "STAFF"]
    users = []

    for i in range(10):
        user = User.objects.create_user(
            username=f"user{i}",
            first_name=f"First{i}",
            last_name=f"Last{i}",
            email=f"user{i}@example.com",
            password="password123",
            utype=random.choice(user_roles),
            mobile=f"98765432{i}",
            whatsappno=f"98765432{i}",
            profile_updated=True,
            status=True,
            regdate=timezone.now(),
            skills="Python, Django",
            bio=f"This is user {i}'s bio."
        )
        users.append(user)
    
    return users

# Create Subjects, Chapters, and Topics
def create_subjects_chapters_topics():
    subjects = []
    for i in range(5):
        subject = Subject.objects.create(
            subject_name=f"Subject {i}",
            youtube_id=f"YT{i}",
            is_active=True,
            is_youtube=bool(random.getrandbits(1))
        )
        subjects.append(subject)
    
    chapters = []
    topics = []
    for subject in subjects:
        for j in range(3):
            chapter = Chapter.objects.create(
                chapter_name=f"Chapter {j} of {subject.subject_name}",
                subject=subject,
                is_active=True,
                is_youtube=False
            )
            chapters.append(chapter)

            for k in range(2):
                topic = Topic.objects.create(
                    topic_name=f"Topic {k} of {chapter.chapter_name}",
                    subject=subject,
                    chapter=chapter
                )
                topics.append(topic)

    return subjects, chapters, topics

# Create Categories and Courses
def create_courses():
    categories = []
    subcategories = []
    courses = []

    for i in range(3):
        category = Category.objects.create(category_name=f"Category {i}")
        categories.append(category)

        for j in range(2):
            subcategory = SubCategory.objects.create(
                category=category,
                subcategory_name=f"SubCategory {j} of {category.category_name}"
            )
            subcategories.append(subcategory)

            for k in range(2):
                course = Course.objects.create(
                    category=category,
                    subcategory=subcategory,
                    course_name=f"Course {k} of {subcategory.subcategory_name}",
                    description="This is a test course.",
                    whatlearn="Learn Python and Django.",
                    includes="Video lectures, PDFs",
                    themecolor=random.choice(["1", "2", "3"]),
                    tags="Python, Django",
                    image="image_url",
                    banner="banner_url",
                    price=random.randint(100, 500)
                )
                courses.append(course)
    
    return categories, subcategories, courses

# Create Batches and Assign Trainers/Learners
def create_batches(users, courses):
    batches = []
    trainers = [u for u in users if u.utype == "TRAINER"]
    learners = [u for u in users if u.utype == "LEARNER"]

    for i in range(3):
        coursetype = CourseType.objects.create(coursetype_name=f"CourseType {i}")
        batch = Batch.objects.create(
            batch_name=f"Batch {i}",
            coursetype=coursetype,
            stdate=timezone.now().date(),
            enddate=timezone.now().date() + datetime.timedelta(days=60)
        )
        batches.append(batch)

        # Assign Courses to Batches
        for course in courses[:2]:  # Assign first two courses to each batch
            BatchCourse.objects.create(batch=batch, course=course)

        # Assign Trainers and Learners to Batches
        if trainers:
            BatchTrainer.objects.create(batch=batch, trainer=random.choice(trainers))

        for _ in range(2):  # Assign two learners per batch
            if learners:
                BatchLearner.objects.create(batch=batch, learner=random.choice(learners), fee=random.randint(200, 500))
    
    return batches

# Create Exams and Questions
def create_exams(batches):
    exams = []
    for batch in batches:
        exam = Exam.objects.create(
            batch=batch,
            exam_name=f"Exam for {batch.batch_name}",
            questiontpye=random.choice(["MCQ", "ShortAnswer"])
        )
        exams.append(exam)

        # Create MCQ Questions
        for i in range(5):
            mcq = McqQuestion.objects.create(
                question=f"MCQ Question {i}?",
                option1="Option A",
                option2="Option B",
                option3="Option C",
                option4="Option D",
                answer=random.choice(["1", "2", "3", "4"]),
                marks=random.randint(1, 5)
            )
            ExamQuestionDettails.objects.create(exam=exam, mcqquestion=mcq)

        # Create Short Questions
        for i in range(3):
            short_q = ShortQuestion.objects.create(
                question=f"Short Question {i}?",
                marks=random.randint(1, 5)
            )
            ExamQuestionDettails.objects.create(exam=exam, shortquestion=short_q)

    return exams

# Create Exam Results
def create_results(users, exams):
    learners = [u for u in users if u.utype == "LEARNER"]
    for learner in learners:
        for exam in exams:
            McqResult.objects.create(
                learner=learner,
                exam=exam
            )

# Run all functions to populate the database
users = create_users()
subjects, chapters, topics = create_subjects_chapters_topics()
categories, subcategories, courses = create_courses()
batches = create_batches(users, courses)
exams = create_exams(batches)
create_results(users, exams)

print("Database successfully populated with sample data.")
