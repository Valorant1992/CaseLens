# --------------------------------------------------------------
# 1️⃣ Build stage – compile the Vite app
# --------------------------------------------------------------
FROM node:20-alpine AS builder
WORKDIR /app

# Install only production‑ready dependencies
COPY package*.json ./
RUN npm ci               # installs exactly what package-lock.json describes

# Copy source files and build the static site
COPY . .
RUN npm run build        # creates the static assets in /app/dist

# --------------------------------------------------------------
# 2️⃣ Runtime stage – serve the built files
# --------------------------------------------------------------
FROM node:20-alpine
WORKDIR /app

# Install a tiny static‑file server (serve)
RUN npm install -g serve

# Bring the compiled assets from the builder stage
COPY --from=builder /app/dist ./dist

# Hugging Face expects the app to listen on port 8080
EXPOSE 8080

# Launch the server
CMD ["serve", "-s", "dist", "-l", "8080"]
