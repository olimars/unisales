# Django CRM Project

A comprehensive Customer Relationship Management (CRM) system built with Django and Django REST Framework.

## Features

- **Contact Management**
  - Store and manage customer information
  - Track interaction history
  - Contact segmentation
  - Import/Export capabilities

- **Sales Pipeline**
  - Opportunity tracking
  - Deal management
  - Sales forecasting
  - Activity logging

- **Marketing Automation**
  - Email campaign management
  - Automated workflows
  - Campaign analytics
  - Template management

- **Support Ticketing**
  - Ticket management
  - Knowledge base
  - SLA tracking
  - Support analytics

- **Reporting & Analytics**
  - Customizable dashboards
  - Report generation
  - Data visualization
  - Export capabilities

- **Integrations**
  - Third-party service connections
  - Webhook management
  - Data synchronization
  - API access

## Technical Stack

- **Backend**: Django 5.1, Django REST Framework 3.15
- **Database**: PostgreSQL (default)
- **Authentication**: JWT (JSON Web Tokens)
- **Task Queue**: Celery with Redis
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Testing**: pytest, factory-boy
- **Code Quality**: black, flake8, isort

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crm_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
crm_project/
├── core/                 # Core functionality and user management
├── contacts/            # Contact management
├── sales/              # Sales pipeline and opportunity management
├── marketing/          # Marketing campaigns and automation
├── support/            # Support tickets and knowledge base
├── reports/            # Reporting and analytics
├── integrations/       # Third-party integrations
└── crm_project/        # Project configuration
```

## API Documentation

The API documentation is available at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Check code quality:
```bash
black .
flake8
isort .
```

## Deployment

1. Set up production environment variables
2. Install production dependencies
3. Configure web server (e.g., Nginx)
4. Set up SSL certificates
5. Configure database
6. Set up task queue (Celery + Redis)
7. Configure static files serving
8. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the repository or contact the development team.

## Security

To report security vulnerabilities, please contact security@example.com.

## Acknowledgments

- Django and Django REST Framework communities
- All contributors to the project
- Open source packages used in this project