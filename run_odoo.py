#!/usr/bin/env python3
"""
Odoo Entry Point Script
Reads configuration from .env file and starts Odoo with the specified parameters.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from git_auto_update import run_git_auto_update
from reset_password import run_reset_password

def load_environment():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)
    
    load_dotenv(env_path)
    return True

def get_env_var(key, default=None, required=True):
    """Get environment variable with optional default and required check"""
    value = os.getenv(key, default)
    if required and not value:
        print(f"Error: Required environment variable {key} is not set")
        sys.exit(1)
    return value


def build_odoo_command():
    """Build the Odoo command based on environment variables"""
    odoo_bin_path = get_env_var('ODOO_BIN_PATH')
    odoo_script_path = get_env_var('ODOO_SCRIPT_PATH')
    
    # Base command
    cmd = [odoo_bin_path, odoo_script_path]
    
    # Database configuration
    db_name = get_env_var('DB_NAME', required=False)
    if db_name:
        cmd.extend(['-d', db_name])
    
    db_host = get_env_var('DB_HOST', required=False)
    if db_host:
        cmd.extend(['--db_host', db_host])
    
    db_port = get_env_var('DB_PORT', required=False)
    if db_port:
        cmd.extend(['--db_port', db_port])
    
    db_user = get_env_var('DB_USER', required=False)
    if db_user:
        cmd.extend(['--db_user', db_user])
    
    db_password = get_env_var('DB_PASSWORD', required=False)
    if db_password:
        cmd.extend(['--db_password', db_password])
    
    # Addons paths
    addons_paths = []
    odoo_addons = get_env_var('ODOO_ADDONS_PATH', required=False)
    base_addons = get_env_var('BASE_ADDONS_PATH', required=False)
    custom_addons = get_env_var('CUSTOM_ADDONS_PATH', required=False)
    
    if odoo_addons:
        addons_paths.append(odoo_addons)
    if base_addons:
        addons_paths.append(base_addons)
    if custom_addons:
        addons_paths.append(custom_addons)
    
    if addons_paths:
        cmd.extend(['--addons-path', ','.join(addons_paths)])
    
    # HTTP configuration
    http_port = get_env_var('HTTP_PORT', required=False)
    if http_port:
        cmd.extend(['--xmlrpc-port', http_port])
    
    # Development mode
    dev_mode = get_env_var('DEV_MODE', required=False)
    if dev_mode and dev_mode.lower() != 'false':
        cmd.extend(['--dev', dev_mode])
    
    # Log level
    log_level = get_env_var('LOG_LEVEL', 'info', required=False)
    if log_level:
        cmd.extend(['--log-level', log_level])
    
    # Modules to install
    modules_install = get_env_var('MODULES_TO_INSTALL', required=False)
    if modules_install:
        cmd.extend(['-i', modules_install])
    
    # Modules to upgrade
    modules_upgrade = get_env_var('MODULES_TO_UPGRADE', required=False)
    if modules_upgrade:
        cmd.extend(['-u', modules_upgrade])
    
    # Test mode
    test_enable = get_env_var('TEST_ENABLE', 'false', required=False)
    if test_enable.lower() == 'true':
        cmd.append('--test-enable')
    
    # Stop after init
    stop_after_init = get_env_var('STOP_AFTER_INIT', 'false', required=False)
    if stop_after_init.lower() == 'true':
        cmd.append('--stop-after-init')
    
    # Without demo data
    without_demo = get_env_var('WITHOUT_DEMO', 'false', required=False)
    if without_demo.lower() == 'true':
        cmd.extend(['--without-demo', 'all'])
    
    return cmd

def main():
    """Main entry point"""
    print("Starting Odoo with configuration from .env file...")
    
    # Load environment variables
    load_environment()
    
    # Reset database user password if requested
    reset_password = get_env_var('RESET_DB_USER_PASSWORD', 'false', required=False)
    if reset_password.lower() == 'true':
        odoo_config = {
            'odoo_bin_path': get_env_var('ODOO_BIN_PATH'),
            'odoo_script_path': get_env_var('ODOO_SCRIPT_PATH'),
            'db_name': get_env_var('DB_NAME'),
            'db_host': get_env_var('DB_HOST', required=False),
            'db_port': get_env_var('DB_PORT', required=False),
            'db_user': get_env_var('DB_USER', required=False),
            'db_password': get_env_var('DB_PASSWORD', required=False)
        }
        run_reset_password(odoo_config)
    
    # Run git auto-update if requested
    git_auto_update = get_env_var('GIT_AUTO_UPDATE', 'false', required=False)
    if git_auto_update.lower() == 'true':
        custom_addons_path = get_env_var('CUSTOM_ADDONS_PATH', required=False)
        odoo_config = {
            'odoo_bin_path': get_env_var('ODOO_BIN_PATH'),
            'odoo_script_path': get_env_var('ODOO_SCRIPT_PATH'),
            'db_name': get_env_var('DB_NAME'),
            'db_host': get_env_var('DB_HOST', required=False),
            'db_port': get_env_var('DB_PORT', required=False),
            'db_user': get_env_var('DB_USER', required=False),
            'db_password': get_env_var('DB_PASSWORD', required=False)
        }
        run_git_auto_update(custom_addons_path, odoo_config)
    
    # Build and execute Odoo command
    cmd = build_odoo_command()
    
    print(f"Executing command: {' '.join(cmd)}")
    print("=" * 80)
    
    try:
        # Start Odoo process
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Odoo process failed with return code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nOdoo process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting Odoo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()