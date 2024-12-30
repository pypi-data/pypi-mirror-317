from rich import print as rprint
import questionary

def generate_docker():
    # Get user preferences for additional services
    additional_services = questionary.checkbox(
        'Select additional services to include:',
        choices=[
            questionary.Separator('╔═════════════════════════════════╗'),
            questionary.Separator('║ Database                        ║'),
            questionary.Separator('╚═════════════════════════════════╝'),
            'Postgres',
            questionary.Separator('╔═════════════════════════════════╗'),
            questionary.Separator('║ Message Brokers and Cache       ║'),
            questionary.Separator('╚═════════════════════════════════╝'),
            'Redis',
            'Kafka',
            'RabbitMQ',
            questionary.Separator('╔═════════════════════════════════╗'),
            questionary.Separator('║ Logs and Monitoring             ║'),
            questionary.Separator('╚═════════════════════════════════╝'),
            'Sentry',
        ],
        style=questionary.Style([
            ('separator', 'fg:#6c5ce7'),
            ('selected', 'fg:#2d3436 bg:#a3e4d7'),
        ])
    ).ask()

    # Base Dockerfile and services
    dockerfile_content = '''FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    compose_services = {
        'app': '''  app:
    build: .
    ports:
      - "8000:8000"
    environment:
        - ENVIRONMENT=development
        # Set environment variables here
    networks:
      - app-network''',

        'postgres': '''  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=postgres_db
      - POSTGRES_USER=postgres_user
      - POSTGRES_PASSWORD=postgres_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network''',

        'redis': '''  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    networks:
      - app-network''',

        'sentry': '''  sentry:
    image: getsentry/sentry:latest
    depends_on:
      - redis
      - postgres
    ports:
      - "9000:9000"
    environment:
      - SENTRY_SECRET_KEY=replace_with_random_key
    networks:
      - app-network''',

        'kafka': '''  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - app-network

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    networks:
      - app-network''',

        'rabbitmq': '''  rabbitmq:
    image: rabbitmq:management
    ports:
      - "5672:5672"
      - "15672:15672"
    networks:
      - app-network'''
    }

    # Build docker-compose content
    compose_content = 'version: \'3.8\'\nservices:\n'
    compose_content += compose_services['app']
    volumes_section = ""

    # Add selected additional services
    if 'Postgres' in additional_services:
        compose_content += '\n' + compose_services['postgres']
        volumes_section += "  postgres_data:\n    driver: local\n"
        rprint("[blue]✨ Added Postgres service[/blue]")

    if 'Redis' in additional_services:
        compose_content += '\n' + compose_services['redis']
        volumes_section += "  redis_data:\n    driver: local\n"
        rprint("[blue]✨ Added Redis service[/blue]")

    if 'Kafka' in additional_services:
        compose_content += '\n' + compose_services['kafka']
        volumes_section += "  kafka_data:\n    driver: local\n  zookeeper_data:\n    driver: local\n  zookeeper_log:\n    driver: local\n"
        rprint("[blue]✨ Added Kafka service with Zookeeper[/blue]")

    if 'RabbitMQ' in additional_services:
        compose_content += '\n' + compose_services['rabbitmq']
        volumes_section += "  rabbitmq_data:\n    driver: local\n"
        rprint("[blue]✨ Added RabbitMQ service[/blue]")

    if 'Sentry' in additional_services:
        compose_content += '\n' + compose_services['sentry']
        rprint("[blue]✨ Added Sentry service[/blue]")

    # Add volumes and networks
    compose_content += f'''
volumes:
{volumes_section if volumes_section else ''}
networks:
  app-network:
    driver: bridge
'''

    dockerignore_content = '''__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
*.sqlite3
.git
.gitignore
'''

    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)
    with open('.dockerignore', 'w') as f:
        f.write(dockerignore_content)

    rprint("[bold green]✅ Docker files generated successfully![/bold green]")
    rprint("[blue]Generated files:[/blue]")
    rprint("  - Dockerfile")
    rprint("  - docker-compose.yml")
    rprint("  - .dockerignore")