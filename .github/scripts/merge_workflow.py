#!/usr/bin/env python3
"""
Merge workflow jobs from template files into the generator workflow.
"""
import sys
import os
from ruamel.yaml import YAML


def main():
    if len(sys.argv) != 2:
        print("Usage: merge_workflow.py <source-workflow-file>", file=sys.stderr)
        sys.exit(1)
    
    source_workflow_file = sys.argv[1]
    workflow_file = '.github/workflows/generator.yml'
    
    # Create YAML instance that preserves formatting
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    yaml.width = 4096  # Prevent line wrapping
    
    # Load current workflow
    with open(workflow_file, 'r') as f:
        current_workflow = yaml.load(f)
    
    # Load source workflow template
    with open(source_workflow_file, 'r') as f:
        source_workflow = yaml.load(f)
    
    # Extract the job from source workflow (should be the only job)
    source_jobs = source_workflow.get('jobs', {})
    if not source_jobs:
        print(f"ERROR: No jobs found in {source_workflow_file}", file=sys.stderr)
        sys.exit(1)
    
    source_job_name = list(source_jobs.keys())[0]
    source_job = source_jobs[source_job_name]
    
    # Add 'needs' dependency to ensure it runs after check-and-generate
    source_job['needs'] = 'check-and-generate'
    
    # Ensure jobs dict exists and preserve check-and-generate job
    if 'jobs' not in current_workflow:
        current_workflow['jobs'] = {}
    
    # Save the check-and-generate job
    check_and_generate_job = current_workflow['jobs'].get('check-and-generate')
    
    # Rebuild jobs dict with check-and-generate first, then the project-specific job
    # Use CommentedMap to preserve ordering
    from ruamel.yaml.comments import CommentedMap
    new_jobs = CommentedMap()
    if check_and_generate_job:
        new_jobs['check-and-generate'] = check_and_generate_job
    
    new_jobs[source_job_name] = source_job
    
    # Replace jobs with the new ordered dict
    current_workflow['jobs'] = new_jobs
    
    # Write updated workflow back to file
    with open(workflow_file, 'w') as f:
        yaml.dump(current_workflow, f)
    
    print(f"Successfully updated workflow with '{source_job_name}' job from {source_workflow_file}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
