---
name: feature-request-template
about: Request new features
assignees: mkpro118
labels: enhancement
title: "New Feature: "
body:
- type: textarea
  id: problem
  attributes:
    label: Please describe the problem to be solved
    description: |
      Please present a concise description of the problem to be addressed by this feature request.
      Please be clear what parts of the problem are considered to be in-scope and out-of-scope.
  validations:
    required: true

- type: textarea
  id: suggestions
  attributes:
    label: (Optional): Suggest A Solution
    description: |
      Please present a concise description of the problem to be addressed by this feature request.
      Please be clear what parts of the problem are considered to be in-scope and out-of-scope.
    value: |
      A concise description of your preferred solution. Things to address include:
      - Details of the technical implementation
      - Tradeoffs made in design decisions
      - Caveats and considerations for the future
      
      If there are multiple solutions, please present each one separately. 
      Save comparisons for the very end.
  validations:
    required: false
- type: checkboxes
  id: seen-existing-issues
  attributes:
    label: Please confirm you have checked for similar existing issues
    options:
      - label: I have confirmed there are no similar existing issues.
        required: true
---
