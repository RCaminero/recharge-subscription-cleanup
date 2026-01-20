# Recharge Subscription Cleanup

## Purpose
Safely clean up duplicate Recharge subscriptions while protecting revenue and avoiding billing failures.

## What this tool guarantees
- Never cancels the longest subscription (12m > 3m > 1m)
- Never leaves a customer with a faulty payment method
- Full audit log of every action
- Rollback support (reactivate cancelled subscriptions)
- Recharge API executes decisions made by data, not business logic inside Recharge

## Typical Use Case
Customers with two active Recharge subscriptions caused by edge cases during signup or migrations.

## Workflow
1. Input subscription IDs (CSV or manual)
2. Retrieve subscription data from Recharge
3. Decide KEEP / CANCEL / MANUAL_REVIEW
4. Cancel only when it is safe
5. Log every action
6. Allow rollback if needed

## Safety Rules
- Never cancel both subscriptions
- Never cancel the 12-month subscription
- Never cancel if the remaining subscription has a faulty payment method
- Manual review if both subscriptions show payment risk

## Scripts
- dry_run_evaluate.py → Evaluate decisions, no API mutations
- cancel_subscriptions.py → Execute safe cancellations
- restore_subscriptions.py → Rollback using logs

## Environment Variables
See `.env.example`

## Disclaimer
Recharge API is used strictly as an execution layer. All business logic lives in this repository.
