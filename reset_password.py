#!/usr/bin/env python3
"""
Reset Password Module
Resets Odoo database user password for user ID 2 to admin/admin.
"""

import subprocess
from pathlib import Path


def reset_database_user_password(odoo_config):
    """Reset database user password for user ID 2 to admin/admin"""
    print("Resetting database user password...")
    
    # Create temporary script file for password reset
    script_content = """#!/usr/bin/env python3
# Reset admin user (ID 2) password
env['res.users'].browse(2).write({'login': 'admin', 'password': 'admin'})
env.cr.commit()
print("Admin user password reset to admin/admin")
"""
    
    script_path = Path(__file__).parent / 'reset_user_script.py'
    
    try:
        # Write the script file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Construct the shell command to reset user password
        reset_cmd = [
            odoo_config['odoo_bin_path'],
            odoo_config['odoo_script_path'],
            'shell',
            '-d', odoo_config['db_name'],
            '--max-cron-threads', '0',
            '--stop-after-init',
            '--no-http'
        ]
        
        # Add database connection parameters
        if odoo_config.get('db_host'):
            reset_cmd.extend(['--db_host', odoo_config['db_host']])
        if odoo_config.get('db_port'):
            reset_cmd.extend(['--db_port', odoo_config['db_port']])
        if odoo_config.get('db_user'):
            reset_cmd.extend(['--db_user', odoo_config['db_user']])
        if odoo_config.get('db_password'):
            reset_cmd.extend(['--db_password', odoo_config['db_password']])
        
        # Execute the command with script as input
        with open(script_path, 'r', encoding='utf-8') as script_file:
            result = subprocess.run(
                reset_cmd, 
                stdin=script_file,
                capture_output=True, 
                text=True, 
                timeout=60
            )
        
        if result.returncode == 0:
            print("Database user password reset successfully")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"Failed to reset database user password: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("Timeout while resetting database user password")
    except Exception as e:
        print(f"Error resetting database user password: {e}")
    finally:
        # Clean up the temporary script file
        try:
            if script_path.exists():
                script_path.unlink()
        except Exception:
            pass


def run_reset_password(odoo_config):
    """Main function to run password reset process"""
    print("Running password reset...")
    reset_database_user_password(odoo_config)