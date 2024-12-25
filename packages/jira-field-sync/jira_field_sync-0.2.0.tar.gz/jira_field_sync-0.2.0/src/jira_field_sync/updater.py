#!/usr/bin/env python3
import yaml
import requests
import logging
from datetime import datetime
from typing import Dict, List, Optional
import sys
from pathlib import Path
import base64

class JiraFieldUpdater:
    def __init__(self, config_path: str):
        # Setup logging first, before anything else
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create formatters
        detailed_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_formatter = logging.Formatter('%(message)s')  # Simplified console output
        
        # Create handlers
        file_handler = logging.FileHandler(
            log_dir / f'jira_update_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Setup logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Now load config - logger is ready to handle any errors
        self.config = self._load_config(config_path)
        
        # Setup base URL before auth-related operations
        self.base_url = self.config['jira']['url'].rstrip('/')
        
        # Setup Basic Auth
        auth_str = f"{self.config['jira']['email']}:{self.config['jira']['token']}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json"
        }

        # Now we can verify authentication since base_url and headers are set
        self._verify_authentication()

        # Get and store field metadata for all configured fields
        self.field_metadata = {}
        for field_name, field_config in self.config['fields'].items():
            field_id = field_config['id']
            metadata = self.get_field_metadata(field_id)
            if metadata:
                self.field_metadata[field_id] = metadata
                self.logger.debug(f"Field {field_name} ({field_id}) metadata: {metadata}")
            else:
                self.logger.warning(f"Could not fetch metadata for field {field_name} ({field_id})")

        self.project_types = {}
        self._cache_project_types()


    def _verify_authentication(self):
        """Verify that we can authenticate with Jira."""
        try:
            response = requests.get(
                f"{self.base_url}/rest/api/3/myself",
                headers=self.headers
            )
            response.raise_for_status()
            user_info = response.json()
            self.logger.info(f"Successfully authenticated as {user_info.get('displayName', 'unknown user')}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            if response.status_code == 401:
                self.logger.error("Invalid credentials. Please check your email and API token.")
            elif response.status_code == 403:
                self.logger.error("You don't have sufficient permissions.")
            sys.exit(1)

    def _load_config(self, config_path: str) -> dict:
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Validate required fields
            required_fields = ['jira.url', 'jira.email', 'jira.token', 'fields']
            for field in required_fields:
                keys = field.split('.')
                current = config
                for key in keys:
                    if key not in current:
                        raise ValueError(f"Missing required configuration: {field}")
                    current = current[key]
            
            # Set up basic auth for validation
            auth_str = f"{config['jira']['email']}:{config['jira']['token']}"
            encoded_auth = base64.b64encode(auth_str.encode()).decode()
            headers = {
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_auth}",
                "Content-Type": "application/json"
            }
            
            # Validate field values against available options
            for field_name, field_config in config['fields'].items():
                field_id = field_config['id']
                field_num = field_id.replace('customfield_', '')
                
                # Get field options
                try:
                    response = requests.get(
                        f"{config['jira']['url'].rstrip('/')}/rest/api/3/customField/{field_num}/option",
                        headers=headers
                    )
                    response.raise_for_status()
                    options = response.json()
                except requests.exceptions.RequestException as e:
                    raise ValueError(f"Could not fetch options for field {field_name} ({field_id}): {str(e)}")
                
                # Get all valid options for easier reporting
                valid_options = [opt['value'] for opt in options['values']]
                
                # Check each project's value
                invalid_values = []
                for project_key, value in field_config['projects'].items():
                    normalized_value = value.strip().lower()
                    if not any(opt.strip().lower() == normalized_value for opt in valid_options):
                        invalid_values.append((project_key, value))
                
                if invalid_values:
                    error_msg = (f"\nInvalid values found for field {field_name}:"
                            f"\nValid options are: {valid_options}"
                            f"\nInvalid project values:")
                    for project_key, value in invalid_values:
                        error_msg += f"\n  - Project {project_key}: '{value}'"
                    raise ValueError(error_msg)
            
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            sys.exit(1)

    def _cache_project_types(self):
        """Cache project types for all configured projects"""
        for field_config in self.config['fields'].values():
            for project_key in field_config['projects'].keys():
                if project_key not in self.project_types:
                    self.project_types[project_key] = self.get_project_type(project_key)

    def get_project_type(self, project_key: str) -> str:
        """Fetch project type from Jira"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/api/3/project/{project_key}",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            # Check projectTypeKey for next-gen vs company-managed
            project_type_key = data.get('projectTypeKey', '')
            if 'next-gen' in project_type_key.lower():
                return 'next-gen'
            elif 'software' in project_type_key.lower():
                return 'company-managed'
            return 'undetermined'
            
        except Exception as e:
            self.logger.warning(f"Could not determine project type for {project_key}: {str(e)}")
            return 'undetermined'

    def find_issues_needing_update(self, project_key: str, field_id: str, target_value: str) -> List[dict]:
        """Find issues that either have no LOB value or have a different value than target."""
        issues = []
        start_at = 0
        batch_size = 100
        
        # Remove 'customfield_' prefix for JQL
        field_num = field_id.replace("customfield_", "")
        
        while True:
            try:
                # JQL to find both empty and different values
                jql = f'project = "{project_key}" AND issuetype != Epic AND (cf[{field_num}] is EMPTY OR cf[{field_num}] != "{target_value}")'                
                self.logger.debug(f"Searching with JQL: {jql}")  # Add debug logging
                
                search_endpoint = f"{self.base_url}/rest/api/3/search"
                search_payload = {
                    "jql": jql,
                    "startAt": start_at,
                    "maxResults": batch_size,
                    "fields": ["id", "key", "issuetype", field_id]
                }
                
                response = requests.post(
                    search_endpoint,
                    headers=self.headers,
                    json=search_payload
                )
                
                if response.status_code != 200:
                    self.logger.error(
                        f"Failed to search issues for {project_key}:"
                        f"\nStatus code: {response.status_code}"
                        f"\nResponse: {response.text}"
                    )
                    break
                    
                result = response.json()
                
                batch_issues = [{
                    "id": issue['id'],
                    "key": issue['key'],
                    "issue_type": issue['fields']['issuetype']['name'],
                    "current_value": (issue['fields'].get(field_id) or {}).get('value', None),
                } for issue in result['issues']]
                
                issues.extend(batch_issues)
                
                if len(batch_issues) < batch_size:
                    break
                    
                start_at += batch_size
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error finding issues for {project_key}: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    self.logger.error(f"Response content: {e.response.text}")
                break
        
        return issues

    def check_field_screen_config(self, project_key: str, field_id: str):
        """Check if field is properly configured for the project."""
        try:
            metadata_response = requests.get(
                f"{self.base_url}/rest/api/3/issue/createmeta",
                params={
                    'projectKeys': project_key,
                    'expand': 'projects.issuetypes.fields'
                },
                headers=self.headers
            )
            
            if not metadata_response.ok:
                self.logger.error(f"Cannot get project metadata: {metadata_response.text}")
                return False
                
            metadata = metadata_response.json()
            projects = metadata.get('projects', [])
            
            if not projects:
                return False
                
            # Check if field exists in any issuetype
            for issuetype in projects[0].get('issuetypes', []):
                if field_id in issuetype.get('fields', {}):
                    return True
                    
            return False

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            return False


    def get_field_options(self, field_id: str) -> dict:
        """Get available options for a select field."""
        try:
            field_num = field_id.replace('customfield_', '')
            response = requests.get(
                f"{self.base_url}/rest/api/3/customField/{field_num}/option",
                headers=self.headers
            )
            response.raise_for_status()
            options = response.json()
            self.logger.debug(f"Available options: {options}")  # Changed to debug
            return options
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to get field options: {str(e)}")
            return None

    def update_issue_field(self, issue_id: str, field_id: str, value: str, dry_run: bool = False) -> bool:
        try:
            options_response = self.get_field_options(field_id)
            if not options_response:
                return False
            
            # Normalize input value and try to find a match
            normalized_value = value.strip().lower()
            option = next(
                (opt for opt in options_response['values'] 
                 if opt['value'].strip().lower() == normalized_value), 
                None
            )
            
            if not option:
                # Log available options to help with debugging
                available_options = [opt['value'] for opt in options_response['values']]
                self.logger.error(
                    f"Value '{value}' not found in available options. "
                    f"Available options are: {available_options}"
                )
                return False

            if dry_run:
                self.logger.info(f"Would update issue {issue_id} with value: {value}")
                return True

            endpoint = f"{self.base_url}/rest/api/3/issue/{issue_id}"
            payload = {
                "fields": {
                    field_id: {
                        "id": str(option['id']),  # API expects string ID
                        "value": option['value']
                    }
                }
            }

            self.logger.debug(f"Update payload for issue {issue_id}: {payload}")
            
            response = requests.put(
                endpoint, 
                headers=self.headers, 
                json=payload
            )
            
            if response.status_code != 204:  # Jira returns 204 on successful update            
                self.logger.error(f"Failed to update issue {issue_id}: {response.status_code}")
                self.logger.error(f"Response: {response.text}")
                return False
                    
            self.logger.debug(f"Successfully updated issue {issue_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update issue {issue_id}: {str(e)}")
            return False
        
        
    def get_field_metadata(self, field_id: str) -> dict:
        """Get metadata for a specific custom field."""
        try:
            response = requests.get(
                f"{self.base_url}/rest/api/3/field",  # Note: changed endpoint
                headers=self.headers
            )
            response.raise_for_status()
            fields = response.json()
            
            # Find our specific field
            field = next((f for f in fields if f['id'] == field_id), None)
            if field:
                self.logger.info(f"Field metadata: {field}")
            return field
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to get field metadata: {str(e)}")
            return None
    
    def create_or_update_automation_rule(
        self, 
        project_key: str, 
        field_id: str, 
        value: str,
        field_name: str
    ) -> bool:
        """Create or update automation rule for setting field on new issues."""
        try:
            # First, get the automation UUID for this project
            project_endpoint = f"{self.base_url}/gateway/api/automation/internal-api/jira/pro/projects"
            response = requests.get(
                project_endpoint,
                headers=self.headers
            )
            response.raise_for_status()
            projects_data = response.json()
            
            # Find our project and get its automation UUID
            project_data = next(
                (p for p in projects_data['projects'] if p['projectKey'] == project_key),
                None
            )
            
            if not project_data:
                self.logger.error(f"Could not find automation data for project {project_key}")
                return False
                
            automation_uuid = project_data['id']
            
            # Now we can construct the correct rules endpoint
            rules_endpoint = f"{self.base_url}/gateway/api/automation/internal-api/jira/{automation_uuid}/pro/rest/12080/rule"
            
            # Get existing rules
            response = requests.get(
                rules_endpoint,
                headers=self.headers
            )
            response.raise_for_status()
            rules = response.json()
            
            rule_name = f"Set {field_name} for new issues"
            existing_rule = next(
                (rule for rule in rules['values'] if rule['name'] == rule_name),
                None
            )
            
            # Prepare the rule definition
            rule_definition = {
                "name": rule_name,
                "projectKey": project_key,
                "trigger": {
                    "id": "jira.issue.created",
                    "formType": "created",
                    "type": "issueCreated",
                    "configuration": {
                        "projects": [{"value": project_key}]
                    }
                },
                "components": [
                    {
                        "id": "jira.issue.edit",
                        "type": "action",
                        "configuration": {
                            "operations": [
                                {
                                    "field": field_id,
                                    "value": value,
                                    "type": "fieldValue"
                                }
                            ]
                        }
                    }
                ]
            }
            
            if existing_rule:
                # Update existing rule
                self.logger.info(f"Updating existing automation rule for {project_key}")
                response = requests.put(
                    f"{rules_endpoint}/{existing_rule['id']}",
                    headers=self.headers,
                    json=rule_definition
                )
            else:
                # Create new rule
                self.logger.info(f"Creating new automation rule for {project_key}")
                response = requests.post(
                    rules_endpoint,
                    headers=self.headers,
                    json=rule_definition
                )
            
            response.raise_for_status()
            self.logger.info(f"Successfully {'updated' if existing_rule else 'created'} automation rule for {project_key}")
            return True
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to configure automation rule for {project_key}: {str(e)}")
            if hasattr(e, 'response') and e.response:
                self.logger.error(f"Response content: {e.response.text}")
            return False

    def process_all_fields(self, dry_run: bool = False) -> Dict[str, Dict[str, Dict[str, int]]]:
        """Process all fields and projects defined in the configuration."""
        mode = "[DRY RUN] " if dry_run else ""
        self.logger.info(f"\n{mode}Starting field processing...")
        results = {}
        
        for field_name, field_config in self.config['fields'].items():
            self.logger.info(f"\nProcessing field: {field_name}")
            field_results = {}
            field_id = field_config['id']
            
            for project_key, value in field_config['projects'].items():
                # Add project type to logging
                project_type = self.project_types.get(project_key, 'undetermined')
                self.logger.info(f"\nProcessing project {project_key} (Type: {project_type})")
                
                project_results = {
                    'issues_found': 0,
                    'issues_updated': 0,
                    'automation_rule': False,
                    'project_type': project_type,
                    'failed_issues': [],  # Change to store tuples/dicts with (key, type)
                    'successful_issues': [],  # New field to track successes with type
                }

                # Check if field is on screens
                has_field = self.check_field_screen_config(project_key, field_id)
                if has_field is None:
                    self.logger.error(f"Failed to check screen configuration for {project_key}")
                    project_results['error'] = 'Failed to check screen configuration'
                    field_results[project_key] = project_results
                    continue
                elif not has_field:
                    self.logger.error(f"Field {field_name} not found in screens for {project_key}")
                    project_results['error'] = 'Field not configured in project screens'
                    field_results[project_key] = project_results
                    continue                
                
                # Find and update issues
                issues = self.find_issues_needing_update(project_key, field_id, value)

                project_results['issues_found'] = len(issues)
                
                self.logger.info(f"Found {len(issues)} issues to update")
                
                for issue in issues:
                    if self.update_issue_field(issue['id'], field_id, value, dry_run):
                        project_results['issues_updated'] += 1
                        project_results['successful_issues'].append({
                            'key': issue['key'],
                            'type': issue['issue_type']
                        })
                    else:
                        project_results['failed_issues'].append({
                            'key': issue['key'],
                            'type': issue['issue_type']
                        })
                         
                if project_results['failed_issues']:
                    # Sort failed issues by key
                    sorted_failed = sorted(project_results['failed_issues'], key=lambda x: x['key'])
                    
                    # Convert the sorted list to a formatted string
                    failed_issues_str = ', '.join([
                        f"{issue['key']}({issue['type']})" 
                        for issue in sorted_failed
                    ])
                    
                    self.logger.warning(
                        f"\nFailed to update {len(project_results['failed_issues'])} issues in {project_key}:"
                        f"\nFailed issues: {failed_issues_str}"
                    )

                # Create/update automation rule
                project_results['automation_rule'] = self.create_or_update_automation_rule(
                    project_key,
                    field_id,
                    value,
                    field_name
                )
                
                field_results[project_key] = project_results
                
                self.logger.info(
                    f"Project {project_key} completed:"
                    f"\n  - Issues updated: {project_results['issues_updated']}/{project_results['issues_found']}"

                    f"issues updated, automation rule: "
                    f"{'created' if project_results['automation_rule'] else 'failed'}"

                )
            
            results[field_name] = field_results
        
        return results
    
    def get_field_status(self, project_key: str, field_id: str, target_value: str) -> dict:
        """Get status report for a field in a project."""
        try:
            field_num = field_id.replace("customfield_", "")
            jql = f'project = "{project_key}"'
            
            response = requests.post(
                f"{self.base_url}/rest/api/3/search",
                headers=self.headers,
                json={
                    "jql": jql,
                    "fields": ["id", "key", field_id],
                    "maxResults": 0  # Just get total count
                }
            )
            response.raise_for_status()
            total_issues = response.json()['total']

            # Get issues with matching value
            jql_match = f'project = "{project_key}" AND cf[{field_num}] = "{target_value}"'
            response = requests.post(
                f"{self.base_url}/rest/api/3/search",
                headers=self.headers,
                json={
                    "jql": jql_match,
                    "maxResults": 0
                }
            )
            matches = response.json()['total']

            # Get issues with different values
            jql_different = f'project = "{project_key}" AND cf[{field_num}] != "{target_value}" AND cf[{field_num}] IS NOT EMPTY'
            response = requests.post(
                f"{self.base_url}/rest/api/3/search",
                headers=self.headers,
                json={
                    "jql": jql_different,
                    "maxResults": 0
                }
            )
            different = response.json()['total']

            # Calculate missing
            missing = total_issues - matches - different

            return {
                "total": total_issues,
                "matching": matches,
                "different": different,
                "missing": missing,
                "matching_percent": round((matches / total_issues * 100) if total_issues > 0 else 0, 1),
                "field_configured": self.check_field_screen_config(project_key, field_id)
            }
        except Exception as e:
            self.logger.error(f"Error getting status for {project_key}: {str(e)}")
            return None

    def print_status_report(self):
        """Generate and print status report for all fields and projects."""
        self.logger.info("\nField Status Report")
        self.logger.info("=" * 50)
        
        for field_name, field_config in self.config['fields'].items():
            self.logger.info(f"\nField: {field_name}")
            field_id = field_config['id']
            
            for project_key, target_value in field_config['projects'].items():
                status = self.get_field_status(project_key, field_id, target_value)
                if status:
                    project_type = self.project_types.get(project_key, 'undetermined')
                    self.logger.info(f"\n  Project: {project_key} ({project_type})")
                    self.logger.info(f"  Target Value: {target_value}")
                    self.logger.info(f"  Field Configured: {'✓' if status['field_configured'] else '✗'}")
                    self.logger.info(f"  Total Issues: {status['total']}")
                    self.logger.info(f"  Matching Value: {status['matching']} ({status['matching_percent']}%)")
                    self.logger.info(f"  Different Value: {status['different']}")
                    self.logger.info(f"  Missing Value: {status['missing']}")  

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file (e.g. config/defaults.yaml)")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying them")
    parser.add_argument("--status", action="store_true", help="Show field status report without updates")
    args = parser.parse_args()
    
    updater = JiraFieldUpdater(args.config)
    
    if args.status:
        updater.print_status_report()
    else:
        results = updater.process_all_fields(dry_run=args.dry_run)
        
        print("\nUpdate Summary:")
        print("=" * 50)
        for field_name, field_results in results.items():
            print(f"\nField: {field_name}")
            for project, stats in field_results.items():
                print(f"\n  Project: {project} ({stats['project_type']})")
                print(f"  Issues found without value: {stats['issues_found']}")
                print(f"  Issues successfully updated: {stats['issues_updated']}")
                print(f"  Automation rule: {'✓' if stats['automation_rule'] else '✗'}")

        print("\nCheck the log file for detailed information.")

if __name__ == "__main__":
    main()
