# Five Controls Before an Agent Can Touch Production

This is a deliberately short public checklist. It is not a certification or complete security program.

## 1. Separate confidence from authorization

Model confidence may influence routing. It must not be treated as permission to access a resource or perform an action.

## 2. Scope tool permissions server-side

Do not rely on a prompt such as “only update customer records.” Enforce allowed actions and resource scope at the tool/API boundary.

## 3. Require explicit approval for designated high-impact actions

Define which actions require a human decision before execution. Approval should be tied to the exact task/action, not a vague session-level confirmation.

## 4. Design retries for idempotency

Agent workflows retry. A retry must not accidentally create duplicate payments, tickets, messages, orders or database mutations.

## 5. Preserve evidence and audit context

Record enough structured context to reconstruct why a route/action occurred without storing secrets or unnecessary sensitive prompt content.

## What is not in this free checklist

The Complete Implementation Kit contains an **18-control zero-trust security audit** plus acceptance, risk and deployment assets.

Complete kit: https://whop.com/drdemon/enterprise-ai-blueprint/
