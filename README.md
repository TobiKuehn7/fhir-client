# fhir‑client

> A lightweight, opinionated Python client for working with FHIR servers via the REST API.

[![PyPI version](https://badge.fury.io/py/fhir-client.svg)](https://pypi.org/project/fhir-server-client/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/numpy.svg?label=PyPI%20downloads)](https://pypi.org/project/fhir-server-client/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/TobiKuehn7/fhir-client/actions/workflows/python-package.yml/badge.svg)](https://github.com/TobiKuehn7/fhir-client/actions/workflows/python-package.yml)

---

## 📚 Table of Contents
- [What is fhir‑client?](#-what-is-fhir-client)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Getting Started](#-getting-started)
- [Examples](#-examples)
  - [Basic CRUD](#basic-crud)
  - [Search & Filtering](#search--filtering)
  - [Authentication](#authentication)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🔍 What is fhir‑client?

`fhir-client` is a minimal wrapper around the [FHIR REST API](https://www.hl7.org/fhir/).  
It handles:

- **Standard CRUD operations** (`GET`, `POST`, `PUT`, `DELETE`)
- **Automatic JSON serialization/deserialization**
- **Optional authentication** (Basic Auth, OAuth2)

Designed for developers who want to get started quickly without the overhead of a full‑blown SDK.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Simple API** | `FHIRClient` exposes high‑level methods that map directly to FHIR operations. |
| **Configurable** | Base URL and authentication can be set globally or per request. |

---

## 📦 Installation

```bash
# From PyPI
pip install fhir-server-client
```

> **Developed and tested on Python 3.12**

---

## 🚀 Getting Started

```python
from fhir_client.client import FhirClient

# Create a client pointing at the HAPI FHIR demo server
client = FhirClient(base_url="https://hapi.fhir.org/baseR4")

# Perform a GET request for a Patient
patient = client.get("Patient", _id=123)
print(patient)

# Or use the generic GET method
patients = client.get("/Patient")
print(patients)
```

---

## 📚 Examples

Below are a few common use cases. Feel free to copy‑paste and adapt.

### 📦 Basic CRUD

```python
# CREATE a new Patient
new_patient = {
    "resourceType": "Patient",
    "name": [{"family": "Doe", "given": ["John"]}],
    "gender": "male",
    "birthDate": "1974-12-25"
}
created = client.post("Patient", data=new_patient)
print("Created patient ID:", created["id"])

# READ the newly created Patient
patient = client.get("Patient", _id=created["id"])
print(patient)

# UPDATE the Patient
patient["name"][0]["given"] = ["Jonathan"]
updated = client.put("Patient", id=created["id"], data=patient)
print("Updated patient:", updated)

# DELETE the Patient
client.delete(resource_type="Patient", _id=patient["id"])
print("Patient deleted.")
```

### 🔍 Search & Filtering

```python
# Search for patients named "John" with a minimum age of 18
results = client.get("Patient", name="John", birthdate="ge1975-01-01")

for patient in results["entry"]:
    print(patient["resource"]["id"], patient["resource"]["name"][0]["given"])

# Checking for and getting self, next and previous links
if client.has_self():
    self_link = client.self

if client.has_next():
    next_link = client.next

if client.has_previous():
    previous_link = client.previous
```

> The `get` method accepts search parameters as python keyword arguments. Those are appended in the FHIR Search Query

### 🔐 Authentication

```python
# Using Basic Auth
from fhir_client.auth import FhirAuth

auth = FhirAuth().set_basic_auth("username", "password")
client = FHIRClient("https://fhir.example.com", auth=auth)

# Using OAuth2 (client credentials flow)
from fhir_client.auth import FhirAuth

auth = FhirAuth().set_o_auth(
    auth_url="https://auth.example.com/token",
    client_id="client-id",
    client_secret="client-secret"
)
client = FHIRClient(base_url="https://fhir.example.com", auth=auth)
```

---

## 🤝 Contributing (WORK IN PROGRESS)

We love contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on coding style, testing, and pull requests.

### Steps to get started

1. Fork the repo and clone it locally.
2. Create a new branch (`git checkout -b feature/foo`).
3. Write tests for your change.
4. Run the test suite (`pytest`).
5. Submit a pull request.

---

## 📄 License

MIT © 2026 <Your Name>

See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [HL7 FHIR](https://www.hl7.org/fhir/)
- [HAPI FHIR](https://hapifhir.io/)
- Contributors who opened issues and pull requests

--- 

Happy coding! 🎉

