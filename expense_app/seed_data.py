# seed_data.py
from django_seed import Seed
from django.contrib.auth import get_user_model
from expense_app.models import Reimbursement


seeder = Seed.seeder()

def seed_reimbursements():
    users = get_user_model().objects.all()

    seeder.add_entity(Reimbursement, 10, {
        'user': lambda x: seeder.choice(users),
        'amount': seeder.faker.pydecimal(left_digits=5, right_digits=2, positive=True),
        'description': seeder.faker.text(),
        'date_requested': seeder.faker.date_this_decade(),
        'is_approved': seeder.faker.boolean(chance_of_getting_true=50),
        'image_data': seeder.faker.text(max_nb_chars=100, ext_word_list=None),
    })

seed_reimbursements()
