# Password Policy

## 1. Policy Objectives

The password policy exists to reduce account takeover risk while keeping signup and login friction manageable.

Goals:

1. Enforce minimum baseline strength.
2. Prevent trivial/common credential choices.
3. Support secure reset and recovery workflows.

## 2. Baseline Requirements

Recommended minimum policy for this project:

1. Minimum length: 8 characters.
2. Must include at least one uppercase letter.
3. Must include at least one lowercase letter.
4. Must include at least one digit.
5. Must include at least one special character.
6. Must not be too similar to user-identifying fields.
7. Must not be in common-password blocklists.

## 3. Django Validator Strategy

Use Django built-in validators plus optional custom validator.

Built-in validators typically include:

1. UserAttributeSimilarityValidator
2. MinimumLengthValidator
3. CommonPasswordValidator
4. NumericPasswordValidator

Optional custom validator can enforce character class complexity.

## 4. UX and Error Messaging

Guidelines:

1. Display clear requirement hints near password field.
2. Show specific validation reason, not generic failure.
3. Keep messaging language-consistent with selected UI language.
4. Avoid revealing account existence during reset requests.

## 5. Password Reset Policy

1. Reset tokens should expire quickly.
2. Tokens must be single-use.
3. Force old session invalidation on reset if supported.
4. Notify user by email on password changes.

## 6. Security Best Practices

1. Never log plaintext passwords.
2. Never transmit passwords in URLs.
3. Use HTTPS only in production.
4. Use Django default password hashers or stronger approved alternatives.
5. Periodically review authentication event logs for suspicious behavior.

## 7. Testing Matrix

Add tests for:

1. Password too short.
2. Missing uppercase.
3. Missing lowercase.
4. Missing digit.
5. Missing symbol.
6. Common password rejection.
7. Similar-to-email rejection.
8. Valid strong password acceptance.

Example command:

```powershell
python manage.py test customers
```

## 8. Example Strong Password Format

Pattern guidance for users:

1. Three random words plus symbols and numbers.
2. Avoid brand name, email, date of birth, or keyboard patterns.

Example pattern (not literal password):

1. WordWordWord!12

## 9. Operational Procedures

When updating policy:

1. Communicate changes in release notes.
2. Update frontend helper text.
3. Update tests and validator config.
4. Verify reset and signup flows in staging.

