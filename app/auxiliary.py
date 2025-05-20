import random
import string
from datetime import datetime, timedelta, timezone

nomes = [
    "Ana Clara", "Bruno", "Camila", "Diego", "Eduarda",
    "Felipe", "Gabriela", "Heitor", "Isabela", "João Pedro",
    "Kauã", "Larissa", "Matheus", "Natália", "Otávio",
    "Paula", "Quésia", "Rafael", "Sabrina", "Tiago"
]

sobrenomes = [
    "Silva", "Santos", "Oliveira", "Souza", "Pereira",
    "Lima", "Carvalho", "Costa", "Almeida", "Ferreira",
    "Rodrigues", "Martins", "Gomes", "Barbosa", "Ribeiro",
    "Araújo", "Dias", "Cavalcante", "Moura", "Teixeira",
    "Monteiro", "Correia", "Rocha", "Nascimento", "Freitas",
    "Andrade", "Batista", "Vieira", "Medeiros", "Fonseca"
]

def generate_random_name():
    return random.choice(nomes)

def generate_random_last_name():
    return random.choice(sobrenomes)

def generate_random_birthdate():
    # Gera uma data entre 18 e 65 anos atrás
    today = datetime.today()
    min_age = 18
    max_age = 65
    start_date = today - timedelta(days=365 * max_age)
    end_date = today - timedelta(days=365 * min_age)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d 00:00:00")

def generate_random_phone_number():
    ddd = random.choice(["11", "21", "31", "41", "51", "61", "71", "81", "91"])
    prefix = random.randint(90000, 99999)
    suffix = random.randint(1000, 9999)
    return f"({ddd}) {prefix}-{suffix}"

def generate_random_email():
    user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(3, 6)))
    domain = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))
    tld = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 3)))
    return f"{user}@{domain}.{tld}"

def generate_random_cpf():
    def generate_digit(numbers):
        s = sum([v * (len(numbers) + 1 - i) for i, v in enumerate(numbers)])
        d = 11 - s % 11
        return d if d < 10 else 0

    numbers = [random.randint(0, 9) for _ in range(9)]
    numbers.append(generate_digit(numbers))
    numbers.append(generate_digit(numbers))
    cpf = ''.join(map(str, numbers))
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def generate_random_training_since():
    today = datetime.now(timezone.utc)
    past = today - timedelta(days=random.randint(30, 365 * 10))
    return past.isoformat()

def generate_random_bio_gender():
    return random.choice(["M", "F"])  # Male, Female, Other

def generate_random_availability():
    return {
        "sunday": random.choice([True, False]),
        "monday": random.choice([True, False]),
        "tuesday": random.choice([True, False]),
        "wednesday": random.choice([True, False]),
        "thursday": random.choice([True, False]),
        "friday": random.choice([True, False]),
        "saturday": random.choice([True, False])
    }

def generate_random_conditions():
    return {
        "diabetes": random.choice([True, False]),
        "hyper_tension": random.choice([True, False]),
        "cardiovascular_disease": random.choice([True, False]),
        "obesity": random.choice([True, False]),
        "asthma": random.choice([True, False]),
        "arthritis": random.choice([True, False]),
        "osteoporosis": random.choice([True, False]),
        "chronic_back_pain": random.choice([True, False]),
        "damaged_left_upper_body": random.choice([True, False]),
        "damaged_right_upper_body": random.choice([True, False]),
        "damaged_left_lower_body": random.choice([True, False]),
        "damaged_right_lower_body": random.choice([True, False]),
        "damaged_body_core": random.choice([True, False]),
        "recent_surgery": random.choice([True, False]),
        "pregnancy": random.choice([True, False])
    }

def generate_random_payload():
    first_name = generate_random_name()
    last_name = generate_random_last_name()
    last_name2 = generate_random_last_name()
    return {
        "first_name": first_name,
        "last_name": last_name + " " + last_name2,
        "username": first_name + last_name2,
        "cpf": generate_random_cpf(),
        "birth_date": generate_random_birthdate(),
        "email": generate_random_email(),
        "phone_number": generate_random_phone_number(),
        "password": "debug",
        "personal_info": {
            "weight_kg": random.randint(45, 130),
            "height_cm": random.randint(140, 210),
            "bio_gender": generate_random_bio_gender(),
            "training_since": generate_random_training_since()
        },
        "training_availability": generate_random_availability(),
        "condition": generate_random_conditions(),
        "available_time": f"{random.choice([30, 45, 60, 90, 120, 150, 165, 180])}min"
    }