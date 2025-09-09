#!/usr/bin/env python3
"""
Git Auto-Update Module
Detects uncommitted changes in custom Odoo modules and updates them automatically.
"""

import os
import subprocess
from pathlib import Path


def get_changed_modules(custom_addons_path):
    """Detect modules with uncommitted git changes in custom addons path"""
    print("Detecting modules with git changes...")
    
    if not custom_addons_path:
        return []
    
    custom_path = Path(custom_addons_path)
    if not custom_path.exists():
        print(f"Custom addons path not found: {custom_addons_path}")
        return []
    
    changed_modules = []
    original_cwd = os.getcwd()
    
    try:
        # Change to custom addons directory
        os.chdir(custom_path)
        
        # Get git status for modified and new files
        result = subprocess.run(
            ['git', 'status', '--porcelain'], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if result.returncode != 0:
            print("Not a git repository or git command failed")
            return []
        
        # Parse git status output
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue
                
            # Git status format: XY filename (handle different spacing)
            status = line[:2]
            # Skip the status part and any whitespace
            filename = line[2:].strip()
            
            # Skip if file is deleted
            if 'D' in status:
                continue
                
            # Extract module name from path (handle both / and \ separators)
            if '/' in filename:
                path_parts = filename.split('/')
            elif '\\' in filename:
                path_parts = filename.split('\\')
            else:
                # File is in root directory, not a module
                continue
                
            if len(path_parts) > 0:
                module_name = path_parts[0]
                
                # Check if it's a valid Odoo module directory
                module_path = custom_path / module_name
                if (module_path.exists() and 
                    module_path.is_dir() and 
                    (module_path / '__manifest__.py').exists()):
                    
                    if module_name not in changed_modules:
                        changed_modules.append(module_name)
                        print(f"Found changed module: {module_name}")
        
        return changed_modules
        
    except subprocess.TimeoutExpired:
        print("Timeout while checking git status")
        return []
    except Exception as e:
        print(f"Error detecting git changes: {e}")
        return []
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


def update_modules_via_shell(modules, odoo_config):
    """Update specified modules using Odoo shell command"""
    if not modules:
        return
        
    print(f"Updating modules via shell: {', '.join(modules)}")
    
    # Create temporary script file for module updates
    modules_str = "'" + "','".join(modules) + "'"
    script_content = f"""#!/usr/bin/env python3
# Auto-update modules with git changes
modules_to_update = [{modules_str}]
print(f"Updating modules: {{modules_to_update}}")

try:
    # Get module records
    module_obj = env['ir.module.module']
    for module_name in modules_to_update:
        module = module_obj.search([('name', '=', module_name)])
        if module:
            print(f"Updating module: {{module_name}}")
            module.button_immediate_upgrade()
        else:
            print(f"Module not found: {{module_name}}")
    
    env.cr.commit()
    print("Modules updated successfully")
except Exception as e:
    print(f"Error updating modules: {{e}}")
"""
    
    script_path = Path(__file__).parent / 'update_modules_script.py'
    
    try:
        # Write the script file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Construct the shell command
        update_cmd = [
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
            update_cmd.extend(['--db_host', odoo_config['db_host']])
        if odoo_config.get('db_port'):
            update_cmd.extend(['--db_port', odoo_config['db_port']])
        if odoo_config.get('db_user'):
            update_cmd.extend(['--db_user', odoo_config['db_user']])
        if odoo_config.get('db_password'):
            update_cmd.extend(['--db_password', odoo_config['db_password']])
        
        # Execute the command with script as input
        with open(script_path, 'r', encoding='utf-8') as script_file:
            result = subprocess.run(
                update_cmd, 
                stdin=script_file,
                capture_output=True, 
                text=True, 
                timeout=120
            )
        
        if result.returncode == 0:
            print("Modules updated successfully via shell")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"Failed to update modules via shell: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("Timeout while updating modules")
    except Exception as e:
        print(f"Error updating modules: {e}")
    finally:
        # Clean up the temporary script file
        try:
            if script_path.exists():
                script_path.unlink()
        except Exception:
            pass


def run_git_auto_update(custom_addons_path, odoo_config):
    """Main function to run git auto-update process"""
    print("Running git auto-update...")
    
    # Detect changed modules
    changed_modules = get_changed_modules(custom_addons_path)
    
    if not changed_modules:
        print("No modules with uncommitted changes found")
        return []
    
    # Update the changed modules
    update_modules_via_shell(changed_modules, odoo_config)
    
    return changed_modules