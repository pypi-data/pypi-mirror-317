# Release Information

## Latest Release (v0.1.0)

This is the initial release of the Dell Unisphere Mock API, a FastAPI-based implementation for testing and development purposes.

### Installation

```bash
pip install dell-unisphere-mock-api
```

For development:
```bash
pip install "dell-unisphere-mock-api[test,dev]"
```

### Quick Start

```python
from dell_unisphere_mock_api import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### System Requirements

- Python 3.12 or higher
- FastAPI 0.104.1 or higher
- Pydantic 2.5.2 or higher
- See requirements.txt for full dependencies

### Configuration

The API server can be configured through environment variables:
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `DEBUG`: Enable debug mode (default: False)

### Known Limitations

1. API Coverage
   - Limited subset of Dell EMC Unisphere API endpoints
   - Focus on core storage management features

2. Authentication
   - Basic authentication with CSRF tokens
   - Simplified for testing purposes

3. Data Persistence
   - In-memory storage only
   - Data reset on server restart

### Security Considerations

1. This is a mock API intended for testing and development
2. Do not use default credentials in production
3. CSRF protection is implemented but simplified
4. No SSL/TLS configuration included

### Future Development

Planned features for upcoming releases:
1. Extended API coverage
2. Persistent storage options
3. Enhanced authentication
4. Dynamic mock data generation
5. WebSocket support
6. Docker containerization

### Support

- GitHub Issues: [Report a bug](https://github.com/nirabo/dell-unisphere-mock-api/issues)
- Documentation: Available at http://localhost:8000/docs when running
- Contributing: See CONTRIBUTING.md

### License

MIT License - See LICENSE file for details
