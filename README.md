# 🌍 AI-Powered Travel Itinerary Optimization

An intelligent travel planning application that uses artificial intelligence and optimization algorithms to create personalized travel itineraries. The system analyzes landmarks, hotels, travel times, and user preferences to generate optimal routes that maximize tourist experiences while respecting time and budget constraints.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Optimization Algorithms](#optimization-algorithms)
- [API Endpoints](#api-endpoints)
- [Frontend Components](#frontend-components)
- [Data Structure](#data-structure)
- [Testing](#testing)
- [Contributing](#contributing)

---

## 🎯 Overview

This project implements a comprehensive travel itinerary optimization system that combines **multiple AI algorithms** to solve complex travel planning problems. Users can specify their starting hotel, destination, trip duration, and interests, and the system generates optimized itineraries that:

- ✅ Maximize tourist attraction satisfaction
- ✅ Minimize total travel time
- ✅ Respect landmark operating hours
- ✅ Consider hotel constraints
- ✅ Adapt to different optimization strategies

The application uses a **full-stack approach** with a Python FastAPI backend handling complex computations and a React frontend providing an intuitive user interface with interactive maps.

---

## ✨ Features

### 🤖 AI & Optimization
- **7 Different Optimization Algorithms**: ACS, Genetic Algorithm, Simulated Annealing, Hill Climbing, Greedy Search, Artificial Bee Colony, and Constraint Satisfaction Problem (CSP)
- **Hybrid Approaches**: Combines multiple algorithms (e.g., ACS with Simulated Annealing)
- **Parameter Tuning**: Extensive testing and optimization of algorithm parameters
- **Comparison Tools**: Analyzes performance differences between algorithms

### 🗺️ Travel Planning
- **Interactive Map Integration**: Leaflet-based map visualization with routing
- **Landmark Management**: Comprehensive landmark database with ratings and opening hours
- **Hotel Support**: Multiple hotel options with location data
- **Travel Time Matrix**: Pre-computed travel times between locations
- **Time Constraints**: Respects landmark opening hours and visit durations

### 👤 User Management
- **Authentication System**: User login and registration
- **User Profiles**: Store and manage user preferences and itinerary history
- **Personalized Recommendations**: Tailored results based on user interests

### 💾 Data Management
- **CSV-Based Datasets**: Hotels and landmarks data in structured CSV format
- **GeoJSON Support**: Geographic data for advanced mapping features
- **Dynamic Data Loading**: Efficient data management and preprocessing

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Modern, fast web framework for building APIs |
| **Python 3.x** | Core language for algorithm implementation |
| **SQLAlchemy** | ORM for database operations |
| **PostgreSQL** | Relational database with psycopg2 driver |
| **Uvicorn** | ASGI server for running FastAPI |
| **Pydantic** | Data validation and schema definition |
| **Pandas & NumPy** | Data processing and numerical computations |

### Frontend
| Technology | Purpose |
|-----------|---------|
| **React 19** | UI framework |
| **Vite** | Build tool and dev server |
| **React Router DOM** | Client-side routing |
| **Leaflet** | Interactive map library |
| **Leaflet Routing Machine** | Route optimization and display |
| **Material-UI (MUI)** | Component library |
| **Tailwind CSS** | Utility-first CSS framework |
| **Emotion** | CSS-in-JS styling |

---

## 📁 Project Structure

```
Intro_to_AI_Travel_Project/
├── Algorithms/                          # Optimization Algorithms
│   ├── ACS.py                          # Ant Colony System
│   ├── artificial_bee_colony.py         # ABC Algorithm
│   ├── GA.py                           # Genetic Algorithm
│   ├── Greedy.py                       # Greedy Search
│   ├── hill_climbing.py                # Hill Climbing
│   ├── Simulated_Anealing.py          # Simulated Annealing
│   └── CSP_Solver.py                   # Constraint Satisfaction
│
├── backend/                             # FastAPI Backend
│   ├── main.py                         # Application entry point
│   ├── requirements.txt                # Python dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── solver.py                   # Core solving logic
│   │   ├── routes/
│   │   │   ├── solve.py               # Optimization endpoints
│   │   │   ├── auth.py                # Authentication
│   │   │   └── itinerary.py           # Itinerary management
│   │   ├── models/
│   │   │   └── schemas.py             # Data schemas
│   │   ├── database/
│   │   │   └── database.py            # DB configuration
│   │   └── utils/
│   │       └── helpers.py             # Utility functions
│   ├── ai_integration/
│   │   ├── algorithms/                # Algorithm implementations
│   │   └── core/                      # Core classes
│   └── data/
│       ├── hotels.csv
│       ├── landmarks.csv
│       └── time_matrix.json
│
├── core/                                # Core Problem Definitions
│   ├── Node_Classes.py                 # Landmark & Hotel classes
│   ├── Problem_AntColony.py           # ACS environment setup
│   ├── Problem_InformedSearch.py      # Informed search problems
│   ├── Problem_LocalSearch.py         # Local search problems
│   └── Solution.py                     # Solution representation
│
├── frontend/                            # React Vite Application
│   ├── package.json                    # Dependencies
│   ├── vite.config.js                  # Vite configuration
│   ├── tailwind.config.cjs             # Tailwind config
│   ├── index.html                      # Entry HTML
│   ├── src/
│   │   ├── App.jsx                     # Main app component
│   │   ├── main.jsx                    # React entry point
│   │   ├── components/
│   │   │   ├── home/                  # Home page
│   │   │   ├── plan/                  # Trip planning page
│   │   │   ├── itinerary/             # Itinerary display
│   │   │   ├── map/                   # Map component
│   │   │   ├── navbar/                # Navigation
│   │   │   ├── login/                 # Login page
│   │   │   ├── register/              # Registration page
│   │   │   ├── profile/               # User profile
│   │   │   └── footer/                # Footer
│   │   └── styles/
│   ├── public/
│   │   ├── images/
│   │   └── data/
│   └── README.md
│
├── utils/                               # Utility Modules
│   ├── data_loader.py                  # Data loading utilities
│   ├── evaluation.py                   # Performance evaluation
│   ├── time_matrix_generator.py        # Time matrix generation
│   └── time_matrix files               # Pre-computed matrices
│
├── Tests/                               # Testing Suite
│   ├── ABC_test.py
│   ├── ACS_Test.py
│   ├── GA_test.py
│   ├── Greedy_test.py
│   ├── hill_climbing_test.py
│   ├── SA_Test.py
│   ├── csp_test.py
│   └── Results/                        # Test results & benchmarks
│
├── dataset/                             # Data Files
│   ├── hotels/
│   │   └── Algiers_hotels.csv
│   └── landmarks/
│       └── Algiers_Landmarks.csv
│
├── scripts/                             # Data Processing Scripts
│   ├── gemini_solution/
│   ├── scraping method/
│   ├── using overpass data/
│   └── using scraped data/
│
├── notebook.ipynb                       # Jupyter Notebook for exploration
└── README.md                            # This file
```

---

## 💻 Installation & Setup

### Prerequisites
- **Python 3.8+**
- **Node.js 16+** and **npm**
- **PostgreSQL 12+** (optional, for full database setup)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Intro_to_AI_Travel_Project
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional)
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/travel_db
   DEBUG=True
   ```

5. **Run database initialization** (if PostgreSQL is set up)
   ```bash
   python -c "from app.database.database import init_db; init_db()"
   ```

6. **Start the backend server**
   ```bash
   uvicorn main:app --reload
   ```
   - API Documentation: http://localhost:8000/docs
   - ReDoc Documentation: http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   - Access at: http://localhost:5173

4. **Build for production**
   ```bash
   npm run build
   ```

---

## 🚀 Usage

### Basic Workflow

1. **Register/Login**
   - Create an account on the application
   - Complete your user profile

2. **Plan Your Journey**
   - Select your starting hotel and destination
   - Choose trip duration
   - Select your interests and preferences

3. **Generate Itinerary**
   - Choose optimization algorithm
   - System generates optimal routes
   - View results on interactive map

4. **View Details**
   - Check landmark information
   - Review time schedule
   - See travel routes

### Example API Request

```bash
# Start optimization (curl example)
curl -X POST "http://localhost:8000/api/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "hotel_id": 1,
    "landmarks": [1, 24, 31, 51],
    "trip_duration": 8,
    "algorithm": "ACS"
  }'
```

---

## 🧠 Optimization Algorithms

### 1. **Ant Colony System (ACS)**
- Inspired by ant pheromone behavior
- Excellent for finding near-optimal solutions
- Exploration vs exploitation balance
- Ideal for large landmark sets

**Parameters**: `alpha`, `beta`, `rho`, `q0`, `iterations`

### 2. **Genetic Algorithm (GA)**
- Population-based evolutionary approach
- Crossover and mutation operations
- Good for diverse solution spaces
- Requires careful parameter tuning

**Parameters**: `population_size`, `generations`, `mutation_rate`, `crossover_rate`

### 3. **Simulated Annealing (SA)**
- Probabilistic optimization technique
- Mimics metal annealing process
- Escapes local optima through temperature control
- Good for small to medium problems

**Parameters**: `initial_temp`, `cooling_rate`, `min_temp`, `iterations`

### 4. **Hill Climbing**
- Simple greedy local search
- Fast but may stuck in local optima
- Good starting point for hybrid approaches
- Minimal parameters needed

### 5. **Greedy Search**
- Straightforward heuristic approach
- Always selects best immediate choice
- Fastest execution time
- Provides baseline solutions

### 6. **Artificial Bee Colony (ABC)**
- Swarm intelligence based on bee foraging
- Employee, onlooker, and scout bees
- Good exploration and exploitation balance

**Parameters**: `colony_size`, `iterations`, `limit`

### 7. **Constraint Satisfaction Problem (CSP)**
- Constraint-based approach
- Ensures all constraints are satisfied
- Best for problems with hard constraints
- May take longer but guarantees feasibility

---

## 📡 API Endpoints

### Solve Routes (`/api/solve`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/solve` | Generate optimized itinerary |
| POST | `/solve/compare` | Compare multiple algorithms |
| GET | `/algorithms` | List available algorithms |
| GET | `/results/{id}` | Retrieve previous result |

### Authentication Routes (`/api/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | User registration |
| POST | `/login` | User login |
| POST | `/logout` | User logout |
| GET | `/profile` | Get user profile |
| PUT | `/profile` | Update user profile |

### Itinerary Routes (`/api/itinerary`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/itineraries` | List user itineraries |
| POST | `/itineraries` | Create new itinerary |
| GET | `/itineraries/{id}` | Get itinerary details |
| PUT | `/itineraries/{id}` | Update itinerary |
| DELETE | `/itineraries/{id}` | Delete itinerary |

---

## 🎨 Frontend Components

### Pages
- **Home** - Landing page with project overview
- **Plan Journey** - Trip planning interface
- **Itinerary** - Detailed itinerary view and management
- **Map** - Interactive map with routes
- **Login** - User authentication
- **Register** - User registration
- **Profile** - User account management

### Key Components
- **Navbar** - Navigation bar
- **Footer** - Footer section
- **Map Component** - Leaflet integration with routing
- **Time Plan Display** - Schedule visualization
- **Landmark List** - Browsable landmark listings

---

## 📊 Data Structure

### Landmark Class
```python
class Landmark:
    id: int                          # Unique identifier
    name: str                        # Landmark name
    lon: float                       # Longitude
    lat: float                       # Latitude
    interest_score: float            # User interest rating
    opening_hours: dict[str, list]   # Hours for each day
    visit_duration: int              # Visit time in minutes
    landmark_type: str               # Category (Museum, Park, etc.)
```

### Hotel Class
```python
class Hotel:
    id: int                          # Unique identifier
    name: str                        # Hotel name
    lon: float                       # Longitude
    lat: float                       # Latitude
    opening_hours: dict[str, list]   # Operating hours
```

### Solution Representation
```python
class Solution:
    state: List[Landmark]            # Ordered list of landmarks
    score: float                     # Solution quality score
    
# Score calculation: (7 * total_rating) - total_travel_time
```

---

## ✅ Testing

The project includes comprehensive test suite:

```bash
# Run all tests
python -m pytest Tests/

# Run specific algorithm tests
python -m pytest Tests/ACS_Test.py
python -m pytest Tests/GA_test.py
python -m pytest Tests/SA_Test.py

# Run with coverage
python -m pytest --cov=Algorithms Tests/
```

### Test Results Location
- `Tests/ABC_test_results/` - ABC algorithm benchmarks
- `Tests/ACS-results/` - ACS results and parameters
- `Tests/GA_test_results/` - Genetic algorithm results
- `Tests/Greedy_test_results/` - Greedy search results
- `Tests/Comparison_results/` - Algorithm comparisons

---

## 🔍 Data Sources

### Datasets
- **Hotels**: `dataset/hotels/Algiers_hotels.csv`
- **Landmarks**: `dataset/landmarks/Algiers_Landmarks.csv`
- **Geographic Data**: `scripts/using overpass data/landmarks.geojson`

### Data Processing
- Landmark enrichment with web scraping
- Travel time matrix generation
- GeoJSON conversion and validation

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make changes and test**
   ```bash
   python -m pytest Tests/
   ```
4. **Commit with descriptive messages**
   ```bash
   git commit -m "Add feature: description"
   ```
5. **Push to branch**
   ```bash
   git push origin feature/your-feature
   ```
6. **Open Pull Request**

---

## 📝 File Naming Conventions

- **Algorithms**: `algorithm_name.py`
- **Tests**: `algorithm_name_test.py`
- **Results**: `algorithm_name_results/`
- **Data Files**: Lowercase with underscores

---

## 🔧 Configuration

### Backend Configuration
- Located in `backend/main.py`
- CORS settings for frontend integration
- Database initialization

### Frontend Configuration
- `frontend/vite.config.js` - Build settings
- `frontend/tailwind.config.cjs` - Styling
- `frontend/eslint.config.js` - Code quality

---

## 📞 Support & Contact

For issues, questions, or suggestions:
1. Create an issue in the repository
2. Contact the development team
3. Check documentation in `notebook.ipynb`

---

## 📄 License

This project is part of an educational initiative for AI and optimization algorithms.

---

## 🎓 Academic Reference

This project demonstrates practical applications of:
- **Swarm Intelligence** (ACS, ABC)
- **Evolutionary Algorithms** (GA)
- **Local Search Methods** (Hill Climbing, SA)
- **Heuristic Approaches** (Greedy)
- **Constraint Programming** (CSP)
- **Web Development** (Full-stack)
- **Data Analysis** (Pandas, NumPy)

---

**Last Updated**: May 2026  
**Version**: 1.0.0  
**Status**: Active Development
