# Step 1: Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first for caching
COPY web/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY web .

# Build the Next.js app
RUN npm run build


# Step 2: Production runner
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/next.config.js ./next.config.js

# Expose port (default for Next.js)
EXPOSE 3000

# Run production server
CMD ["npm", "start"]
