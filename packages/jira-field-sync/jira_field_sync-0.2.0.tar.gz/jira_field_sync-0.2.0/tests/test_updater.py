import pytest
from jira_defaults.updater import JiraFieldUpdater
from pathlib import Path
import yaml


@pytest.fixture
def sample_config(tmp_path):
    config = {
        'jira': {
            'url': 'https://test.atlassian.net',
            'token': 'test-token'
        },
        'fields': {
            'lob': {
                'id': 'customfield_11195',
                'projects': {
                    'TEST': 'Test Value'
                }
            }
        }
    }
    
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    return str(config_file)


def test_load_config(sample_config):
    updater = JiraFieldUpdater(sample_config)
    assert updater.base_url == 'https://test.atlassian.net'
    assert 'Bearer test-token' in updater.headers['Authorization']
