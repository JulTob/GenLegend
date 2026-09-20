#!/usr/bin/env bash
#
# One-time setup so GitHub can publish to Cloud Run without holding a key.
#
# Run it once, in Cloud Shell, where you are already signed in:
#
#     bash scripts/setup-github-deploy.sh
#
# It prints three values at the end. Put those into GitHub under
# Settings -> Secrets and variables -> Actions -> Variables. They are
# Variables, not Secrets: none of them is a password.
#
# What it builds, and why there is no key anywhere:
#
#   GitHub already knows who it is, and can hand out a signed statement
#   saying "I am a workflow running on JulTob/GenLegend". Workload Identity
#   Federation is Google agreeing to trust statements of exactly that shape,
#   and issuing a token good for a few minutes in exchange. Nothing
#   long-lived is created, so nothing long-lived can leak.
#
# Safe to run twice. Steps that already exist say so and are skipped.

set -euo pipefail

PROJECT_ID="${PROJECT_ID:-gen-legend}"
REPO="${REPO:-JulTob/GenLegend}"
POOL="github"
PROVIDER="github"
SA_NAME="github-deployer"

echo "Project : ${PROJECT_ID}"
echo "Repo    : ${REPO}"
echo

PROJECT_NUMBER="$(
	gcloud projects describe "${PROJECT_ID}" --format='value(projectNumber)'
	)"
SA="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
RUNTIME_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# --- 1. The services this needs ------------------------------------------
echo "[1/6] Enabling the services..."
gcloud services enable \
	iamcredentials.googleapis.com \
	sts.googleapis.com \
	run.googleapis.com \
	cloudbuild.googleapis.com \
	artifactregistry.googleapis.com \
	--project="${PROJECT_ID}"

# --- 2. The account GitHub will act as ------------------------------------
echo "[2/6] Creating the deployer account..."
gcloud iam service-accounts create "${SA_NAME}" \
	--project="${PROJECT_ID}" \
	--display-name="GitHub Actions deployer" \
	|| echo "      already exists, continuing"

# --- 3. What it is allowed to do ------------------------------------------
# Deploy the service, run the build, push the image, and use the bucket
# Cloud Build stages sources in. Nothing wider.
echo "[3/6] Granting its roles..."
for role in \
		roles/run.admin \
		roles/cloudbuild.builds.editor \
		roles/artifactregistry.admin \
		roles/storage.admin ; do
	gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
		--member="serviceAccount:${SA}" \
		--role="${role}" \
		--condition=None \
		--quiet > /dev/null
	echo "      ${role}"
done

# A Cloud Run service runs *as* an account, and whoever deploys it must be
# allowed to hand it that identity.
echo "      roles/iam.serviceAccountUser on ${RUNTIME_SA}"
gcloud iam service-accounts add-iam-policy-binding "${RUNTIME_SA}" \
	--project="${PROJECT_ID}" \
	--member="serviceAccount:${SA}" \
	--role="roles/iam.serviceAccountUser" \
	--quiet > /dev/null

# --- 4. The pool ----------------------------------------------------------
echo "[4/6] Creating the identity pool..."
gcloud iam workload-identity-pools create "${POOL}" \
	--project="${PROJECT_ID}" \
	--location=global \
	--display-name="GitHub" \
	|| echo "      already exists, continuing"

# --- 5. The provider, locked to this repository ---------------------------
# The attribute condition is the security. Without it, a workflow in
# anybody's repository could ask Google for this token.
echo "[5/6] Creating the provider, restricted to ${REPO}..."
gcloud iam workload-identity-pools providers create-oidc "${PROVIDER}" \
	--project="${PROJECT_ID}" \
	--location=global \
	--workload-identity-pool="${POOL}" \
	--display-name="GitHub" \
	--issuer-uri="https://token.actions.githubusercontent.com" \
	--attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
	--attribute-condition="assertion.repository=='${REPO}'" \
	|| echo "      already exists, continuing"

# --- 6. Let this repository, and only this one, act as the account --------
echo "[6/6] Letting ${REPO} act as the deployer..."
gcloud iam service-accounts add-iam-policy-binding "${SA}" \
	--project="${PROJECT_ID}" \
	--role="roles/iam.workloadIdentityUser" \
	--member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/attribute.repository/${REPO}" \
	--quiet > /dev/null

cat <<END

Done.

Put these three into GitHub, as Variables (not Secrets), under
Settings -> Secrets and variables -> Actions -> Variables:

  GCP_PROJECT_ID
  ${PROJECT_ID}

  GCP_SERVICE_ACCOUNT
  ${SA}

  GCP_WORKLOAD_IDENTITY_PROVIDER
  projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL}/providers/${PROVIDER}

Then, to keep the deploy on your word rather than automatic, create an
Environment named  production  under Settings -> Environments and add
yourself as a required reviewer. Without it GitHub treats the environment
name as auto-approved and publishes without asking.

END
