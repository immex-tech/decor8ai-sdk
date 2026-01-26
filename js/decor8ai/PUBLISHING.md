# Publishing decor8ai to npm

## npm Authentication (Post Dec 2025)

As of December 2025, npm has revoked all classic tokens. Publishing now requires:

1. **Session-based login** (2-hour tokens) for local publishing
2. **Granular access tokens** for CI/CD
3. **OIDC trusted publishing** for GitHub Actions (recommended)

## Local Publishing

### Step 1: Login to npm
```bash
npm login
```
This creates a 2-hour session token. You'll need to re-authenticate periodically.

### Step 2: Verify package
```bash
npm run publish:dry-run
```

### Step 3: Publish
```bash
npm run publish:release
```

## CI/CD Publishing

### Option A: OIDC Trusted Publishing (Recommended)

No tokens needed! Configure on npm:

1. Go to https://www.npmjs.com/package/decor8ai/access
2. Click "Add trusted publisher"
3. Select "GitHub Actions"
4. Configure:
   - Repository: `immex-tech/decor8ai-sdk`
   - Workflow: `publish-npm.yml`
   - Branch: `main`

Then trigger the GitHub Action by creating a release with tag `js-v*`.

### Option B: Granular Access Token

1. Create token via CLI:
   ```bash
   npm token create --cidr=0.0.0.0/0 --description="GitHub Actions"
   ```
   Or create at: https://www.npmjs.com/settings/~/tokens

2. Add to GitHub Secrets as `NPM_TOKEN`

3. For automated workflows, enable "Bypass 2FA" and limit to 90 days max.

## Version Bumping

```bash
# Patch release (0.0.x)
npm version patch

# Minor release (0.x.0)
npm version minor

# Major release (x.0.0)
npm version major
```

This automatically:
- Updates package.json version
- Creates a git commit
- Creates a git tag
- Pushes to origin (via postversion script)

## Pre-publish Checklist

- [ ] All tests pass (`npm test`)
- [ ] Version updated in package.json
- [ ] CHANGELOG updated (if applicable)
- [ ] index.d.ts types are current
- [ ] No localhost/test URLs in code
- [ ] README is up to date

## Troubleshooting

### "You must be logged in to publish"
Run `npm login` again - your 2-hour session may have expired.

### "This package requires 2FA"
2FA is enabled by default. Use an authenticator app during publish.

### "Token expired"
Create a new granular token or re-login with `npm login`.
