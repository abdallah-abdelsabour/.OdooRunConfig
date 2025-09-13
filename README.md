# Odoo Run Configuration

This directory contains configuration files and settings for running the   Odoo custom modules.

## Overview

The `.OdooRunConfig` directory is used to store runtime configuration and temporary files for the Odoo development environment. This directory is typically excluded from version control via `.gitignore` to avoid committing environment-specific configurations.

## Environment Variables (.env)

The `.env` file contains all the configuration options for running Odoo. Here's a detailed explanation of each option:

### Odoo Executable Paths
- **`ODOO_BIN_PATH`**: Path to the Python executable used to run Odoo
  - Value: `C:\Users\Admin\odoo\18\python\python.exe`
  - Purpose: Specifies the Python interpreter for running Odoo (embedded Python 3.12)

- **`ODOO_SCRIPT_PATH`**: Path to the main Odoo executable script
  - Value: `C:\Users\Admin\odoo\18\odoo\odoo-bin`
  - Purpose: The main Odoo binary file that starts the server

### Addons Paths
- **`ODOO_ADDONS_PATH`**: Path to core Odoo addons
  - Value: `C:\Users\Admin\odoo\18\odoo\addons`
  - Purpose: Contains standard community addons that come with Odoo

- **`BASE_ADDONS_PATH`**: Path to enterprise addons
  - Value: `C:\Users\Admin\odoo\18\enterprise`
  - Purpose: Contains commercial enterprise modules (requires license)

- **`CUSTOM_ADDONS_PATH`**: Path to custom developed addons
  - Value: `C:\Users\Admin\odoo\18\custom\ custtom_addons_path`
  - Purpose: Contains project-specific custom modules for odoo project custom

### Database Configuration
- **`DB_NAME`**: Name of the PostgreSQL database
  - Value: `18_db_6_27`
  - Purpose: The database where Odoo data is stored

- **`DB_HOST`**: Database server hostname
  - Value: `localhost`
  - Purpose: Location of the PostgreSQL server (local machine)

- **`DB_PORT`**: Database server port
  - Value: `5432`
  - Purpose: Port number for PostgreSQL connection (default PostgreSQL port)

- **`DB_USER`**: Database username
  - Value: `odoo18`
  - Purpose: PostgreSQL user account for Odoo database access

- **`DB_PASSWORD`**: Database password
  - Value: `odoo18`
  - Purpose: Password for the PostgreSQL user account

### Server Configuration
- **`HTTP_PORT`**: Web server port for HTTP connections
  - Value: `8018`
  - Purpose: Port where Odoo web interface is accessible (http://localhost:8018)

- **`XMLRPC_PORT`**: XML-RPC API port
  - Value: `8018`
  - Purpose: Port for external API connections (same as HTTP port)

### Development Settings
- **`DEV_MODE`**: Development mode flags
  - Value: `all`
  - Purpose: Enables all development features (auto-reload, debugging tools)
  - Options: `all`, `reload`, `qweb`, `werkzeug`, `xml`

- **`LOG_LEVEL`**: Logging verbosity level
  - Value: `info`
  - Purpose: Controls how much information is logged
  - Options: `debug`, `info`, `warning`, `error`, `critical`

- **`AUTO_RELOAD`**: Automatic code reloading
  - Value: `true`
  - Purpose: Automatically restarts server when code changes are detected

### Module Management
- **`MODULES_TO_INSTALL`**: Modules to install on startup
  - Value: `sale_updates`
  - Purpose: Comma-separated list of modules to install when starting Odoo

- **`MODULES_TO_UPGRADE`**: Modules to upgrade on startup
  - Value: `sale_updates,pos_hide_closing_fields`
  - Purpose: Comma-separated list of modules to upgrade when starting Odoo

### System Management
- **`RESET_DB_USER_PASSWORD`**: Reset admin user password
  - Value: `false`
  - Purpose: When `true`, resets the admin user password to default on startup

- **`GIT_AUTO_UPDATE`**: Automatic Git updates
  - Value: `true`
  - Purpose: Automatically updates modules with uncommitted changes from Git

### Testing & Initialization
- **`TEST_ENABLE`**: Enable automated testing
  - Value: `false`
  - Purpose: When `true`, runs automated tests after module installation

- **`STOP_AFTER_INIT`**: Stop after initialization
  - Value: `false`
  - Purpose: When `true`, stops the server after completing initialization tasks

- **`WITHOUT_DEMO`**: Skip demo data installation
  - Value: `false`
  - Purpose: When `true`, skips installing demo data for modules

## Usage

This directory is automatically managed by the Odoo development environment and IDE configurations. To modify Odoo behavior, update the values in the `.env` file according to your needs.

### Common Configuration Changes

1. **Change database**: Update `DB_NAME` to point to a different database
2. **Change port**: Modify `HTTP_PORT` and `XMLRPC_PORT` to run on different ports
3. **Install modules**: Add module names to `MODULES_TO_INSTALL` or `MODULES_TO_UPGRADE`
4. **Enable testing**: Set `TEST_ENABLE=true` to run tests automatically
5. **Debug mode**: Change `LOG_LEVEL` to `debug` for more detailed logging

## Related Files

- `../.gitignore` - Contains rules to exclude this directory from version control
- `../CLAUDE.md` - Project-specific instructions for Claude Code development assistant
- `.env` - Environment variables configuration file (this file contains sensitive information and should not be committed to version control)