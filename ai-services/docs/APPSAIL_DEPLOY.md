# Catalyst AppSail deploy helpers for CrimeMatrix AI Services
#
# Prerequisites:
#   1. Docker Desktop running
#   2. Catalyst CLI: npm install -g zcatalyst-cli
#   3. Logged in: catalyst login
#   4. Project initialized (run from a directory with catalyst.json)
#
# Build + archive:
#   cd ai-services
#   docker build -t crimematrix-ai:latest .
#   docker save crimematrix-ai:latest -o crimematrix-ai.tar
#
# Deploy (from Catalyst project root):
#   catalyst deploy appsail standalone \
#     --name crimematrix-ai \
#     --source docker-archive://./ai-services/crimematrix-ai.tar \
#     --command "sh -c 'uvicorn main:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT}'" \
#     --port 9000
#
# Then in Catalyst console → AppSail → crimematrix-ai:
#   - Memory: 2048 MB
#   - Env: OPENROUTER_API_KEY, OPENROUTER_MODEL (optional), BACKEND_URL (later)
#
# Verify:
#   python ai-services/scripts/smoke_appsail.py --base https://<appsail-url>
