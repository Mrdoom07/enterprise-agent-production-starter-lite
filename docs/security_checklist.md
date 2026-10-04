# Five Controls Before an Agent Can Touch Production

This is a deliberately short public checklist. It is not a certification or complete security program.

## 1. Separate model judgment from authorization

A model may propose an action or expose a confidence score. Do not treat that score as permission. Route through independently validated context and deterministic policy.

## 2. Scope actions and resources outside the model

Do not rely on a prompt such as “only update customer records.” Resolve allowed actions and target resources outside the model and enforce scope at the tool/API boundary.

## 3. Require explicit approval for designated high-impact actions

Define which actions require a human decision before execution. Approval should be tied to the exact action/resource/version, not a vague session-level confirmation.

## 4. Design retries around the resource being changed

Agent workflows retry and multiple workers can race. Replay protection should be scoped to the resource + action + operation version rather than only to a task id. A real deployment also needs durable storage and concurrency control.

## 5. Log successful decisions as well as escalations

Recording only failures misses slow policy drift. Preserve structured context for `ALLOW`, review, rework and approval decisions so operators can reconstruct why a route occurred without storing unnecessary secrets.

## What is not in this free checklist

The Complete Implementation Kit contains an **18-control zero-trust security audit** plus acceptance, risk and deployment assets.

Complete kit: https://whop.com/drdemon/enterprise-ai-blueprint/
