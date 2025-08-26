#!/usr/bin/env python3
"""
Python version of doit.sh - BB services management script
Kills processes, cleans logs, starts services, and verifies they're running
"""

import subprocess
import time
import os
import sys
import glob
import threading
import re
from pathlib import Path
from datetime import datetime

class BBServiceManager:
    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.mnms_dir = f"{self.home_dir}/mnms"
        self.services = {
            'bbrootsvc': {
                'process_name': 'bbrootsvc',
                'executable': f"{self.mnms_dir}/bbrootsvc/bbrootsvc",
                'args': ['-n', 'root1', '-debuglog', '-O', 'bblog-root1.log', '-ss', 'localhost:6666'],
                'description': 'BB Root Service',
                'port': '27182',
                'log_file': 'bblog-root1.log'
            },
            'bbnmssvc': {
                'process_name': 'bbnmssvc',
                'executable': f"{self.mnms_dir}/bbnmssvc/bbnmssvc",
                'args': ['-n', 'nms1', '-r', 'http://localhost:27182', '-rs', 'localhost:6666', '-debuglog', '-O', 'bblog-nms1.log'],
                'description': 'BB NMS Service',
                'port': None,
                'log_file': 'bblog-nms1.log'
            },
            'bblogsvc': {
                'process_name': 'bblogsvc',
                'executable': f"{self.mnms_dir}/bblogsvc/bblogsvc",
                'args': ['-n', 'log1', '-r', 'http://localhost:27182', '-O', 'bblog-log1.log', '-debuglog', '-rs', 'localhost:6666', '-ss', 'localhost:7777'],
                'description': 'BB Log Service',
                'port': '7777',
                'log_file': 'bblog-log1.log'
            },
            'bbpollsvc': {
                'process_name': 'bbpollsvc',
                'executable': f"{self.mnms_dir}/bbpollsvc/bbpollsvc",
                'args': ['-n', 'poll1', '-r', 'http://localhost:27182', '-debuglog', '-O', 'bblog-poll1.log', '-rs', 'localhost:6666', '-nsn', 'nms1'],
                'description': 'BB Poll Service',
                'port': None,
                'log_file': 'bblog-poll1.log'
            }
        }
        
        # Log monitoring setup
        self.monitoring = False
        self.monitor_threads = []
        self.log_positions = {}  # Track file positions for each log
        
        # Error patterns to look for in logs
        self.error_patterns = [
            (r'(?i)error', '🔴 ERROR'),
            (r'(?i)exception', '🔴 EXCEPTION'),
            (r'(?i)failed?', '🟠 FAILED'),
            (r'(?i)warning', '🟡 WARNING'),
            (r'(?i)critical', '🔴 CRITICAL'),
            (r'(?i)fatal', '🔴 FATAL'),
            (r'(?i)panic', '🔴 PANIC'),
            (r'(?i)timeout', '🟠 TIMEOUT'),
            (r'(?i)connection.*refused', '🔴 CONNECTION REFUSED'),
            (r'(?i)cannot.*connect', '🔴 CONNECTION FAILED'),
            (r'(?i)segmentation fault', '🔴 SEGFAULT'),
            (r'(?i)out of memory', '🔴 OOM'),
        ]

    def print_step(self, message, success=None):
        """Print a formatted step message"""
        if success is None:
            print(f"\n🔵 {message}")
        elif success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    def run_command(self, command, check_output=False, timeout=10):
        """Run a command with error handling"""
        try:
            if check_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
                return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
            else:
                result = subprocess.run(command, shell=True, timeout=timeout)
                return result.returncode == 0, "", ""
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)

    def kill_processes(self):
        """Kill all BB processes"""
        self.print_step("STEP 1: Killing BB processes")
        
        processes_to_kill = ['bbrootsvc', 'bbnmssvc', 'bblogsvc', 'bbpollsvc']
        
        for process in processes_to_kill:
            print(f"  Killing {process}...")
            success, stdout, stderr = self.run_command(f"sudo killall -9 {process} 2>/dev/null")
            if success or "no process found" in stderr.lower():
                self.print_step(f"  {process} terminated", True)
            else:
                self.print_step(f"  {process} - no running processes found", True)
        
        # Give processes time to terminate
        time.sleep(2)
        self.print_step("All BB processes killed", True)

    def clean_log_files(self):
        """Clean up log files"""
        self.print_step("STEP 2: Cleaning log files")
        
        # Clean /tmp/bblog* files
        bblog_files = glob.glob("/tmp/bblog*")
        if bblog_files:
            print(f"  Found {len(bblog_files)} bblog files in /tmp")
            success, stdout, stderr = self.run_command("sudo rm /tmp/bblog*")
            if success:
                self.print_step(f"  Removed {len(bblog_files)} bblog files from /tmp", True)
            else:
                self.print_step(f"  Failed to remove bblog files: {stderr}", False)
        else:
            self.print_step("  No bblog files found in /tmp", True)
        
        # Clean local log files
        local_logs = glob.glob("bblog-*.log")
        if local_logs:
            print(f"  Found {len(local_logs)} local log files")
            for log_file in local_logs:
                try:
                    os.remove(log_file)
                    print(f"    Removed {log_file}")
                except Exception as e:
                    print(f"    Failed to remove {log_file}: {e}")
        
        self.print_step("Log files cleaned", True)

    def start_service(self, service_name, service_config):
        """Start a single BB service"""
        executable = service_config['executable']
        args = service_config['args']
        description = service_config['description']
        
        # Check if executable exists
        if not os.path.exists(executable):
            self.print_step(f"  {description} executable not found: {executable}", False)
            return False
        
        # Build command
        cmd_parts = ['sudo', executable] + args + ['&']
        command = ' '.join(cmd_parts)
        
        print(f"  Starting {description}...")
        print(f"    Command: {command}")
        
        # Start the service
        success, stdout, stderr = self.run_command(command)
        
        if success:
            self.print_step(f"  {description} started successfully", True)
            return True
        else:
            self.print_step(f"  Failed to start {description}: {stderr}", False)
            return False

    def start_services(self):
        """Start all BB services in the correct order"""
        self.print_step("STEP 3: Starting BB services")
        
        # Start services in order
        service_order = ['bbrootsvc', 'bbnmssvc', 'bblogsvc', 'bbpollsvc']
        started_services = []
        
        for service_name in service_order:
            service_config = self.services[service_name]
            if self.start_service(service_name, service_config):
                started_services.append(service_name)
                # Wait a bit between services
                if service_name == 'bbrootsvc':
                    print("    Waiting 3 seconds for root service to initialize...")
                    time.sleep(3)
                else:
                    time.sleep(1)
            else:
                self.print_step(f"Failed to start {service_name}, stopping here", False)
                return False
        
        self.print_step(f"All {len(started_services)} services started", True)
        return True

    def check_process_running(self, process_name):
        """Check if a process is running with sudo permissions"""
        # Check if process is running
        success, stdout, stderr = self.run_command(f"pgrep -f {process_name}", check_output=True)
        if not success or not stdout:
            return False, "Process not found"
        
        pids = stdout.split('\n')
        
        # Check each PID for sudo permissions
        for pid in pids:
            if pid.strip():
                # Check process details
                success, ps_output, _ = self.run_command(f"ps -p {pid.strip()} -o pid,euid,cmd --no-headers", check_output=True)
                if success and ps_output:
                    parts = ps_output.strip().split(None, 2)
                    if len(parts) >= 3:
                        euid = parts[1]
                        cmd = parts[2]
                        if process_name in cmd:
                            # EUID 0 means root/sudo
                            if euid == '0':
                                return True, f"Running as root (PID: {pid.strip()})"
                            else:
                                return True, f"Running but not as root (PID: {pid.strip()}, EUID: {euid})"
        
        return False, "Process found but details unclear"

    def verify_services(self):
        """Verify all services are running correctly"""
        self.print_step("STEP 4: Verifying services")
        
        # Wait a moment for all services to fully start
        print("  Waiting 5 seconds for services to initialize...")
        time.sleep(5)
        
        all_running = True
        
        for service_name, service_config in self.services.items():
            process_name = service_config['process_name']
            description = service_config['description']
            
            print(f"\n  Checking {description} ({process_name})...")
            
            running, details = self.check_process_running(process_name)
            
            if running:
                self.print_step(f"    {description}: {details}", True)
                
                # Additional checks for specific services
                if service_name == 'bbrootsvc':
                    print("    Testing root service HTTP endpoint...")
                    success, stdout, stderr = self.run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:27182 --connect-timeout 3", check_output=True)
                    if success and stdout:
                        if stdout in ['200', '404', '405']:  # Any HTTP response is good
                            self.print_step("    Root service HTTP endpoint responding", True)
                        else:
                            self.print_step(f"    Root service HTTP endpoint returned: {stdout}", False)
                    else:
                        self.print_step("    Could not test root service HTTP endpoint", False)
                
            else:
                self.print_step(f"    {description}: {details}", False)
                all_running = False
        
        if all_running:
            self.print_step("All services verified and running correctly", True)
        else:
            self.print_step("Some services failed verification", False)
        
        return all_running

    def show_service_status(self):
        """Show final status of all services"""
        self.print_step("STEP 5: Final service status")
        
        print("\n📊 Service Status Summary:")
        print("-" * 50)
        
        for service_name, service_config in self.services.items():
            process_name = service_config['process_name']
            description = service_config['description']
            
            running, details = self.check_process_running(process_name)
            status = "🟢 RUNNING" if running else "🔴 STOPPED"
            print(f"{status} {description:20} | {details}")
        
        print("-" * 50)

    def print_log_message(self, service, message, level="INFO"):
        """Print a formatted log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        service_short = service[:8].upper()
        print(f"[{timestamp}] [{service_short:8}] {level} | {message.strip()}")

    def check_for_errors(self, line):
        """Check if a log line contains error patterns"""
        for pattern, label in self.error_patterns:
            if re.search(pattern, line):
                return label
        return None

    def monitor_log_file(self, service_name, log_file):
        """Monitor a single log file for new entries"""
        file_path = os.path.join(os.getcwd(), log_file)
        
        # Initialize position tracking
        self.log_positions[log_file] = 0
        
        while self.monitoring:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        # Seek to last known position
                        f.seek(self.log_positions[log_file])
                        
                        # Read new lines
                        new_lines = f.readlines()
                        
                        if new_lines:
                            # Update position
                            self.log_positions[log_file] = f.tell()
                            
                            # Process new lines
                            for line in new_lines:
                                line = line.strip()
                                if line:  # Skip empty lines
                                    error_type = self.check_for_errors(line)
                                    if error_type:
                                        self.print_log_message(service_name, line, error_type)
                                    elif any(keyword in line.lower() for keyword in ['started', 'listening', 'connected', 'initialized']):
                                        self.print_log_message(service_name, line, "✅ INFO")
                                    # Uncomment the next line to show all log messages (can be very verbose)
                                    # else:
                                    #     self.print_log_message(service_name, line, "DEBUG")
                
                time.sleep(0.5)  # Check every 500ms
                
            except Exception as e:
                if self.monitoring:  # Only print error if we're still monitoring
                    print(f"⚠️  Error monitoring {log_file}: {e}")
                time.sleep(1)

    def start_log_monitoring(self):
        """Start monitoring all log files in separate threads"""
        print("\n🔍 Starting log monitoring...")
        print("   Monitoring for errors, warnings, and important events.")
        print("   Press Ctrl+C to stop monitoring and exit.\n")
        
        self.monitoring = True
        self.monitor_threads = []
        
        for service_name, service_config in self.services.items():
            log_file = service_config['log_file']
            thread = threading.Thread(
                target=self.monitor_log_file, 
                args=(service_name, log_file),
                daemon=True
            )
            thread.start()
            self.monitor_threads.append(thread)
            print(f"📋 Monitoring {service_config['description']} log: {log_file}")
        
        print("\n" + "="*70)
        print("LOG MONITORING ACTIVE - Press Ctrl+C to stop")
        print("="*70)

    def stop_log_monitoring(self):
        """Stop all log monitoring threads"""
        print("\n🛑 Stopping log monitoring...")
        self.monitoring = False
        
        # Wait for threads to finish (with timeout)
        for thread in self.monitor_threads:
            thread.join(timeout=1)
        
        print("✅ Log monitoring stopped.")

    def periodic_health_check(self):
        """Periodically check if all services are still running"""
        while self.monitoring:
            try:
                time.sleep(30)  # Check every 30 seconds
                
                if not self.monitoring:
                    break
                    
                print(f"\n🔍 [{datetime.now().strftime('%H:%M:%S')}] Health check...")
                
                all_healthy = True
                for service_name, service_config in self.services.items():
                    process_name = service_config['process_name']
                    running, details = self.check_process_running(process_name)
                    
                    if not running:
                        print(f"⚠️  {service_config['description']} is no longer running!")
                        all_healthy = False
                
                if all_healthy:
                    print("✅ All services healthy")
                else:
                    print("❌ Some services are down - consider restarting")
                    
            except Exception as e:
                if self.monitoring:
                    print(f"⚠️  Health check error: {e}")
            
    def wait_for_enter(self, message, timeout=5):
        """Wait for user input with timeout"""
        print(f"\n⏳ {message} (Press Enter to continue or wait {timeout} seconds)...")
        try:
            # Simple timeout implementation
            import select
            import sys
            
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                sys.stdin.readline()
                print("✅ User input received, continuing...")
            else:
                print("⏰ Timeout reached, continuing...")
        except:
            # Fallback for systems without select
            time.sleep(timeout)
            print("⏰ Timeout reached, continuing...")

    def run(self):
        """Main execution method"""
        print("🚀 BB Services Management Script")
        print("=" * 50)
        
        try:
            # Step 1: Kill processes
            self.kill_processes()
            self.wait_for_enter("Processes killed, ready to clean logs", 3)
            
            # Step 2: Clean logs
            self.clean_log_files()
            self.wait_for_enter("Logs cleaned, ready to start services", 3)
            
            # Step 3: Start services
            if not self.start_services():
                print("\n❌ Failed to start all services. Exiting.")
                return False
            
            self.wait_for_enter("Services started, ready to verify", 3)
            
            # Step 4: Verify services
            if not self.verify_services():
                print("\n⚠️  Some services failed verification.")
            
            # Step 5: Show final status
            self.show_service_status()
            
            print("\n🎉 BB Services management completed!")
            
            # Step 6: Start log monitoring and stay running
            self.wait_for_enter("Ready to start log monitoring", 3)
            self.start_log_monitoring()
            
            # Start health check thread
            health_thread = threading.Thread(target=self.periodic_health_check, daemon=True)
            health_thread.start()
            
            # Main monitoring loop
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n⚠️  Monitoring interrupted by user")
                self.stop_log_monitoring()
                return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Script interrupted by user")
            if self.monitoring:
                self.stop_log_monitoring()
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            if self.monitoring:
                self.stop_log_monitoring()
            return False

def main():
    """Main entry point"""
    if os.geteuid() != 0:
        print("⚠️  Note: This script uses sudo for process management.")
        print("   You may be prompted for your password.\n")
    
    manager = BBServiceManager()
    try:
        success = manager.run()
        print("\n👋 BB Services Management Script finished.")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    
    # No sys.exit() - let the script end naturally

if __name__ == "__main__":
    main()
