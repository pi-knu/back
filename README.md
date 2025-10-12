# 🚀 Guide for newcomer:

## 📚 Table of Contents

1. 🏃 **Run**
    - **Unix** — [Go to section](#-for-unix-systems)
        - **Dev**
            - [Script](#-development-mode)
            - [Manual](#-development)
        - **Prod**
            - [Script](#-production-mode)
            - [Manual](#-production)
2. 📖 **See Documentation**
    - [API](#api-documentation)

---

## 🐧 For Unix Systems

### 🔧 Development Mode

```bash
cd ./docker
chmod +x ./run-dev.sh
./run-dev.sh
```

### 🏗️ Production Mode

```bash
cd ./docker
chmod +x ./run-prod.sh
./run-prod.sh
```

---

## ⚙️ Manual Run (Alternative Way)

### 🧩 Development

> **Note:** Make sure to add SMTP credentials to `notification/.env`

#### 1. Copy environment files:

```bash
cp ../postgres/example.env ../postgres/.env
cp ../auth/example.env ../auth/.env
cp ../notification/example.env ../notification/.env
cp ../docs/example.env ../docs/.env
```

#### 2. Start containers:

```bash
docker compose -f docker-compose.dev.yml up -d
```

---

### 🚢 Production

> **Note:** Make sure to add SMTP credentials to `notification/.env`

#### 1. Copy environment files:

```bash
cp ../postgres/example.env ../postgres/.env
cp ../auth/example.env ../auth/.env
cp ../notification/example.env ../notification/.env
cp ../docs/example.env ../docs/.env
```

#### 2. Build Docker images:

```bash
docker build -t pi-knu-auth:latest ../auth/auth
docker build -t pi-knu-migration:latest ../migration_module
docker build -t pi-knu-notification:latest ../notification
```

#### 3. Deploy containers:

```bash
docker compose -f docker-compose.prod.yml up -d
```

---

## Documentation
### Api Documentation
For see swagger docs you need work with dir: [docs](docs)

**How to run**:

You need up in [docker-compose.dev.yml](docker/docker-compose.dev.yml) services: `nginx`, `docs`

And in browser view: http://locahost/docs

**OR**

You can view swagger yaml docs in this [**dir**](docs/docs)
