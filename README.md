# Multiplayer Game Backend

## Description
Welcome to the **Multiplayer Game Backend** — a social gaming platform backend designed to power a vibrant multiplayer experience!

- **User Management:** Sign up as a user and log in to access the app.
- **Profiles:** Create and customize your profile with info like:
  - Country  
  - Bio  
  - Profile Image
- **Social Interaction:** Follow and be followed by other players, building your social circle.
- **Game Points & Leaderboards:** Earn points by playing the game and climb the leaderboard ranks! You can even filter rankings by country to see how you stack up locally or globally.

---

## CI/CD Integration

This project features a fully automated **CI/CD pipeline** powered by **GitHub Actions**!  
Every push to the repository triggers a workflow defined in `./.github/workflows` that:

- Builds the latest Docker image of the backend.
- Pushes the Docker image to Docker Hub automatically.

---

## How to Run

1. **Create a `.env` file** in the root directory of the project.  
   This file should contain all your configuration settings required by the app.  
   Refer to `./app/core/config.py` for the environment variables you need to define.

2. **Build the Docker image:**  
   ```bash
   docker build . -t multiplayergame:latest

3. **Run the Docker container with your environment variables and port mapping:**
   ```bash
   docker run --env-file .env -p 8000:8000 multiplayergame:latest

4. **Access the API documentation:**
    Open your browser and navigate to:
    `http://localhost:8000/docs`
    This interactive Swagger UI lets you explore and test the API endpoints.

## Contribution & Support
Feel free to submit your feedback. 