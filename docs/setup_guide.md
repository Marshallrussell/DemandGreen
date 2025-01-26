# Setup Guide for GreenTech Gig Platform

This guide will help you set up the GreenTech Gig Platform on your local machine for development and testing purposes. Follow the steps below to get started.

---

## **Prerequisites**

Before setting up the project, ensure you have the following installed:

1. **Node.js** (v16 or later)
   - [Download Node.js](https://nodejs.org/)
2. **PostgreSQL** (v13 or later)
   - [Download PostgreSQL](https://www.postgresql.org/download/)
3. **Git**
   - [Download Git](https://git-scm.com/)
4. **npm** or **yarn** (comes with Node.js)

---

## **Step 1: Clone the Repository**

1. Open a terminal.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/greentech-gig-platform.git
   ```
3. Navigate to the project directory:
   ```bash
   cd greentech-gig-platform
   ```

---

## **Step 2: Install Dependencies**

1. Install the backend dependencies:
   ```bash
   cd backend
   npm install
   ```

2. Install the frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

---

## **Step 3: Configure Environment Variables**

1. Create a `.env` file in the `backend` directory:
   ```bash
   touch backend/.env
   ```

2. Add the following variables to `backend/.env`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/greentech
   JWT_SECRET=your_jwt_secret
   NODE_ENV=development
   PORT=5000
   ```
   Replace `username`, `password`, and other placeholders with your PostgreSQL credentials and desired settings.

3. Create a `.env` file in the `frontend` directory (if needed for environment-specific settings).

---

## **Step 4: Set Up the Database**

1. Create a new PostgreSQL database named `greentech`.
   ```bash
   psql -U postgres
   CREATE DATABASE greentech;
   ```

2. Run database migrations (if applicable):
   ```bash
   cd backend
   npm run migrate
   ```

---

## **Step 5: Run the Application**

1. Start the backend server:
   ```bash
   cd backend
   npm start
   ```
   The backend server will run on `http://localhost:5000` by default.

2. Start the frontend server:
   ```bash
   cd frontend
   npm start
   ```
   The frontend will run on `http://localhost:3000` by default.

---

## **Step 6: Verify the Setup**

1. Open your browser and navigate to `http://localhost:3000`.
2. Verify that the application loads successfully.

---

## **Optional: Running Tests**

### Backend Tests:
- Run the backend test suite:
  ```bash
  cd backend
  npm test
  ```

### Frontend Tests:
- Run the frontend test suite:
  ```bash
  cd frontend
  npm test
  ```

---

## **Troubleshooting**

1. **Database Connection Issues**:
   - Ensure PostgreSQL is running and the `DATABASE_URL` in `.env` is correct.

2. **Dependency Errors**:
   - Delete `node_modules` and reinstall dependencies:
     ```bash
     rm -rf node_modules
     npm install
     ```

3. **Port Conflicts**:
   - Ensure ports `5000` (backend) and `3000` (frontend) are not in use.

For additional help, open an issue on the [GitHub Repository](https://github.com/yourusername/greentech-gig-platform/issues).

---

Congratulations! You have successfully set up the GreenTech Gig Platform. Happy coding!
