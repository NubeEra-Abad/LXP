from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command
from lxpapiapp.models import *
class Command(BaseCommand):
    help = 'Create a superuser and a teacher with predefined credentials'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Running makemigrations...'))
        call_command('makemigrations')

        self.stdout.write(self.style.NOTICE('Running migrate...'))
        call_command('migrate')
        
        User = get_user_model()

        # Creating the superuser
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'  # Change this to your desired password

        self.stdout.write(self.style.WARNING(f'Creating Admin'))

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        
        self.stdout.write(self.style.NOTICE('Create subjects, chapters, and topics...'))
         # Define category, subcategory, and course details
        categories_info = {
            'Linux': {
                'subcategory': 'Linux Administration',
                'course': {
                    'course_name': 'Mastering Linux Administration',
                    'description': 'In-depth course on Linux administration, including system management, security, and networking.',
                    'whatlearn': 'Learn advanced Linux commands, system administration techniques, and network management.',
                    'includes': 'System management, security, user management, disk management, networking basics.',
                    'tags': 'Linux, Administration, Advanced, Networking, Security',
                    'price': 299,
                    'image': 'linux_image_url',
                    'banner': 'linux_banner_url'
                }
            },
            'Python': {
                'subcategory': 'Python Programming',
                'course': {
                    'course_name': 'Intermediate Python Programming',
                    'description': 'An intermediate course on Python programming, covering advanced topics and libraries.',
                    'whatlearn': 'Master Python programming, including libraries like NumPy, Pandas, and Matplotlib.',
                    'includes': 'Advanced functions, object-oriented programming, libraries, and debugging techniques.',
                    'tags': 'Python, Programming, Intermediate, OOP, Libraries',
                    'price': 199,
                    'image': 'python_image_url',
                    'banner': 'python_banner_url'
                }
            },
            'Networking': {
                'subcategory': 'Network Administration',
                'course': {
                    'course_name': 'Advanced Networking Concepts',
                    'description': 'An advanced course on networking, covering routing, IP addressing, and network security.',
                    'whatlearn': 'Learn advanced network routing protocols, IP subnetting, and network security.',
                    'includes': 'Routing protocols, IP subnetting, network security strategies, troubleshooting.',
                    'tags': 'Networking, Routing, Security, Advanced, IP Addressing',
                    'price': 249,
                    'image': 'networking_image_url',
                    'banner': 'networking_banner_url'
                }
            },
            'Databases': {
                'subcategory': 'Database Management',
                'course': {
                    'course_name': 'Intermediate SQL and Database Management',
                    'description': 'Learn intermediate database concepts, focusing on SQL queries, design, and administration.',
                    'whatlearn': 'Master SQL queries, database design, normalization, and administration techniques.',
                    'includes': 'SQL queries, normalization, relational database design, database optimization.',
                    'tags': 'SQL, Database, Administration, Intermediate, Design',
                    'price': 179,
                    'image': 'databases_image_url',
                    'banner': 'databases_banner_url'
                }
            },
            'Cloud Computing': {
                'subcategory': 'Cloud Basics',
                'course': {
                    'course_name': 'Introduction to Cloud Computing',
                    'description': 'A beginner-friendly course on cloud computing, covering the basics of cloud models and services.',
                    'whatlearn': 'Understand the basics of cloud computing, including services and deployment models.',
                    'includes': 'Cloud deployment models, types of cloud services, and popular cloud providers.',
                    'tags': 'Cloud Computing, Basics, AWS, Google Cloud, Azure',
                    'price': 129,
                    'image': 'cloud_image_url',
                    'banner': 'cloud_banner_url'
                }
            }
        }
        subjects_info = {
            'Linux': {
                'chapters': [
                    {'name': 'Introduction to Linux', 'topics': ['What is Linux?', 'History of Linux', 'Linux Distributions', 'Linux Installation', 'Linux Shell Basics']},
                    {'name': 'Linux File System', 'topics': ['File System Hierarchy', 'File Permissions', 'File Types', 'File Management Commands', 'Disk Management']},
                    {'name': 'Linux Commands', 'topics': ['ls', 'cd', 'mkdir', 'rm', 'chmod']},
                    {'name': 'Linux Process Management', 'topics': ['ps', 'top', 'kill', 'jobs', 'bg/fg']},
                    {'name': 'Linux Networking', 'topics': ['ping', 'ifconfig', 'netstat', 'ssh', 'scp']}
                ]
            },
            'Python': {
                'chapters': [
                    {'name': 'Introduction to Python', 'topics': ['What is Python?', 'Python Installation', 'Python Syntax', 'Variables and Data Types', 'Basic Operators']},
                    {'name': 'Control Flow', 'topics': ['If-Else Statements', 'For Loops', 'While Loops', 'Break and Continue', 'Pass Statement']},
                    {'name': 'Functions in Python', 'topics': ['Defining Functions', 'Arguments and Return Values', 'Lambda Functions', 'Recursion', 'Modules']},
                    {'name': 'Object-Oriented Programming', 'topics': ['Classes and Objects', 'Inheritance', 'Polymorphism', 'Encapsulation', 'Abstraction']},
                    {'name': 'Python Libraries', 'topics': ['NumPy', 'Pandas', 'Matplotlib', 'Requests', 'BeautifulSoup']}
                ]
            },
            'Networking': {
                'chapters': [
                    {'name': 'Networking Basics', 'topics': ['What is Networking?', 'Types of Networks', 'OSI Model', 'TCP/IP Model', 'IP Addressing']},
                    {'name': 'Network Devices', 'topics': ['Router', 'Switch', 'Hub', 'Modem', 'Access Point']},
                    {'name': 'IP Addressing and Subnetting', 'topics': ['IPv4', 'IPv6', 'Subnet Masks', 'CIDR Notation', 'Subnetting Methods']},
                    {'name': 'Routing Protocols', 'topics': ['RIP', 'OSPF', 'BGP', 'Static Routing', 'Dynamic Routing']},
                    {'name': 'Network Security', 'topics': ['Firewalls', 'VPN', 'Encryption', 'Authentication', 'Intrusion Detection Systems']}
                ]
            },
            'Databases': {
                'chapters': [
                    {'name': 'Database Basics', 'topics': ['What is a Database?', 'Relational Databases', 'SQL Basics', 'Normalization', 'Database Models']},
                    {'name': 'SQL Queries', 'topics': ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'JOIN']},
                    {'name': 'Database Design', 'topics': ['Entity-Relationship Model', 'Primary Keys', 'Foreign Keys', 'Normalization', 'Indexes']},
                    {'name': 'Database Administration', 'topics': ['Backup and Recovery', 'User Management', 'Transactions', 'Database Security', 'Performance Tuning']},
                    {'name': 'NoSQL Databases', 'topics': ['What is NoSQL?', 'Types of NoSQL Databases', 'MongoDB', 'Cassandra', 'Redis']}
                ]
            },
            'Cloud Computing': {
                'chapters': [
                    {'name': 'Introduction to Cloud Computing', 'topics': ['What is Cloud Computing?', 'Cloud Models', 'Cloud Service Providers', 'Benefits of Cloud Computing', 'Cloud Deployment Models']},
                    {'name': 'Cloud Storage', 'topics': ['What is Cloud Storage?', 'Storage Types', 'Google Drive', 'AWS S3', 'Security in Cloud Storage']},
                    {'name': 'Cloud Security', 'topics': ['Encryption', 'Access Control', 'Identity Management', 'Compliance', 'Data Breaches']},
                    {'name': 'Cloud Networking', 'topics': ['Virtual Networks', 'Load Balancing', 'CDN', 'DNS in Cloud', 'Network Security']},
                    {'name': 'Cloud Platforms and Tools', 'topics': ['AWS', 'Google Cloud Platform', 'Azure', 'Kubernetes', 'Docker']}
                ]
            }
        }

        # Create subjects, chapters, topics, and course chapters
        for subject_name, subject_data in subjects_info.items():
            # Create the subject
            subject = Subject.objects.create(subject_name=subject_name)
            subject.save()

            # Create chapters for each subject
            for chapter_data in subject_data['chapters']:
                chapter = Chapter.objects.create(chapter_name=chapter_data['name'], subject_id=subject.id)
                chapter.save()

                # Create topics for each chapter
                for topic_name in chapter_data['topics']:
                    topic = Topic.objects.create(topic_name=topic_name, chapter_id=chapter.id)
                    topic.save()

        # Create categories, subcategories, and courses with multiple chapters
        for category_name, category_data in categories_info.items():
            # Step 1: Create the category
            category, created = Category.objects.get_or_create(category_name=category_name)
            
            # Step 2: Create the subcategory
            subcategory, created = SubCategory.objects.get_or_create(
                subcategory_name=category_data['subcategory'],
                category=category
            )
            
            # Step 3: Create the course
            course_data = category_data['course']
            
            course = Course.objects.create(
                category=category,
                subcategory=subcategory,
                course_name=course_data['course_name'],
                description=course_data['description'],
                whatlearn=course_data['whatlearn'],
                includes=course_data['includes'],
                tags=course_data['tags'],
                image=course_data['image'],
                banner=course_data['banner'],
                price=course_data['price'],
                themecolor='Green'  # You can adjust the theme color as needed
            )
            course.save()

            # Step 4: Create CourseChapter entries for each combination of subject and chapter
            for subject_name, subject_data in subjects_info.items():
                # For each subject, create CourseChapter entries for its chapters
                if category_name == subject_name:  # Match the course to the subject
                    for chapter_data in subject_data['chapters']:
                        chapter = Chapter.objects.get(chapter_name=chapter_data['name'], subject__subject_name=subject_name)
                        
                        # Create a CourseChapter entry for each subject-chapter combination
                        CourseChapter.objects.create(course=course, subject_id=subject.id, chapter=chapter)
                        self.stdout.write(self.style.SUCCESS(f"Created CourseChapter for {course.course_name} -> {chapter.chapter_name}"))

        self.stdout.write(self.style.SUCCESS('Categories, subcategories, courses, and course chapters created successfully!'))


        
        