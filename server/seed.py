from app import app
from config import db
from models import (
    Task,
    User,
)


with app.app_context():
    print("Deleting records...")
    Task.query.delete()
    User.query.delete()

    print("Creating users...")
    aneesh = User(username='aneesh')
    aneesh.password_hash = 'password123'

    sam = User(username='sam')
    sam.password_hash = 'password123'

    maya = User(username='maya')
    maya.password_hash = 'password123'

    users = [aneesh, sam, maya]

    db.session.add_all(users)
    db.session.commit()

    print("Creating tasks...")
    tasks = [
        Task(
            title='Plan weekly study schedule',
            description='Block time for Flask review, project work, and interview practice.',
            priority='high',
            status='in progress',
            due_date='2026-05-22',
            user_id=aneesh.id
        ),
        Task(
            title='Finish backend auth routes',
            description='Verify signup, login, check session, and logout with Postman.',
            priority='high',
            status='not started',
            due_date='2026-05-24',
            user_id=aneesh.id
        ),
        Task(
            title='Draft project README',
            description='Document setup, migrations, seed instructions, and API endpoints.',
            priority='medium',
            status='not started',
            due_date='2026-05-26',
            user_id=aneesh.id
        ),
        Task(
            title='Review pagination behavior',
            description='Confirm page and per_page query parameters return the expected task subset.',
            priority='medium',
            status='complete',
            due_date='2026-05-18',
            user_id=sam.id
        ),
        Task(
            title='Organize task backlog',
            description='Group open work by priority and move completed items out of active view.',
            priority='low',
            status='in progress',
            due_date='2026-05-28',
            user_id=sam.id
        ),
        Task(
            title='Prepare demo checklist',
            description='List the key API flows to test before submitting the final project.',
            priority='medium',
            status='not started',
            due_date='2026-05-30',
            user_id=maya.id
        ),
    ]

    db.session.add_all(tasks)
    db.session.commit()

    print("Seeding complete.")
    print("Demo users all use password: password123")